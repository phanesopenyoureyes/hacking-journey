#!/usr/bin/env python3
"""Regenera la tabla de índice del README entre los marcadores INDICE:INICIO/FIN.

Lista las máquinas en estado 'publicado' agrupadas por dificultad (omite
'privado' y 'pendiente'). No edites la tabla a mano: este script la sobrescribe.
El texto fuera de los marcadores nunca se toca.
"""
import glob
import os
import re
import sys

INI = "<!-- INDICE:INICIO -->"
FIN = "<!-- INDICE:FIN -->"
SO = {"linux": "Linux", "windows": "Windows"}
DIFICULTADES = [("facil", "Fácil"), ("media", "Media"), ("dificil", "Difícil"), ("insane", "Insane")]


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


def publicadas(slug):
    out = []
    for f in sorted(glob.glob(f"maquinas/htb/{slug}/*/README.md")):
        d = fm(open(f, encoding="utf-8").read())
        if not d or d.get("estado") != "publicado":
            continue
        d["_dir"] = os.path.dirname(f)
        out.append(d)
    out.sort(key=lambda d: d.get("fecha", ""), reverse=True)
    return out


def bloque(base):
    partes = []
    for slug, nombre in DIFICULTADES:
        items = publicadas(slug)
        if not items:
            continue
        partes.append(f"### {nombre}\n")
        filas = ["| Máquina | SO | Fecha | Técnicas |", "| --- | --- | --- | --- |"]
        for d in items:
            rel = os.path.relpath(d["_dir"], base)
            tec = ", ".join(f"`{t.strip()}`" for t in d.get("tecnicas", "").strip("[]").split(",") if t.strip())
            filas.append(f"| [{d['titulo']}]({rel}/) | {SO.get(d['so'], d['so'])} | {d['fecha']} | {tec} |")
        partes.append("\n".join(filas) + "\n")
    return "\n".join(partes) if partes else "_Aún no hay máquinas publicadas._\n"


def main():
    tocados = 0
    for f in glob.glob("**/README.md", recursive=True):
        if f.startswith((".agents/", "site/", "docs/")):
            continue
        txt = open(f, encoding="utf-8").read()
        if INI not in txt or FIN not in txt:
            continue
        base = os.path.dirname(f) or "."
        nuevo = f"{INI}\n\n{bloque(base)}\n{FIN}"
        txt2 = re.sub(re.escape(INI) + r".*?" + re.escape(FIN), nuevo, txt, flags=re.S)
        if txt2 != txt:
            open(f, "w", encoding="utf-8").write(txt2)
            tocados += 1
        print(f"{f}: índice regenerado")
    if tocados == 0:
        print("Aviso: no se tocó ningún README (sin cambios o sin marcadores)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
