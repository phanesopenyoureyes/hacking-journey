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
| [Horizontall](facil/horizontall/) | Linux | 2026-11-11 | `enumeracion-web`, `vhosts`, `strapi`, `cve`, `rce`, `pwnkit` |
| [Postman](facil/postman/) | Linux | 2026-11-08 | `redis`, `inyeccion-clave-ssh`, `crackeo-de-hash`, `webmin`, `cve` |
| [Keeper](facil/keeper/) | Linux | 2026-11-07 | `request-tracker`, `credenciales-por-defecto`, `keepass`, `cve`, `clave-ssh` |
| [Delivery](facil/delivery/) | Linux | 2026-11-06 | `osticket`, `mattermost`, `fuga-de-informacion`, `reutilizacion-de-credenciales`, `crackeo-de-hash` |
| [Broker](facil/broker/) | Linux | 2026-11-05 | `activemq`, `cve`, `rce`, `sudo-misconfig`, `gtfobins` |
| [Sau](facil/sau/) | Linux | 2026-11-04 | `ssrf`, `cve`, `inyeccion-de-comandos`, `reverse-shell`, `sudo-misconfig`, `gtfobins` |
| [Pilgrimage](facil/pilgrimage/) | Linux | 2026-11-03 | `exposicion-git`, `imagemagick`, `lectura-de-ficheros`, `cve`, `reutilizacion-de-credenciales`, `binwalk-rce` |
| [Bank](facil/bank/) | Linux | 2026-11-01 | `dns`, `vhosts`, `enumeracion-web`, `carga-de-archivos`, `suid` |
| [Antique](facil/antique/) | Linux | 2026-10-31 | `snmp`, `telnet`, `cups`, `lectura-de-ficheros`, `cve` |
| [Irked](facil/irked/) | Linux | 2026-10-30 | `enumeracion-web`, `unrealircd-backdoor`, `esteganografia`, `suid`, `path-hijacking` |
| [Buff](facil/buff/) | Windows | 2026-10-28 | `enumeracion-web`, `file-upload`, `rce`, `pivoting`, `chisel`, `buffer-overflow` |
| [ServMon](facil/servmon/) | Windows | 2026-10-27 | `ftp-anonimo`, `directory-traversal`, `nvms-1000`, `reutilizacion-de-credenciales`, `nsclient-abuse` |
| [Cap](facil/cap/) | Linux | 2026-10-26 | `idor`, `analisis-de-pcap`, `reutilizacion-de-credenciales`, `linux-capabilities` |
| [Traverxec](facil/traverxec/) | Linux | 2026-10-25 | `enumeracion-web`, `rce`, `crackeo-de-hash`, `sudo-misconfig`, `gtfobins` |
| [Optimum](facil/optimum/) | Windows | 2026-10-24 | `http-file-server`, `rce`, `kernel-exploit` |
| [Devel](facil/devel/) | Windows | 2026-10-23 | `ftp-anonimo`, `carga-de-archivos`, `iis`, `kernel-exploit` |
| [Nibbles](facil/nibbles/) | Linux | 2026-10-22 | `enumeracion-web`, `fuzzing`, `carga-de-archivos`, `sudo-misconfig` |
| [Bashed](facil/bashed/) | Linux | 2026-10-21 | `enumeracion-web`, `exposicion-de-herramienta`, `sudo-misconfig`, `cron-abuse` |
| [Shocker](facil/shocker/) | Linux | 2026-10-20 | `enumeracion-web`, `fuzzing`, `shellshock`, `sudo-misconfig`, `gtfobins` |
| [Knife](facil/knife/) | Linux | 2026-10-19 | `enumeracion-web`, `php-backdoor`, `sudo-misconfig`, `gtfobins` |
| [Granny](facil/granny/) | Windows | 2026-10-18 | `iis`, `webdav`, `buffer-overflow`, `token-impersonation` |
| [Blue](facil/blue/) | Windows | 2026-10-16 | `enumeracion-smb`, `ms17-010`, `eternalblue` |
| [Legacy](facil/legacy/) | Windows | 2026-10-16 | `enumeracion-smb`, `ms08-067` |
| [Lame](facil/lame/) | Linux | 2026-10-15 | `enumeracion-smb`, `samba`, `rce` |
| [Validation](facil/validation/) | Linux | 2026-10-12 | `inyeccion-sql`, `webshell`, `reutilizacion-de-credenciales` |

### Media

| Máquina | SO | Fecha | Técnicas |
| --- | --- | --- | --- |
| [Solid State](media/solid-state/) | Linux | 2026-11-10 | `apache-james`, `credenciales-por-defecto`, `cve`, `rce`, `pop3`, `cron-abuse` |
| [Querier](media/querier/) | Windows | 2026-11-09 | `enumeracion-smb`, `mssql`, `fuga-de-informacion`, `crackeo-de-hash`, `evasion-av`, `gpp-passwords` |
| [Cronos](media/cronos/) | Linux | 2026-11-02 | `dns`, `vhosts`, `inyeccion-sql`, `bypass-autenticacion`, `command-injection`, `cron-abuse` |

<!-- INDICE:FIN -->
