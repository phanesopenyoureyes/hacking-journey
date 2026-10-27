#!/usr/bin/env python3
"""Prepara docs/ para MkDocs a partir de los writeups publicados.

Copia a docs/maquinas/ solo los writeups en estado 'publicado' (deja fuera los
'privado' y 'pendiente') con sus capturas, y escribe docs/index.md con la
portada y la tabla de máquinas. El contenido generado está en .gitignore; se
reconstruye en cada build, también en CI.
"""
import glob
import os
import re
import shutil

SO = {"linux": "Linux", "windows": "Windows"}
DST = "docs/maquinas"


def fm(texto):
    if not texto.startswith("---"):
        return None
    c = texto.find("\n---", 3)
    if c == -1:
        return None
    d = {}
    for linea in texto[3:c].split("\n"):
        m = re.match(r"([a-z_]+):\s*(.*)", linea)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"')
    return d


def main():
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)
    pub = []
    for f in sorted(glob.glob("maquinas/htb/*/README.md")):
        d = fm(open(f, encoding="utf-8").read())
        if not d or d.get("estado") != "publicado":
            continue
        k = os.path.basename(os.path.dirname(f))
        shutil.copytree(os.path.dirname(f), f"{DST}/{k}")
        d["_k"] = k
        pub.append(d)
    pub.sort(key=lambda d: d.get("fecha", ""), reverse=True)

    filas = ["| Máquina | SO | Dificultad | Fecha | Técnicas |", "| --- | --- | --- | --- | --- |"]
    for d in pub:
        tec = ", ".join(f"`{t.strip()}`" for t in d.get("tecnicas", "").strip("[]").split(",") if t.strip())
        filas.append(f"| [{d['titulo']}](maquinas/{d['_k']}/README.md) | {SO.get(d['so'], d['so'])} | {d['dificultad']} | {d['fecha']} | {tec} |")

    index = (
        "# Hacking-Journey\n\n"
        "Writeups de máquinas **retiradas** de Hack The Box, documentados paso a paso "
        "por **Francisco Gutiérrez García** como parte de su formación en seguridad "
        "ofensiva. Cada writeup explica el porqué de cada paso y cierra con una nota de "
        "mitigación.\n\n"
        "Usa el buscador (arriba) para encontrar una técnica, un servicio o una máquina.\n\n"
        "## Máquinas\n\n" + "\n".join(filas) + "\n\n"
        "---\n\n"
        "El código fuente está en "
        "[github.com/phanesopenyoureyes/hacking-journey]"
        "(https://github.com/phanesopenyoureyes/hacking-journey).\n"
    )
    open("docs/index.md", "w", encoding="utf-8").write(index)
    print(f"sitio generado: {len(pub)} máquinas publicadas en {DST}/")


if __name__ == "__main__":
    main()
