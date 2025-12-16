@echo off
echo Starting Phishing Email Detector...
echo.

echo Starting Flask backend...
start cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Vue frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo Application started successfully!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Close the terminal windows to stop the servers.
