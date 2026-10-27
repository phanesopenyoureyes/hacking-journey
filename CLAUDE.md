# CLAUDE.md

Reglas de trabajo para agentes en `hacking-journey`. Se aplican en todas las sesiones.

## Qué es este repo

Writeups propios de máquinas **retiradas** de Hack The Box, en español, que se están
convirtiendo en portfolio. El lector objetivo (tutor de FCT o responsable técnico) mira
el repo cinco minutos: tiene que ver qué sé hacer, dónde está la prueba y que escribo
de forma ordenada.

Estado actual: 14 writeups en `HTB/machines/easy/<Maquina>/README.md`, cada uno con
sus capturas al lado. El plan de reorganización está en fases (0 a 6); cada fase se
pide en una sesión distinta y termina en un commit revisable.

## Git

- Trabajar en la rama `portfolio-refactor`. Un commit por fase, con mensaje descriptivo
  en español.
- Nunca `push --force` sobre `main`. No reescribir el historial (nada de rebase, amend
  sobre commits publicados ni `filter-repo`).
- Mover o renombrar siempre con `git mv`, nunca con `rm`. Antes de mover nada, listar
  en pantalla `origen → destino` y esperar confirmación.
- Los movimientos de ficheros van en un commit aparte de los cambios de contenido, para
  que el diff se lea bien.

## Contenido

- No inventar contenido técnico. Si falta información de una máquina, poner
  `PENDIENTE` y avisar; no redactar pasos que no estén documentados.
- Al migrar writeups antiguos se conserva literalmente el texto que ya escribí: se
  reordena y se completan metadatos, no se reescribe.
- Nada de material del eJPT ni de otra formación de pago: ni copiado ni parafraseado.
  Solo apuntes propios y referencias.
- Las prácticas del ciclo (ISO y demás módulos) no van en este repo. Si aparecen,
  listarlas para moverlas a su propio repo; nunca borrarlas.

## Lo que nunca se publica

- Credenciales: contraseñas, hashes, claves SSH o privadas, ficheros `.ovpn`, tokens.
- IPs internas del instituto, de casa (`192.168.x.x`) o la IP pública propia, y
  nombres o datos de compañeros y profesores.

Las IPs del laboratorio de HTB (`10.129.x.x`, `10.10.10.x` y la propia de la VPN,
`10.10.14-16.x`) **sí se pueden publicar**: son privadas, solo se alcanzan desde la VPN
de HTB y se reasignan entre usuarios. Es lo habitual en cualquier writeup.

Las credenciales que forman parte de la propia máquina (la contraseña por defecto que
se explota, el hash que se crackea) son contenido del writeup y se pueden mostrar.
Lo que nunca se publica son credenciales propias.
- Writeups de máquinas **activas** de HTB: se marcan `estado: privado` y se excluyen
  del índice y del sitio.

Si se encuentra un secreto ya commiteado en el historial: **parar todo y avisar** antes
de tocar nada.

## Licencias

- Textos y writeups: **CC BY 4.0**.
- Código (`scripts/` y demás utilidades): **Apache 2.0**.

## Convenciones (a partir de la fase 1)

- Carpetas y ficheros en `kebab-case`, sin acentos, espacios ni mayúsculas.
- Un writeup es una carpeta: `maquinas/htb/<nombre-maquina>/README.md` + `capturas/`.
- Fechas en formato `AAAA-MM-DD`.
- Capturas en `.png` optimizado o `.webp`, nombradas por lo que muestran
  (`nmap-puertos.png`, no `Captura1.png`).

## Tareas rutinarias

Casi todo lo que se pide es una de estas cosas:

| Petición | Qué hacer |
| --- | --- |
| Añadir un writeup | `scripts/nuevo-writeup.sh <nombre> htb` crea la carpeta con la plantilla. Rellenar el front-matter y pedir al autor el texto técnico; no redactarlo por él. |
| Publicar los cambios | Pasar el validador y el comprobador de enlaces, commit, push, y comprobar que el workflow de Pages acaba en verde. |
| Actualizar el índice | `python scripts/generar-indice.py`. Nunca editar a mano las tablas entre los marcadores. |
| Cambiar el aspecto del sitio | Solo `mkdocs.yml`. No tocar las plantillas del tema. |
| Actualizar dependencias | Solo si lo pide el autor: fijar la versión nueva en `requirements.txt`, probar en local y decir qué cambia. Las versiones están fijadas a propósito. |

## Cuando algo se rompe

El fallo casi siempre está en el contenido, no en la infraestructura. Antes de tocar
configuración, reproducir en local con `mkdocs build --strict` y leer la primera línea
del error, que suele señalar fichero y línea.

Prohibido:

- «Arreglar» un fallo desactivando comprobaciones (`--no-verify`, quitar `--strict`) o
  borrando ficheros que molestan.
- Cambiar la versión de una dependencia para esquivar un error sin decirlo.
- Hacer un cambio estructural sin explicarlo antes y esperar confirmación.

Al terminar cualquier tarea, dejar escrito en una línea qué se cambió y por qué.
