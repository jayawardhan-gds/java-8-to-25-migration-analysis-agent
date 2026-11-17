@echo off
set TARGET=%1
if "%TARGET%"=="" set TARGET=sample-java8-app
if not exist .venv\Scripts\python.exe (echo Run scripts\setup.bat first & exit /b 2)
.venv\Scripts\python.exe -m analysis_agent.cli "%TARGET%" --output reports
if errorlevel 3 exit /b %errorlevel%
if errorlevel 1 (echo Analysis completed with significant findings - expected for sample. & exit /b 0)
