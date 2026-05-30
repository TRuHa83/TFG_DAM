#!/bin/bash
clear

echo "[*] Verificando cambios en archivos de recursos y UI..."

# Aseguramos que el directorio de destino existe
mkdir -p interface

if [ ! -f interface/window.py ] || [ forms/window.ui -nt interface/window.py ]; then
    echo "[+] Cambios en forms/window.ui, compilando..."
    pyside6-uic forms/window.ui -o interface/window.py

    # Ajuste automático del import para que funcione como paquete
    sed -i 's/^import assets_rc.*/from . import assets_rc/' interface/window.py
fi

if [ ! -f interface/assets_rc.py ] || [ ../resources/assets.qrc -nt interface/assets_rc.py ]; then
    echo "[+] Cambios en assets.qrc, compilando..."
    pyside6-rcc ../resources/assets.qrc -o interface/assets_rc.py
fi

if [ ! -f widgets/assets_rc.py ] || [ ../resources/assets_wdgt.qrc -nt widgets/assets_rc.py ]; then
    echo "[+] Cambios en assets_wdgt.qrc, compilando..."
    pyside6-rcc ../resources/assets_wdgt.qrc -o widgets/assets_rc.py
fi
