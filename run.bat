@echo off

python "%~dp0updater.py"

REM uruchamiamy aplikację
python "%~dp0gui.py"

REM po zamknięciu GUI stosujemy aktualizację
python - <<EOF
import updater
updater.apply_pending_update()
EOF
