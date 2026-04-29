@echo off
echo Compilando PTJ.exe...

REM Verificar si PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Error al instalar PyInstaller. Por favor, instálelo manualmente con: pip install pyinstaller
        pause
        exit /b 1
    )
)

echo Compilando ejecutable...
pyinstaller ptj.spec

if %errorlevel% neq 0 (
    echo Error al compilar el ejecutable.
    pause
    exit /b 1
)

echo.
echo Compilación completada con éxito!
echo El ejecutable se encuentra en la carpeta "dist"
echo.

pause