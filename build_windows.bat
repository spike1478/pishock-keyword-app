@echo off
REM Build script for Windows version of PiShock Universal App

echo Building PiShock Universal App for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create build directory
if not exist "build\windows" mkdir "build\windows"
cd build\windows

REM Copy source files
copy ..\..\pishock_app.py .
copy ..\..\requirements.txt .
copy ..\..\pishock_app.spec .

REM Build the executable
echo Building Windows executable...
pyinstaller pishock_app.spec

REM Check if build was successful
if exist "dist\pishock_app.exe" (
    echo.
    echo ✅ Build successful!
    echo Executable created: build\windows\dist\pishock_app.exe
    echo.
    echo To run the app:
    echo build\windows\dist\pishock_app.exe
    echo.
) else (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

pause
