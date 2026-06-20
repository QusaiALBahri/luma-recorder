@echo off
set "APPDIR=%~dp0"
echo This will remove Luma Recorder, settings, and recordings from:
echo %APPDIR%
choice /m "Continue"
if errorlevel 2 exit /b
cd /d "%TEMP%"
timeout /t 2 /nobreak >nul
rmdir /s /q "%APPDIR%"
