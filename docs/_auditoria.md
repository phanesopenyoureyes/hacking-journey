# Auditoría del repo (fase 0)

Fecha: 2026-10-27. Rama: `portfolio-refactor`, desde `main` (`2f356bc`).
Auditoría de solo lectura: este fichero es lo único que se añade en esta fase.

## Inventario

| Concepto | Valor |
| --- | --- |
| Carpetas con contenido | `HTB/machines/easy/<Maquina>/` (14 máquinas) |
| Ficheros `.md` | 16 (14 writeups, `README.md` raíz, `CLAUDE.md`) |
| Imágenes `.png` | 29 |
| Scripts / binarios | 0 / 0 |
| Peso del árbol | 15,5 MB (casi todo imágenes) |
| Peso del historial (`.git`) | 15,2 MB |
| Ficheros de más de 1 MB | 4 (ver abajo) |

Ficheros de más de 1 MB, todos capturas a resolución de pantalla completa:

| Fichero | Tamaño |
| --- | --- |
| `Optimum/optimum-04-preparando-privesc.png` | 2,6 MB |
| `Traverxec/traverxec-06-enumeracion-david.png` | 2,6 MB |
| `Traverxec/traverxec-05-john-passphrase.png` | 2,2 MB |
| `Nibbles/nibbles-02-ffuf-general.png` | 2,1 MB |

## Writeups

| Máquina | SO | Fecha | Capturas | Secciones actuales |
| --- | --- | --- | --- | --- |
| Bashed | Linux | 2026-10-21 | 2 | Enumeración, Fuzzing, Escalada, Resumen rápido |
| Blue | Windows | 2026-10-16* | 0 | Enumeración, Explotación, Post-explotación, Conclusión |
| Devel | Windows | 2026-10-23 | 1 | Enumeración, Explotación, Escalada, Post-explotación, Resumen rápido |
| Grandpa | Windows | 2026-10-19* | 0 | Ficha, Enumeración, Explotación, Post-explotación (sin título H1) |
| Granny | Windows | 2026-10-18* | 0 | Enumeración, Explotación, Escalada, Post-explotación, Conclusión |
| Jerry | Windows | 2026-10-14 | 0 | Índice, Reconocimiento, Enumeración, Explotación, Postexplotación |
| Knife | Linux | 2026-10-19 | 6 | Enumeración, Explotación, Notas de aprendizaje, Resumen rápido |
| Lame | Linux | 2026-10-15* | 0 | Enumeración, Análisis, Explotación, Post-explotación, Conclusiones |
| Legacy | Windows | 2026-10-16* | 0 | Enumeración, Explotación, Post-explotación, Conclusión |
| Nibbles | Linux | 2026-10-22 | 8 | Enumeración, Fuzzing, Fuerza bruta, Revisión web, Explotación, Post-explotación, Resumen rápido |
| Optimum | Windows | 2026-10-24 | 5 | Enumeración, Explotación, Escalada, Alternativa Metasploit, Resumen rápido |
| Shocker | Linux | 2026-10-20 | 1 | Enumeración, Explotación, Resumen rápido |
| Traverxec | Linux | 2026-10-25 | 6 | Enumeración, Explotación, www-data → david, david → root, Resumen rápido |
| Validation | Linux | 2026-10-12* | 0 | Narrativa por pasos, Flags, Lo que me llevo |

\* Sin fecha en el texto: se toma la del primer commit del fichero.

Estructura de facto: casi todos siguen Enumeración → Explotación → Escalada/Post-explotación
y cierran con «Resumen rápido» o «Conclusión». Ninguno tiene metadatos (front-matter).

**Ningún writeup tiene sección de Mitigación**, aunque el README raíz dice que todos
cierran con una nota de mitigación. Es el hueco más importante del repo.

## Nombres problemáticos

- Mayúsculas en todas las carpetas: `HTB/`, `HTB/machines/easy/Knife/`, etc.
- Capturas sin prefijo en Knife y Shocker (`01-pagina-web.png` existe en las dos).
- Sin espacios ni acentos en ningún nombre.

## Enlaces e imágenes

- Enlaces rotos: ninguno. Todas las imágenes referenciadas existen.
- Imágenes sin usar: ninguna.
- Duplicados (mismo contenido en dos sitios): ninguno.
- Problema de formato: en `Lame/README.md` hay líneas `# usuario: anonymous` y
  `# password: (enter)` fuera de un bloque de código, que se renderizan como títulos H1.

## Secretos

No se pudo ejecutar `gitleaks` ni `trufflehog` en este entorno (no se permite descargar
binarios). Se usó `detect-secrets` sobre el árbol y una búsqueda de patrones en todo el
historial (`git log --all -p`): claves privadas, `.ovpn`, tokens de GitHub, AWS y Slack.
`gitleaks` queda configurado para ejecutarse en CI (fase 6).

Resultado:

- **Ningún secreto propio** en el árbol ni en el historial: ni `.ovpn`, ni claves, ni
  tokens, ni IPs de casa o del instituto.
- Sí hay **credenciales de las propias máquinas**, que son parte del writeup:
  `uhc-9qual-global-pw` (Validation), `s3cret` (Jerry), el hash `.htpasswd` de `david`
  y la passphrase `hunter` (Traverxec). Según `CLAUDE.md` se pueden publicar.
- Hay **flags** (`user.txt` / `root.txt`) en Bashed, Grandpa, Jerry y Nibbles.
- IPs: solo de HTB (`10.129.x.x`, `10.10.10.x`), de la VPN propia (`10.10.15-16.x`) y
  `127.0.0.1`.
- Capturas: ninguna tiene EXIF. Solo llevan los bloques PNG `sRGB`, `gAMA` y `pHYs`.

## Decisiones

Las decisiones que dependían del autor se han tomado así, por indicación suya de no
preguntar y aplicar el criterio más conservador:

| Decisión | Qué se ha hecho |
| --- | --- |
| Qué queda privado | Nada: las 14 máquinas están retiradas. |
| Writeups sin Mitigación | `estado: pendiente` hasta que el autor la escriba. Se excluyen del índice público y del sitio. La sección queda con `PENDIENTE`, no se redacta por él. |
| Resumen y «Qué he aprendido» | Se rellenan con el «Resumen rápido» / «Conclusión» / «Lo que me llevo» que ya existían. Si no hay, `PENDIENTE`. |
| Flags en el texto | Se mantienen. En HTB las flags cambian en cada despliegue, pero conviene quitarlas: no aportan nada al lector. |
| Credenciales de las máquinas | Se mantienen como contenido del writeup. |
| Carpetas de clase | No hay ninguna. |
| Qué se borra o se fusiona | Nada. |
| Capturas grandes | Se recomprimen sin pérdida en la fase 4. |
