import argparse
import ast
import hmac
import json
import os
import signal
import subprocess
import sys
import threading
import time
import uuid
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
REPORT_MARKER = "__QWEN_REPORT__:"


class RequestError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class Runs:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()
        self.token = uuid.uuid4().hex
        self.jobs = {}
        self.processes = {}
        self.lock = threading.Lock()

    def samples(self):
        paths = [
            self.root / "order_calculator.py",
            self.root.parent / "unit-test-feedback/src/test_feedback/web/shopping_cart.py",
        ]
        return [
            {"filename": path.name, "source": path.read_text()} for path in paths if path.is_file()
        ]

    def start(self, data):
        if not isinstance(data, dict):
            raise RequestError("Expected a JSON object.")
        filename, source = data.get("filename", ""), data.get("source", "")
        key, fresh, budget = data.get("api_key", ""), data.get("fresh", True), data.get("budget", 2)
        if (
            not isinstance(filename, str)
            or Path(filename).name != filename
            or Path(filename).suffix != ".py"
            or not Path(filename).stem.isidentifier()
            or Path(filename).stem == "tests"
        ):
            raise RequestError("Use a Python filename such as shopping_cart.py, not a path.")
        if not isinstance(source, str) or not source.strip() or len(source.encode()) > 65536:
            raise RequestError("Source must be nonempty Python text, at most 64 KB.")
        try:
            ast.parse(source)
        except (SyntaxError, ValueError):
            raise RequestError("Source is not valid Python.") from None
        if not isinstance(key, str) or len(key) > 4096:
            raise RequestError("Invalid API key.")
        if type(fresh) is not bool or type(budget) is not int or budget not in (0, 1, 2):
            raise RequestError("Invalid run mode or feedback budget.")
        if fresh and not key.strip():
            raise RequestError("A fresh paid run needs a Google Gemini API key.")
        with self.lock:
            if any(job["status"] == "running" for job in self.jobs.values()):
                raise RequestError("A run is already active. Wait before starting another.", 409)
            for old_id in list(self.jobs)[:-19]:
                del self.jobs[old_id]
            job_id = uuid.uuid4().hex
            folder = self.root / "qwen_results/ui_sources" / job_id
            folder.mkdir(parents=True)
            source_file = folder / filename
            source_file.write_text(source)
            self.jobs[job_id] = {
                "id": job_id,
                "filename": filename,
                "fresh": fresh,
                "status": "running",
                "logs": deque(["Preparing source and frozen mutants..."], maxlen=500),
                "report": None,
            }
        threading.Thread(
            target=self._execute,
            args=(job_id, source_file, key.strip(), fresh, budget),
            daemon=True,
        ).start()
        return job_id

    def _execute(self, job_id, source_file, key, fresh, budget):
        process = None
        try:
            env = {
                name: os.environ[name]
                for name in ("PATH", "LANG", "SYSTEMROOT", "SSL_CERT_FILE")
                if name in os.environ
            }
            env["PYTHONUNBUFFERED"] = "1"
            process = subprocess.Popen(
                [sys.executable, str(ROOT / "qwen_ui.py"), "--worker"],
                cwd=self.root,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
            )
            with self.lock:
                self.processes[job_id] = process
            process.stdin.write(
                json.dumps(
                    {
                        "source_file": str(source_file),
                        "api_key": key,
                        "fresh": fresh,
                        "budget": budget,
                        "root": str(self.root),
                    }
                )
            )
            process.stdin.close()
            report = None
            for line in process.stdout:
                line = line.rstrip()
                if key:
                    line = line.replace(key, "[redacted]")
                if line.startswith(REPORT_MARKER):
                    report = json.loads(line[len(REPORT_MARKER) :])
                elif line:
                    with self.lock:
                        self.jobs[job_id]["logs"].append(line)
            process.wait()
            if report is None:
                report = {
                    "status": "blocked",
                    "quality_passed": False,
                    "error": "Worker ended without a result. See the progress log.",
                }
            with self.lock:
                self.jobs[job_id]["report"] = report
                self.jobs[job_id]["status"] = (
                    "verified" if report.get("quality_passed") else "blocked"
                )
        except Exception:
            with self.lock:
                self.jobs[job_id].update(
                    status="blocked",
                    report={
                        "status": "blocked",
                        "quality_passed": False,
                        "error": "Local worker failed; no success or scores are claimed.",
                    },
                )
        finally:
            key = ""
            if process is not None:
                if process.poll() is None:
                    process.terminate()
                    process.wait()
                if process.stdout:
                    process.stdout.close()
            with self.lock:
                self.processes.pop(job_id, None)

    def get(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)
            if job is None:
                raise RequestError("Run not found.", 404)
            return {**job, "logs": list(job["logs"])}

    def latest(self):
        with self.lock:
            job_id = next(reversed(self.jobs), None)
        return self.get(job_id) if job_id else {"id": None}

    def artifact(self, job_id, name):
        if name not in {"tests.py", "report.json", "initial_response.json"}:
            raise RequestError("Artifact not available.", 404)
        report = self.get(job_id)["report"] or {}
        directory = Path(report.get("result_dir", "")).resolve()
        if not directory.is_relative_to(self.root / "qwen_results/verified"):
            raise RequestError("Artifact not available.", 404)
        path = directory / name
        if not path.is_file():
            raise RequestError("Artifact not available.", 404)
        return path.read_bytes()

    def stop(self):
        with self.lock:
            processes = list(self.processes.values())
        for process in processes:
            if process.poll() is None:
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGTERM)
                else:
                    process.terminate()


