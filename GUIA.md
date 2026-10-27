# Guía para publicar (sin Claude)

Esta guía explica cómo añadir una **máquina**, una **certificación** o una
**herramienta** y que aparezca sola en la web. No hace falta Claude ni saber mucho:
la web se actualiza sola cada vez que subes algo a GitHub.

## La regla de oro

Todo funciona igual, sea lo que sea:

1. Creas una **carpeta** con un fichero **`README.md`** dentro.
2. Rellenas el texto y pones **`estado: publicado`**.
3. Lo subes a GitHub (push).
4. En 1–2 minutos aparece solo en la web. Refresca con **Ctrl + Shift + R**.

Si pones `estado: pendiente`, se guarda pero **no** sale en la web (útil para borradores).

---

## Dónde va cada cosa

| Qué subes | Carpeta |
| --- | --- |
| Máquina fácil | `maquinas/htb/facil/<nombre>/README.md` |
| Máquina media | `maquinas/htb/media/<nombre>/README.md` |
| Máquina difícil | `maquinas/htb/dificil/<nombre>/README.md` |
| Máquina insane | `maquinas/htb/insane/<nombre>/README.md` |
| Certificación | `certificaciones/<nombre>/README.md` |
| Herramienta | `herramientas/<nombre>/README.md` |

`<nombre>` en minúsculas, sin tildes ni espacios (usa guiones): `blue`, `active-directory`, `ejpt`.

Las capturas van en una subcarpeta `capturas/` al lado del `README.md`, y se enlazan así:
`![lo que muestra](capturas/nmap-puertos.png)`.

---

## Método A — Desde la web de GitHub (lo más fácil, sin instalar nada)

Ideal si no quieres usar la terminal.

1. Entra en el repo: <https://github.com/phanesopenyoureyes/hacking-journey>
2. Pulsa **Add file → Create new file** (botón arriba a la derecha).
3. En el nombre del fichero, escribe la ruta completa **incluida la carpeta**. Ejemplo
   para una máquina insane llamada «Scrambled»:
   ```
   maquinas/htb/insane/scrambled/README.md
   ```
   (al escribir las `/`, GitHub crea las carpetas solas)
4. Pega la plantilla que toque (más abajo) y rellénala. Pon `estado: publicado`.
5. Abajo, pulsa **Commit changes**.
6. Espera 1–2 minutos y refresca la web. Ya está.

**Para las capturas:** entra en la carpeta de tu máquina en GitHub, **Add file → Upload
files**, arrástralas, y nómbralas por lo que muestran. Luego en el `README.md` las
enlazas con `![descripción](capturas/nombre.png)`.

---

## Método B — Desde tu ordenador (con los scripts)

Si tienes el repo clonado, es aún más rápido porque el script crea la carpeta y la
plantilla por ti:

```bash
# Máquina (la dificultad: facil | media | dificil | insane)
scripts/nuevo-writeup.sh "Scrambled" insane

# Certificación
scripts/nueva-certificacion.sh "eJPT"

# Herramienta
scripts/nueva-herramienta.sh "mi-script"
```

Luego:

1. Abre el `README.md` que te ha creado y escribe el contenido.
2. Cambia `estado: pendiente` por `estado: publicado`.
3. Sube los cambios:
   ```bash
   git add .
   git commit -m "writeup: Scrambled"
   git push
   ```
4. En 1–2 minutos está en la web.

---

## Plantillas para copiar y pegar (Método A)

Copia el bloque entero, incluidas las líneas con `---` de arriba.

### Máquina

```markdown
---
titulo: "Nombre de la máquina"
fecha: 2026-01-01
plataforma: htb
so: linux
dificultad: Insane
estado: publicado
tecnicas: [enumeracion-web, sudo-misconfig]
herramientas: [nmap, nc]
---

# Nombre de la máquina

## Resumen

Tres líneas: qué era, por dónde entraste y cómo escalaste.

## Reconocimiento

Primeros pasos: ping, TTL, superficie de ataque.

## Enumeración

Puertos, servicios, versiones y lo que descubres.

## Explotación

El paso que funcionó y por qué.

## Escalada de privilegios

Del usuario inicial a control total.

## Mitigación

Cómo se habría evitado el fallo.

## Qué he aprendido

Dos o tres líneas honestas, incluido lo que te costó.
```

> `so:` es `linux` o `windows`. `dificultad:` es `Fácil`, `Media`, `Difícil` o `Insane`
> (debe coincidir con la carpeta). Las tres secciones **Resumen**, **Mitigación** y
> **Qué he aprendido** no pueden quedar vacías si está `publicado`.

### Certificación

```markdown
---
titulo: "Nombre de la certificación"
fecha: 2026-01-01
entidad: "Entidad que la emite"
estado: publicado
enlace: ""
temas: [redes, linux]
---

# Nombre de la certificación

## Resumen

Qué certificación es, quién la emite y qué nivel acredita.

## Qué cubre

Los temas y competencias que evalúa.

## Qué aprendí

Qué te llevas de prepararla y de obtenerla.
```

### Herramienta

```markdown
---
titulo: "Nombre de la herramienta"
fecha: 2026-01-01
tipo: "script"
estado: publicado
repo: ""
temas: [enumeracion]
---

# Nombre de la herramienta

## Qué hace

Para qué sirve y qué problema resuelve.

## Uso

Cómo se instala y se ejecuta, con un ejemplo.

## Notas

Limitaciones, ideas de mejora o cosas aprendidas.
```

---

## Cosas a recordar

- **La fecha** va en formato `AAAA-MM-DD` (ejemplo: `2026-10-27`).
- **Solo sale en la web lo que está `publicado`.** Para ocultar algo, pon `pendiente` o `privado`.
- **No publiques** contraseñas, claves o ficheros `.ovpn` tuyos, ni IPs de casa o del
  instituto. Las credenciales de la propia máquina de HTB (las que se explotan) sí se
  pueden mostrar: son parte del writeup.
- **Solo máquinas retiradas** de Hack The Box (las activas no, por sus normas).
- No tienes que tocar el menú ni el índice: se generan solos.

## Si algo no aparece

- ¿Pusiste `estado: publicado`? Es el motivo más habitual.
- ¿La carpeta está en el sitio correcto (la tabla de arriba)?
- Mira la pestaña **Actions** del repo: si el último trabajo está en rojo, ábrelo y la
  última línea roja suele decir qué falta (casi siempre un dato del bloque de arriba mal
  escrito). Arréglalo y vuelve a guardar.
- Acuérdate de refrescar con **Ctrl + Shift + R**.
