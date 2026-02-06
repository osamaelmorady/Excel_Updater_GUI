@echo off
setlocal enabledelayedexpansion

:: ==========================================
:: CONFIGURATION
:: ==========================================
set "REQUIRED_VERSION=3.12"
set "VENV_DIR=.venv"
:: ==========================================

echo [1/4] Checking Python version...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    pause
    exit /b
)

:: Extract version and validate
for /f "tokens=2" %%a in ('python --version') do set "INSTALLED_VERSION=%%a"
echo %INSTALLED_VERSION% | findstr /b /c:"%REQUIRED_VERSION%" >nul

if %errorlevel% neq 0 (
    echo [ERROR] Python %REQUIRED_VERSION% is required. 
    echo Found: %INSTALLED_VERSION%
    echo Please install the correct version and try again.
    pause
    exit /b
)
echo [SUCCESS] Python %INSTALLED_VERSION% detected.

:: ==========================================
echo [2/4] Setting up Virtual Environment...
:: ==========================================

if not exist %VENV_DIR% (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv. 
        echo If using MSYS2, run: pacman -S mingw-w64-ucrt-x86_64-python-venv
        pause
        exit /b
    )
) else (
    echo Virtual environment already exists.
)

:: Find the correct executable path (MSYS2 uses /bin/, Windows uses /Scripts/)
if exist "%VENV_DIR%\Scripts\python.exe" (
    set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
) else if exist "%VENV_DIR%\bin\python.exe" (
    set "VENV_PYTHON=%VENV_DIR%\bin\python.exe"
) else (
    echo [ERROR] Could not find python.exe inside the virtual environment.
    pause
    exit /b
)

:: ==========================================
echo [3/4] Installing requirements...
:: ==========================================

:: Using the absolute path to the venv python ensures it DOES NOT 
:: install to your system/MSYS2 folders.
echo Upgrading pip...
"%VENV_PYTHON%" -m pip install --upgrade pip

if exist requirements.txt (
    echo Installing from requirements.txt...
    "%VENV_PYTHON%" -m pip install -r requirements.txt
) else (
    echo [SKIP] No requirements.txt found.
)

:: ==========================================
echo [4/4] Finalizing...
:: ==========================================

echo.
echo ======================================================
echo SETUP COMPLETE
echo ======================================================
echo To run your project, use:
echo %VENV_PYTHON% main.py
echo ======================================================
pause