@echo off

REM Autor: Suárez, V.V.

REM Comprobar que pyinstaller este instalado
pyinstaller --version > nul 2>&1

if errorlevel 1 (
    echo.
    echo PyInstaller no esta instalado.
    echo.
    pause
    exit /b 1
)

echo.
echo Generando ejecutable...
echo.

REM Creando el ejecutable
pyinstaller --onefile --windowed --icon images\App.ico --name "Metodos-Numericos" --add-data "images;images" src\menuMetodos.py

if errorlevel 1 (
    echo.
    echo Error al general el ejecutable.
    echo.
    pause
    exit /b 1
)

move dist\Metodos-Numericos.exe .
 rmdir /s /q build
 rmdir /s /q dist
 del *.spec

echo.
echo Ejecutable generado correctamente.
echo.
echo Ubicacion: dist\Metodos-Numericos.exe
echo.
pause