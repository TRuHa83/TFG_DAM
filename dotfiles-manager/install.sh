#!/usr/bin/env bash

set -euo pipefail

# --- Colores ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- Configuración para instalación remota (GitHub / TFG_DAM) ---
GITHUB_USER="TRuHa83"
GITHUB_REPO="TFG_DAM"
GITHUB_BRANCH="main"
GITHUB_SUBDIR="dotfiles-manager"

REMOTE_GIT_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
REMOTE_INSTALL_SPEC="git+${REMOTE_GIT_URL}#subdirectory=${GITHUB_SUBDIR}"
RAW_BASE_URL="https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/${GITHUB_BRANCH}/${GITHUB_SUBDIR}"

# --- Rutas Locales ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

# Determinar si estamos en un repositorio local clonado (modo desarrollo)
IS_LOCAL=false
if [[ -f "pyproject.toml" ]]; then
    IS_LOCAL=true
elif [[ -f "${SCRIPT_DIR}/pyproject.toml" ]]; then
    IS_LOCAL=true
    cd "$SCRIPT_DIR"
fi

# --- Helpers de Logging ---
log_success() { echo -e "  [ ${GREEN}OK${RESET} ] $1"; }
log_info()    { echo -e "  [${CYAN}INFO${RESET}] $1"; }
log_warn()    { echo -e "  [${YELLOW}WARN${RESET}] $1"; }
log_err()     { echo -e "  [${RED}FAIL${RESET}] $1"; }


show_banner() {
    echo -e "${BOLD}${CYAN}"
    cat << "EOF"
  ____        _    __ _ _                     __  __                                   
 |  _ \  ___ | |_ / _(_) | ___  ___          |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
 | | | |/ _ \| __| |_| | |/ _ \/ __|  _____  | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |_| | (_) | |_|  _| | |  __/\__ \ |_____| | |  | | (_| | | | | (_| | (_| |  __/ |   
 |____/ \___/ \__|_| |_|_|\___||___/         |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
                                                                       |___/  v0.1.0
EOF
    echo -e "    ───────────────────────── Instalador ──────────────────────────${RESET}"
    echo ""
}


verify_requirements() {
    # 1. Verificar sistema operativo Linux
    if [[ "$(uname -s)" != "Linux" ]]; then
        log_err "Este instalador y la aplicación dotmng solo están soportados en sistemas Linux."
        exit 1
    fi

    # 2. Verificar que uv esté instalado
    if ! command -v uv &> /dev/null; then
        log_err "uv no está instalado. Por favor, instálalo primero: https://docs.astral.sh/uv/"
        exit 1
    fi

    # 3. Verificar requisitos adicionales para instalación remota
    if [ "$IS_LOCAL" = false ]; then
        if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
            log_err "Se requiere 'curl' o 'wget' para realizar la instalación remota."
            exit 1
        fi

        if ! command -v git &> /dev/null; then
            log_err "Se requiere 'git' instalado en el sistema para descargar el paquete de GitHub."
            exit 1
        fi
    fi
}


install_tool() {
    if [ "$IS_LOCAL" = true ]; then
        log_info "Modo local detectado. Instalando/Actualizando dotmng con uv..."
        if uv tool install --quiet --force . ; then
            log_success "Herramienta CLI instalada/actualizada correctamente desde el directorio local."
        else
            log_err "Error durante la instalación local de la herramienta CLI."
            exit 1
        fi
    else
        log_info "Modo remoto detectado. Instalando dotmng directamente desde GitHub..."
        log_info "Repositorio: ${REMOTE_GIT_URL} (Carpeta: ${GITHUB_SUBDIR})"
        if uv tool install --quiet --force "${REMOTE_INSTALL_SPEC}" ; then
            log_success "Herramienta CLI instalada/actualizada correctamente desde GitHub."
        else
            log_err "Error al instalar la herramienta desde GitHub."
            log_err "Verifica tu conexión a internet o que el repositorio de GitHub sea público."
            exit 1
        fi
    fi
}


download_file() {
    local url="$1"
    local dest="$2"
    if command -v curl &> /dev/null; then
        curl -sSL -o "$dest" "$url"
    elif command -v wget &> /dev/null; then
        wget -q -O "$dest" "$url"
    else
        return 1
    fi
}


install_desktop_entry() {
    local icons_dir="$HOME/.local/share/icons"
    local apps_dir="$HOME/.local/share/applications"
    local desktop_file="$apps_dir/dotmng.desktop"
    local icon_dest="$icons_dir/dotmng.png"

    mkdir -p "$icons_dir" "$apps_dir"
    echo ""

    if [ "$IS_LOCAL" = true ]; then
        local icon_src="$SCRIPT_DIR/src/dotmng/resources/logo.png"
        local desktop_src="$SCRIPT_DIR/src/dotmng/resources/dotmng.desktop"

        if [[ -f "$icon_src" ]]; then
            cp "$icon_src" "$icon_dest"
            log_success "Icono instalado en: $icon_dest"

            if [[ -f "$desktop_src" ]]; then
                cp "$desktop_src" "$desktop_file"
                update-desktop-database "$apps_dir" 2>/dev/null || true
                log_success "Entrada de escritorio copiada a: $desktop_file"
            else
                log_warn "No se encontró el archivo fuente $desktop_src"
            fi
        else
            log_warn "No se encontró icono de aplicación local. Entrada .desktop no generada."
        fi
    else
        log_info "Descargando recursos visuales desde GitHub..."
        local icon_url="${RAW_BASE_URL}/src/dotmng/resources/logo.png"
        local desktop_url="${RAW_BASE_URL}/src/dotmng/resources/dotmng.desktop"

        if download_file "$icon_url" "$icon_dest"; then
            log_success "Icono descargado e instalado en: $icon_dest"

            if download_file "$desktop_url" "$desktop_file"; then
                update-desktop-database "$apps_dir" 2>/dev/null || true
                log_success "Entrada de escritorio descargada e instalada en: $desktop_file"
            else
                log_warn "No se pudo descargar el archivo .desktop desde: $desktop_url"
            fi
        else
            log_warn "No se pudo descargar el icono desde: $icon_url. Entrada .desktop no generada."
        fi
    fi
}


check_path() {
    echo ""
    if echo "$PATH" | tr ':' '\n' | grep -qx "$INSTALL_DIR"; then
        log_success "${BOLD}$INSTALL_DIR${RESET} ya está en tu PATH."
        echo ""
        echo -e "  ${BOLD}✨ Instalación completada con éxito.${RESET}"
        echo -e "     Puedes usar: ${CYAN}dotmng help${RESET}"
    else
        log_warn "${BOLD}$INSTALL_DIR${RESET} no está en tu PATH."
        echo ""
        echo -e "  Añádelo agregando esta línea a tu ${BOLD}~/.bashrc${RESET} o ${BOLD}~/.zshrc${RESET}:"
        echo -e "     ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
        echo ""
        echo -e "  Luego recarga tu shell:"
        echo -e "     ${CYAN}source ~/.bashrc${RESET}  ${RESET}# o source ~/.zshrc"
        echo ""
        echo -e "  O usa la ruta completa hasta entonces:"
        echo -e "     ${CYAN}$HOME/.local/bin/dotmng help${RESET}"
    fi
}


main() {
    show_banner
    verify_requirements
    install_tool
    install_desktop_entry
    check_path
    echo ""
}


# --- Ejecución ---
main
