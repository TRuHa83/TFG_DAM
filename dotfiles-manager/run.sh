#!/usr/bin/env bash
# =============================================================================
# run.sh — Wrapper para ejecutar dotmng desde cualquier directorio del terminal
# Se invoca a través del symlink instalado por install.sh
# =============================================================================

# Resolver la ruta real del script (siguiendo symlinks)
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

# Moverse al directorio del proyecto para que uv encuentre pyproject.toml
cd "$SCRIPT_DIR" || {
    echo "Error: No se pudo acceder al directorio del proyecto: $SCRIPT_DIR" >&2
    exit 1
}

# Delegar la ejecución a uv, pasando todos los argumentos recibidos
exec uv run dotmng "$@"
