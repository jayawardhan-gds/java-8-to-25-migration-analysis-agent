#!/usr/bin/env bash
set -u

TARGET="${1:-sample-java8-app}"

if [ ! -x .venv/bin/python ]; then
    echo "Run ./scripts/setup.sh first"
    exit 2
fi

.venv/bin/python -m analysis_agent.cli "$TARGET" --output reports
code=$?

if [ "$code" -eq 1 ]; then
    echo "Analysis completed with significant findings (expected for sample)."
    exit 0
fi

exit "$code"