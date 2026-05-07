@echo off
title Building YTDownloader

echo Cleaning old build...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q YTDownloader.exe 2>nul

echo Building launcher.exe...
python -m PyInstaller --noconsole --onefile launcher.py

copy /Y dist\launcher.exe YTDownloader.exe >nul

echo Building installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

echo DONE!
pause
