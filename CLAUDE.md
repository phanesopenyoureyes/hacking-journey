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
- IPs internas del instituto y nombres o datos de compañeros y profesores.
- Writeups de máquinas **activas** de HTB: se marcan `estado: privado` y se excluyen
  del índice y del sitio.

Si se encuentra un secreto ya commiteado en el historial: **parar todo y avisar** antes
de tocar nada.

## Convenciones (a partir de la fase 1)

- Carpetas y ficheros en `kebab-case`, sin acentos, espacios ni mayúsculas.
- Un writeup es una carpeta: `maquinas/htb/<nombre-maquina>/README.md` + `capturas/`.
- Fechas en formato `AAAA-MM-DD`.
- Capturas en `.png` optimizado o `.webp`, nombradas por lo que muestran
  (`nmap-puertos.png`, no `Captura1.png`).
