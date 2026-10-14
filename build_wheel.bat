@echo off
setlocal
set "PYTHON_EXE=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
if defined VIRTUAL_ENV set "PYTHON_EXE=%VIRTUAL_ENV%\Scripts\python.exe"
"%PYTHON_EXE%" -m build --outdir "%~dp0dist" "%~dp0."
exit /b %errorlevel%