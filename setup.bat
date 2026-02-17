@echo off
echo ==========================================
echo      SkyGuard AI Environment Setup
echo ==========================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

echo [INFO] Creating virtual environment...
python -m venv venv

echo [INFO] Activating virtual environment...
call venv\Scripts\activate

echo [INFO] Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo        Setup Complete!
echo ==========================================
echo.
echo To run the dashboard:
echo    streamlit run dashboard.py
echo.
echo To run the main mission loop:
echo    python main.py
echo.
pause
