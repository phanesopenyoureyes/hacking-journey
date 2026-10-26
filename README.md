<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0b1a,45:2e1065,100:8b5cf6&height=220&section=header&text=HACK%20THE%20BOX%20WRITEUPS&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Documentaci%C3%B3n%20t%C3%A9cnica%20de%20m%C3%A1quinas%20resueltas%20%C2%B7%20ph4n3s&descSize=18&descAlignY=60&animation=fadeIn" alt="Hack The Box Writeups" width="100%"/>

<br>

[![HTB](https://img.shields.io/badge/Hack_The_Box-1a1033?style=for-the-badge&logo=hackthebox&logoColor=a78bfa)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-5b21b6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

![Writeups](https://img.shields.io/badge/Writeups-14-a78bfa?style=flat-square&labelColor=1a1033)
![Estado](https://img.shields.io/badge/Estado-Activo-8b5cf6?style=flat-square&labelColor=1a1033)
![Uso](https://img.shields.io/badge/Uso-Educativo-6d28d9?style=flat-square&labelColor=1a1033)

**[Writeups](#writeups)** · **[Competencias](#competencias-trabajadas)** · **[Aviso legal](#aviso-legal)** · **[Contacto](#contacto)**

</div>

---

## Sobre este repositorio

Colección de writeups de Hack The Box que documenta mi formación en ciberseguridad ofensiva. Cada writeup recoge el proceso completo: enumeración, explotación, escalada de privilegios y lecciones aprendidas, con especial atención a cómo se mitiga cada vulnerabilidad.

---

## Metodología

Todos los writeups siguen el mismo flujo de trabajo:

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#2e1065','primaryTextColor':'#ede9fe','primaryBorderColor':'#8b5cf6','lineColor':'#a78bfa','secondaryColor':'#1a1033','tertiaryColor':'#0d0b1a','fontFamily':'ui-sans-serif,system-ui'}}}%%
flowchart LR
    A[Reconocimiento] --> B[Enumeración]
    B --> C[Explotación]
    C --> D[Acceso inicial]
    D --> E[Escalada de privilegios]
    E --> F[Obtención de flags]
    F --> G[Lecciones aprendidas]
```

---

## Writeups

**14 máquinas completadas** · 7 Linux · 7 Windows · 14 de dificultad Easy

| Máquina | Sistema | Dificultad | Técnicas principales | Writeup |
|:--|:-:|:-:|:--|:-:|
| **Bashed** | Linux | Easy | `Fuzzing web` · `Webshell expuesta` · `Sudo mal configurado` | [Leer](./HTB/Bashed) |
| **Blue** | Windows | Easy | `SMB` · `MS17-010 (EternalBlue)` | [Leer](./HTB/Blue) |
| **Devel** | Windows | Easy | `FTP anónimo` · `Subida de ASPX` · `Kernel exploit` | [Leer](./HTB/Devel) |
| **Grandpa** | Windows | Easy | `IIS 6.0 WebDAV` · `CVE-2017-7269` · `Token impersonation` | [Leer](./HTB/Grandpa) |
| **Granny** | Windows | Easy | `IIS 6.0 WebDAV` · `Subida de ficheros` · `Token impersonation` | [Leer](./HTB/Granny) |
| **Jerry** | Windows | Easy | `Apache Tomcat` · `Credenciales por defecto` · `WAR malicioso` | [Leer](./HTB/Jerry) |
| **knife** | Linux | Easy | `PHP 8.1.0-dev backdoor` · `Sudo (knife)` | [Leer](./HTB/knife) |
| **Lame** | Linux | Easy | `Samba` · `CVE-2007-2447` | [Leer](./HTB/Lame) |
| **Legacy** | Windows | Easy | `SMB` · `MS08-067 / MS17-010` | [Leer](./HTB/Legacy) |
| **Nibbles** | Linux | Easy | `Nibbleblog` · `CVE-2015-6967` · `Sudo + script editable` | [Leer](./HTB/Nibbles) |
| **Optimum** | Windows | Easy | `HttpFileServer 2.3` · `CVE-2014-6287` · `Kernel exploit` | [Leer](./HTB/Optimum) |
| **Shocker** | Linux | Easy | `CGI` · `Shellshock` · `Sudo (perl)` | [Leer](./HTB/Shocker) |
| **Traverxec** | Linux | Easy | `Nostromo` · `CVE-2019-16278` · `Clave SSH` · `journalctl` | [Leer](./HTB/Traverxec) |
| **Validation** | Linux | Easy | `SQLi` · `Inyección de comandos` | [Leer](./HTB/Validation) |

<sub>La tabla se actualiza con cada nueva máquina completada.</sub>

---

## Competencias trabajadas

- Enumeración de servicios y reconocimiento de superficie de ataque (SMB, FTP, HTTP, WebDAV).
- Identificación y análisis de vulnerabilidades conocidas mediante su CVE.
- Escalada de privilegios en Linux (configuraciones de `sudo`) y en Windows (token impersonation, exploits de kernel).
- Revisión de configuraciones inseguras: credenciales por defecto, servicios expuestos y permisos excesivos.
- Documentación técnica estructurada, con medidas de mitigación en cada caso.

---

## Estructura de cada writeup

<details>
<summary><b>Ver el formato estándar</b></summary>

<br>

1. **Resumen**: visión general de la máquina y del camino seguido.
2. **Enumeración**: qué se descubrió y cómo.
3. **Explotación**: acceso inicial, paso a paso.
4. **Escalada de privilegios**: del usuario al control total.
5. **Lecciones aprendidas**: conclusiones y medidas de mitigación.
6. **Referencias**: recursos consultados.

</details>

---

## Aviso legal

> [!WARNING]
> Todo el contenido de este repositorio tiene **fines exclusivamente educativos**.
>
> - Solo se publican writeups de **máquinas retiradas** de Hack The Box, conforme a sus normas.
> - Las técnicas se aplican únicamente en **entornos autorizados**.
> - El autor no se responsabiliza del uso indebido de esta información.
>
> Atacar sistemas sin autorización es ilegal.

---

## Contacto

<div align="center">

[![HTB](https://img.shields.io/badge/Hack_The_Box-Perfil-1a1033?style=for-the-badge&logo=hackthebox&logoColor=a78bfa)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Contacto-5b21b6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

</div>

---

<div align="center">

Si el contenido le resulta útil, puede valorar el repositorio con una estrella.

<sub>Autor: Francisco Gutiérrez García (ph4n3s)</sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0b1a,45:2e1065,100:8b5cf6&height=100&section=footer" width="100%" alt=""/>

</div>
