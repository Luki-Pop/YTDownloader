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

    ; Kopiujemy pliki aplikacji
    File "main.py"
    File "gui.py"
    File "run.bat"
    File "requirements.txt"

    ; Instalujemy zależności Pythona
    DetailPrint "Installing Python dependencies..."
    nsExec::ExecToLog 'cmd /c pip install -r "$INSTDIR\requirements.txt"'

    ; Tworzymy skrót na pulpicie
    CreateShortcut "$DESKTOP\YTDownloader.lnk" "$INSTDIR\run.bat"

    ; Tworzymy uninstall
    WriteUninstaller "$INSTDIR\uninstall.exe"

    ; Dodajemy wpis do rejestru
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"

SectionEnd


Section "Uninstall"

    Delete "$DESKTOP\YTDownloader.lnk"
    Delete "$INSTDIR\main.py"
    Delete "$INSTDIR\gui.py"
    Delete "$INSTDIR\run.bat"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\uninstall.exe"

    RMDir "$INSTDIR"

    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

SectionEnd
