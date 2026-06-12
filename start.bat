@echo off
title Symphony Door Game
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
echo Dependencies installed. Starting server...
start /b python app.py
:: Wait for the server to start
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000
echo Server is running! Press any key to exit.
pause >nul
:: Terminate the background server process
taskkill /f /im python.exe /fi "WINDOWTITLE eq Symphony Door Game" >nul 2>&1