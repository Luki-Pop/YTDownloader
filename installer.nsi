!define APPNAME "YTDownloader"
!define VERSION "1.0"
!define INSTALLDIR "$LOCALAPPDATA\YTDownloader"

OutFile "YTDownloader-Installer.exe"
InstallDir "${INSTALLDIR}"
RequestExecutionLevel user

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"

    SetOutPath "$INSTDIR"

    ; --- Pliki aplikacji ---
    File "YTDownloader.exe"     ; launcher.exe skompilowany PyInstallerem
    File "main.py"
    File "gui.py"
    File "updater.py"
    File "version.txt"
    File "requirements.txt"

    ; --- Instalacja zależności Pythona ---
    DetailPrint "Installing Python dependencies..."
    nsExec::ExecToLog 'cmd /c pip install -r "$INSTDIR\requirements.txt"'

    ; --- Skrót na pulpicie ---
    CreateShortcut "$DESKTOP\YTDownloader.lnk" "$INSTDIR\YTDownloader.exe"

    ; --- Uninstaller ---
    WriteUninstaller "$INSTDIR\uninstall.exe"

    ; --- Rejestr (dla Panelu Sterowania) ---
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"

SectionEnd


Section "Uninstall"

    ; --- Usuwanie skrótu ---
    Delete "$DESKTOP\YTDownloader.lnk"

    ; --- Usuwanie plików ---
    Delete "$INSTDIR\YTDownloader.exe"
    Delete "$INSTDIR\main.py"
    Delete "$INSTDIR\gui.py"
    Delete "$INSTDIR\updater.py"
    Delete "$INSTDIR\version.txt"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\launcher.log"
    Delete "$INSTDIR\app.lock"
    Delete "$INSTDIR\uninstall.exe"

    ; --- Usuwanie folderu ---
    RMDir "$INSTDIR"

    ; --- Usuwanie wpisu z rejestru ---
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

SectionEnd
