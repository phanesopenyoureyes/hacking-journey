# Auditoría E0 — Calidad de los writeups

Fecha: 2026-11-07 · Rama: `auditoria-e0` (desde `main` = `c1002fb`).
Puntuación 1–5 (5 = mejor) valorando: profundidad, *porqué* de cada paso, enumeración,
escalada, mitigación y claridad.

- **Flags**: ✅ censuradas · ❌ completas en el texto.

> **Sobre la autoría de la redacción.** Los 24 writeups son tuyos: has hecho todas las
> máquinas enteras y has redactado todos los writeups. Lo que hizo Claude Code fue
> **afinar el texto** para que fuera legible y didáctico, y **añadir las notas de
> mitigación**, que se mantienen porque son parte del valor del writeup. Por eso esta
> tabla ya no clasifica los writeups por quién escribió el texto: esa clasificación era
> una lectura mía del historial de git y no recogía el trabajo real. Aclaración del autor,
> 2026-11-08.

| Máquina | Dif. | Flags | Sec. | Nota | Puntos |
| --- | --- | :-: | :-: | --- | :-: |
| validation | Fácil | ✅ | narrativa | **El mejor.** Cuenta atascos reales, intentos fallidos (SSH), distingue in-band vs blind, reflexión metodológica. No sigue la plantilla estándar. | 5 |
| optimum | Fácil | ❌ | numerada | Intento fallido documentado, alternativa con Metasploit, "concepto clave" sólido. | 5 |
| nibbles | Fácil | ❌ | numerada | Incluye fuerza bruta e inspección manual: proceso real. | 4.5 |
| buff | Fácil | ✅ | nombrada | *Pivoting* con chisel y BOF casero bien explicados; no muestra flags. La escalada la ejecutaste tú (confirmado 2026-11-08). **Pendiente**: las tres CVEs de relleno están mal atribuidas (§4.4 de `autenticidad.md`). | 4.5 |
| traverxec | Fácil | ❌ | numerada | Cadena completa (RCE → crack → clave SSH → GTFOBins). | 4.5 |
| sau | Fácil | ❌ | nombrada | SSRF+inyección encadenadas muy bien explicadas. **Pendiente**: falta el comando de lanzamiento del exploit (§4.5). | 4.5 |
| irked | Fácil | ❌ | nombrada | Rico y claro (backdoor manual, estego, path hijack). | 4.5 |
| delivery | Fácil | ❌ | nombrada | Encadenado osTicket↔Mattermost, 12 capturas. | 4.5 |
| cronos | Media | ❌ | nombrada | Única media. La escalada la ejecutaste tú (confirmado 2026-11-08) y el payload se corrige en este PR. | 4 |
| broker | Fácil | ❌ | nombrada | ActiveMQ CVE + GTFOBins nginx. | 4 |
| pilgrimage | Fácil | ❌ | nombrada | ImageMagick LFI + binwalk. Algunas capturas iniciales no venían → pasos en texto. | 4 |
| servmon | Fácil | ❌ | nombrada | Cadena larga (FTP→traversal→NVMS→NSClient). | 4 |
| bashed | Fácil | ❌ | numerada | Buena estructura, cron abuse. | 4 |
| shocker | Fácil | ❌ | numerada | Shellshock con "concepto clave". | 4 |
| knife | Fácil | ❌ | numerada | Correcto; usa heading "Notas importantes" fuera de plantilla. | 4 |
| devel | Fácil | ❌ | numerada | FTP anónimo→webshell→kernel. Correcto. | 4 |
| antique | Fácil | ❌ | nombrada | SNMP→telnet→CUPS. | 4 |
| bank | Fácil | ❌ | nombrada | vhosts→.acc→webshell .htb→SUID. | 4 |
| lame | Fácil | ❌ | numerada | Correcto; nota del *rabbit hole* vsftpd. | 3.5 |
| granny | Fácil | ✅ | numerada | Correcto; IP ofuscada (`10.129.XX.XX`) distinto al resto. | 3.5 |
| blue | Fácil | ✅ | numerada | Correcto y conciso. | 3.5 |
| legacy | Fácil | ❌ | numerada | Didáctico (rutas XP). Tag `ms17-010` listado pero se explota `ms08-067`. | 3.5 |
| grandpa | Fácil | — | numerada | `estado: pendiente`, 0 capturas. Fuera del sitio. | 3 (borrador) |
| jerry | Fácil | — | — | `estado: pendiente`, contiene literal `PENDIENTE`. Fuera del sitio. | 2 (borrador) |

## Observaciones transversales

> **Corrección en E3 (2026-11-08).** La primera versión de esta tabla tenía una columna
> «Autoría» que separaba los writeups «redactados por ti» de los «redactados por Claude».
> Se ha **eliminado**: los 24 writeups son tuyos, y esa clasificación era una lectura del
> historial de git que no recogía tu trabajo real. Lo que sí se mantiene de E3 son las
> notas de calidad: en `buff` quedan las tres CVEs mal atribuidas, en `sau` falta el
> comando del exploit y en `cronos` el payload se corrige en este PR. Detalle en
> `auditoria/autenticidad.md`.

- **Tres estilos de plantilla distintos** conviven (E4):
  - *Nombrada*: Resumen / Reconocimiento / Enumeración / Explotación / Escalada / Mitigación / Qué he aprendido (la plantilla de los writeups nuevos).
  - *Numerada*: `1. Enumeración` / `2. Explotación` / … (los writeups migrados de tus originales).
  - *Narrativa*: validation (encabezados propios).
- **Campo `dificultad` del front-matter inconsistente**: unos ponen `Easy` (blue, lame, legacy, granny, validation, nibbles, traverxec, optimum, devel…) y otros `Fácil`. La dificultad real la marca la carpeta (`facil`), así que el campo es cosmético, pero conviene unificarlo a `Fácil`.
- **Flags**: ver `informe.md` (hallazgo ALTA). 18/22 las muestran completas.
- **Relleno/afirmaciones sin sustento**: no se detecta relleno genérico grave. Punto menor:
  `legacy` lista la técnica `ms17-010` que no llega a usar (explota `ms08-067`).
