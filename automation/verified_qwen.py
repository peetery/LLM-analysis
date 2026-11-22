import ast
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    from .suite_refinement import validated_numeric_edits
except ImportError:
    from suite_refinement import validated_numeric_edits

MODEL = "qwen/qwen3-coder-30b-a3b-instruct"
GEMINI_MODEL = "gemini-3.6-flash"
MODEL_PROFILES = {
    MODEL: {"provider": "openrouter", "max_tokens": 6000, "thinking_level": None},
    GEMINI_MODEL: {"provider": "google", "max_tokens": 8192, "thinking_level": "low"},
}
WORKER = Path(__file__).with_name("quality_worker.py")


def digest(value):
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()


def save(path, value):
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        temporary.write_text(json.dumps(value, indent=2))
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def environment():
    return {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "coverage": importlib.metadata.version("coverage"),
        "mutmut": importlib.metadata.version("mutmut"),
        "worker_sha256": digest(WORKER.read_text()),
        "pipeline_sha256": digest(Path(__file__).read_text()),
        "repair_guard_sha256": digest(Path(__file__).with_name("suite_refinement.py").read_text()),
        "provider_sha256": digest(
            Path(__file__).parent.joinpath("cli_automation/qwen_client.py").read_text()
        ),
        "google_provider_sha256": digest(
            Path(__file__).parent.joinpath("cli_automation/gemini_api_client.py").read_text()
        ),
    }


def worker(source, tests, module_name, coverage=False, freeze=False):
    with tempfile.TemporaryDirectory(prefix="verified-qwen-") as directory:
        root = Path(directory).resolve()
        (root / (module_name + ".py")).write_text(source)
        if tests is not None:
            (root / "tests.py").write_text(tests)
        (root / "setup.cfg").write_text("[mutmut]\nsource_paths = .\n")
        command = [sys.executable, "-I", str(WORKER), "--module", module_name]
        if freeze:
            command.append("--freeze")
        if coverage:
            command.append("--coverage")
        if sys.platform == "darwin" and Path("/usr/bin/sandbox-exec").exists():
            readable = [
                "/System",
                "/usr",
                "/Library",
                "/opt/homebrew",
                "/dev",
                "/private/var/db",
                "/private/etc",
                str(Path(sys.prefix).resolve()),
                str(WORKER.parent.resolve()),
                str(root),
            ]
            profile = "\n".join(
                [
                    "(version 1)",
                    "(deny default)",
                    "(allow process*)",
                    "(allow sysctl-read)",
                    "(allow mach-lookup)",
                    "(allow file-read-metadata)",
                    '(allow file-read* (literal "/"))',
                    "(allow file-read* "
                    + " ".join(f"(subpath {json.dumps(path)})" for path in readable)
                    + ")",
                    f'(allow file-write* (subpath {json.dumps(str(root))}) (literal "/dev/null"))',
                    "(deny file-write* "
                    + " ".join(
                        f"(literal {json.dumps(str(root / name))})"
                        for name in (module_name + ".py", "tests.py")
                    )
                    + ")",
                ]
            )
            command = ["/usr/bin/sandbox-exec", "-p", profile, *command]
        env = {
            "PATH": str(Path(sys.executable).parent) + os.pathsep + "/usr/bin:/bin",
            "HOME": str(root),
            "TMPDIR": str(root),
            "PYTHONHASHSEED": "0",
            "LANG": "en_US.UTF-8",
        }
        if "SYSTEMROOT" in os.environ:
            env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
        try:
            result = subprocess.run(
                command,
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                timeout=120 if freeze else 15,
            )
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "tests": 0, "log": "Isolated execution timed out."}
        if result.returncode != 0:
            return {"status": "worker_error", "tests": 0, "log": result.stderr[-6000:]}
        return json.loads(result.stdout)


