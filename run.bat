@echo off
cd /d %~dp0

REM Optional: activate virtual environment if you use one
REM call venv\Scripts\activate.bat

REM Run Python script
py -u src\main.py

