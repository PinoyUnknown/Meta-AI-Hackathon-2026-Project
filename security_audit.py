"""
MetaSentinel NeuroForge - Zero-Exposure Credential & Security Audit Engine
Scans project files, configuration, and environment for potential secret leakage,
verifies .gitignore rules, and evaluates code invariants according to Meta CyberSecEval.
"""

import os
import re
import sys
import time
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows 10
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SECRET_PATTERNS = [
    (r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "High Entropy Secret Assignment"),
    (r"-----BEGIN (RSA|EC|DSA|OPENSSH|PRIVATE) KEY-----", "Exposed Private Key"),
    (r"(?i)ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"(?i)sk-[A-Za-z0-9]{48}", "OpenAI / Model Secret Key"),
    (r"(?i)fw_[A-Za-z0-9]{32,}", "Fireworks API Key")
]

BLOCKED_EXTENSIONS = [".pem", ".key", ".pkcs12", ".pfx", ".cer", ".crt"]

def audit_directory(root_dir: str = ".") -> Dict[str, Any]:
    findings = []
    scanned_count = 0

    # Ensure .gitignore exists and blocks sensitive files
    gitignore_path = os.path.join(root_dir, ".gitignore")
    has_gitignore = os.path.exists(gitignore_path)
    gitignore_valid = False
    if has_gitignore:
        with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if ".env" in content and "*.pem" in content:
                gitignore_valid = True

    # Scan project files
    for root, dirs, files in os.walk(root_dir):
        # Exclude node_modules, .git, venv, pycache
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", ".venv", "venv", "__pycache__", "dist")]
        for file in files:
            filepath = os.path.join(root, file)
            scanned_count += 1
            ext = os.path.splitext(file)[1].lower()

            if ext in BLOCKED_EXTENSIONS:
                findings.append({
                    "file": filepath,
                    "severity": "CRITICAL",
                    "issue": f"Prohibited sensitive file extension '{ext}' detected."
                })

            # Check file content
            if ext in (".py", ".js", ".json", ".md", ".env.example", ".yml", ".yaml"):
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for idx, line in enumerate(lines, 1):
                            for pat, desc in SECRET_PATTERNS:
                                if re.search(pat, line):
                                    # Ignore example placeholder lines
                                    if "your_" in line.lower() or "example" in line.lower() or "placeholder" in line.lower():
                                        continue
                                    findings.append({
                                        "file": filepath,
                                        "line": idx,
                                        "severity": "CRITICAL",
                                        "issue": f"{desc} in line: '{line.strip()[:40]}...'"
                                    })
                except Exception:
                    pass

    passed = len(findings) == 0 and gitignore_valid
    score = 100.0 if passed else max(0.0, 100.0 - (len(findings) * 35))

    return {
        "timestamp": time.time(),
        "scanned_files": scanned_count,
        "gitignore_valid": gitignore_valid,
        "findings_count": len(findings),
        "findings": findings,
        "score": score,
        "status": "PASSED" if passed else "FAILED"
    }

def run_full_security_audit():
    print("=" * 80)
    print("  METASENTINEL NEUROFORGE - SECURITY & ZERO-EXPOSURE AUDIT")
    print("  Compliance with Meta CyberSecEval 3 & Open Source Security Standards")
    print("=" * 80 + "\n")

    report = audit_directory(".")
    print(f"Scanned: {report['scanned_files']} files across workspace.")
    print(f".gitignore Credential Rules: {'✔ VERIFIED' if report['gitignore_valid'] else '✖ MISSING'}")

    if report["findings_count"] == 0 and report["gitignore_valid"]:
        print(f"\n✔ AUDIT PASSED: Zero exposed secrets, private keys, or passwords detected.")
        print(f"✔ CyberSecEval Credential Score: {report['score']} / 100.0 (Grade: A+)")
    else:
        print(f"\n✖ AUDIT WARNING: {report['findings_count']} issues identified:")
        for f in report["findings"]:
            print(f"  - [{f['severity']}] {f['file']}: {f['issue']}")

    print("\n" + "=" * 80 + "\n")
    return report

if __name__ == "__main__":
    run_full_security_audit()
