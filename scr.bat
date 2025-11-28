@echo off
REM ======= BACKEND SETUP =======
echo Starting backend server...

start cmd /k "cd /d C:\Users\ASUS\Desktop\parking proj v2\backend && call ..\.env\Scripts\activate && flask run"

REM ======= FRONTEND SETUP =======
echo Starting frontend server...

start cmd /k "cd /d C:\Users\ASUS\Desktop\parking proj v2\frontend && npm run dev"

echo Both servers started successfully!
pause
