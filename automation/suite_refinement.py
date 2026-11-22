import ast
import copy
import json
import math
import re
from pathlib import Path


def numeric_literal(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = numeric_literal(node.operand)
        if value is not None:
            return -value if isinstance(node.op, ast.USub) else value
    return None


def validated_numeric_edits(previous, response, failure_log):
    fenced = re.fullmatch(r"\s*```(?:json)?\s*\n(.*?)\n```\s*", response, re.DOTALL)
    payload = json.loads(fenced.group(1) if fenced else response, strict=False)
    if not isinstance(payload, dict) or set(payload) != {"edits"}:
        raise ValueError("Return only a JSON object with an edits list.")
    if not isinstance(payload["edits"], list) or not payload["edits"]:
        raise ValueError("No repair edits were supplied.")
    failed_lines = {
        int(line) for line in re.findall(
            r'File "[^"\n]+[/\\]tests\.py", line (\d+), in test_\w+', failure_log
        )
    }
    ranges = []
    for edit in payload["edits"]:
        if (not isinstance(edit, dict) or set(edit) != {"old", "new", "reason"} or
                not all(isinstance(edit[key], str) and edit[key] for key in edit)):
            raise ValueError("Each edit needs old text, new text and a source-backed reason.")
        matches = list(re.finditer(re.escape(edit["old"]), previous))
        if len(matches) > 1:
            matches = [
                match for match in matches
                if any(
                    previous.count("\n", 0, match.start()) + 1 <= line
                    <= previous.count("\n", 0, match.end() - 1) + 1
                    for line in failed_lines
                )
            ]
        if len(matches) != 1:
            raise ValueError("Each edit must match exactly once on an unambiguous failing assertion.")
        start = matches[0].start()
        ranges.append((start, start + len(edit["old"]), edit["new"]))
    ranges.sort()
    if any(a[1] > b[0] for a, b in zip(ranges, ranges[1:])):
        raise ValueError("Repair edits cannot overlap.")
    candidate = previous
    for start, end, new in reversed(ranges):
        candidate = candidate[:start] + new + candidate[end:]
    before = ast.parse(previous)
    after = ast.parse(candidate)
    before_calls = [node for node in ast.walk(before) if isinstance(node, ast.Call)]
    after_calls = [node for node in ast.walk(after) if isinstance(node, ast.Call)]
    if len(before_calls) != len(after_calls):
        raise ValueError("Repair cannot add or remove calls.")
    repairs = []
    for old, new in zip(before_calls, after_calls):
        if ast.dump(old, include_attributes=False) == ast.dump(new, include_attributes=False):
            continue
        if (old.lineno not in failed_lines or not isinstance(old.func, ast.Attribute) or
                not isinstance(old.func.value, ast.Name) or old.func.value.id != "self" or
                old.func.attr not in {"assertEqual", "assertAlmostEqual"} or
                len(old.args) < 2 or len(new.args) < 2):
            raise ValueError("Only a reported failing numeric expectation can change.")
        old_value, new_value = numeric_literal(old.args[1]), numeric_literal(new.args[1])
        if (old_value is None or new_value is None or
                (isinstance(old_value, float) and not math.isfinite(old_value)) or
                (isinstance(new_value, float) and not math.isfinite(new_value))):
            raise ValueError("Repairs must use finite numeric literals.")
        original, proposed = copy.deepcopy(old), copy.deepcopy(new)
        original.args[1] = proposed.args[1] = ast.Constant(value=0)
        if ast.dump(original, include_attributes=False) != ast.dump(proposed, include_attributes=False):
            raise ValueError("Inputs, actual expressions, assertion type and tolerance must stay unchanged.")
        repairs.append({
            "line": old.lineno, "expected_before": old_value, "expected_after": new_value,
            "review_status": "pending", "kind": "numeric_expectation"
        })
        old.args[1] = new.args[1] = ast.Constant(value=0)
    if not repairs or ast.dump(before, include_attributes=False) != ast.dump(after, include_attributes=False):
        raise ValueError("Repair changed code outside the failing numeric expectations.")
    return candidate, repairs, payload["edits"]


def refine_failed_suite(runner, result_dir, experiment_data, analysis, client=None, response=None):
    compilation = (analysis or {}).get("compilation", {})
    if compilation.get("execution_success") or not compilation.get("compilation_success"):
        raise ValueError("Refinement requires a compiled suite with execution failures.")
    result_dir = Path(result_dir).resolve()
    previous = (result_dir / "tests.py").read_text()
    source = (result_dir / f"{runner.module_name}.py").read_text()
    failures = "\n".join(compilation.get("test_errors", []))
    prompt = (
        "Repair only the failing numeric assertion expectations in the suite below.\n"
        "Return JSON: {\"edits\": [{\"old\": \"exact existing text\", "
        "\"new\": \"replacement text\", \"reason\": \"source-derived arithmetic\"}]}.\n"
        "Escape JSON strings. Preserve all methods, inputs, calls, assertions and tolerances.\n"
        "Do not add tests, weaken checks, or copy observed outputs as expected values.\n"
        "Derive expectations from the source's defaults and helper calls. For totals, "
        "calculate subtotal, discount, shipping eligibility after discount, and tax "
        "on discounted subtotal PLUS shipping. Explain each intermediate in reason.\n"
        f"\nSOURCE:\n{source}\n\nSUITE:\n{previous}\n\nFAILURES:\n{failures}"
    )
    destination = result_dir / "refinement_001"
    destination.mkdir(exist_ok=False)
    (destination / f"{runner.module_name}.py").write_text(source)
    (destination / "request.json").write_text(json.dumps({"prompt": prompt}, indent=2))
    origin = "manual_source_audit" if response is not None else "qwen_refinement"
    if response is None:
        if client is None:
            raise ValueError("A model client or audited edit response is required.")
        try:
            response = client.send_prompt(prompt)
        except RuntimeError as exc:
            audit = {"accepted": False, "origin": origin, "error": str(exc)}
            (destination / "repair_audit.json").write_text(json.dumps(audit, indent=2))
            return {"audit": audit, "analysis": None, "result_dir": str(destination)}
    (destination / "response.json").write_text(json.dumps({"origin": origin, "content": response}, indent=2))
    try:
        candidate, repairs, edits = validated_numeric_edits(previous, response, failures)
        (destination / "tests.py").write_text(candidate)
        data = {**experiment_data, "test_file": str(destination / "tests.py")}
        validated = runner.run_analysis(destination, data, mutation_testing=False)
        accepted = bool(
            validated and validated["compilation"]["execution_success"] and
            validated["compilation"]["tests_run"] == compilation["tests_run"]
        )
        audit = {
            "accepted": accepted, "origin": origin, "repairs": repairs,
            "edits": edits, "original_tests": str(result_dir / "tests.py"),
            "requires_oracle_review": True
        }
        if not accepted:
            audit["error"] = "Candidate still fails or changed the test count; original retained."
    except (ValueError, SyntaxError) as exc:
        audit = {"accepted": False, "origin": origin, "error": str(exc)}
        validated = None
    (destination / "repair_audit.json").write_text(json.dumps(audit, indent=2))
    return {"audit": audit, "analysis": validated, "result_dir": str(destination)}
