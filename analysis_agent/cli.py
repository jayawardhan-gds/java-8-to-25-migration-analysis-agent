from pathlib import Path

import typer

from analysis_agent.orchestrator import analyze
from analysis_agent.reporting.writer import write_reports

app = typer.Typer(help="Java 8 to Java 25 Migration AnalysisAgent")

@app.command()
def analyze_command(target: Path = typer.Argument(..., exists=True, file_okay=False, readable=True), output: Path = typer.Option(Path("reports"), "--output", "-o"), rules: Path = typer.Option(Path("config/rules.yml"), "--rules")) -> None:
    """Analyze a local Maven Java project and generate HTML, JSON and Markdown reports."""
    if not rules.exists():
        typer.echo(f"Rules file not found: {rules}", err=True)
        raise typer.Exit(2)
    try:
        result = analyze(target, rules)
        write_reports(result, output)
    except Exception as exc:
        typer.echo(f"Analysis failed: {exc}", err=True)
        raise typer.Exit(3) from exc
    typer.echo(f"Analysis complete: {len(result.findings)} finding(s), risk {result.risk_score}/100")
    typer.echo(f"Reports: {output.resolve()}")
    if result.summary["Critical"] or result.summary["High"]:
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
