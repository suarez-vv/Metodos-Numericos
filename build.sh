#!/bin/bash
#Autor: Suárez, V.V.

#Verificar que Python este instalado
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "Python3 no está instalado."
    echo ""
    read aux
    exit 1
fi

#Crear el entorno virtual
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creando entorno virtual"
    echo ""

    if python3 -m venv .venv; then
        echo ""
        echo "Entorno virtual creado correctamente"
        echo ""
    else
        echo ""
        echo "Error al crear el entorno virtual"
        echo ""
        read aux
        exit 1
    fi
fi

#Cambiar al entorno virtual de .venv
source .venv/bin/activate
#Actualiar pip
python -m pip install --upgrade pip

#Instalar las dependencias
if pip install -r requirements.txt; then
    echo ""
    echo "Dependencias instaladas correctamente"
    echo ""
else
    echo ""
    echo "Error al instalar las dependencias"
    echo ""
    read aux
    exit 1
fi