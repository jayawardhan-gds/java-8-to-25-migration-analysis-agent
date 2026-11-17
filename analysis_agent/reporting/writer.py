from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from analysis_agent.models import AnalysisResult


def _context(result: AnalysisResult) -> dict[str, object]:
    return {"target": str(result.target), "generated_at": datetime.now(UTC).isoformat(), "summary": result.summary, "risk_score": result.risk_score, "metadata": result.metadata, "tools": result.tools, "findings": result.findings}

def write_reports(result: AnalysisResult, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    data = _context(result)
    serial = dict(data)
    serial["tools"] = [vars(x) for x in result.tools]
    serial["findings"] = [x.to_dict() for x in result.findings]
    (output / "report.json").write_text(json.dumps(serial, indent=2), encoding="utf-8")
    env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"), autoescape=select_autoescape(["html"]))
    (output / "report.html").write_text(env.get_template("report.html.j2").render(**data), encoding="utf-8")
    (output / "report.md").write_text(env.get_template("report.md.j2").render(**data), encoding="utf-8")
