#!/usr/bin/env bash
# =============================================================================
# install.sh — Instala dotmng en el entorno del usuario
#
# Qué hace:
#   1. Localiza run.sh en el directorio del proyecto
#   2. Le da permisos de ejecución
#   3. Crea (o actualiza) el symlink ~/.local/bin/dotmng → run.sh
#   4. Avisa si ~/.local/bin no está en PATH y cómo añadirlo
# =============================================================================

set -euo pipefail

# --- Colores ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- Rutas ---
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
RUN_SH="$SCRIPT_DIR/run.sh"
INSTALL_DIR="$HOME/.local/bin"
SYMLINK="$INSTALL_DIR/dotmng"

# --- Banner ---
echo ""
echo -e "${BOLD}${CYAN}  Dotfiles Manager — Instalador${RESET}"
echo -e "  ──────────────────────────────"
echo ""

# --- Verificar que run.sh existe ---
if [[ ! -f "$RUN_SH" ]]; then
    echo -e "  ${RED}✗ No se encontró run.sh en:${RESET} $RUN_SH"
    echo -e "  Asegúrate de ejecutar install.sh desde el directorio del proyecto."
    exit 1
fi

# --- Dar permisos de ejecución a run.sh ---
chmod +x "$RUN_SH"
echo -e "  ${GREEN}✔${RESET} Permisos de ejecución aplicados a run.sh"

# --- Crear ~/.local/bin si no existe ---
if [[ ! -d "$INSTALL_DIR" ]]; then
    mkdir -p "$INSTALL_DIR"
    echo -e "  ${GREEN}✔${RESET} Directorio creado: $INSTALL_DIR"
fi

# --- Crear o actualizar el symlink ---
if [[ -L "$SYMLINK" ]]; then
    # Ya existe un symlink → actualizarlo
    ln -sf "$RUN_SH" "$SYMLINK"
    echo -e "  ${GREEN}✔${RESET} Symlink actualizado: ${BOLD}$SYMLINK${RESET} → $RUN_SH"
elif [[ -e "$SYMLINK" ]]; then
    # Existe un archivo real con ese nombre (no symlink)
    echo -e "  ${YELLOW}⚠${RESET} Ya existe un archivo en $SYMLINK (no es un symlink)."
    echo -e "    Elimínalo manualmente si quieres que dotmng lo reemplace."
    exit 1
else
    # No existe → crearlo
    ln -s "$RUN_SH" "$SYMLINK"
    echo -e "  ${GREEN}✔${RESET} Symlink creado: ${BOLD}$SYMLINK${RESET} → $RUN_SH"
fi

# --- Comprobar si ~/.local/bin está en PATH ---
echo ""
if echo "$PATH" | tr ':' '\n' | grep -qx "$INSTALL_DIR"; then
    echo -e "  ${GREEN}✔${RESET} ${BOLD}$INSTALL_DIR${RESET} ya está en tu PATH."
    echo ""
    echo -e "  ${BOLD}Instalación completada.${RESET} Puedes usar:"
    echo -e "  ${CYAN}  dotmng help${RESET}"
else
    echo -e "  ${YELLOW}⚠${RESET} ${BOLD}$INSTALL_DIR${RESET} no está en tu PATH."
    echo ""
    echo -e "  Añádelo agregando esta línea a tu ${BOLD}~/.bashrc${RESET} o ${BOLD}~/.zshrc${RESET}:"
    echo -e "  ${CYAN}  export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
    echo ""
    echo -e "  Luego recarga tu shell:"
    echo -e "  ${CYAN}  source ~/.bashrc${RESET}  ${RESET}# o source ~/.zshrc"
    echo ""
    echo -e "  O usa la ruta completa hasta entonces:"
    echo -e "  ${CYAN}  $SYMLINK help${RESET}"
fi

# --- Generar entrada .desktop si hay icono disponible ---
ICON_SRC="$SCRIPT_DIR/src/dotmng/resources/icons/dotmng.png"
ICONS_DIR="$HOME/.local/share/icons"
APPS_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$APPS_DIR/dotmng.desktop"

echo ""
if [[ -f "$ICON_SRC" ]]; then
    mkdir -p "$ICONS_DIR" "$APPS_DIR"

    cp "$ICON_SRC" "$ICONS_DIR/dotmng.png"
    echo -e "  ${GREEN}✔${RESET} Icono instalado en: $ICONS_DIR/dotmng.png"

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Dotfiles Manager
GenericName=Gestor de dotfiles
Comment=Gestiona y sincroniza tus dotfiles y aplicaciones
Exec=$SYMLINK
Icon=dotmng
Terminal=false
Categories=Utility;System;FileManager;
Keywords=dotfiles;config;home;sync;
StartupNotify=true
EOF

    # Actualizar base de datos de aplicaciones del escritorio (si está disponible)
    update-desktop-database "$APPS_DIR" 2>/dev/null || true

    echo -e "  ${GREEN}✔${RESET} Entrada de escritorio creada: $DESKTOP_FILE"
else
    echo -e "  ${YELLOW}⚠${RESET} No se encontró icono de aplicación. Entrada .desktop no generada."
    echo -e "    Coloca un icono PNG en: ${BOLD}src/dotmng/resources/icons/dotmng.png${RESET}"
    echo -e "    y vuelve a ejecutar install.sh."
fi

echo ""
