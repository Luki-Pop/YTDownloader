!define APPNAME "YTDownloader"
!define VERSION "1.0"
!define INSTALLDIR "$LOCALAPPDATA\YTDownloader"

Icon "YTDownloader.ico"
UninstallIcon "YTDownloader.ico"

OutFile "YTDownloader-Installer.exe"
InstallDir "${INSTALLDIR}"
RequestExecutionLevel user

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"

    SetOutPath "$INSTDIR"

    File "YTDownloader.exe"
    File "main.py"
    File "gui.py"
    File "updater.py"
    File "version.txt"
    File "requirements.txt"
    File "YTDownloader.ico"

    Delete "$INSTDIR\launcher.log"
    Delete "$INSTDIR\app.lock"

    DetailPrint "Installing Python dependencies..."
    nsExec::ExecToLog 'cmd /c pip install -r "$INSTDIR\requirements.txt"'

    File "YTDownloader.ico"
    CreateShortcut "$DESKTOP\YTDownloader.lnk" "$INSTDIR\YTDownloader.exe" "" "$INSTDIR\YTDownloader.ico"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"

SectionEnd

Section "Uninstall"

    Delete "$DESKTOP\YTDownloader.lnk"

    Delete "$INSTDIR\YTDownloader.exe"
    Delete "$INSTDIR\main.py"
    Delete "$INSTDIR\gui.py"
    Delete "$INSTDIR\updater.py"
    Delete "$INSTDIR\version.txt"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\launcher.log"
    Delete "$INSTDIR\app.lock"
    Delete "$INSTDIR\uninstall.exe"

    RMDir "$INSTDIR"

    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

SectionEnd
