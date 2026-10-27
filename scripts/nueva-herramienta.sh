#!/usr/bin/env bash
# Crea una herramienta nueva a partir de la plantilla.
# Uso: scripts/nueva-herramienta.sh <nombre>
set -euo pipefail
[ $# -ge 1 ] || { echo "Uso: $0 <nombre>" >&2; exit 1; }
raiz="$(cd "$(dirname "$0")/.." && pwd)"
nombre="$1"
slug="$(echo "$nombre" | iconv -t ascii//TRANSLIT 2>/dev/null | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')"
dst="$raiz/herramientas/$slug"
[ -e "$dst" ] && { echo "Ya existe $dst" >&2; exit 1; }
mkdir -p "$dst/capturas"
sed -e "s/^titulo:.*/titulo: \"$nombre\"/" -e "s/^fecha:.*/fecha: $(date +%F)/" \
    -e "s/^# Nombre de la herramienta/# $nombre/" \
    "$raiz/.plantillas/herramienta.md" > "$dst/README.md"
echo "Creado $dst/README.md  (pon 'estado: publicado' cuando esté lista)"
