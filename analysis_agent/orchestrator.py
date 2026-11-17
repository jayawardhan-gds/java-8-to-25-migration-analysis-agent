from pathlib import Path

from analysis_agent.models import AnalysisResult, ToolRun
from analysis_agent.tools.discovery import discover
from analysis_agent.tools.jdk import run_jdk_tools
from analysis_agent.tools.maven import analyze_pom, run_maven
from analysis_agent.tools.source import scan_sources


def analyze(target: Path, rules: Path) -> AnalysisResult:
    target = target.resolve()
    result = AnalysisResult(target)
    result.metadata = discover(target)
    result.tools.append(ToolRun("Discovery", "passed", f"Found {result.metadata['java_sources']} Java sources"))
    for pom_name in result.metadata["pom_files"]:
        result.findings.extend(analyze_pom(target, target / str(pom_name)))
    result.tools.append(ToolRun("POM analysis", "passed", f"Analyzed {len(result.metadata['pom_files'])} POM file(s)"))
    result.findings.extend(scan_sources(target, rules))
    result.tools.append(ToolRun("Source rules", "passed", "Configured heuristic rules completed"))
    maven_findings, maven_run = run_maven(target)
    result.findings.extend(maven_findings); result.tools.append(maven_run)
    jdk_findings, jdk_runs = run_jdk_tools(target)
    result.findings.extend(jdk_findings); result.tools.extend(jdk_runs)
    if result.metadata["java_tests"] == 0:
        from analysis_agent.models import Finding
        result.findings.append(Finding("TEST-001", "High", "Testing readiness", "No Java tests detected", "Migration safety cannot be established without an executable test baseline.", "Add characterization and regression tests before making migration changes.", evidence="0 files under src/test"))
    result.deduplicate()
    return result
