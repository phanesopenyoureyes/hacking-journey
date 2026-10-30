#!/usr/bin/env python3
"""Prepara docs/ para MkDocs a partir del contenido publicado del repo.

Estructura que genera:
- Máquinas agrupadas por dificultad: docs/maquinas/<dificultad>/<maquina>/
- Certificaciones:                   docs/certificaciones/<slug>/
- Herramientas:                      docs/herramientas/<slug>/

Solo copia lo que está en estado 'publicado' (deja fuera 'privado' y
'pendiente'). Las secciones y las dificultades aparecen siempre, aunque estén
vacías, con una página que lo indica. Escribe los .pages (títulos y orden del
menú) y la portada docs/index.md. Todo docs/ generado está en .gitignore y se
reconstruye en cada build, también en CI.
"""
import glob
import os
import re
import shutil

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


def publicados(patron):
    out = []
    for f in sorted(glob.glob(patron)):
        d = fm(open(f, encoding="utf-8").read())
        if not d or d.get("estado") != "publicado":
            continue
        d["_src"] = os.path.dirname(f)
        d["_slug"] = os.path.basename(os.path.dirname(f))
        out.append(d)
    out.sort(key=lambda d: d.get("fecha", ""), reverse=True)
    return out


def escribir(path, texto):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(texto)


def tabla_maquinas(items, base_rel):
    filas = ["| Máquina | SO | Fecha | Técnicas |", "| --- | --- | --- | --- |"]
    for d in items:
        tec = ", ".join(f"`{t.strip()}`" for t in d.get("tecnicas", "").strip("[]").split(",") if t.strip())
        filas.append(f"| [{d['titulo']}]({base_rel}{d['_slug']}/README.md) | {SO.get(d['so'], d['so'])} | {d.get('fecha','')} | {tec} |")
    return "\n".join(filas)


def seccion_maquinas():
    base = "docs/maquinas"
    total = 0
    for slug, nombre in DIFICULTADES:
        items = publicados(f"maquinas/htb/{slug}/*/README.md")
        total += len(items)
        destdir = f"{base}/{slug}"
        os.makedirs(destdir, exist_ok=True)
        for d in items:
            shutil.copytree(d["_src"], f"{destdir}/{d['_slug']}")
        if items:
            cuerpo = (
                f"# Máquinas · {nombre}\n\n"
                f"Máquinas de dificultad **{nombre}** resueltas ({len(items)}).\n\n"
                + tabla_maquinas(items, "")
                + "\n"
            )
        else:
            cuerpo = f"# Máquinas · {nombre}\n\nAún no hay máquinas de dificultad **{nombre}** publicadas.\n"
        escribir(f"{destdir}/index.md", cuerpo)
        # orden dentro de la dificultad: la portada primero, luego por fecha
        pages = f"title: {nombre}\nnav:\n  - index.md\n" + "".join(f"  - {d['_slug']}\n" for d in items)
        escribir(f"{destdir}/.pages", pages)
    # .pages de la sección Máquinas: orden de dificultades
    nav = "".join(f"  - {slug}\n" for slug, _ in DIFICULTADES)
    escribir(f"{base}/.pages", f"title: Máquinas\nnav:\n{nav}")
    return total


def seccion_simple(carpeta, titulo, titulo_sing, columnas, emoji, intro=None, vacio=None):
    """Genera una sección tipo lista (certificaciones, herramientas, preparación)."""
    items = publicados(f"{carpeta}/*/README.md")
    base = f"docs/{carpeta}"
    os.makedirs(base, exist_ok=True)
    for d in items:
        shutil.copytree(d["_src"], f"{base}/{d['_slug']}")
    if items:
        intro_txt = intro.format(n=len(items)) if intro else f"Mis {titulo.lower()} ({len(items)})."
        filas = ["| " + " | ".join(c[0] for c in columnas) + " |",
                 "| " + " | ".join("---" for _ in columnas) + " |"]
        for d in items:
            celdas = [c[1](d) for c in columnas]
            filas.append("| " + " | ".join(celdas) + " |")
        cuerpo = f"# {emoji} {titulo}\n\n{intro_txt}\n\n" + "\n".join(filas) + "\n"
    else:
        vacio_txt = vacio or f"Aún no hay {titulo.lower()} publicadas. Se añadirán aquí según las vaya documentando."
        cuerpo = f"# {emoji} {titulo}\n\n{vacio_txt}\n"
    escribir(f"{base}/index.md", cuerpo)
    pages = f"title: {titulo}\nnav:\n  - index.md\n" + "".join(f"  - {d['_slug']}\n" for d in items)
    escribir(f"{base}/.pages", pages)
    return len(items)


