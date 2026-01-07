@echo off
setlocal enabledelayedexpansion

:: Change to script directory
cd /d "%~dp0"

echo ========================================
echo   YouTube Music Migration Tool
echo ========================================
echo.

:: Define paths
set "PYTHON_DIR=%~dp0runtime_templates\windows\python"
set "PYTHON_EXE=%PYTHON_DIR%\python.exe"
set "SITE_PACKAGES=%~dp0runtime_templates\windows\site-packages"
set "MIGRATE_SCRIPT=%~dp0migrate.py"

:: Verify Windows runtime exists
if not exist "%PYTHON_DIR%" (
    echo [ERROR] Windows runtime directory not found!
    echo Expected location: %PYTHON_DIR%
    echo.
    echo Please ensure the runtime_templates\windows\python folder exists.
    pause
    exit /b 1
)

:: Verify Python executable exists
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python executable not found!
    echo Expected location: %PYTHON_EXE%
    echo.
    echo Please ensure python.exe is in runtime_templates\windows\python\
    pause
    exit /b 1
)

:: Verify site-packages exists
if not exist "%SITE_PACKAGES%" (
    echo [ERROR] Site-packages directory not found!
    echo Expected location: %SITE_PACKAGES%
    echo.
    echo Please ensure runtime_templates\windows\site-packages exists.
    pause
    exit /b 1
)

:: Verify ytmusicapi package exists
if not exist "%SITE_PACKAGES%\ytmusicapi" (
    echo [ERROR] ytmusicapi package not found!
    echo Expected location: %SITE_PACKAGES%\ytmusicapi
    echo.
    echo Please ensure ytmusicapi is installed in site-packages.
    pause
    exit /b 1
)

:: Verify migrate.py exists
if not exist "%MIGRATE_SCRIPT%" (
    echo [ERROR] migrate.py not found!
    echo Expected location: %MIGRATE_SCRIPT%
    echo.
    pause
    exit /b 1
)

:: Verify spotify_data.json exists
if not exist "%~dp0spotify_data.json" (
    echo [ERROR] spotify_data.json not found!
    echo Expected location: %~dp0spotify_data.json
    echo.
    echo Please ensure your Spotify data file is in the same directory.
    pause
    exit /b 1
)

echo [OK] Environment verification passed
echo.
echo Python: %PYTHON_EXE%
echo Site-packages: %SITE_PACKAGES%
echo Script: %MIGRATE_SCRIPT%
echo.
echo Starting migration...
echo ========================================
echo.

:: Run the migration script
"%PYTHON_EXE%" "%MIGRATE_SCRIPT%"

:: Capture exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ========================================
if %EXIT_CODE% equ 0 (
    echo Migration script completed successfully.
) else (
    echo Migration script exited with code: %EXIT_CODE%
)
echo ========================================
echo.

:: Keep window open
pause
exit /b %EXIT_CODE%
