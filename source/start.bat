@echo off
tasklist /FI "IMAGENAME eq HC.exe" 2>NUL | find /I /N "HC.exe">NUL
if "%ERRORLEVEL%"=="0" (
    taskkill /F /IM HC.exe /T
    taskkill /F /IM AIHC.exe /T
    msg %username% "An error has occurred because an AIHC process is already running and we have ended it. Therefore, please run this program again"
    exit
)

start http://127.0.0.1:5726/