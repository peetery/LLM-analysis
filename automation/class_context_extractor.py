"""
Class Context Extractor for Universal Test Generation.

This module provides functionality to analyze any Python source file and extract
class information at different levels of detail for use in LLM-based test generation.

Supported context levels:
    - interface: Method signatures only (body replaced with 'pass')
    - interface_docstring: Signatures with docstrings preserved
    - full_context: Complete source code implementation

The extractor also handles:
    - Auto-detection of the main class (when single class in file)
    - Helper type extraction (TypedDict, dataclass, Enum, NamedTuple)
    - Import statement generation
    - Base class detection
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass


@dataclass
class ClassInfo:
    """
    Information about an analyzed class.

    Attributes:
        name: The name of the class
        module_name: The module name (filename without .py)
        file_path: Path to the source file
        public_methods: List of public method names (excluding _private)
        helper_types: Names of helper types (TypedDict, dataclass, etc.)
        base_classes: Names of base classes
        import_statement: Ready-to-use import statement
    """
    name: str
    module_name: str
    file_path: Path
    public_methods: List[str]
    helper_types: List[str]
    base_classes: List[str]
    import_statement: str


class ContextLevel:
    """Constants for context extraction levels."""
    INTERFACE = "interface"
    INTERFACE_DOCSTRING = "interface_docstring"
    FULL_CONTEXT = "full_context"

    ALL = [INTERFACE, INTERFACE_DOCSTRING, FULL_CONTEXT]


class ClassContextExtractor:
    """
    Extracts context from any Python class at different detail levels.

    This class parses a Python source file and extracts information about
    a specified class (or auto-detected if single class) for use in
    generating LLM prompts for test generation.

    Usage:
        extractor = ClassContextExtractor(Path("my_module.py"))
        info = extractor.get_class_info()
        interface = extractor.extract_context("interface")
        full = extractor.extract_context("full_context")

    Args:
        source_file: Path to the Python source file
        class_name: Name of the class to extract (optional, auto-detected if single class)

    Raises:
        FileNotFoundError: If the source file doesn't exist
        ValueError: If class cannot be detected or specified class not found
    """

    # Types that should be extracted as helper types
    HELPER_TYPE_DECORATORS = {'dataclass', 'dataclasses.dataclass'}
    HELPER_TYPE_BASES = {'TypedDict', 'NamedTuple', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag'}

    def __init__(self, source_file: Path, class_name: Optional[str] = None):
        self.source_file = Path(source_file)

        if not self.source_file.exists():
            raise FileNotFoundError(f"Source file not found: {self.source_file}")

        if not self.source_file.suffix == '.py':
            raise ValueError(f"Source file must be a Python file (.py): {self.source_file}")

        self.source_content = self.source_file.read_text(encoding='utf-8')
        self.source_lines = self.source_content.split('\n')

        try:
            self.tree = ast.parse(self.source_content)
        except SyntaxError as e:
            raise ValueError(f"Failed to parse Python file: {e}")

        self.module_name = self.source_file.stem

        # Detect or validate class name
        if class_name:
            self.class_name = class_name
            self._validate_class_exists()
        else:
            self.class_name = self._detect_main_class()

        # Find the main class node
        self.class_node = self._find_class_node(self.class_name)

        # Analyze helper types
        self._helper_types: Dict[str, ast.ClassDef] = {}
        self._analyze_helper_types()

    def _validate_class_exists(self) -> None:
        """Validate that the specified class exists in the file."""
        class_names = self._get_all_class_names()
        if self.class_name not in class_names:
            raise ValueError(
                f"Class '{self.class_name}' not found in {self.source_file}. "
                f"Available classes: {', '.join(class_names)}"
            )

    def _get_all_class_names(self) -> List[str]:
        """Get all class names defined in the file."""
        return [
            node.name for node in ast.walk(self.tree)
            if isinstance(node, ast.ClassDef)
        ]

    def _detect_main_class(self) -> str:
        """
        Auto-detect the main class in the file.

        Returns the class name if exactly one non-helper class is found.

        Raises:
            ValueError: If no classes or multiple main classes found
        """
        all_classes = []
        helper_classes = set()

        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                all_classes.append(node.name)

                # Check if it's a helper type
                if self._is_helper_type(node):
                    helper_classes.add(node.name)

        main_classes = [c for c in all_classes if c not in helper_classes]

        if not main_classes:
            if all_classes:
                raise ValueError(
                    f"No main class found in {self.source_file}. "
                    f"Only helper types found: {', '.join(all_classes)}"
                )
            else:
                raise ValueError(f"No classes found in {self.source_file}")

        if len(main_classes) > 1:
            raise ValueError(
                f"Multiple classes found in {self.source_file}: {', '.join(main_classes)}. "
                f"Use --class-name to specify which class to test."
            )

        return main_classes[0]

    def _is_helper_type(self, node: ast.ClassDef) -> bool:
        """Check if a class is a helper type (TypedDict, dataclass, etc.)."""
        # Check decorators
        for decorator in node.decorator_list:
            dec_name = self._get_decorator_name(decorator)
            if dec_name in self.HELPER_TYPE_DECORATORS:
                return True

        # Check base classes
        for base in node.bases:
            base_name = self._get_base_name(base)
            if base_name in self.HELPER_TYPE_BASES:
                return True

        return False

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{self._get_base_name(decorator.value)}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return ""

    def _get_base_name(self, base: ast.expr) -> str:
        """Extract base class name from AST node."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        elif isinstance(base, ast.Subscript):
            # Handle Generic[T], List[X], etc.
            return self._get_base_name(base.value)
        return ""

    def _find_class_node(self, class_name: str) -> ast.ClassDef:
        """Find the AST node for the specified class."""
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return node
        raise ValueError(f"Class '{class_name}' not found in AST")

    def _analyze_helper_types(self) -> None:
        """Find all helper types used by the main class."""
        # Get type names used in the main class
        used_types = self._get_used_type_names()

        # Find helper type definitions
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef) and node.name != self.class_name:
                if self._is_helper_type(node) and node.name in used_types:
                    self._helper_types[node.name] = node

    def _get_used_type_names(self) -> Set[str]:
        """Get all type names referenced in the main class."""
        type_names = set()

        for node in ast.walk(self.class_node):
            # Check annotations
            if isinstance(node, ast.AnnAssign) and node.annotation:
                type_names.update(self._extract_type_names(node.annotation))

            # Check function annotations
            if isinstance(node, ast.FunctionDef):
                # Return type
                if node.returns:
                    type_names.update(self._extract_type_names(node.returns))
                # Argument types
                for arg in node.args.args + node.args.kwonlyargs:
                    if arg.annotation:
                        type_names.update(self._extract_type_names(arg.annotation))

        return type_names

    def _extract_type_names(self, annotation: ast.expr) -> Set[str]:
        """Extract all type names from an annotation."""
        names = set()

        if isinstance(annotation, ast.Name):
            names.add(annotation.id)
        elif isinstance(annotation, ast.Subscript):
            names.update(self._extract_type_names(annotation.value))
            names.update(self._extract_type_names(annotation.slice))
        elif isinstance(annotation, ast.Tuple):
            for elt in annotation.elts:
                names.update(self._extract_type_names(elt))
        elif isinstance(annotation, ast.List):
            for elt in annotation.elts:
                names.update(self._extract_type_names(elt))
        elif isinstance(annotation, ast.Attribute):
            names.add(annotation.attr)
        elif isinstance(annotation, ast.BinOp):
            # Handle Union types with | operator
            names.update(self._extract_type_names(annotation.left))
            names.update(self._extract_type_names(annotation.right))

        return names

    def get_class_info(self) -> ClassInfo:
        """
        Get basic information about the analyzed class.

        Returns:
            ClassInfo with name, module, methods, helper types, etc.
        """
        return ClassInfo(
            name=self.class_name,
            module_name=self.module_name,
            file_path=self.source_file,
            public_methods=self.get_public_methods(),
            helper_types=list(self._helper_types.keys()),
            base_classes=[self._get_base_name(b) for b in self.class_node.bases],
            import_statement=self.get_import_statement()
        )

    def get_public_methods(self) -> List[str]:
        """
        Get list of public methods (excluding _private methods).

        Returns:
            List of public method names including __init__ if present
        """
        methods = []
        for node in self.class_node.body:
            if isinstance(node, ast.FunctionDef):
                name = node.name
                # Include __init__ but exclude other dunder methods and private methods
                if name == '__init__' or (not name.startswith('_')):
                    methods.append(name)
        return methods

    def get_helper_types(self) -> List[Tuple[str, str]]:
        """
        Get helper types used by the main class.

        Returns:
            List of tuples (type_name, type_source_code)
        """
        result = []
        for name, node in self._helper_types.items():
            source = self._get_node_source(node)
            result.append((name, source))
        return result

    def get_import_statement(self) -> str:
        """
        Generate the import statement for the class.

        Returns:
            Import statement like 'from module import Class, HelperType'
        """
        imports = [self.class_name] + list(self._helper_types.keys())
        return f"from {self.module_name} import {', '.join(imports)}"

    def extract_context(self, level: str) -> str:
        """
        Extract context at the specified level.

        Args:
            level: One of 'interface', 'interface_docstring', or 'full_context'

        Returns:
            Source code at the requested detail level
        """
        if level == ContextLevel.INTERFACE:
            return self.extract_interface()
        elif level == ContextLevel.INTERFACE_DOCSTRING:
            return self.extract_interface_with_docstrings()
        elif level == ContextLevel.FULL_CONTEXT:
            return self.extract_full_context()
        else:
            raise ValueError(
                f"Unknown context level: {level}. "
                f"Must be one of: {', '.join(ContextLevel.ALL)}"
            )

    def extract_interface(self) -> str:
        """
        Extract only method signatures (body replaced with 'pass').

        Returns:
            Class definition with method signatures only
        """
        return self._extract_with_body_level('pass')

    def extract_interface_with_docstrings(self) -> str:
        """
        Extract signatures with docstrings preserved.

        Returns:
            Class definition with signatures and docstrings
        """
        return self._extract_with_body_level('docstring')

    def extract_full_context(self) -> str:
        """
        Extract complete source code including helper types.

        Returns:
            Full source code of the class and its helper types
        """
        parts = []

        # Add relevant imports
        imports = self._extract_relevant_imports()
        if imports:
            parts.append(imports)

        # Add helper types
        for _, source in self.get_helper_types():
            parts.append(source)

        # Add main class
        parts.append(self._get_node_source(self.class_node))

        return '\n\n'.join(parts)

    def _extract_with_body_level(self, body_level: str) -> str:
        """
        Extract class with specified body detail level.

        Args:
            body_level: 'pass' for interface, 'docstring' for interface_docstring
        """
        parts = []

        # Add relevant imports
        imports = self._extract_relevant_imports()
        if imports:
            parts.append(imports)

        # Add helper types (simplified for interface levels)
        for name, _ in self.get_helper_types():
            helper_node = self._helper_types[name]
            simplified = self._simplify_helper_type(helper_node)
            parts.append(simplified)

        # Add main class with modified methods
        class_code = self._create_interface_class(body_level)
        parts.append(class_code)

        return '\n\n'.join(parts)

    def _extract_relevant_imports(self) -> str:
        """Extract imports that are relevant to the class definition."""
        relevant_imports = []

        # Standard typing imports that might be needed
        typing_names = {'List', 'Dict', 'Optional', 'Tuple', 'Set', 'Any',
                       'Union', 'Callable', 'TypeVar', 'Generic', 'TypedDict',
                       'NamedTuple', 'Literal', 'Final'}

        for node in self.tree.body:
            if isinstance(node, ast.Import):
                # Keep dataclasses, enum imports
                for alias in node.names:
                    if alias.name in ('dataclasses', 'enum', 'typing'):
                        relevant_imports.append(self._get_node_source(node))
                        break

            elif isinstance(node, ast.ImportFrom):
                if node.module in ('typing', 'typing_extensions', 'dataclasses', 'enum'):
                    relevant_imports.append(self._get_node_source(node))

        return '\n'.join(relevant_imports)

    def _simplify_helper_type(self, node: ast.ClassDef) -> str:
        """Create a simplified version of a helper type for interface levels."""
        # For TypedDict and similar, we want to keep the full definition
        # as it defines the structure
        return self._get_node_source(node)

    def _create_interface_class(self, body_level: str) -> str:
        """Create the class with interface-level methods."""
        lines = []

        # Class definition line with decorators
        for decorator in self.class_node.decorator_list:
            lines.append(f"@{self._get_decorator_source(decorator)}")

        # Class header
        bases = ', '.join(self._get_base_name(b) for b in self.class_node.bases)
        if bases:
            lines.append(f"class {self.class_name}({bases}):")
        else:
            lines.append(f"class {self.class_name}:")

        # Class docstring if present
        class_docstring = ast.get_docstring(self.class_node)
        if class_docstring and body_level == 'docstring':
            lines.append(self._format_docstring(class_docstring, indent=1))

        # Class body
        has_body = False
        for node in self.class_node.body:
            if isinstance(node, ast.FunctionDef):
                method_code = self._create_interface_method(node, body_level)
                lines.append('')
                lines.append(method_code)
                has_body = True
            elif isinstance(node, ast.AnnAssign):
                # Class-level annotated assignment
                ann_code = self._get_node_source(node)
                lines.append(f"    {ann_code}")
                has_body = True
            elif isinstance(node, ast.Assign):
                # Class-level assignment
                assign_code = self._get_node_source(node)
                lines.append(f"    {assign_code}")
                has_body = True

        if not has_body:
            lines.append("    pass")

        return '\n'.join(lines)

    def _create_interface_method(self, node: ast.FunctionDef, body_level: str) -> str:
        """Create interface version of a method."""
        lines = []
        indent = "    "

        # Decorators
        for decorator in node.decorator_list:
            dec_source = self._get_decorator_source(decorator)
            lines.append(f"{indent}@{dec_source}")

        # Method signature
        sig = self._create_method_signature(node)
        lines.append(f"{indent}{sig}")

        # Body based on level
        if body_level == 'docstring':
            docstring = ast.get_docstring(node)
            if docstring:
                lines.append(self._format_docstring(docstring, indent=2))
            lines.append(f"{indent}{indent}pass")
        else:  # 'pass'
            lines.append(f"{indent}{indent}pass")

        return '\n'.join(lines)

    def _create_method_signature(self, node: ast.FunctionDef) -> str:
        """Create the method signature string."""
        args_parts = []

        args = node.args

        # Regular args
        defaults_offset = len(args.args) - len(args.defaults)
        for i, arg in enumerate(args.args):
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._annotation_to_string(arg.annotation)}"

            # Check for default
            default_idx = i - defaults_offset
            if default_idx >= 0 and default_idx < len(args.defaults):
                default = args.defaults[default_idx]
                arg_str += f"={self._value_to_string(default)}"

            args_parts.append(arg_str)

        # *args
        if args.vararg:
            vararg_str = f"*{args.vararg.arg}"
            if args.vararg.annotation:
                vararg_str += f": {self._annotation_to_string(args.vararg.annotation)}"
            args_parts.append(vararg_str)
        elif args.kwonlyargs:
            args_parts.append('*')

        # Keyword-only args
        for i, arg in enumerate(args.kwonlyargs):
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._annotation_to_string(arg.annotation)}"
            if i < len(args.kw_defaults) and args.kw_defaults[i] is not None:
                arg_str += f"={self._value_to_string(args.kw_defaults[i])}"
            args_parts.append(arg_str)

        # **kwargs
        if args.kwarg:
            kwarg_str = f"**{args.kwarg.arg}"
            if args.kwarg.annotation:
                kwarg_str += f": {self._annotation_to_string(args.kwarg.annotation)}"
            args_parts.append(kwarg_str)

        # Return type
        returns = ""
        if node.returns:
            returns = f" -> {self._annotation_to_string(node.returns)}"

        return f"def {node.name}({', '.join(args_parts)}){returns}:"

    def _annotation_to_string(self, annotation: ast.expr) -> str:
        """Convert an annotation AST node to string."""
        try:
            return ast.unparse(annotation)
        except:
            # Fallback for older Python
            return self._get_node_source(annotation)

    def _value_to_string(self, value: ast.expr) -> str:
        """Convert a value AST node to string."""
        try:
            return ast.unparse(value)
        except:
            return self._get_node_source(value)

    def _get_decorator_source(self, decorator: ast.expr) -> str:
        """Get source code for a decorator."""
        try:
            return ast.unparse(decorator)
        except:
            return self._get_node_source(decorator)

    def _format_docstring(self, docstring: str, indent: int = 1) -> str:
        """Format a docstring with proper indentation."""
        indent_str = "    " * indent

        # Check if multiline
        if '\n' in docstring:
            lines = docstring.split('\n')
            formatted_lines = [f'{indent_str}"""']
            for line in lines:
                formatted_lines.append(f"{indent_str}{line}")
            formatted_lines.append(f'{indent_str}"""')
            return '\n'.join(formatted_lines)
        else:
            return f'{indent_str}"""{docstring}"""'

    def _get_node_source(self, node: ast.AST) -> str:
        """Get the original source code for an AST node."""
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            start_line = node.lineno - 1
            end_line = node.end_lineno
            return '\n'.join(self.source_lines[start_line:end_line])

        # Fallback to ast.unparse
        try:
            return ast.unparse(node)
        except:
            return ""


def main():
    """CLI for testing the extractor."""
    import argparse

    parser = argparse.ArgumentParser(description='Extract class context from Python file')
    parser.add_argument('source_file', help='Path to Python source file')
    parser.add_argument('--class-name', help='Name of class to extract (auto-detected if single)')
    parser.add_argument('--level', choices=ContextLevel.ALL, default=ContextLevel.FULL_CONTEXT,
                        help='Context extraction level')
    parser.add_argument('--info', action='store_true', help='Show class info only')

    args = parser.parse_args()

    try:
        extractor = ClassContextExtractor(Path(args.source_file), args.class_name)

        if args.info:
            info = extractor.get_class_info()
            print(f"Class: {info.name}")
            print(f"Module: {info.module_name}")
            print(f"File: {info.file_path}")
            print(f"Public methods: {', '.join(info.public_methods)}")
            print(f"Helper types: {', '.join(info.helper_types) or 'None'}")
            print(f"Base classes: {', '.join(info.base_classes) or 'None'}")
            print(f"Import: {info.import_statement}")
        else:
            context = extractor.extract_context(args.level)
            print(context)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
