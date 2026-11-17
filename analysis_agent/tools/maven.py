from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

from analysis_agent.models import Finding, ToolRun

NS = {"m": "http://maven.apache.org/POM/4.0.0"}

def _text(root: ET.Element, path: str) -> str | None:
    node = root.find(path, NS)
    return node.text.strip() if node is not None and node.text else None

def analyze_pom(target: Path, pom: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(pom.relative_to(target))
    try:
        root = ET.parse(pom).getroot()
    except ET.ParseError as exc:
        return [Finding("BUILD-000", "Critical", "Build baseline", "Invalid pom.xml", str(exc), "Correct the Maven POM before migration.", rel, evidence=str(exc))]
    candidates = [
        _text(root, "m:properties/m:maven.compiler.release"),
        _text(root, "m:properties/m:maven.compiler.source"),
        _text(root, "m:build/m:plugins/m:plugin[m:artifactId='maven-compiler-plugin']/m:configuration/m:release"),
        _text(root, "m:build/m:plugins/m:plugin[m:artifactId='maven-compiler-plugin']/m:configuration/m:source"),
    ]
    level = next((x for x in candidates if x), None)
    if level in {"1.8", "8"}:
        findings.append(Finding("BUILD-001", "High", "Build baseline", "Project compiles for Java 8", f"Maven declares Java level {level}.", "Move through supported intermediate JDKs, update plugins/dependencies, then set release 25 after tests pass.", rel, evidence=f"compiler level={level}"))
    elif not level:
        findings.append(Finding("BUILD-002", "Medium", "Build baseline", "Java level is not explicit", "No compiler source/release value was found.", "Declare maven.compiler.release explicitly and verify the effective POM.", rel, evidence="No compiler level in pom.xml"))
    for dep in root.findall(".//m:dependency", NS):
        artifact = _text(dep, "m:artifactId") or "unknown"
        version = _text(dep, "m:version")
        if version and version.endswith("-SNAPSHOT"):
            findings.append(Finding("DEP-001", "Medium", "Dependencies", "Snapshot dependency", f"{artifact} uses non-repeatable version {version}.", "Replace it with a verified release before migration.", rel, evidence=f"{artifact}:{version}"))
    return findings

def run_maven(target: Path) -> tuple[list[Finding], ToolRun]:
    wrapper = target / ("mvnw.cmd" if __import__('os').name == 'nt' else "mvnw")
    if wrapper.exists():
        cmd = [str(wrapper)]
    else:
        maven_executable = shutil.which("mvn.cmd" if os.name == "nt" else "mvn")
        if not maven_executable:
                return [], ToolRun(
                "Maven tests",
                "skipped",
                "Maven executable was not found on PATH.",
                )
        cmd = [maven_executable]
    try:
        proc = subprocess.run(
            cmd + ["-q", "test"],
            cwd=target,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return [], ToolRun("Maven tests", "skipped", f"Maven unavailable or timed out: {exc}")
    if proc.returncode == 0:
        return [], ToolRun("Maven tests", "passed", "mvn test completed successfully")
    tail = (proc.stderr or proc.stdout)[-1500:]
    finding = Finding("BUILD-003", "Critical", "Testing readiness", "Maven build or tests failed", "The baseline project did not pass `mvn test`.", "Resolve baseline compilation/test failures before changing the target JDK.", "pom.xml", evidence=tail)
    return [finding], ToolRun("Maven tests", "failed", f"exit code {proc.returncode}")
