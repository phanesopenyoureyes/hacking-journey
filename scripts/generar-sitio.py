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


def seccion_simple(carpeta, titulo, titulo_sing, columnas, emoji):
    """Genera una sección tipo lista (certificaciones, herramientas)."""
    items = publicados(f"{carpeta}/*/README.md")
    base = f"docs/{carpeta}"
    os.makedirs(base, exist_ok=True)
    for d in items:
        shutil.copytree(d["_src"], f"{base}/{d['_slug']}")
    if items:
        filas = ["| " + " | ".join(c[0] for c in columnas) + " |",
                 "| " + " | ".join("---" for _ in columnas) + " |"]
        for d in items:
            celdas = [c[1](d) for c in columnas]
            filas.append("| " + " | ".join(celdas) + " |")
        cuerpo = f"# {emoji} {titulo}\n\nMis {titulo.lower()} ({len(items)}).\n\n" + "\n".join(filas) + "\n"
    else:
        cuerpo = f"# {emoji} {titulo}\n\nAún no hay {titulo.lower()} publicadas. Se añadirán aquí según las vaya documentando.\n"
    escribir(f"{base}/index.md", cuerpo)
    pages = f"title: {titulo}\nnav:\n  - index.md\n" + "".join(f"  - {d['_slug']}\n" for d in items)
    escribir(f"{base}/.pages", pages)
    return len(items)


def main():
    for d in ("docs/maquinas", "docs/certificaciones", "docs/herramientas"):
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

    index = (
        "# Hacking-Journey\n\n"
        "Writeups de máquinas **retiradas** de Hack The Box, certificaciones y "
        "herramientas, documentados paso a paso por **Francisco Gutiérrez García** "
        "como parte de su formación en seguridad ofensiva.\n\n"
        "Usa el buscador (arriba) para encontrar una técnica, un servicio o una máquina.\n\n"
        "## Secciones\n\n"
        f"- **[Máquinas](maquinas/facil/)** — {n_maq} resueltas, agrupadas por dificultad.\n"
        f"- **[Certificaciones](certificaciones/)** — {n_cert} publicadas.\n"
        f"- **[Herramientas](herramientas/)** — {n_herr} publicadas.\n"
        "- **[Sobre mí](sobre-mi/)** — quién soy y cómo contactar.\n"
    )
    escribir("docs/index.md", index)
    print(f"sitio generado: {n_maq} máquinas, {n_cert} certificaciones, {n_herr} herramientas")


if __name__ == "__main__":
    main()