def make_server(runs, port=8766):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def respond(self, status, content, kind="application/json"):
            if isinstance(content, dict) or isinstance(content, list):
                content = json.dumps(content).encode()
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(content)

        def authorize(self, api=False):
            expected = str(self.server.server_port)
            if self.headers.get("Host") not in {"127.0.0.1:" + expected, "localhost:" + expected}:
                raise RequestError("Invalid host.", 403)
            if api:
                token = self.headers.get("X-Qwen-UI-Token", "")
                if not token.isascii() or not hmac.compare_digest(token, runs.token):
                    raise RequestError("Reload the UI before making this request.", 403)

        def do_GET(self):
            try:
                path = urlsplit(self.path).path
                self.authorize(api=path.startswith("/api/"))
                if path == "/":
                    page = (ROOT / "ui/index.html").read_text().replace("__UI_TOKEN__", runs.token)
                    self.respond(200, page.encode(), "text/html; charset=utf-8")
                elif path == "/api/samples":
                    self.respond(200, runs.samples())
                elif path == "/api/current":
                    self.respond(200, runs.latest())
                elif path.startswith("/api/runs/"):
                    parts = path.split("/")
                    if len(parts) == 4:
                        self.respond(200, runs.get(parts[3]))
                    elif len(parts) == 6 and parts[4] == "artifacts":
                        self.respond(
                            200, runs.artifact(parts[3], parts[5]), "application/octet-stream"
                        )
                    else:
                        raise RequestError("Not found.", 404)
                else:
                    raise RequestError("Not found.", 404)
            except RequestError as exc:
                self.respond(exc.status, {"error": str(exc)})

        def do_POST(self):
            try:
                self.authorize(api=True)
                if self.path != "/api/runs":
                    raise RequestError("Not found.", 404)
                try:
                    size = int(self.headers.get("Content-Length", "0"))
                except ValueError:
                    raise RequestError("Invalid request length.") from None
                if not 0 < size <= 131072:
                    raise RequestError("Request must be at most 128 KB.")
                try:
                    data = json.loads(self.rfile.read(size))
                except (ValueError, UnicodeError):
                    raise RequestError("Invalid JSON.") from None
                job_id = runs.start(data)
                self.respond(202, {"id": job_id})
            except RequestError as exc:
                self.respond(exc.status, {"error": str(exc)})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def run_worker():
    from automation.cli_automation.gemini_api_client import GeminiAPIClient
    from automation.verified_qwen import GEMINI_MODEL, run_verified

    data = json.load(sys.stdin)
    key = data.pop("api_key", "")

    class ProgressClient(GeminiAPIClient):
        def send_prompt(self, prompt, **kwargs):
            print(f"Sending paid Gemini request {len(self.provider_calls) + 1}...", flush=True)
            last_update = None

            def progress(characters):
                nonlocal last_update
                now = time.monotonic()
                if last_update is None or now - last_update >= 5:
                    print(
                        f"Gemini stream active: {characters} test characters received...",
                        flush=True,
                    )
                    last_update = now

            kwargs["on_chunk"] = progress
            response = super().send_prompt(prompt, **kwargs)
            print("Gemini response received; validating tests...", flush=True)
            return response

    try:
        root = Path(data["root"])
        print("Fresh paid generation." if data["fresh"] else "Checking verified cache.", flush=True)
        report = run_verified(
            data["source_file"],
            root / "qwen_results",
            root / ".verified_qwen_cache",
            lambda: ProgressClient(api_key=key),
            mutation_target=60.0,
            branch_target=98.0,
            max_refinements=data["budget"],
            fresh=data["fresh"],
            model=GEMINI_MODEL,
        )
    except Exception:
        report = {
            "status": "blocked",
            "quality_passed": False,
            "error": "Worker could not initialize the analysis pipeline.",
        }
    output = REPORT_MARKER + json.dumps(report)
    if key:
        output = output.replace(key, "[redacted]")
    print(output, flush=True)
    key = ""


def main():
    parser = argparse.ArgumentParser(description="Local fresh-paid Google Gemini demo UI.")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        run_worker()
        return
    runs = Runs()
    server = make_server(runs, args.port)
    print(f"Gemini UI: http://127.0.0.1:{server.server_port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        runs.stop()
        server.server_close()


if __name__ == "__main__":
    main()
