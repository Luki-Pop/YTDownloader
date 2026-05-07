@echo off
title Building YTDownloader

echo Reading current version...
set /p VERSION=<version.txt

for /f "tokens=1,2,3 delims=." %%a in ("%VERSION%") do (
    set /a PATCH=%%c+1
    set NEW_VERSION=%%a.%%b.!PATCH!
)

for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd"') do set DATE=%%i
echo %NEW_VERSION% (%DATE%)>version.txt

echo Cleaning old build...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q YTDownloader.exe 2>nul

echo Building launcher.exe...
python -m PyInstaller --noconsole --onefile --icon=YTDownloader.ico launcher.py

copy /Y dist\launcher.exe YTDownloader.exe >nul

echo Building installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

echo DONE! Version %NEW_VERSION%
pause