def main():
    for d in ("docs/maquinas", "docs/certificaciones", "docs/herramientas", "docs/preparacion"):
        if os.path.isdir(d):
            shutil.rmtree(d)

    n_maq = seccion_maquinas()
    n_cert = seccion_simple(
        "certificaciones", "Certificaciones", "certificación",
        [("Certificación", lambda d: f"[{d['titulo']}]({d['_slug']}/README.md)"),
         ("Entidad", lambda d: d.get("entidad", "")),
         ("Fecha", lambda d: d.get("fecha", ""))],
        "🎓",
    )
    n_herr = seccion_simple(
        "herramientas", "Herramientas", "herramienta",
        [("Herramienta", lambda d: f"[{d['titulo']}]({d['_slug']}/README.md)"),
         ("Tipo", lambda d: d.get("tipo", "")),
         ("Fecha", lambda d: d.get("fecha", ""))],
        "🛠️",
    )
    n_prep = seccion_simple(
        "preparacion", "Preparación para certificaciones", "preparación",
        [("Certificación", lambda d: f"[{d['titulo']}]({d['_slug']}/README.md)"),
         ("Entidad", lambda d: d.get("entidad", ""))],
        "📚",
        intro="Guías y recursos para preparar certificaciones de seguridad ofensiva ({n}).",
        vacio="Aún no hay guías de preparación publicadas. Se añadirán aquí según prepare cada certificación.",
    )

    index = (
        "# Francisco Gutiérrez García\n\n"
        "Seguridad ofensiva · alias **ph4n3s** en Hack The Box.\n{ .hero-sub }\n\n"
        "Writeups de máquinas **retiradas** de Hack The Box, certificaciones y "
        "herramientas, documentados paso a paso como parte de mi formación en "
        "seguridad ofensiva. Cada writeup explica el *porqué* de cada paso y cierra "
        "con una nota de mitigación.\n\n"
        "Usa el buscador (arriba) para encontrar una técnica, un servicio o una máquina.\n\n"
        '<div class="grid cards" markdown>\n\n'
        f"- :material-server-network:{{ .lg .middle }} **[Máquinas](maquinas/facil/)**\n\n"
        f"    ---\n\n    {n_maq} máquinas resueltas, agrupadas por dificultad (Fácil, Media, Difícil, Insane).\n\n"
        f"- :material-certificate:{{ .lg .middle }} **[Certificaciones](certificaciones/)**\n\n"
        f"    ---\n\n    {n_cert} certificaciones publicadas.\n\n"
        f"- :material-book-open-variant:{{ .lg .middle }} **[Preparación para certificaciones](preparacion/)**\n\n"
        f"    ---\n\n    {n_prep} guías de preparación con recursos y temas clave.\n\n"
        f"- :material-tools:{{ .lg .middle }} **[Herramientas](herramientas/)**\n\n"
        f"    ---\n\n    {n_herr} herramientas propias publicadas.\n\n"
        "- :material-account:{ .lg .middle } **[Sobre mí](sobre-mi/)**\n\n"
        "    ---\n\n    Quién soy, mis perfiles y cómo contactar.\n\n"
        "</div>\n"
    )
    escribir("docs/index.md", index)
    print(f"sitio generado: {n_maq} máquinas, {n_cert} certificaciones, {n_prep} preparaciones, {n_herr} herramientas")


if __name__ == "__main__":
    main()
