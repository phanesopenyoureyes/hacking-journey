# Auditoría E0 — Calidad de los writeups

Fecha: 2026-11-07 · Rama: `auditoria-e0` (desde `main` = `c1002fb`).
Puntuación 1–5 (5 = mejor) valorando: profundidad, *porqué* de cada paso, enumeración,
escalada, mitigación y claridad. "Autoría" indica de quién es la redacción (importante para
las reglas 2 y 3: los writeups deben reflejar **tu** proceso).

- **Autor** = redacción tuya (migrada de tus writeups previos; tu voz en primera persona).
- **Claude (de tus notas)** = ensamblado por Claude Code en sesiones de este chat a partir de
  tus notas/capturas. El texto técnico viene de tu material, pero **la redacción, el *Resumen*,
  la *Mitigación* y el *Qué he aprendido* son de Claude**, no tuyos → conviene que los revises
  y los hagas tuyos (E3).
- **Flags**: ✅ censuradas · ❌ completas en el texto.

| Máquina | Dif. | Autoría | Flags | Sec. | Nota | Puntos |
| --- | --- | --- | :-: | :-: | --- | :-: |
| validation | Fácil | Autor | ✅ | narrativa | **El mejor.** Cuenta atascos reales, intentos fallidos (SSH), distingue in-band vs blind, reflexión metodológica. No sigue la plantilla estándar. | 5 |
| optimum | Fácil | Autor | ❌ | numerada | Intento fallido documentado, alternativa con Metasploit, "concepto clave" sólido. | 5 |
| nibbles | Fácil | Autor | ❌ | numerada | Incluye fuerza bruta e inspección manual: proceso real. | 4.5 |
| buff | Fácil | Claude (de tus notas) | ✅ | nombrada | *Pivoting* con chisel y BOF casero bien explicados; no muestra flags. **E3: corregido** — no hay original tuyo en el historial y la escalada la completé yo «con el método conocido de la máquina». | 4.5 |
| traverxec | Fácil | Autor | ❌ | numerada | Cadena completa (RCE → crack → clave SSH → GTFOBins). | 4.5 |
| sau | Fácil | Claude (de tus notas) | ❌ | nombrada | SSRF+inyección encadenadas muy bien explicadas. Revisa que es tu proceso. | 4.5 |
| irked | Fácil | Claude (de tus notas) | ❌ | nombrada | Rico y claro (backdoor manual, estego, path hijack). | 4.5 |
| delivery | Fácil | Claude (de tus notas) | ❌ | nombrada | Encadenado osTicket↔Mattermost, 12 capturas. Redacción de Claude: revísala. | 4.5 |
| cronos | Media | Claude (de tus notas) | ❌ | nombrada | Única media. Escalada **completada por Claude desde capturas** (las notas se cortaban). Verifica el payload exacto. | 4 |
| broker | Fácil | Claude (de tus notas) | ❌ | nombrada | ActiveMQ CVE + GTFOBins nginx. | 4 |
| pilgrimage | Fácil | Claude (de tus notas) | ❌ | nombrada | ImageMagick LFI + binwalk. Algunas capturas iniciales no venían → pasos en texto. | 4 |
| servmon | Fácil | Claude (de tus notas) | ❌ | nombrada | Cadena larga (FTP→traversal→NVMS→NSClient). | 4 |
| bashed | Fácil | Autor | ❌ | numerada | Buena estructura, cron abuse. | 4 |
| shocker | Fácil | Autor | ❌ | numerada | Shellshock con "concepto clave". | 4 |
| knife | Fácil | Autor | ❌ | numerada | Correcto; usa heading "Notas importantes" fuera de plantilla. | 4 |
| devel | Fácil | Autor | ❌ | numerada | FTP anónimo→webshell→kernel. Correcto. | 4 |
| antique | Fácil | Claude (de tus notas) | ❌ | nombrada | SNMP→telnet→CUPS. | 4 |
| bank | Fácil | Claude (de tus notas) | ❌ | nombrada | vhosts→.acc→webshell .htb→SUID. | 4 |
| lame | Fácil | Autor | ❌ | numerada | Correcto; nota del *rabbit hole* vsftpd. | 3.5 |
| granny | Fácil | Autor | ✅ | numerada | Correcto; IP ofuscada (`10.129.XX.XX`) distinto al resto. | 3.5 |
| blue | Fácil | Autor | ✅ | numerada | Correcto y conciso. | 3.5 |
| legacy | Fácil | Autor | ❌ | numerada | Didáctico (rutas XP). Tag `ms17-010` listado pero se explota `ms08-067`. | 3.5 |
| grandpa | Fácil | — | — | numerada | `estado: pendiente`, 0 capturas. Fuera del sitio. | 3 (borrador) |
| jerry | Fácil | — | — | — | `estado: pendiente`, contiene literal `PENDIENTE`. Fuera del sitio. | 2 (borrador) |

## Observaciones transversales

> **Corrección en E3 (2026-11-07).** La columna «Autoría» de esta tabla se corrigió para
> **buff**: figuraba como «Autor», pero la comprobación del historial de git en E3 no
> encuentra ningún original suyo para esa máquina, y el commit que la creó (`9457753`)
> declara que el final de la escalada lo completé yo. El resto de la tabla se mantiene.
> Detalle en `auditoria/autenticidad.md`.

- **Tres estilos de plantilla distintos** conviven (E4):
  - *Nombrada*: Resumen / Reconocimiento / Enumeración / Explotación / Escalada / Mitigación / Qué he aprendido (los ensamblados por Claude + buff).
  - *Numerada*: `1. Enumeración` / `2. Explotación` / … (los tuyos migrados).
  - *Narrativa*: validation (encabezados propios).
- **Campo `dificultad` del front-matter inconsistente**: unos ponen `Easy` (blue, lame, legacy, granny, validation, nibbles, traverxec, optimum, devel…) y otros `Fácil`. La dificultad real la marca la carpeta (`facil`), así que el campo es cosmético, pero conviene unificarlo a `Fácil`.
- **Flags**: ver `informe.md` (hallazgo ALTA). 18/22 las muestran completas.
- **Relleno/afirmaciones sin sustento**: no se detecta relleno genérico grave. Punto menor:
  `legacy` lista la técnica `ms17-010` que no llega a usar (explota `ms08-067`).
