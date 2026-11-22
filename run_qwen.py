import argparse
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Quality-gated Google Gemini test generation.")
    parser.add_argument("source", nargs="?", type=Path, default=root / "order_calculator.py")
    parser.add_argument(
        "--resume-from", type=Path, help="Continue a saved raw or admitted verified-mode Gemini run."
    )
    parser.add_argument(
        "--replay-from", type=Path, help="Revalidate saved feedback with no model calls."
    )
    parser.add_argument(
        "--max-refinements",
        type=int,
        choices=[0, 1, 2],
        default=2,
        help="Maximum feedback requests; initial generation is separate (default: 2).",
    )
    parser.add_argument(
        "--fresh", action="store_true", help="Make a fresh paid generation, bypassing cache."
    )
    parser.add_argument(
        "--additions-only",
        action="store_true",
        help="Require a passing starting suite; reject edits and validate new tests only.",
    )
    args = parser.parse_args()
    if args.fresh and (args.resume_from or args.replay_from):
        parser.error("--fresh cannot be combined with --resume-from or --replay-from")
    command = [
        sys.executable,
        str(root / "automation/cli_experiment_runner.py"),
        "--model",
        "gemini-3.6-flash",
        "--source-file",
        str(args.source.resolve()),
        "--strategy",
        "simple_prompting",
        "--context",
        "full_context",
        "--verified-cache",
        "--mutation-target",
        "60",
        "--branch-target",
        "98",
        "--prompt-key",
        "--results-dir",
        str(root / "qwen_results"),
        "--cache-dir",
        str(root / ".verified_qwen_cache"),
        "--max-refinements",
        str(args.max_refinements),
    ]
    if args.resume_from:
        command += ["--resume-from", str(args.resume_from.resolve())]
    if args.replay_from:
        command += ["--replay-from", str(args.replay_from.resolve())]
    if args.fresh:
        command += ["--fresh"]
    if args.additions_only:
        command += ["--additions-only"]
    return subprocess.run(command, cwd=root).returncode


if __name__ == "__main__":
    sys.exit(main())
