@echo off
echo [INFO] Packaging AnkiDeckGenerator into a Windows Executable...
echo [INFO] Ensuring all dependencies are installed...
pip install -r requirements.txt

echo [INFO] Starting build process...
python -m flet pack main.py ^
    --icon assets/icon.png ^
    --name "Anki Deck Generator" ^
    --add-data "assets;assets" ^
    --add-data "data;data"

echo.
echo [SUCCESS] Build complete! 
echo [INFO] Your executable can be found in the "dist" folder.
echo [INFO] Note: You will need to bring the .env file if you wish to use Discord Webhooks in the EXE version.
pause
