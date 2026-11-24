@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip pyinstaller
python -m PyInstaller --clean --noconfirm proyecto_ciberseguridad.spec

if errorlevel 1 (
    echo.
    echo No se pudo crear el ejecutable.
    exit /b 1
)

echo.
echo Ejecutable creado en dist\ProyectoCiberseguridad.exe
endlocal
