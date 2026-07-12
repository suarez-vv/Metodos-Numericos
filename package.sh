#!/bin/bash
#Autor: Suárez, V.V.

#Comprobar que pyinstaller este instalado
if ! command -v pyinstaller > /dev/null; then
    echo ""
    echo "PyInstaller no está instalado."
    echo ""
    read aux
    exit 1
fi

echo ""
echo "Generando ejecutable..."
echo ""

#Crear el ejecutable
if pyinstaller --onefile --windowed --icon images/App.png --name "Metodos-Numericos" --add-data "images:images" src/menuMetodos.py; then
    mv dist/Metodos-Numericos .
    rm -rf build
    rm -rf dist
    rm -f *.spec
    echo ""
    echo "Ejecutable generado correctamente"
    echo ""
    echo "Ubicación: dist/Metodos-Numericos"
    echo ""
    read aux
else
    echo ""
    echo "Error"
    echo ""
    read aux
    exit 1
fi