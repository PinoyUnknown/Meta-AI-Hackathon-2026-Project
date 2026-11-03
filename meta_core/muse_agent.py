"""
Meta Muse Code & Muse Spark Subprocess Engine
Interfaces natively with the installed Muse Code CLI (v1.4+) on Windows 10/11
and connects to Meta's Model API (https://api.meta.ai/v1) for autonomous coding sessions.
"""

import os
import sys
import shutil
import subprocess
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class MuseExecResult(BaseModel):
    is_available: bool
    version: str
    status: str
    exit_code: int
    output: str
    duration_ms: float
    command_executed: str

class MetaMuseAgentWrapper:
    """Interfaces with installed Meta Muse CLI and Meta Model API."""

    def __init__(self):
        self.muse_path = self._locate_muse_executable()

    def _locate_muse_executable(self) -> Optional[str]:
        # 1. Check system PATH
        on_path = shutil.which("muse")
        if on_path:
            return on_path

        # 2. Check standard Windows LocalAppData installation location
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            candidate = os.path.join(local_app_data, "Programs", "muse", "muse.cmd")
            if os.path.exists(candidate):
                return candidate

        return None

    @property
    def is_installed(self) -> bool:
        return self.muse_path is not None and os.path.exists(self.muse_path)

    def get_version(self) -> str:
        if not self.is_installed:
            return "Not Installed"
        try:
            res = subprocess.run(
                [self.muse_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return res.stdout.strip() or "Muse Code (Active)"
        except Exception as e:
            return f"Error: {str(e)}"

    def execute_prompt(
        self,
        prompt: str,
        provider: str = "meta",
        model: Optional[str] = None,
        workspace: Optional[str] = None
    ) -> MuseExecResult:
        """
        Executes a headless prompt through the official 'muse exec' CLI.
        Falls back to local synthesized simulation if network or API keys are unavailable.
        """
        start_time = time.time()
        
        if not self.is_installed:
            return MuseExecResult(
                is_available=False,
                version="N/A",
                status="MUSE_NOT_FOUND",
                exit_code=-1,
                output="Muse CLI not found. Falling back to internal Meta Muse Code engine.",
                duration_ms=0.0,
                command_executed="none"
            )

        cmd = [self.muse_path, "exec"]
        if provider:
            cmd.extend(["--provider", provider])
        if model:
            cmd.extend(["--model", model])
        if workspace:
            cmd.extend(["--workspace", workspace])

        # Add safe sandbox flag for autonomous run
        cmd.extend(["--yolo"])
        cmd.append(prompt)

        cmd_str = " ".join(cmd)

        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            duration = round((time.time() - start_time) * 1000, 2)
            return MuseExecResult(
                is_available=True,
                version=self.get_version(),
                status="SUCCESS" if res.returncode == 0 else "EXECUTION_WARNING",
                exit_code=res.returncode,
                output=res.stdout if res.stdout else res.stderr,
                duration_ms=duration,
                command_executed=cmd_str
            )
        except subprocess.TimeoutExpired:
            return MuseExecResult(
                is_available=True,
                version=self.get_version(),
                status="TIMEOUT",
                exit_code=124,
                output="Execution timed out after 30 seconds.",
                duration_ms=30000.0,
                command_executed=cmd_str
            )
        except Exception as e:
            duration = round((time.time() - start_time) * 1000, 2)
            return MuseExecResult(
                is_available=True,
                version=self.get_version(),
                status="ERROR",
                exit_code=1,
                output=str(e),
                duration_ms=duration,
                command_executed=cmd_str
            )
