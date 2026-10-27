# Máquinas de Hack The Box

Writeups de máquinas **retiradas** de Hack The Box, organizados por máquina. Cada
carpeta contiene el writeup (`README.md`) y sus capturas en `capturas/`.

Solo se listan aquí las máquinas publicadas. Las que están en estado `pendiente`
(les falta la nota de mitigación o de aprendizaje) o `privado` no aparecen en esta
tabla ni en el sitio web, aunque su carpeta exista en el repositorio.

La tabla se genera sola con `python scripts/generar-indice.py`. No la edites a mano.

<!-- INDICE:INICIO -->

| Máquina | SO | Dificultad | Fecha | Técnicas |
| --- | --- | --- | --- | --- |
| [Traverxec](traverxec/) | Linux | Easy | 2026-10-25 | `enumeracion-web`, `rce`, `crackeo-de-hash`, `sudo-misconfig`, `gtfobins` |
| [Optimum](optimum/) | Windows | Easy | 2026-10-24 | `http-file-server`, `rce`, `kernel-exploit` |
| [Devel](devel/) | Windows | Easy | 2026-10-23 | `ftp-anonimo`, `carga-de-archivos`, `iis`, `kernel-exploit` |
| [Nibbles](nibbles/) | Linux | Easy | 2026-10-22 | `enumeracion-web`, `fuzzing`, `carga-de-archivos`, `sudo-misconfig` |
| [Bashed](bashed/) | Linux | Easy | 2026-10-21 | `enumeracion-web`, `exposicion-de-herramienta`, `sudo-misconfig`, `cron-abuse` |
| [Shocker](shocker/) | Linux | Easy | 2026-10-20 | `enumeracion-web`, `fuzzing`, `shellshock`, `sudo-misconfig`, `gtfobins` |
| [Knife](knife/) | Linux | Easy | 2026-10-19 | `enumeracion-web`, `php-backdoor`, `sudo-misconfig`, `gtfobins` |
| [Granny](granny/) | Windows | Easy | 2026-10-18 | `iis`, `webdav`, `buffer-overflow`, `token-impersonation` |
| [Blue](blue/) | Windows | Easy | 2026-10-16 | `enumeracion-smb`, `ms17-010`, `eternalblue` |
| [Legacy](legacy/) | Windows | Easy | 2026-10-16 | `enumeracion-smb`, `ms08-067`, `ms17-010` |
| [Lame](lame/) | Linux | Easy | 2026-10-15 | `enumeracion-smb`, `samba`, `rce` |
| [Validation](validation/) | Linux | Easy | 2026-10-12 | `inyeccion-sql`, `webshell`, `reutilizacion-de-credenciales` |

<!-- INDICE:FIN -->
