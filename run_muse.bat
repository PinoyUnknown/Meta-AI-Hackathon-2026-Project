@echo off
REM Launcher for Meta Muse CLI bypassing Windows Sandbox user credential error
echo ================================================================================
echo   META MUSE CODE 1.4 - RUNNING WITH LOCAL EXECUTION (SANDBOX BYPASS)
echo ================================================================================
echo.

set MUSE_EXE=%LOCALAPPDATA%\Programs\muse\muse.CMD
if not exist "%MUSE_EXE%" (
    set MUSE_EXE=muse
)

"%MUSE_EXE%" --disable-sandbox %*
