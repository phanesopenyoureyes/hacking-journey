#!/usr/bin/env python3
"""Regenera las tablas de índice entre los marcadores INDICE:INICIO / INDICE:FIN.

Lee el front-matter de cada writeup de maquinas/ y escribe una tabla con las
máquinas en estado 'publicado' (omite 'privado' y 'pendiente'). No edites las
tablas a mano: este script las sobrescribe. El texto fuera de los marcadores
nunca se toca.
"""
import glob
import os
import re
import sys

INI = "<!-- INDICE:INICIO -->"
FIN = "<!-- INDICE:FIN -->"
SO = {"linux": "Linux", "windows": "Windows"}


def fm(texto):
    if not texto.startswith("---"):
        return None
    corte = texto.find("\n---", 3)
    if corte == -1:
        return None
    d = {}
    for linea in texto[3:corte].split("\n"):
        m = re.match(r"([a-z_]+):\s*(.*)", linea)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"')
    return d


def maquinas():
    out = []
    for f in sorted(glob.glob("maquinas/**/README.md", recursive=True)):
        if os.path.basename(os.path.dirname(f)) in ("maquinas", "htb"):
            continue
        d = fm(open(f, encoding="utf-8").read())
        if not d or d.get("estado") != "publicado":
            continue
        d["_dir"] = os.path.dirname(f)
        out.append(d)
    out.sort(key=lambda d: d.get("fecha", ""), reverse=True)
    return out


def tabla(items, base):
    filas = [
        "| Máquina | SO | Dificultad | Fecha | Técnicas |",
        "| --- | --- | --- | --- | --- |",
    ]
    for d in items:
        rel = os.path.relpath(d["_dir"], base)
        tec = ", ".join(f"`{t.strip()}`" for t in d.get("tecnicas", "").strip("[]").split(",") if t.strip())
        filas.append(
            f"| [{d['titulo']}]({rel}/) | {SO.get(d['so'], d['so'])} | {d['dificultad']} | {d['fecha']} | {tec} |"
        )
    return "\n".join(filas)


def main():
    items = maquinas()
    n = 0
    for f in glob.glob("**/README.md", recursive=True):
        txt = open(f, encoding="utf-8").read()
        if INI not in txt or FIN not in txt:
            continue
        base = os.path.dirname(f) or "."
        nuevo = f"{INI}\n\n{tabla(items, base)}\n\n{FIN}"
        txt2 = re.sub(re.escape(INI) + r".*?" + re.escape(FIN), nuevo, txt, flags=re.S)
        if txt2 != txt:
            open(f, "w", encoding="utf-8").write(txt2)
            n += 1
        print(f"{f}: {len(items)} máquinas publicadas")
    if n == 0 and not any(INI in open(f, encoding="utf-8").read() for f in glob.glob("**/README.md", recursive=True)):
        print("Aviso: ningún README tiene los marcadores INDICE:INICIO/FIN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
