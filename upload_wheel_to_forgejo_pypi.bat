@echo off
REM Upload wheel to Forgejo PyPI for this project
setlocal
set PYPIRC_SRC=%~dp0.pypirc
set PYPIRC_DEST=%USERPROFILE%\.pypirc
copy /Y "%PYPIRC_SRC%" "%PYPIRC_DEST%"
call .venv\Scripts\activate.bat
python -m pip install --upgrade twine
cd /d %~dp0
REM Build wheel if not present
if not exist dist\*.whl (
	echo Building wheel...
	call "%~dp0build_wheel.bat"
	if errorlevel 1 exit /b 1
)
twine upload -r forgejo dist\*.whl
call .venv\Scripts\deactivate.bat
del "%PYPIRC_DEST%"
endlocal
pause
