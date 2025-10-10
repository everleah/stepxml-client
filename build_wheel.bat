@echo off
REM Use venv Python if VIRTUAL_ENV is set, else fallback to system Python
if defined VIRTUAL_ENV (
	set PYTHON_EXE=%VIRTUAL_ENV%\Scripts\python.exe
) else (
	set PYTHON_EXE=python
)
call "%PYTHON_EXE%" setup.py bdist_wheel
pause