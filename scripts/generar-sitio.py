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
import hashlib
import os
import re
import shutil
from collections import Counter

SO = {"linux": "Linux", "windows": "Windows"}
OS_ICONO = {"linux": ":material-linux:", "windows": ":material-microsoft-windows:"}
DIFICULTADES = [("facil", "Fácil"), ("media", "Media"), ("dificil", "Difícil"), ("insane", "Insane")]

# Writeups destacados de la portada (dificultad, slug, nombre, por qué).
DESTACADOS = [
    ("facil", "validation", "Validation",
     "Inyección SQL explotada a mano con Burp Suite; documenta los atascos reales y "
     "distingue bien los tipos de inyección."),
    ("facil", "optimum", "Optimum",
     "RCE sobre HttpFileServer y escalada por un exploit de kernel (MS16-032), con un "
     "intento fallido y la alternativa que sí funcionó."),
    ("facil", "delivery", "Delivery",
     "Encadena una fuga de información en osTicket con la reutilización de contraseñas "
     "y termina con un hash de MySQL crackeado con hashcat."),
]


def lista(campo):
    """Convierte un valor de front-matter tipo `[a, b, c]` en lista de strings."""
    return [t.strip() for t in str(campo or "").strip().strip("[]").split(",") if t.strip()]


def cuenta(n, singular, plural):
    """Devuelve 'N palabra' concordando singular/plural (1 certificación / 2 certificaciones)."""
    return f"{n} {singular if n == 1 else plural}"


