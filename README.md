# Java 8 to Java 25 Migration AnalysisAgent

A deterministic-first, local analysis agent for assessing a Maven-based Java 8 project before migration to Java 25. It does not rewrite application code and does not upload source code.

## Prerequisites

- Python 3.11+
- JDK 25 recommended (`java`, `jdeps`, and `jdeprscan` on PATH)
- Maven 3.9+ or a Maven Wrapper in the target repository
- Git

The agent still produces source and Maven findings when JDK or Maven tools are unavailable.

## Setup

### Linux/macOS or GitHub Codespaces

```bash
./scripts/setup.sh
source .venv/bin/activate
```

### Windows PowerShell/cmd

```bat
scripts\setup.bat
.venv\Scripts\activate
```

## Execute

```bash
./scripts/run.sh sample-java8-app
```

Windows:

```bat
scripts\run.bat sample-java8-app
```

Or invoke the CLI directly:

```bash
java-migration-agent analyze sample-java8-app --output reports
```

Open `reports/report.html`; also review `reports/report.md` and `reports/report.json`.

## Run quality checks

```bash
pytest
ruff check .
mypy analysis_agent
```

## Push to GitHub

Create an empty GitHub repository, then run:

```bash
git init
git add .
git commit -m "Initial Java migration analysis agent MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USER/java-8-to-25-migration-analysis-agent.git
git push -u origin main
```

Do not add generated reports, virtual environments, credentials, or proprietary source code.

## Exit codes

- `0`: analysis completed with no High/Critical finding
- `1`: analysis completed and High/Critical findings exist
- `2`: invalid configuration or target
- `3`: unexpected execution failure
