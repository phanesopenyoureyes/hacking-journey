#!/usr/bin/env python3
"""Comprueba que los enlaces e imágenes relativos de los .md existan en disco.

No comprueba URLs externas (http/https). Falla (código 1) listando los enlaces
rotos con fichero y línea.
"""
import glob
import os
import re
import sys

PAT = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
IGN = (".agents/", "site/", "docs/maquinas/", "node_modules/")


def main():
    rotos = []
    for f in glob.glob("**/*.md", recursive=True):
        if f.startswith(IGN):
            continue
        base = os.path.dirname(f)
        for n, linea in enumerate(open(f, encoding="utf-8"), 1):
            for dest in PAT.findall(linea):
                d = dest.split("#")[0]
                if not d or d.startswith(("http://", "https://", "mailto:", "/")):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(base, d))):
                    rotos.append(f"{f}:{n}: enlace roto -> {dest}")
    if rotos:
        print(f"Enlaces rotos: {len(rotos)}\n")
        for r in rotos:
            print("  -", r)
        return 1
    print("Enlaces OK: todos los enlaces relativos resuelven.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
