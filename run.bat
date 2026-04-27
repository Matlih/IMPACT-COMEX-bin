@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

set "MAIN_SCRIPT=main.py"
set "TEST_CAMERA_SCRIPT=tests\camera.py"
set "REQ_FILE=requirements\windows.txt"

:menu
cls
echo ===== Python Menu (Windows) =====
echo 1. Install requirements
echo 2. Run main.py
echo 3. Run main.py (headless)
echo 4. Tests menu
echo 0. Exit
echo.
set /p choice=Enter option: 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto run_main
if "%choice%"=="3" goto run_main_headless
if "%choice%"=="4" goto tests_menu
if "%choice%"=="0" goto end
echo Invalid option. Please choose 1, 2, 3, 4, or 0.
pause
goto menu

:tests_menu
cls
echo ===== Tests Menu (Windows) =====
echo 1. Run camera test
echo 0. Back
echo.
set /p test_choice=Enter option: 

if "%test_choice%"=="1" goto run_camera_test
if "%test_choice%"=="0" goto menu
echo Invalid option. Please choose 0 or 1.
pause
goto tests_menu

:install
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment in .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        goto menu
    )
)

echo Installing dependencies from %REQ_FILE% ...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r "%REQ_FILE%"
if errorlevel 1 (
    echo Dependency install failed.
) else (
    echo Dependencies installed successfully.
)
pause
goto menu

:run_main
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Run option 1 first.
    pause
    goto menu
)
".venv\Scripts\python.exe" "%MAIN_SCRIPT%"
pause
goto menu

:run_main_headless
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Run option 1 first.
    pause
    goto menu
)
".venv\Scripts\python.exe" "%MAIN_SCRIPT%" --headless
pause
goto menu

:run_camera_test
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Run option 1 first.
    pause
    goto tests_menu
)
".venv\Scripts\python.exe" "%TEST_CAMERA_SCRIPT%"
pause
goto tests_menu

:end
echo Exiting.
endlocal
exit /b 0
