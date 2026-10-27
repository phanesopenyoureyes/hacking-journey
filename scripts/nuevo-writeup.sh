#!/usr/bin/env bash
# Crea un writeup nuevo a partir de la plantilla, dentro de su dificultad.
# Uso: scripts/nuevo-writeup.sh <nombre-maquina> <dificultad> [plataforma]
#   dificultad: facil | media | dificil | insane
#   plataforma: htb (por defecto)
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Uso: $0 <nombre-maquina> <dificultad> [plataforma]" >&2
  echo "  dificultad: facil | media | dificil | insane" >&2
  exit 1
fi

raiz="$(cd "$(dirname "$0")/.." && pwd)"
nombre="$1"
dif="$2"
plataforma="${3:-htb}"

case "$dif" in
  facil|media|dificil|insane) ;;
  *) echo "Dificultad no válida: $dif (usa facil|media|dificil|insane)" >&2; exit 1 ;;
esac

slug="$(echo "$nombre" | iconv -t ascii//TRANSLIT 2>/dev/null | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')"
dst="$raiz/maquinas/$plataforma/$dif/$slug"

if [ -e "$dst" ]; then
  echo "Ya existe $dst" >&2
  exit 1
fi

mkdir -p "$dst/capturas"
# dificultad en el front-matter, legible
case "$dif" in
  facil) dnom="Fácil" ;; media) dnom="Media" ;; dificil) dnom="Difícil" ;; insane) dnom="Insane" ;;
esac
sed -e "s/^titulo:.*/titulo: \"$nombre\"/" \
    -e "s/^fecha:.*/fecha: $(date +%F)/" \
    -e "s/^plataforma:.*/plataforma: $plataforma/" \
    -e "s/^dificultad:.*/dificultad: $dnom/" \
    -e "s/^# Nombre de la máquina/# $nombre/" \
    "$raiz/.plantillas/writeup.md" > "$dst/README.md"

echo "Creado $dst/README.md"
echo "Rellénalo y pon 'estado: publicado' cuando esté listo. Capturas en $dst/capturas/"
