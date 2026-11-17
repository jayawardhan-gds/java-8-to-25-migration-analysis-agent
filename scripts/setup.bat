@echo off
py -3.11 -m venv .venv || exit /b 2
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
echo Setup complete. Activate with: .venv\Scripts\activate
