@echo off
rem run_create_repo.bat - Run create_github_repo.py from the repository root.
rem Usage: run_create_repo.bat [remote-url]

setlocal enableextensions enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"

rem Helper: run command and capture errorlevel
set "PY_CMD="

rem If a virtual environment is active, prefer its python
if defined VIRTUAL_ENV (
  if exist "%VIRTUAL_ENV%\Scripts\python.exe" set "PY_CMD=%VIRTUAL_ENV%\Scripts\python.exe"
)

rem Try system python on PATH if we don't have one yet
if not defined PY_CMD (
  where python >nul 2>&1
  if %errorlevel%==0 set "PY_CMD=python"
)

rem Try the py launcher as a last resort
if not defined PY_CMD (
  where py >nul 2>&1
  if %errorlevel%==0 set "PY_CMD=py"
)

if not defined PY_CMD (
  echo ERROR: Could not find Python on PATH. Install Python or activate a virtualenv.
  pause
  endlocal
  exit /b 1
)

echo Running with: %PY_CMD%
echo Script: "%SCRIPT_DIR%create_github_repo.py"

"%PY_CMD%" "%SCRIPT_DIR%create_github_repo.py" %*
set "RC=%ERRORLEVEL%"

if %RC% NEQ 0 (
  echo.
  echo The script exited with code %RC%.
  echo Check the output above for the error details.
  echo.
  pause
)

endlocal
exit /b %RC%
