"""
Cross-Platform Windows 10/11 & Linux/macOS Helper for Meta Legal Agent Workshop
Runs all workshop operations natively in Python without requiring bash or WSL.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 on Windows 10
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent

def load_env():
    env_file = ROOT / ".env"
    if not env_file.exists():
        example = ROOT / ".env.example"
        if example.exists():
            import shutil
            shutil.copy(example, env_file)

    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v

    if "CASE_DIR" not in os.environ or not os.environ["CASE_DIR"]:
        os.environ["CASE_DIR"] = str((ROOT.parent / "cases" / "northbridge-v-caldera").resolve())

def run_cmd(cmd_args, env=None):
    current_env = os.environ.copy()
    if env:
        current_env.update(env)
    return subprocess.run([sys.executable] + cmd_args, env=current_env, cwd=ROOT)

def main():
    load_env()

    parser = argparse.ArgumentParser(description="Meta Legal Agent Workshop Helper")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # setup
    p_setup = subparsers.add_parser("setup", help="Initialize case documents, check keys and workspace")

    # test
    p_test = subparsers.add_parser("test", help="Run offline unit tests")
    p_test.add_argument("--verification", action="store_true", help="Enable verification tests")

    # reset
    p_reset = subparsers.add_parser("reset", help="Reset workspace to initial case documents")
    p_reset.add_argument("--clear-runs", action="store_true", help="Clear previous runs")

    # run
    p_run = subparsers.add_parser("run", help="Run the autonomous agent")
    p_run.add_argument("--turns", type=int, default=30, help="Turn limit")
    p_run.add_argument("--resume", type=str, help="Resume specific run ID")

    # verify
    p_verify = subparsers.add_parser("verify", help="Run verification checks on a run")
    p_verify.add_argument("run_id", help="Run ID to verify")
    p_verify.add_argument("--memo", action="store_true", help="Verify memo")
    p_verify.add_argument("--checklist", action="store_true", help="Verify checklist")

    # branch
    p_branch = subparsers.add_parser("branch", help="Branch a run with verification enabled")
    p_branch.add_argument("run_id", help="Run ID to branch from")

    # review
    p_review = subparsers.add_parser("review", help="Review an escalated run")
    p_review.add_argument("run_id", help="Run ID")
    p_review.add_argument("--approve", action="store_true")
    p_review.add_argument("--reject", action="store_true")
    p_review.add_argument("--answer", type=str)
    p_review.add_argument("--notes", type=str, default="")

    # describe
    p_describe = subparsers.add_parser("describe", help="Output case description JSON")

    args, unknown = parser.parse_known_args()

    if args.command == "setup":
        run_cmd(["scripts/reset_case.py"])
        run_cmd(["scripts/preflight.py", "--expect-release", "initial"])
        print("\n✔ Workshop Setup Complete! You are ready to run on Windows 10.")
    elif args.command == "reset":
        cmd = ["scripts/reset_case.py"]
        if getattr(args, "clear_runs", False):
            cmd.append("--clear-runs")
        run_cmd(cmd)
    elif args.command == "test":
        ver_flag = "on" if getattr(args, "verification", False) else "off"
        run_cmd(["scripts/preflight.py", "--expect-release", "auto"], env={"VERIFICATION": ver_flag})
        run_cmd(["-m", "unittest", "discover", "-s", "tests"], env={"VERIFICATION": ver_flag})
    elif args.command == "run":
        cmd = ["-m", "legal_agent"]
        if args.turns:
            cmd.extend(["--turns", str(args.turns)])
        if args.resume:
            cmd.extend(["--resume", args.resume])
        run_cmd(cmd)
    elif args.command == "verify":
        cmd = ["scripts/verify.py", args.run_id]
        if args.memo:
            cmd.append("--memo")
        if args.checklist:
            cmd.append("--checklist")
        run_cmd(cmd)
    elif args.command == "branch":
        run_cmd(["scripts/branch.py", args.run_id])
    elif args.command == "review":
        cmd = ["scripts/review.py", args.run_id]
        if args.approve:
            cmd.append("--approve")
        elif args.reject:
            cmd.append("--reject")
        elif args.answer:
            cmd.extend(["--answer", args.answer])
        if args.notes:
            cmd.extend(["--notes", args.notes])
        run_cmd(cmd)
    elif args.command == "describe":
        run_cmd(["scripts/describe.py"])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
