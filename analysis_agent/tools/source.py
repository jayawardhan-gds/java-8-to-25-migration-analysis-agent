from __future__ import annotations

import re
from pathlib import Path

import yaml

from analysis_agent.models import Finding


def scan_sources(target: Path, config: Path) -> list[Finding]:
    definitions = yaml.safe_load(config.read_text(encoding="utf-8"))["rules"]
    findings: list[Finding] = []
    for source in target.rglob("*.java"):
        rel = str(source.relative_to(target))
        for line_no, line in enumerate(source.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for rule in definitions:
                if re.search(rule["pattern"], line):
                    findings.append(Finding(rule["id"], rule["severity"], rule["category"], rule["title"], rule["explanation"], rule["recommendation"], rel, line_no, line.strip(), True))
    return findings
