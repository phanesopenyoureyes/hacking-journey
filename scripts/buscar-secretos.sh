#!/usr/bin/env bash
# Busca secretos propios de alto riesgo en los ficheros versionados del repo.
# No marca credenciales de las máquinas (forman parte del writeup); solo busca
# claves privadas, ficheros .ovpn y tokens de API filtrados por error.
set -uo pipefail

raiz="$(cd "$(dirname "$0")/.." && pwd)"
cd "$raiz"

patrones=(
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'client[[:space:]]*\n?remote[[:space:]].*\.ovpn'
  'ghp_[A-Za-z0-9]{36}'
  'github_pat_[A-Za-z0-9_]{80,}'
  'AKIA[0-9A-Z]{16}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  '-----BEGIN OPENVPN STATIC KEY'
)

encontrados=0
ficheros="$(git ls-files -- ':!.agents/**')"
for p in "${patrones[@]}"; do
  if hits="$(echo "$ficheros" | xargs -d '\n' grep -InE "$p" 2>/dev/null)"; then
    if [ -n "$hits" ]; then
      echo "Posible secreto ($p):"
      echo "$hits"
      encontrados=1
    fi
  fi
done

if [ "$encontrados" -ne 0 ]; then
  echo "Se han encontrado posibles secretos. Revísalos antes de commitear." >&2
  exit 1
fi
echo "Sin secretos propios detectados."
