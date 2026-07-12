@echo off

REM Autor: Suárez, V.V.

REM Comprobar que Python este instalado
python --version > nul 2>&1

if errorlevel 1 (
    echo .
    echo Python no esta instalado
    echo .
    pause
    exit /b 1
)

REM Crear el entorno virtual
if not exist ".venv"(
    echo .
    echo Creando entorno virtual...
    echo .

    python -m venv .venv

    if errorlevel 1 (
        echo .
        echo Error al crear el entorno virtual.
        echo .
        pause
        exit /b 1
    )

    echo .
    echo Entorno virtual creado correctamente.
    echo .
)

REM Cambiar al entorno virtual de .venv
call .venv\Scripts\activate

REM Actualización de pip
python -m pip install --upgrade pip

REM Instalación de dependencias

pip install -r requirements.txt

if errorlevel 1 (
    echo .
    echo Error al instalar las dependencias.
    echo .
    pause
    exit /b 1
)

echo .
echo Dependencias instaladas correctamente.
echo .