def inspect_suite(code, module_name):
    tree = ast.parse(code)
    allowed = {
        module_name,
        "unittest",
        "math",
        "copy",
        "decimal",
        "fractions",
        "itertools",
        "collections",
        "typing",
        "contextlib",
        "operator",
    }
    imported_subject = {module_name}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
            imported_subject.update(
                alias.asname or alias.name for alias in node.names if alias.name == module_name
            )
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or ""]
            if any(
                alias.name in {"*", "skip", "skipIf", "skipUnless", "expectedFailure", "mock"}
                for alias in node.names
            ):
                raise ValueError(
                    "Wildcard imports and skipped/expected-failure helpers are not accepted."
                )
            if node.module == module_name:
                imported_subject.update(alias.asname or alias.name for alias in node.names)
        else:
            modules = []
        if any(name.split(".")[0] not in allowed for name in modules):
            raise ValueError("Suite uses an unapproved import.")
        if any(".mock" in name for name in modules):
            raise ValueError("Mocking the application is not accepted.")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {
                "open",
                "eval",
                "exec",
                "compile",
                "__import__",
                "breakpoint",
                "setattr",
                "delattr",
            }:
                raise ValueError("Suite uses an unsupported dynamic or external operation.")
        if isinstance(node, ast.Attribute) and node.attr in {
            "skip",
            "skipIf",
            "skipUnless",
            "skipTest",
            "expectedFailure",
            "mock",
        }:
            raise ValueError("Skipped tests, expected failures and patching are not accepted.")
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id in imported_subject
                ):
                    raise ValueError("Suite cannot replace the application implementation.")
    instances = set()
    assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)]
    for _ in range(len(assignments) + 1):
        previous = set(instances)
        for node in assignments:
            value = node.value
            constructor = isinstance(value, ast.Call) and (
                isinstance(value.func, ast.Name)
                and value.func.id in imported_subject
                or isinstance(value.func, ast.Attribute)
                and ast.unparse(value.func.value) in imported_subject
            )
            if constructor or ast.unparse(value) in instances:
                instances.update(ast.unparse(target) for target in node.targets)
        if instances == previous:
            break

    def subject_state(target):
        while isinstance(target, (ast.Attribute, ast.Subscript)):
            if ast.unparse(target.value) in instances:
                return True
            target = target.value
        return False

    for node in ast.walk(tree):
        targets = (
            node.targets
            if isinstance(node, (ast.Assign, ast.Delete))
            else [node.target]
            if isinstance(node, (ast.AugAssign, ast.AnnAssign))
            else []
        )
        if any(subject_state(target) for target in targets):
            raise ValueError("Tests must use public APIs, not write application instance state.")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = node.func.value
            if ast.unparse(owner) in instances and node.func.attr.startswith("_"):
                raise ValueError("Tests must not call private application methods.")
            if subject_state(owner) and node.func.attr in {
                "append",
                "extend",
                "insert",
                "pop",
                "remove",
                "clear",
                "update",
                "setdefault",
                "__setitem__",
                "__delitem__",
            }:
                raise ValueError("Tests must not mutate application instance containers.")
    return tree


def extract_python(response):
    fenced = re.fullmatch(r"\s*```(?:python)?[ \t]*\n(.*?)\n```\s*", response, re.DOTALL)
    code = fenced.group(1) if fenced else response
    ast.parse(code)
    return code


