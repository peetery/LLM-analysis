import argparse
import contextlib
import difflib
import hashlib
import importlib.metadata
import io
import json
import random
import sys
import unittest
from pathlib import Path


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def freeze(source, module_name):
    from libcst.metadata import MetadataWrapper, PositionProvider
    from mutmut.mutation.file_mutation import create_mutations

    module, mutations, _, _ = create_mutations(module_name + ".py", source)
    positions = MetadataWrapper(module, unsafe_skip_copy=True).resolve(PositionProvider)
    seen = {sha(source)}
    items = []
    for mutation in mutations:
        changed = module.deep_replace(mutation.original_node, mutation.mutated_node).code
        identity = sha(changed)
        if identity in seen:
            continue
        seen.add(identity)
        try:
            compile(changed, module_name + ".py", "exec")
        except (SyntaxError, ValueError):
            continue
        location = positions[mutation.original_node]
        items.append(
            {
                "id": identity[:16],
                "sha256": identity,
                "source": changed,
                "start_line": location.start.line,
                "end_line": location.end.line,
                "diff": "".join(
                    difflib.unified_diff(
                        source.splitlines(keepends=True),
                        changed.splitlines(keepends=True),
                        fromfile="reference/" + module_name + ".py",
                        tofile="mutant/" + module_name + ".py",
                    )
                ),
            }
        )
    items.sort(key=lambda item: (item["start_line"], item["end_line"], item["id"]))
    clusters = []
    end = -1
    for item in items:
        if item["start_line"] > end:
            clusters.append([])
        clusters[-1].append(item)
        end = max(end, item["end_line"])
    if len(clusters) < 2:
        raise ValueError("Need mutants in at least two disjoint source regions.")
    random.Random(2026).shuffle(clusters)
    mutants = [
        {**item, "split": "development" if index % 2 == 0 else "heldout"}
        for index, cluster in enumerate(clusters)
        for item in cluster
    ]
    return {
        "source_sha256": sha(source),
        "module": module_name,
        "seed": 2026,
        "mutmut_version": importlib.metadata.version("mutmut"),
        "mutants": mutants,
    }


def execute(module_name, collect_coverage):
    coverage = None
    if collect_coverage:
        from coverage import Coverage

        coverage = Coverage(branch=True, source=[module_name], config_file=False)
        coverage.start()
    captured = io.StringIO()
    sys.path.insert(0, str(Path.cwd()))
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        suite = unittest.defaultTestLoader.loadTestsFromName("tests")
        result = unittest.TextTestRunner(stream=captured, verbosity=2).run(suite)
    report = {
        "status": "passed"
        if (result.wasSuccessful() and result.testsRun > 0 and not result.expectedFailures)
        else "failed",
        "tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "log": captured.getvalue(),
        "failure_details": [
            {"test": str(test), "traceback": trace}
            for test, trace in result.failures + result.errors
        ],
    }
    if coverage is not None:
        coverage.stop()
        coverage.json_report(outfile="coverage.json")
        data = json.loads(Path("coverage.json").read_text())
        for filename, entry in data["files"].items():
            if Path(filename).name == module_name + ".py":
                summary = entry["summary"]
                report.update(
                    statement_coverage=(
                        100 * summary["covered_lines"] / summary["num_statements"]
                        if summary["num_statements"]
                        else 100.0
                    ),
                    branch_coverage=(
                        100 * summary["covered_branches"] / summary["num_branches"]
                        if summary["num_branches"]
                        else 100.0
                    ),
                    missing_lines=entry["missing_lines"],
                    missing_branches=entry["missing_branches"],
                )
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--coverage", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        result = freeze(Path(args.module + ".py").read_text(), args.module)
    else:
        result = execute(args.module, args.coverage)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
