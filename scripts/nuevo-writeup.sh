#!/usr/bin/env bash
# Crea un writeup nuevo a partir de la plantilla.
# Uso: scripts/nuevo-writeup.sh <nombre-maquina> [plataforma]
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Uso: $0 <nombre-maquina> [plataforma]   (plataforma por defecto: htb)" >&2
  exit 1
fi

raiz="$(cd "$(dirname "$0")/.." && pwd)"
nombre="$1"
plataforma="${2:-htb}"
# kebab-case, sin acentos, sin mayúsculas
slug="$(echo "$nombre" | iconv -t ascii//TRANSLIT 2>/dev/null | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')"
dst="$raiz/maquinas/$plataforma/$slug"

if [ -e "$dst" ]; then
  echo "Ya existe $dst" >&2
  exit 1
fi

mkdir -p "$dst/capturas"
sed -e "s/^titulo:.*/titulo: \"$nombre\"/" \
    -e "s/^fecha:.*/fecha: $(date +%F)/" \
    -e "s/^plataforma:.*/plataforma: $plataforma/" \
    -e "s/^# Nombre de la máquina/# $nombre/" \
    "$raiz/.plantillas/writeup.md" > "$dst/README.md"

echo "Creado $dst/README.md"
echo "Rellena el front-matter y las secciones. Las capturas van en $dst/capturas/"