def load_qwen_suite(original, source, module_name, model=MODEL):
    original = Path(original).resolve()
    if (original / (module_name + ".py")).read_text() != source:
        raise ValueError("Archived source differs from the current source.")
    if (original / "experiment_results.json").exists():
        data = json.loads((original / "experiment_results.json").read_text())
        raw_results = data.get("raw_results", {})
        calls = raw_results.get("provider_calls", [])
        if not calls or any(
            call.get("model") != model or call.get("finish_reason") != "stop" for call in calls
        ):
            raise ValueError("Resume requires an archived complete Qwen generation.")
        tests = (original / "tests.py").read_text()
        raw_response = raw_results.get("final_response") or raw_results.get("response", "")
        raw_tree = ast.parse(extract_python(raw_response))
        extracted = ast.Module(
            body=[
                node
                for node in raw_tree.body
                if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef))
            ],
            type_ignores=[],
        )
        if ast.dump(extracted, include_attributes=False) != ast.dump(
            ast.parse(tests), include_attributes=False
        ):
            raise ValueError(
                "Archived tests differ from the original Qwen response; manual suites cannot seed this cache."
            )
        inspect_suite(tests, module_name)
        return tests, [
            {
                "origin": "resumed_qwen",
                "tests_sha256": digest(tests),
                "original_run": str(original),
                "provider_calls": calls,
            }
        ]
    report = json.loads((original / "report.json").read_text())
    chain = report.get("provenance", [])
    if not chain:
        raise ValueError("Verified-run resume requires a Qwen response lineage.")
    if chain[0].get("original_run"):
        tests, provenance = load_qwen_suite(chain[0]["original_run"], source, module_name, model)
    elif chain[0].get("origin") in {"qwen_generation", "gemini_generation"}:
        initial_file = Path(chain[0].get("response_file", original / "initial_response.json"))
        initial = json.loads(initial_file.read_text())
        calls = initial.get("provider_calls", [])
        if not calls or any(
            call.get("model") != model or call.get("finish_reason") != "stop" for call in calls
        ):
            raise ValueError("Initial suite is not a complete Qwen generation.")
        tests = extract_python(initial["content"])
        if digest(tests) != chain[0]["tests_sha256"]:
            raise ValueError("Initial suite differs from the recorded Qwen response.")
        inspect_suite(tests, module_name)
        provenance = [{**chain[0], "response_file": str(initial_file)}]
    else:
        raise ValueError("Verified-run resume requires an original Qwen generation.")
    for stage in chain[1:]:
        if stage.get("origin") not in {"qwen_refinement", "gemini_refinement"}:
            continue
        response_file = Path(
            stage.get("response_file", original / f"round_{stage['round']}" / "response.json")
        )
        request_file = Path(stage.get("request_file", response_file.with_name("request.json")))
        response = json.loads(response_file.read_text())
        calls = response.get("provider_calls", [])
        if not calls or any(
            call.get("model") != model or call.get("finish_reason") != "stop" for call in calls
        ):
            raise ValueError("Accepted response is not a complete Qwen generation.")
        if response.get("replayed_from"):
            saved = json.loads(Path(response["replayed_from"]).read_text())
            if saved["content"] != response["content"]:
                raise ValueError("Replayed response differs from its saved Qwen output.")
        prompt = json.loads(request_file.read_text())["prompt"]
        if f"CURRENT SUITE:\n{tests}\n\nEXECUTION:" not in prompt or source not in prompt:
            raise ValueError("Accepted response targets a different source or suite.")
        feedback = json.JSONDecoder().raw_decode(
            prompt.partition(f"CURRENT SUITE:\n{tests}\n\nEXECUTION:\n")[2]
        )[0]
        additions_only = stage.get("additions_only", False)
        repairs_only = stage.get("repairs_only", False)
        if additions_only and feedback.get("status") != "passed":
            raise ValueError("Additions-only admission requires a passing original suite.")
        if repairs_only and feedback.get("status") != "failed":
            raise ValueError("Repair-only admission requires a failing original suite.")
        tests, _ = apply_response(
            tests,
            response["content"],
            feedback.get("log", ""),
            module_name,
            additions_only=additions_only,
            repairs_only=repairs_only,
        )
        if digest(tests) != stage["tests_sha256"]:
            raise ValueError("Accepted suite differs from its saved Qwen response.")
        provenance.append(
            {**stage, "response_file": str(response_file), "request_file": str(request_file)}
        )
    if tests != (original / "tests.py").read_text():
        raise ValueError("Archived verified suite has been modified outside Qwen admission.")
    return tests, provenance


def response_payload(response):
    fenced = re.fullmatch(r"\s*```(?:json)?[ \t]*\n(.*?)\n```\s*", response, re.DOTALL)
    text = (fenced.group(1) if fenced else response).lstrip()
    payload, end = json.JSONDecoder(strict=False).raw_decode(text)
    if text[end:].strip() not in {"", "```"}:
        raise ValueError("Unexpected content after the complete JSON response.")
    if (
        not isinstance(payload, dict)
        or set(payload) != {"edits", "additions"}
        or not isinstance(payload["edits"], list)
    ):
        raise ValueError("Expected edits and additions JSON.")
    if isinstance(payload["additions"], list) and all(
        isinstance(code, str) for code in payload["additions"]
    ):
        payload["additions"] = "\n\n".join(payload["additions"])
    if not isinstance(payload["additions"], str):
        raise ValueError("Additions must be Python text or a list of Python text blocks.")
    return payload


