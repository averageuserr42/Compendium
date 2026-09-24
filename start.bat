@echo off
rem Startet das Compendium-Backend: Datenbank neu erzeugen, dann Flask-Server.
rem Doppelklick genuegt. Das Fenster bleibt offen, solange der Server laeuft.

cd /d "%~dp0"

echo [1/2] Datenbank wird erzeugt (seed.py) ...
python seed.py
if errorlevel 1 (
    echo FEHLER: seed.py ist fehlgeschlagen. Ist Python installiert?
    pause
    exit /b 1
)

echo [2/2] Server startet: http://127.0.0.1:5000
echo Zum Stoppen: Strg+C oder Fenster schliessen.
python app.py

pause
