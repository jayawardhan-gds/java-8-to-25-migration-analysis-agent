from pathlib import Path

from analysis_agent.orchestrator import analyze


def test_sample_has_expected_findings():
    root = Path(__file__).parents[1]
    result = analyze(root / "sample-java8-app", root / "config/rules.yml")
    ids = {f.rule_id for f in result.findings}
    assert "BUILD-001" in ids
    assert "SRC-003" in ids
    assert "SRC-004" in ids
