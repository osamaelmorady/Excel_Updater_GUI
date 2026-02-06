@echo off
echo ==============================
echo Cleaning old build files...
echo ==============================

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul

echo.
echo ==============================
echo Activating virtual environment...
echo ==============================

call .venv\Scripts\activate

echo.
echo ==============================
echo Building EXE with PyInstaller...
echo ==============================

pyinstaller --onefile --noconsole --paths src --collect-all openpyxl --collect-all pandas --distpath bin src/main.py

echo.
echo ==============================
echo Build finished.
echo Output: dist\main.exe
echo ==============================

REM pause
