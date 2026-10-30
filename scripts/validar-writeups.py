#!/usr/bin/env python3
"""Valida el contenido de maquinas/, certificaciones/ y herramientas/.

Comprueba el front-matter completo y las secciones obligatorias de cada tipo, y
falla (código 1) indicando fichero, campo o sección que falta. El contenido con
estado distinto de 'publicado' solo se valida a nivel de metadatos, porque es
borrador excluido del sitio.
"""
import glob
import re
import sys
import unicodedata

ESTADOS = {"publicado", "privado", "pendiente"}
DIFICULTADES = {"facil", "media", "dificil", "insane"}

# tipo -> (patrón glob, campos de front-matter, secciones H2 obligatorias)
TIPOS = {
    "maquina": (
        "maquinas/htb/*/*/README.md",
        ["titulo", "fecha", "plataforma", "so", "dificultad", "estado", "tecnicas", "herramientas"],
        ["resumen", "mitigacion", "que he aprendido"],
    ),
    "certificacion": (
        "certificaciones/*/README.md",
        ["titulo", "fecha", "entidad", "estado", "temas"],
        ["resumen", "que aprendi"],
    ),
    "herramienta": (
        "herramientas/*/README.md",
        ["titulo", "fecha", "tipo", "estado", "temas"],
        ["que hace", "uso"],
    ),
    "preparacion": (
        "preparacion/*/README.md",
        ["titulo", "fecha", "entidad", "estado", "temas"],
        ["resumen", "recursos"],
    ),
}


def pelar(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def partes(texto):
    if not texto.startswith("---"):
        return None, texto
    fin = texto.find("\n---", 3)
    if fin == -1:
        return None, texto
    return texto[3:fin].strip(), texto[fin + 4 :]


def parse_fm(bloque):
    datos = {}
    for linea in bloque.split("\n"):
        if linea.strip().startswith("#"):
            continue
        linea = linea.split("  #")[0].rstrip()
        m = re.match(r"([a-z_]+):\s*(.*)", linea)
        if m:
            datos[m.group(1)] = m.group(2).strip()
    return datos


def h2(cuerpo):
    fuera, out = True, []
    for linea in cuerpo.split("\n"):
        if linea.startswith("```"):
            fuera = not fuera
        if fuera and re.match(r"##\s+", linea):
            out.append(pelar(linea[2:]))
    return out


def seccion_pendiente(cuerpo, titulo):
    ms = list(re.finditer(r"^##\s+(.*)$", cuerpo, re.M))
    for i, m in enumerate(ms):
        if titulo in pelar(m.group(1)):
            ini = m.end()
            fin = ms[i + 1].start() if i + 1 < len(ms) else len(cuerpo)
            return "PENDIENTE" in cuerpo[ini:fin]
    return False


def main():
    errores = []
    total = 0
    for tipo, (patron, campos, secciones) in TIPOS.items():
        for f in sorted(glob.glob(patron)):
            total += 1
            texto = open(f, encoding="utf-8").read()
            bloque, cuerpo = partes(texto)
            if bloque is None:
                errores.append(f"{f}: falta el front-matter YAML")
                continue
            fm = parse_fm(bloque)
            for c in campos:
                if c not in fm or fm[c] == "":
                    errores.append(f"{f}: falta el campo '{c}' en el front-matter")
            estado = fm.get("estado", "")
            if estado and estado not in ESTADOS:
                errores.append(f"{f}: estado '{estado}' no válido (publicado|privado|pendiente)")
            if "fecha" in fm and not re.match(r"\d{4}-\d{2}-\d{2}", fm["fecha"]):
                errores.append(f"{f}: fecha '{fm['fecha']}' no está en formato AAAA-MM-DD")
            if tipo == "maquina":
                dif = f.split("/")[2]
                if dif not in DIFICULTADES:
                    errores.append(f"{f}: dificultad de carpeta '{dif}' no válida (facil|media|dificil|insane)")
            secs = h2(cuerpo)
            for s in secciones:
                if not any(s in h for h in secs):
                    errores.append(f"{f}: falta la sección obligatoria '## {s}'")
            if estado == "publicado":
                for s in secciones:
                    if seccion_pendiente(cuerpo, s):
                        errores.append(f"{f}: la sección '{s}' está PENDIENTE pero es 'publicado'")
    if errores:
        print(f"Validación FALLIDA — {len(errores)} problema(s):\n")
        for e in errores:
            print("  -", e)
        return 1
    print(f"Validación OK — {total} elementos correctos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
