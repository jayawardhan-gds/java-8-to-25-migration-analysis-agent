from __future__ import annotations

import subprocess
from pathlib import Path

from analysis_agent.models import Finding, ToolRun


def _run(name: str, command: list[str], cwd: Path) -> tuple[list[Finding], ToolRun]:
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return [], ToolRun(name, "skipped", f"Unavailable or timed out: {exc}")
    output = (proc.stdout + "\n" + proc.stderr).strip()
    if proc.returncode not in (0, 1):
        return [], ToolRun(name, "failed", f"exit code {proc.returncode}: {output[-500:]}")
    if not output:
        return [], ToolRun(name, "passed", "No findings reported")
    finding = Finding(f"JDK-{name.upper().replace(' ', '-')}", "High", "JDK API usage", f"{name} reported migration concerns", "The JDK tool produced output requiring review.", "Review the captured evidence, update the affected code, and rerun the analysis.", evidence=output[-3000:])
    return [finding], ToolRun(name, "findings", "Tool produced reviewable output")

def run_jdk_tools(target: Path) -> tuple[list[Finding], list[ToolRun]]:
    classes = target / "target" / "classes"
    if not classes.exists():
        return [], [ToolRun("jdeps", "skipped", "target/classes not available"), ToolRun("jdeprscan", "skipped", "target/classes not available")]
    all_findings, runs = [], []
    for name, command in [("jdeps", ["jdeps", "--jdk-internals", "-R", str(classes)]), ("jdeprscan", ["jdeprscan", "--release", "25", str(classes)])]:
        findings, run = _run(name, command, target)
        all_findings.extend(findings); runs.append(run)
    return all_findings, runs