def apply_response(
    previous, response, failure_log, module_name, additions_only=False, repairs_only=False
):
    if additions_only and repairs_only:
        raise ValueError("Choose additions-only or repair-only admission, not both.")
    payload = response_payload(response)
    candidate = previous
    repairs = []
    if payload["edits"] and not additions_only:
        candidate, repairs, _ = validated_numeric_edits(
            previous, json.dumps({"edits": payload["edits"]}), failure_log
        )
    additions = "" if repairs_only else payload["additions"].strip()
    if additions:
        names = set()
        imports = {}
        for node in ast.parse(previous).body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                names.add(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    binding = alias.asname or (
                        alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name
                    )
                    names.add(binding)
                    imports[binding] = (getattr(node, "module", None), alias.name, alias.asname)
            elif isinstance(node, ast.Assign):
                names.update(target.id for target in node.targets if isinstance(target, ast.Name))
        methods = 0
        for node in ast.parse(additions).body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    binding = alias.asname or (
                        alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name
                    )
                    signature = (getattr(node, "module", None), alias.name, alias.asname)
                    if binding in names and imports.get(binding) != signature:
                        raise ValueError("Additions cannot shadow existing names or imports.")
                    names.add(binding)
                    imports[binding] = signature
                continue
            if not isinstance(node, ast.ClassDef) or node.name in names:
                raise ValueError("Additions may contain imports and new test classes only.")
            names.add(node.name)
            methods += sum(
                isinstance(method, ast.FunctionDef) and method.name.startswith("test")
                for method in node.body
            )
        limit = 32 if additions_only else 16
        if methods > limit:
            raise ValueError(
                "Add at most thirty-two tests in additions-only mode."
                if additions_only
                else "Add at most sixteen focused grouped tests per round."
            )
        candidate = candidate.rstrip() + "\n\n" + additions + "\n"
    inspect_suite(candidate, module_name)
    return candidate, repairs


def frozen_pool(source, module_name, cache):
    identity = digest(
        {
            "source": digest(source),
            "module": module_name,
            "engine": importlib.metadata.version("mutmut"),
            "seed": 2026,
            "worker_sha256": digest(WORKER.read_text()),
        }
    )
    pools = cache / "mutants"
    pools.mkdir(parents=True, exist_ok=True)
    path = pools / (identity + ".json")
    if path.exists():
        pool = json.loads(path.read_text())
    else:
        pool = worker(source, None, module_name, freeze=True)
        if "mutants" not in pool:
            raise RuntimeError("Mutant generation failed: " + pool.get("log", "no pool"))
        save(path, pool)
    if pool["source_sha256"] != digest(source) or not pool["mutants"]:
        raise ValueError("Frozen mutant pool does not match the source.")
    for item in pool["mutants"]:
        if digest(item["source"]) != item["sha256"]:
            raise ValueError("Frozen mutant contents were modified.")
    return pool


def mutation_results(tests, mutants, module_name):
    outcomes = []
    for mutant in mutants:
        result = worker(mutant["source"], tests, module_name)
        outcome = {"passed": "survived", "failed": "killed", "timeout": "timeout"}.get(
            result["status"], "unviable"
        )
        outcomes.append({"id": mutant["id"], "outcome": outcome})
    return outcomes


def score(outcomes):
    return (
        100 * sum(item["outcome"] == "killed" for item in outcomes) / len(outcomes)
        if outcomes
        else None
    )


def quality_passed(baseline, outcomes, mutation_target, branch_target):
    mutation_score = score(outcomes)
    return bool(
        baseline.get("status") == "passed"
        and baseline.get("tests", 0) > 0
        and not baseline.get("skipped")
        and not baseline.get("expected_failures")
        and baseline.get("branch_coverage", -1) >= branch_target
        and mutation_score is not None
        and mutation_score > mutation_target
    )


def cache_identity(source, pool, mutation_target, branch_target, module_name, model=MODEL):
    return digest(
        {
            "source_sha256": digest(source),
            "pool_sha256": digest(pool),
            "environment": environment(),
            "model": model,
            "provider": MODEL_PROFILES[model]["provider"],
            "temperature": 0.2,
            "max_tokens": MODEL_PROFILES[model]["max_tokens"],
            "thinking_level": MODEL_PROFILES[model]["thinking_level"],
            "mutation_strictly_greater_than": mutation_target,
            "branch_at_least": branch_target,
            "module": module_name,
        }
    )


def source_branches(source, missing_arcs=None):
    tree = ast.parse(source)
    functions = [
        node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    branches = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        scopes = [
            function
            for function in functions
            if function.lineno <= node.lineno <= function.end_lineno
        ]
        if not scopes:
            continue
        scope = min(scopes, key=lambda function: function.end_lineno - function.lineno)
        if scope.name.startswith("_") and scope.name != "__init__":
            continue
        arcs = (
            [arc for arc in missing_arcs if arc[0] == node.lineno]
            if missing_arcs is not None
            else [None]
        )
        for arc in arcs:
            branches.append(
                {
                    "method": scope.name,
                    "parameters": ast.unparse(scope.args),
                    "line": node.lineno,
                    "condition": ast.unparse(node.test),
                    "true_path": ast.unparse(node.body[0]),
                    "missing_arc": arc,
                }
            )
    return branches


def feedback_prompt(source, tests, baseline, development, outcomes, rejection=None):
    if baseline.get("status") == "failed":
        return (
            "Repair this failing unittest suite. Return ONLY JSON "
            '{"edits":[{"old":"exact old text","new":"replacement","reason":"source arithmetic"}],'
            '"additions":""}.\n'
            "REPAIR-ONLY PHASE: no new tests, helpers, or state changes. Any additions are "
            "rejected. Change only finite numeric expected literals on reported failing "
            "assertEqual/assertAlmostEqual lines; preserve all inputs, setup, assertions and "
            "tolerances. Use SOURCE and actual test setup, not misleading method names or "
            "comments. Derive each item price*quantity, subtotal, discount, shipping eligibility "
            "against the actual configured threshold, tax base and final total. Do not copy "
            "observed outputs as independent oracle evidence. Include consistent source-backed "
            "arithmetic in reason. No Markdown fences or prose.\n"
            f"\nSOURCE:\n{source}\n\nCURRENT SUITE:\n{tests}\n\nEXECUTION:\n"
            + json.dumps({"status": baseline["status"], "log": baseline.get("log", "")})
            + "\nPREVIOUS REJECTED CANDIDATE FEEDBACK:\n"
            + json.dumps(rejection)
        )
    survived = {item["id"] for item in outcomes if item["outcome"] != "killed"}
    challenges = []
    lines = set()
    for item in development:
        if item["id"] in survived and item["start_line"] not in lines:
            challenges.append({"line": item["start_line"], "diff": item["diff"]})
            lines.add(item["start_line"])
        if len(challenges) == 20:
            break
    exception_literals = [
        {
            "line": node.lineno,
            "exception": ast.unparse(node.exc.func),
            "message": node.exc.args[0].value,
        }
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Raise)
        and isinstance(node.exc, ast.Call)
        and node.exc.args
        and isinstance(node.exc.args[0], ast.Constant)
        and isinstance(node.exc.args[0].value, str)
    ]
    return (
        "Improve this unittest suite. Return ONLY JSON "
        '{"edits":[{"old":"exact old text","new":"replacement","reason":"source arithmetic"}],'
        '"additions":"new unittest.TestCase classes"}.\n'
        "Preserve every existing test, input, assertion, tolerance and setup. Only a reported "
        "failing numeric expected literal may be edited. New coverage belongs in NEW classes, "
        "at most sixteen methods; prefer eight grouped methods using fresh state and subTest. "
        "additions must be a Python string (a list of complete Python strings is also accepted).\n"
        "Cover exact SOURCE-defined error messages using assertRaises as caught then "
        "assertEqual(str(caught.exception), fixed_expected_message), as implementation-conformance "
        "checks. Each error row needs its own expected exception type and message; separate wrong-type "
        "inputs from invalid numeric ranges and actually call the API with that row's inputs. "
        "Cover constructor and invalid-input paths, defaults, zero/one endpoints, "
        "shipping threshold equality, duplicate items and state changes. Use expected messages "
        "from SOURCE, never mutant strings. Never skip, mock, patch, or call private methods. "
        "Do not force unreachable defensive branches by corrupting state.\n"
        "Prioritize MISSING BRANCH TARGETS before adding duplicate tests or mutation challenges. "
        "For each reachable missing guard, invoke its method with inputs that take that exact "
        "path. Test EACH argument's type guard separately with all other arguments valid. "
        "Do not invent negative-input errors unless SOURCE actually rejects that input. "
        "When only a few reachable branches are missing, return only the minimal tests needed, "
        "not unrelated totals or already-covered state/constructor cases. "
        "Use assertAlmostEqual for independently derived floating-point expectations.\n"
        "For totals derive subtotal, discount, shipping AFTER discount, and tax on subtotal PLUS "
        "shipping. Include a source-backed arithmetic reason for each numeric edit. "
        "Escape JSON strings; omit unchanged code.\n"
        + (
            "EXECUTION PASSED: edits MUST be []. All proposed edits will be rejected; "
            "only additions are considered (up to 32 new methods).\n"
            if baseline.get("status") == "passed"
            else ""
        )
        + "\nMISSING BRANCH TARGETS (source predicates, not observed expected values):\n"
        + json.dumps(source_branches(source, baseline.get("missing_branches") or []))
        + f"\nSOURCE:\n{source}\n\nCURRENT SUITE:\n{tests}\n\nEXECUTION:\n"
        + json.dumps(
            {
                key: baseline.get(key)
                for key in ("status", "log", "missing_lines", "missing_branches")
            }
        )
        + "\nDEVELOPMENT MUTANT CHALLENGES (not assertion evidence):\n"
        + json.dumps(challenges)
        + "\nPREVIOUS REJECTED CANDIDATE FEEDBACK:\n"
        + json.dumps(rejection)
        + "\nSOURCE EXCEPTION LITERALS (not runtime observations):\n"
        + json.dumps(exception_literals)
    )


def run_verified(
    source_file,
    output,
    cache_dir,
    client_factory,
    mutation_target=60,
    branch_target=98,
    resume_from=None,
    max_refinements=2,
    replay_from=None,
    additions_only=False,
    fresh=False,
    model=MODEL,
):
    if model not in MODEL_PROFILES:
        raise ValueError("Unsupported verified-mode model.")
    profile = MODEL_PROFILES[model]
    label = "Gemini" if profile["provider"] == "google" else "Qwen"
    if not (
        math.isfinite(mutation_target)
        and 0 <= mutation_target < 100
        and math.isfinite(branch_target)
        and 0 <= branch_target <= 100
    ):
        raise ValueError("Targets must be finite percentages; mutation must be below 100.")
    if type(max_refinements) is not int or not 0 <= max_refinements <= 2:
        raise ValueError("Use zero, one or two feedback refinements.")
    if fresh and (resume_from or replay_from):
        raise ValueError("Fresh generation cannot resume or replay an existing suite.")
    source_file = Path(source_file).resolve()
    module_name = source_file.stem
    if not module_name.isidentifier():
        raise ValueError("Source filename must be a valid Python module name.")
    if module_name == "tests":
        raise ValueError("The source module cannot be named tests.")
    source = source_file.read_text()
    pool = frozen_pool(source, module_name, Path(cache_dir))
    replay_root = Path(replay_from).resolve() if replay_from else None
    replay_records = []
    if replay_root:
        replay_config = json.loads((replay_root / "config.json").read_text())
        replay_report = json.loads((replay_root / "report.json").read_text())
        if replay_config["source_sha256"] != digest(source) or replay_config[
            "pool_sha256"
        ] != digest(pool):
            raise ValueError("Replay source or frozen mutant pool differs from this run.")
        if not resume_from:
            resume_from = replay_config.get("resume_from")
            provenance = replay_report.get("provenance", [])
            if not resume_from and not provenance:
                raise ValueError("Replay requires an archived Qwen response lineage.")
            resume_from = resume_from or provenance[0].get("original_run") or replay_root
        for response_file in sorted(replay_root.glob("round_*/response.json")):
            record = json.loads(response_file.read_text())
            calls = record.get("provider_calls", [])
            if not calls or any(
                call.get("model") != model or call.get("finish_reason") != "stop" for call in calls
            ):
                raise ValueError("Replay requires complete Qwen responses from the expected model.")
            request = json.loads(response_file.with_name("request.json").read_text())
            replay_records.append((response_file, record, request["prompt"]))
    identity = cache_identity(source, pool, mutation_target, branch_target, module_name, model)
    entries = Path(cache_dir) / "entries"
    entries.mkdir(parents=True, exist_ok=True)
    cache_file = entries / (identity + ".json")
    directory = (
        Path(output)
        / "verified"
        / (datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8])
    )
    directory.mkdir(parents=True)
    (directory / (module_name + ".py")).write_text(source)
    save(
        directory / "config.json",
        {
            "cache_identity": identity,
            "source_sha256": digest(source),
            "pool_sha256": digest(pool),
            "environment": environment(),
            "model": model,
            "provider": profile["provider"],
            "generation_settings": profile,
            "mutation_strictly_greater_than": mutation_target,
            "branch_at_least": branch_target,
            "max_refinements": max_refinements,
            "resume_from": str(Path(resume_from).resolve()) if resume_from else None,
            "additions_only": additions_only,
            "fresh": fresh,
            "protocol": "verified_source_conformance",
            "evaluation": "Frozen practical benchmark; not an independently replicated paper result.",
        },
    )
    if cache_file.exists() and not fresh:
        try:
            entry = json.loads(cache_file.read_text())
            inspect_suite(entry["tests"], module_name)
            baseline = worker(source, entry["tests"], module_name, coverage=True)
            if (
                entry["identity"] == identity
                and digest(entry["tests"]) == entry["tests_sha256"]
                and len(entry["outcomes"]) == len(pool["mutants"])
                and {item["id"] for item in entry["outcomes"]}
                == {item["id"] for item in pool["mutants"]}
                and baseline["tests"] == entry["report"]["baseline"]["tests"]
                and quality_passed(baseline, entry["outcomes"], mutation_target, branch_target)
            ):
                report = {
                    **entry["report"],
                    "cache_hit": True,
                    "model_requests_this_run": 0,
                    "replayed_responses_this_run": 0,
                    "baseline": baseline,
                    "result_dir": str(directory),
                }
                (directory / "tests.py").write_text(entry["tests"])
                save(directory / "report.json", report)
                print(
                    f"Verified cache hit: tests passed locally; zero {label} requests.", flush=True
                )
                return report
        except (ValueError, KeyError, TypeError, SyntaxError):
            pass
    tests = ""
    calls = 0
    replayed = 0
    provenance = []
    client = None
    development = [item for item in pool["mutants"] if item["split"] == "development"]
    heldout = [item for item in pool["mutants"] if item["split"] == "heldout"]
    try:
        if resume_from:
            original = Path(resume_from).resolve()
            tests, provenance = load_qwen_suite(original, source, module_name, model)
        else:
            client = client_factory()
            if isinstance(getattr(client, "model", None), str) and client.model != model:
                raise ValueError("Client model differs from the selected verified model.")
            prompt = (
                f"Generate compact deterministic Python unittest tests for module {module_name}. "
                "Return only a complete Python module. Use only unittest and standard-library "
                "helpers. Cover public APIs, constructors, type/range boundaries, exact source "
                "exception messages, defaults, duplicate items and state changes. Group related "
                "cases with subTest and fresh instances. No skipping, mocks, patching or private APIs. "
                "Derive arithmetic independently, including shipping after discount and tax on "
                "discounted subtotal PLUS shipping. Never invent ambiguous expectations. "
                "These are source-conformance tests.\nSOURCE:\n"
                + source
                + "\nSOURCE BRANCH CHECKLIST:\n"
                + json.dumps(source_branches(source))
                + "\nCover each reachable guard's true and false paths. Exercise EACH argument's "
                "wrong-type guard separately, keeping all other arguments valid. Do not invent "
                "negative-input rejection where SOURCE has no such guard. Do not force unreachable "
                "branches by corrupting state. Use assertAlmostEqual for source-derived floats."
            )
            save(directory / "initial_request.json", {"prompt": prompt})
            calls += 1
            response = client.send_prompt(prompt)
            save(
                directory / "initial_response.json",
                {"content": response, "provider_calls": client.provider_calls},
            )
            tests = extract_python(response)
            inspect_suite(tests, module_name)
            provenance.append(
                {
                    "origin": "gemini_generation" if model == GEMINI_MODEL else "qwen_generation",
                    "tests_sha256": digest(tests),
                    "response_file": str((directory / "initial_response.json").resolve()),
                }
            )
        (directory / "initial_tests.py").write_text(tests)
        baseline = worker(source, tests, module_name, coverage=True)
        save(directory / "initial_validation.json", baseline)
        if additions_only and baseline["status"] != "passed":
            raise ValueError("Additions-only admission requires a passing original suite.")
        dev_outcomes = []
        rejection = None
        for round_number in range(max_refinements + 1):
            if baseline["status"] == "passed":
                dev_outcomes = mutation_results(tests, development, module_name)
                print(
                    f"Development mutation: {score(dev_outcomes):.2f}%; "
                    f"branch: {baseline.get('branch_coverage', 0):.2f}%",
                    flush=True,
                )
                if quality_passed(baseline, dev_outcomes, mutation_target, branch_target):
                    break
            if round_number == max_refinements:
                break
            replay_record = None
            if replay_root:
                for index, (response_file, record, original_prompt) in enumerate(replay_records):
                    if (
                        f"CURRENT SUITE:\n{tests}\n\nEXECUTION:" in original_prompt
                        and source in original_prompt
                    ):
                        replay_record = (response_file, record)
                        replay_records.pop(index)
                        break
                if replay_record is None:
                    break
            elif client is None:
                client = client_factory()
            round_dir = directory / f"round_{round_number + 1}"
            round_dir.mkdir()
            prompt = feedback_prompt(source, tests, baseline, development, dev_outcomes, rejection)
            save(round_dir / "request.json", {"prompt": prompt})
            if replay_record:
                response_file, record = replay_record
                response = record["content"]
                replayed += 1
                save(round_dir / "response.json", {**record, "replayed_from": str(response_file)})
                print(
                    f"Replaying saved Qwen response {round_number + 1}; no model request.",
                    flush=True,
                )
            else:
                print(
                    f"{label} feedback refinement {round_number + 1}/{max_refinements}", flush=True
                )
                calls += 1
                response = client.send_prompt(prompt)
                save(
                    round_dir / "response.json",
                    {"content": response, "provider_calls": client.provider_calls[-1:]},
                )
            try:
                stage_additions_only = additions_only or baseline["status"] == "passed"
                stage_repairs_only = baseline["status"] == "failed"
                candidate, repairs = apply_response(
                    tests,
                    response,
                    baseline.get("log", ""),
                    module_name,
                    additions_only=stage_additions_only,
                    repairs_only=stage_repairs_only,
                )
                (round_dir / "candidate.py").write_text(candidate)
                validation = worker(source, candidate, module_name, coverage=True)
                save(round_dir / "validation.json", validation)
                accepted = validation["status"] == "passed" and not validation["skipped"]
                save(
                    round_dir / "admission.json",
                    {
                        "accepted": accepted,
                        "repairs": repairs,
                        "requires_oracle_review": bool(repairs),
                        "additions_only": stage_additions_only,
                        "repairs_only": stage_repairs_only,
                        "rejected_additions": response_payload(response)["additions"]
                        if stage_repairs_only
                        else "",
                        "rejected_edits": response_payload(response)["edits"]
                        if stage_additions_only
                        else [],
                    },
                )
                if accepted:
                    tests, baseline = candidate, validation
                    dev_outcomes = []
                    rejection = None
                    provenance.append(
                        {
                            "origin": "gemini_refinement"
                            if model == GEMINI_MODEL
                            else "qwen_refinement",
                            "round": round_number + 1,
                            "tests_sha256": digest(tests),
                            "repairs": repairs,
                            "replayed_from": str(replay_record[0]) if replay_record else None,
                            "response_file": str((round_dir / "response.json").resolve()),
                            "request_file": str((round_dir / "request.json").resolve()),
                            "additions_only": stage_additions_only,
                            "repairs_only": stage_repairs_only,
                        }
                    )
                else:
                    rejection = {
                        "status": validation["status"],
                        "log": validation.get("log", "")[-6000:],
                    }
            except (ValueError, SyntaxError) as exc:
                save(round_dir / "admission.json", {"accepted": False, "error": str(exc)})
                rejection = {"error": str(exc)}
        outcomes = []
        if baseline["status"] == "passed":
            if not dev_outcomes:
                dev_outcomes = mutation_results(tests, development, module_name)
            outcomes = dev_outcomes + mutation_results(tests, heldout, module_name)
        passed = quality_passed(baseline, outcomes, mutation_target, branch_target)
        blocked_reason = None
        if not passed:
            blocked_reason = (
                f"Quality gate not met: mutation={score(outcomes)}, "
                f"branch={baseline.get('branch_coverage')}, reference_status={baseline['status']}."
            )
            if rejection:
                blocked_reason += " Last rejected candidate: " + json.dumps(rejection)
        report = {
            "model": model,
            "provider": profile["provider"],
            "quality_passed": passed,
            "status": "verified" if passed else "blocked",
            "cache_hit": False,
            "model_requests_this_run": calls,
            "replayed_responses_this_run": replayed,
            "baseline": baseline,
            "mutation_score": score(outcomes),
            "mutants": len(outcomes),
            "killed": sum(item["outcome"] == "killed" for item in outcomes),
            "development_score": score(dev_outcomes),
            "outcomes": outcomes,
            "provenance": provenance,
            "result_dir": str(directory),
            "mutation_strictly_greater_than": mutation_target,
            "branch_at_least": branch_target,
            "evaluation_note": "Fixed source-conformance benchmark, not a guarantee for changed inputs.",
            "error": blocked_reason,
        }
        (directory / "tests.py").write_text(tests)
        save(directory / "report.json", report)
        if passed:
            save(
                cache_file,
                {
                    "identity": identity,
                    "tests": tests,
                    "tests_sha256": digest(tests),
                    "outcomes": outcomes,
                    "report": report,
                },
            )
        return report
    except (RuntimeError, ValueError, SyntaxError) as exc:
        report = {
            "model": model,
            "provider": profile["provider"],
            "quality_passed": False,
            "status": "blocked",
            "error": str(exc),
            "cache_hit": False,
            "model_requests_this_run": calls,
            "result_dir": str(directory),
        }
        save(directory / "report.json", report)
        return report
    finally:
        if client is not None:
            client.cleanup()
