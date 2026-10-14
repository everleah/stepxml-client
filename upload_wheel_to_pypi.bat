@echo off
setlocal
set "PYTHON_EXE=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
if defined VIRTUAL_ENV set "PYTHON_EXE=%VIRTUAL_ENV%\Scripts\python.exe"
if "%~1"=="" (
    "%PYTHON_EXE%" "%~dp0publish_pypi.py" --publish
) else (
    "%PYTHON_EXE%" "%~dp0publish_pypi.py" %*
)
exit /b %errorlevel%
