@echo off
REM Push current branch to upstream remote
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%b

echo Pushing branch %BRANCH% to upstream...
git push upstream %BRANCH%
if %ERRORLEVEL%==0 (
    echo Push to upstream successful.
) else (
    echo Push to upstream failed.
)
pause