def _negritas(txt):
    """Convierte **texto** en <strong> (para usar en bloques HTML sin Markdown)."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)


def sec_head(badge, titulo, intro):
    """Cabecera de sección: badge grande + título + subtítulo (HTML, sin Markdown)."""
    return (
        '<div class="sec-head">'
        f'<span class="sec-head__badge">{badge}</span>'
        '<div class="sec-head__text">'
        f'<h1 class="sec-head__title">{titulo}</h1>'
        f'<p class="sec-head__sub">{_negritas(intro)}</p>'
        '</div></div>'
    )


def ficha_maquina(d, dif_nombre):
    """Cabecera interactiva (icono + metadatos + técnicas) de una máquina."""
    slug, titulo = d["_slug"], d["titulo"]
    htb = d.get("htb", "")
    so = d.get("so", "")
    dif_slug = next((s for s, n in DIFICULTADES if n == dif_nombre), "facil")
    tecs = "".join(f'<span class="tec">{t}</span>' for t in lista(d.get("tecnicas")))
    herr = "".join(f'<span class="tec tec--herr">{t}</span>' for t in lista(d.get("herramientas")))
    ini = (f'<a class="ficha__ico" href="{htb}" target="_blank" rel="noopener" '
           f'title="Ver {titulo} en Hack The Box">') if htb else '<span class="ficha__ico">'
    fin = "</a>" if htb else "</span>"
    cta = (f'<a class="btn-htb" href="{htb}" target="_blank" rel="noopener" '
           f'aria-label="Ver {titulo} en Hack The Box">'
           f':simple-hackthebox: <span class="btn-htb__txt">Ver en Hack The Box</span>'
           f'<span class="btn-htb__arrow" aria-hidden="true">→</span></a>') if htb else ""
    return (
        '<div class="ficha" markdown>\n'
        f'{ini}<img src="capturas/{slug}-icono.png" alt="Icono de {titulo} en Hack The Box" '
        f'loading="lazy">{fin}\n'
        '<div class="ficha__info" markdown>\n\n'
        f'# {titulo}\n\n'
        '<span class="ficha__chips">'
        f'<span class="chip chip--os chip--{so}">{OS_ICONO.get(so, "")} {SO.get(so, so)}</span>'
        f'<span class="chip chip--dif chip--dif-{dif_slug}">{dif_nombre}</span>'
        f'<span class="chip chip--date">:material-calendar-outline: {d.get("fecha", "")}</span>'
        '</span>\n\n'
        f'<div class="ficha__tecs">{tecs}{herr}</div>\n\n'
        f'{cta}\n'
        '</div>\n'
        '</div>'
    )


def reescribir_con_ficha(path, d, dif_nombre):
    """Sustituye el `# Título` + icono suelto del README por la ficha interactiva."""
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n.*?\n---\n", txt, re.S)
    fm_txt = m.group(0) if m else ""
    body = txt[m.end():] if m else txt
    # El H1 va dentro del bloque HTML de la ficha, así que MkDocs no lo detecta
    # como título (y la página saldría como "Index"). Fijamos el título de la
    # página con la clave `title:` del front-matter, que MkDocs sí respeta.
    if m and not re.search(r"^title:\s", fm_txt, re.M):
        fm_txt = fm_txt.replace("---\n", f'---\ntitle: "{d["titulo"]}"\n', 1)
    nuevas, h1_fuera = [], False
    for ln in body.split("\n"):
        if ".maquina-icono" in ln:
            continue
        if not h1_fuera and re.match(r"#\s+\S", ln):
            h1_fuera = True
            continue
        nuevas.append(ln)
    body = "\n".join(nuevas).lstrip("\n")
    open(path, "w", encoding="utf-8").write(f"{fm_txt}\n{ficha_maquina(d, dif_nombre)}\n\n{body}")


def galeria_maquinas(items, base_rel):
    """Rejilla de tarjetas clicables de máquinas para los índices por dificultad."""
    cards = []
    for d in items:
        slug, so = d["_slug"], d.get("so", "")
        cards.append(
            f'<a class="maq-card maq-card--{so}" href="{base_rel}{slug}/">'
            f'<img class="maq-card__ico" src="{base_rel}{slug}/capturas/{slug}-icono.png" '
            f'alt="" loading="lazy">'
            f'<span class="maq-card__nombre">{d["titulo"]}</span>'
            f'<span class="maq-card__meta">'
            f'<span class="chip chip--os chip--{so}">{SO.get(so, so)}</span>'
            f'<span class="maq-card__fecha">{d.get("fecha", "")}</span>'
            f'</span></a>'
        )
    return '<div class="maq-grid">\n' + "\n".join(cards) + "\n</div>"


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
            destino = f"{destdir}/{d['_slug']}"
            shutil.copytree(d["_src"], destino)
            reescribir_con_ficha(f"{destino}/README.md", d, nombre)
        cab = (f'---\ntitle: "Máquinas · {nombre}"\nhide:\n  - toc\n---\n\n')
        if items:
            cuerpo = (
                cab
                + sec_head("🖥️", f"Máquinas · {nombre}",
                           f"Máquinas de dificultad **{nombre}** resueltas ({len(items)}).")
                + "\n\n"
                + galeria_maquinas(items, "")
                + "\n"
            )
        else:
            cuerpo = (
                cab
                + sec_head("🖥️", f"Máquinas · {nombre}",
                           f"Aún no hay máquinas de dificultad **{nombre}** publicadas.")
                + "\n"
            )
        escribir(f"{destdir}/index.md", cuerpo)
        # orden dentro de la dificultad: la portada primero, luego por fecha
        pages = f"title: {nombre}\nnav:\n  - index.md\n" + "".join(f"  - {d['_slug']}\n" for d in items)
        escribir(f"{destdir}/.pages", pages)
    # .pages de la sección Máquinas: orden de dificultades
    nav = "".join(f"  - {slug}\n" for slug, _ in DIFICULTADES)
    escribir(f"{base}/.pages", f"title: Máquinas\nnav:\n{nav}")
    return total


def tarjetas_certs(items, badge, estado, clase):
    """Rejilla de tarjetas (certificaciones / preparación) en vez de una tabla."""
    cards = []
    for d in items:
        meta = " · ".join(x for x in [d.get("entidad", ""), d.get("fecha", "")] if x)
        temas = lista(d.get("temas"))
        chips = ("".join(f'<span class="cert-card__tema">{t}</span>' for t in temas))
        temas_html = f'<span class="cert-card__temas">{chips}</span>' if temas else ""
        cards.append(
            f'<a class="cert-card" href="{d["_slug"]}/">'
            f'<span class="cert-card__top">'
            f'<span class="cert-card__badge">{badge}</span>'
            f'<span class="cert-card__estado cert-card__estado--{clase}">{estado}</span>'
            f'</span>'
            f'<span class="cert-card__tit">{d["titulo"]}'
            f'<span class="cert-card__arrow" aria-hidden="true">→</span></span>'
            f'<span class="cert-card__meta">{meta}</span>'
            f'{temas_html}'
            f'</a>'
        )
    return '<div class="cert-grid">' + "".join(cards) + "</div>"


def seccion_simple(carpeta, titulo, titulo_sing, columnas, emoji, intro=None, vacio=None,
                   ocultar_si_vacia=False, tarjeta=None):
    """Genera una sección tipo lista (certificaciones, herramientas, preparación).

    Con `ocultar_si_vacia=True`, si no hay contenido publicado no se genera nada:
    la sección no aparece en el nav ni en la portada (no deja páginas vacías).
    Con `tarjeta={"badge","estado","clase"}` se renderiza como tarjetas; si no, tabla.
    """
    items = publicados(f"{carpeta}/*/README.md")
    if not items and ocultar_si_vacia:
        return 0
    base = f"docs/{carpeta}"
    os.makedirs(base, exist_ok=True)
    for d in items:
        shutil.copytree(d["_src"], f"{base}/{d['_slug']}")
    if items:
        intro_txt = intro.format(n=len(items)) if intro else f"Mis {titulo.lower()} ({len(items)})."
        if tarjeta:
            contenido = tarjetas_certs(items, tarjeta["badge"], tarjeta["estado"], tarjeta["clase"])
        else:
            filas = ["| " + " | ".join(c[0] for c in columnas) + " |",
                     "| " + " | ".join("---" for _ in columnas) + " |"]
            for d in items:
                celdas = [c[1](d) for c in columnas]
                filas.append("| " + " | ".join(celdas) + " |")
            contenido = "\n".join(filas)
        cuerpo = (f'---\ntitle: "{titulo}"\nhide:\n  - toc\n---\n\n'
                  + sec_head(emoji, titulo, intro_txt) + "\n\n" + contenido + "\n")
    else:
        vacio_txt = vacio or f"Aún no hay {titulo.lower()} publicadas. Se añadirán aquí según las vaya documentando."
        cuerpo = (f'---\ntitle: "{titulo}"\nhide:\n  - toc\n---\n\n'
                  + sec_head(emoji, titulo, vacio_txt) + "\n")
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
        ocultar_si_vacia=True,
        tarjeta={"badge": "🎓", "estado": "Obtenida", "clase": "ok"},
    )
    n_herr = seccion_simple(
        "herramientas", "Herramientas", "herramienta",
        [("Herramienta", lambda d: f"[{d['titulo']}]({d['_slug']}/README.md)"),
         ("Tipo", lambda d: d.get("tipo", "")),
         ("Fecha", lambda d: d.get("fecha", ""))],
        "🛠️",
        ocultar_si_vacia=True,
    )
    n_prep = seccion_simple(
        "preparacion", "Preparación para certificaciones", "preparación",
        [("Certificación", lambda d: f"[{d['titulo']}]({d['_slug']}/README.md)"),
         ("Entidad", lambda d: d.get("entidad", ""))],
        "📚",
        intro="Guías y recursos para preparar certificaciones de seguridad ofensiva ({n}).",
        ocultar_si_vacia=True,
        tarjeta={"badge": "📚", "estado": "En preparación", "clase": "prep"},
    )

    # Nav superior: solo las secciones con contenido (oculta las vacías).
    nav = ["  - index.md\n", "  - maquinas\n"]
    if n_cert:
        nav.append("  - certificaciones\n")
    if n_prep:
        nav.append("  - preparacion\n")
    if n_herr:
        nav.append("  - herramientas\n")
    nav.append("  - Sobre mí: sobre-mi.md\n")
    escribir("docs/.pages", "nav:\n" + "".join(nav))

    # Tarjetas de la portada: solo las secciones con contenido, con plural correcto.
    cards = [
        f"- :material-server-network:{{ .lg .middle }} **[Máquinas](maquinas/facil/)**\n\n"
        f"    ---\n\n    {cuenta(n_maq, 'máquina resuelta', 'máquinas resueltas')}, "
        f"agrupadas por dificultad.\n"
    ]
    if n_cert:
        cards.append(
            f"- :material-certificate:{{ .lg .middle }} **[Certificaciones](certificaciones/)**\n\n"
            f"    ---\n\n    {cuenta(n_cert, 'certificación publicada', 'certificaciones publicadas')}.\n"
        )
    if n_prep:
        cards.append(
            f"- :material-book-open-variant:{{ .lg .middle }} **[Preparación para certificaciones](preparacion/)**\n\n"
            f"    ---\n\n    {cuenta(n_prep, 'guía de preparación', 'guías de preparación')} "
            f"con recursos y temas clave.\n"
        )
    if n_herr:
        cards.append(
            f"- :material-tools:{{ .lg .middle }} **[Herramientas](herramientas/)**\n\n"
            f"    ---\n\n    {cuenta(n_herr, 'herramienta propia publicada', 'herramientas propias publicadas')}.\n"
        )
    cards.append(
        "- :material-account:{ .lg .middle } **[Sobre mí](sobre-mi/)**\n\n"
        "    ---\n\n    Quién soy, mis perfiles y cómo contactar.\n"
    )

    # --- Datos reales agregados para la portada ---
    maquinas_all = []
    dif_counts = []
    for _slug, _nombre in DIFICULTADES:
        _its = publicados(f"maquinas/htb/{_slug}/*/README.md")
        if _its:
            dif_counts.append((_nombre, len(_its)))
        maquinas_all += _its
    n_linux = sum(1 for d in maquinas_all if d.get("so") == "linux")
    n_win = sum(1 for d in maquinas_all if d.get("so") == "windows")
    tec_count = Counter(t for d in maquinas_all for t in lista(d.get("tecnicas")))
    n_tec = len(tec_count)
    top_tecs = [t for t, _ in tec_count.most_common(24)]
    nube = "".join(f'<span class="tec">{t}</span>' for t in top_tecs)

    # Desglose de plataformas para el hero (muestra alcance Linux/Windows).
    pills = []
    if n_linux:
        pills.append(f'<span class="hero__pill"><span class="hero__pill-n">{n_linux}</span> Linux</span>')
    if n_win:
        pills.append(f'<span class="hero__pill"><span class="hero__pill-n">{n_win}</span> Windows</span>')
    hero_meta = '<div class="hero__meta">' + "".join(pills) + "</div>" if pills else ""

    # Writeups destacados como tarjetas con icono.
    destacados_cards = "".join(
        f'<a class="dest-card" href="maquinas/{dif}/{slug}/">'
        f'<img class="dest-card__ico" src="maquinas/{dif}/{slug}/capturas/{slug}-icono.png" '
        f'alt="" loading="lazy">'
        f'<span class="dest-card__body">'
        f'<span class="dest-card__nombre">{nombre}'
        f'<span class="dest-card__arrow" aria-hidden="true">→</span></span>'
        f'<span class="dest-card__txt">{por_que}</span></span></a>'
        for dif, slug, nombre, por_que in DESTACADOS
    )

    # Capacidades (lo que domino), basadas en las competencias reales del repo.
    capacidades = [
        (":material-magnify:", "Enumeración",
         "Mapeo de la superficie de ataque: SMB, FTP, HTTP, WebDAV, CGI y servicios menos comunes."),
        (":material-bug-outline:", "Identificación de vulnerabilidades",
         "De la versión del servicio a su CVE y al exploit que la aprovecha."),
        (":material-linux:", "Escalada en Linux",
         "`sudo` mal configurado, tareas cron, binarios SUID y GTFOBins."),
        (":material-microsoft-windows:", "Escalada en Windows",
         "*Token impersonation*, exploits de kernel y Metasploit."),
        (":material-shield-alert-outline:", "Configuraciones inseguras",
         "Credenciales por defecto, servicios expuestos, permisos excesivos y reúso de contraseñas."),
        (":material-file-document-edit-outline:", "Documentación técnica",
         "Cada writeup sigue la misma plantilla, pasa un validador y cierra con su mitigación."),
    ]
    cap_cards = "\n".join(
        f"- {ic}{{ .lg .middle }} **{tit}**\n\n    ---\n\n    {desc}\n"
        for ic, tit, desc in capacidades
    )

    pasos = ["Reconocimiento", "Enumeración", "Explotación",
             "Acceso inicial", "Escalada", "Mitigación"]
    metodo = "".join(
        f'<span class="metodo__step">'
        f'<span class="metodo__n">{i + 1}</span>'
        f'<span class="metodo__lbl">{p}</span></span>'
        for i, p in enumerate(pasos)
    )

    index = (
        "---\nhide:\n  - navigation\n  - toc\n---\n\n"
        # ---------- HERO ----------
        '<div class="hero" markdown>\n\n'
        '<p class="hero__term"><span class="hero__term-ps">ph4n3s@htb:~$</span> whoami</p>\n\n'
        "# Francisco Gutiérrez García\n\n"
        '<p class="hero__tagline">Seguridad ofensiva · alias <strong>ph4n3s</strong> '
        'en Hack The Box</p>\n\n'
        "Resuelvo y documento máquinas **retiradas** de Hack The Box: para cada una "
        "explico el *porqué* de cada paso —no solo el comando— y cierro con la nota de "
        "mitigación que habría evitado el fallo.\n\n"
        '<div class="hero__stats">\n'
        f'<div class="stat"><span class="stat__num">{n_maq}</span>'
        '<span class="stat__lbl">máquinas resueltas y documentadas</span></div>\n'
        '<div class="stat"><span class="stat__num">eJPT</span>'
        '<span class="stat__lbl">certificación obtenida</span></div>\n'
        '<div class="stat"><span class="stat__num">CPTS</span>'
        '<span class="stat__lbl">certificación en preparación</span></div>\n'
        "</div>\n\n"
        + hero_meta + "\n\n"
        "[:material-server-network: Ver máquinas](maquinas/facil/){ .md-button .md-button--primary }\n"
        "[:simple-hackthebox: Hack The Box](https://app.hackthebox.com/users/4011018){ .md-button }\n"
        "[:fontawesome-brands-linkedin: LinkedIn](https://www.linkedin.com/in/francisco-gutierrez-garcia){ .md-button }\n"
        "[:fontawesome-brands-github: GitHub](https://github.com/phanesopenyoureyes){ .md-button }\n\n"
        "</div>\n\n"
        # ---------- LO QUE DOMINO ----------
        "## En qué me enfoco\n\n"
        "Lo que practico en cada máquina, del reconocimiento a la escalada:\n\n"
        '<div class="grid cards" markdown>\n\n'
        + cap_cards
        + "\n</div>\n\n"
        # ---------- METODOLOGÍA ----------
        "## Metodología\n\n"
        "Cada writeup sigue el mismo recorrido y se cierra con una nota de mitigación:\n\n"
        '<div class="metodo">'
        + metodo
        + "</div>\n\n"
        # ---------- TÉCNICAS ----------
        "## Técnicas que he practicado\n\n"
        f"Las {n_tec} técnicas que aparecen en los writeups de las {n_maq} máquinas. "
        "Una muestra:\n\n"
        '<div class="tec-cloud">'
        + nube
        + "</div>\n\n"
        # ---------- DESTACADOS ----------
        "## Writeups destacados\n\n"
        "Tres writeups que resumen cómo trabajo:\n\n"
        '<div class="dest-grid">'
        + destacados_cards
        + "</div>\n\n"
        # ---------- EXPLORAR ----------
        "## Explorar\n\n"
        '<div class="grid cards" markdown>\n\n'
        + "\n".join(cards)
        + "\n</div>\n\n"
        "> Todo el contenido tiene **fines exclusivamente educativos** y se limita a "
        "máquinas **retiradas** de Hack The Box, resueltas en entornos de laboratorio "
        "autorizados.\n"
    )
    escribir("docs/index.md", index)
    cache_bust_css()
    print(f"sitio generado: {n_maq} máquinas, {n_cert} certificaciones, "
          f"{n_prep} preparaciones, {n_herr} herramientas")


def cache_bust_css():
    """Añade ?v=<hash> a extra.css en mkdocs.yml para forzar recarga al cambiar.

    Evita que los navegadores sirvan una hoja de estilos antigua con HTML nuevo
    (lo que deja las tarjetas y botones sin estilo). El hash depende del
    contenido del CSS, así que solo cambia cuando cambia el CSS.
    """
    css = "docs/stylesheets/extra.css"
    if not (os.path.exists(css) and os.path.exists("mkdocs.yml")):
        return
    h = hashlib.md5(open(css, "rb").read()).hexdigest()[:10]
    mk = open("mkdocs.yml", encoding="utf-8").read()
    nuevo = re.sub(r"(stylesheets/extra\.css)(\?v=[A-Za-z0-9]+)?", rf"\1?v={h}", mk)
    if nuevo != mk:
        open("mkdocs.yml", "w", encoding="utf-8").write(nuevo)


if __name__ == "__main__":
    main()
