from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SEVERITY_WEIGHT = {"Critical": 10, "High": 7, "Medium": 4, "Low": 1, "Informational": 0}

@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    category: str
    title: str
    explanation: str
    recommendation: str
    file: str | None = None
    line: int | None = None
    evidence: str | None = None
    heuristic: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class ToolRun:
    name: str
    status: str
    detail: str

@dataclass
class AnalysisResult:
    target: Path
    findings: list[Finding] = field(default_factory=list)
    tools: list[ToolRun] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def deduplicate(self) -> None:
        unique: dict[tuple[Any, ...], Finding] = {}
        for item in self.findings:
            key = (item.rule_id, item.file, item.line, item.evidence)
            unique[key] = item
        self.findings = sorted(unique.values(), key=lambda f: (-SEVERITY_WEIGHT[f.severity], f.rule_id, f.file or "", f.line or 0))

    @property
    def summary(self) -> dict[str, int]:
        values = {name: 0 for name in SEVERITY_WEIGHT}
        for finding in self.findings:
            values[finding.severity] += 1
        return values

    @property
    def risk_score(self) -> int:
        return min(100, sum(SEVERITY_WEIGHT[f.severity] for f in self.findings))
