@echo off
REM Bhutan Rainfall Explorer - Setup Script for Windows
REM This script sets up the project environment and dependencies

echo 🌄 Setting up Bhutan Rainfall Explorer...
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=2" %%i in ('python --version') do echo 🐍 Python version detected: %%i

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully!
) else (
    echo ❌ Failed to install dependencies. Please check your Python environment.
    pause
    exit /b 1
)

REM Check if Streamlit is properly installed
streamlit --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🚀 Streamlit is ready!
) else (
    echo ⚠️  Streamlit installation might have issues.
)

echo.
echo 🎉 Setup complete!
echo.
echo To run the application:
echo   streamlit run app.py
echo.
echo To start Jupyter notebook:
echo   jupyter notebook notebooks/
echo.
echo Happy exploring! 🐉
pause
