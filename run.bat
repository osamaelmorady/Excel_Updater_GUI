@echo off
cd /d %~dp0

REM Optional: activate virtual environment if you use one
REM call venv\Scripts\activate.bat

REM Run Python script
REM python -u src\main.py
.venv\Scripts\python.exe src\main.py
