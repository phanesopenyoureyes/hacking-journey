# Máquinas de Hack The Box

Writeups de máquinas **retiradas** de Hack The Box, organizados por dificultad:
`facil/`, `media/`, `dificil/` e `insane/`. Cada máquina es una carpeta con su
writeup (`README.md`) y sus capturas en `capturas/`.

Para añadir una: `scripts/nuevo-writeup.sh <nombre> <dificultad>`. Solo se listan
abajo las máquinas publicadas; las que están en `pendiente` o `privado` no aparecen
en esta tabla ni en el sitio, aunque su carpeta exista.

La tabla se genera sola con `python scripts/generar-indice.py`. No la edites a mano.

<!-- INDICE:INICIO -->

### Fácil

| Máquina | SO | Fecha | Técnicas |
| --- | --- | --- | --- |
| [Buff](facil/buff/) | Windows | 2026-10-28 | `enumeracion-web`, `file-upload`, `rce`, `pivoting`, `chisel`, `buffer-overflow` |
| [ServMon](facil/servmon/) | Windows | 2026-10-27 | `ftp-anonimo`, `directory-traversal`, `nvms-1000`, `reutilizacion-de-credenciales`, `nsclient-abuse` |
| [Traverxec](facil/traverxec/) | Linux | 2026-10-25 | `enumeracion-web`, `rce`, `crackeo-de-hash`, `sudo-misconfig`, `gtfobins` |
| [Optimum](facil/optimum/) | Windows | 2026-10-24 | `http-file-server`, `rce`, `kernel-exploit` |
| [Devel](facil/devel/) | Windows | 2026-10-23 | `ftp-anonimo`, `carga-de-archivos`, `iis`, `kernel-exploit` |
| [Nibbles](facil/nibbles/) | Linux | 2026-10-22 | `enumeracion-web`, `fuzzing`, `carga-de-archivos`, `sudo-misconfig` |
| [Bashed](facil/bashed/) | Linux | 2026-10-21 | `enumeracion-web`, `exposicion-de-herramienta`, `sudo-misconfig`, `cron-abuse` |
| [Shocker](facil/shocker/) | Linux | 2026-10-20 | `enumeracion-web`, `fuzzing`, `shellshock`, `sudo-misconfig`, `gtfobins` |
| [Knife](facil/knife/) | Linux | 2026-10-19 | `enumeracion-web`, `php-backdoor`, `sudo-misconfig`, `gtfobins` |
| [Granny](facil/granny/) | Windows | 2026-10-18 | `iis`, `webdav`, `buffer-overflow`, `token-impersonation` |
| [Blue](facil/blue/) | Windows | 2026-10-16 | `enumeracion-smb`, `ms17-010`, `eternalblue` |
| [Legacy](facil/legacy/) | Windows | 2026-10-16 | `enumeracion-smb`, `ms08-067`, `ms17-010` |
| [Lame](facil/lame/) | Linux | 2026-10-15 | `enumeracion-smb`, `samba`, `rce` |
| [Validation](facil/validation/) | Linux | 2026-10-12 | `inyeccion-sql`, `webshell`, `reutilizacion-de-credenciales` |

<!-- INDICE:FIN -->
