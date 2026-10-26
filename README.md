<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0b1a,45:2e1065,100:8b5cf6&height=220&section=header&text=HACKING%20JOURNEY&fontSize=55&fontColor=ffffff&fontAlignY=38&desc=Writeups%20de%20Hack%20The%20Box%20%C2%B7%20by%20ph4n3s&descSize=18&descAlignY=60&animation=fadeIn" alt="Hacking Journey" width="100%"/>

<br>

[![HTB](https://img.shields.io/badge/Hack_The_Box-1a1033?style=for-the-badge&logo=hackthebox&logoColor=a78bfa)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-5b21b6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

![Writeups](https://img.shields.io/badge/Writeups-14-a78bfa?style=flat-square&labelColor=1a1033)
![Estado](https://img.shields.io/badge/Estado-Activo-8b5cf6?style=flat-square&labelColor=1a1033)
![Uso](https://img.shields.io/badge/Uso-Educativo-6d28d9?style=flat-square&labelColor=1a1033)

**[📚 Writeups](#-writeups)** · **[📫 Contacto](#-contacto)**

</div>

---

## 👁️ Sobre este repositorio

Colección de **writeups de Hack The Box** documentando mi aprendizaje en ciberseguridad ofensiva. Cada writeup recoge el proceso completo: enumeración, explotación, escalada de privilegios y las lecciones aprendidas.

---

## 🧭 Metodología

Todos los writeups siguen el mismo flujo de trabajo:

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#2e1065','primaryTextColor':'#ede9fe','primaryBorderColor':'#8b5cf6','lineColor':'#a78bfa','secondaryColor':'#1a1033','tertiaryColor':'#0d0b1a','fontFamily':'ui-sans-serif,system-ui'}}}%%
flowchart LR
    A[🔍 Reconocimiento] --> B[📡 Enumeración]
    B --> C[💥 Explotación]
    C --> D[🚪 Acceso inicial]
    D --> E[⬆️ Escalada de privilegios]
    E --> F[🏁 Flags]
    F --> G[📝 Lecciones aprendidas]
```

---

## 📚 Writeups

> 🟢 Easy · 🟡 Medium · 🟠 Hard · 🔴 Insane

**14 máquinas completadas** · 🐧 7 Linux · 🪟 7 Windows · 🟢 14 Easy

| Máquina | SO | Dificultad | Técnicas principales | Writeup |
|:--|:-:|:-:|:--|:-:|
| **Bashed** | 🐧 Linux | 🟢 Easy | `Fuzzing web` · `Webshell expuesta` · `Sudo mal configurado` | [📖 Leer](./HTB/Bashed) |
| **Blue** | 🪟 Windows | 🟢 Easy | `SMB` · `MS17-010 (EternalBlue)` | [📖 Leer](./HTB/Blue) |
| **Devel** | 🪟 Windows | 🟢 Easy | `FTP anónimo` · `Subida de ASPX` · `Kernel exploit` | [📖 Leer](./HTB/Devel) |
| **Grandpa** | 🪟 Windows | 🟢 Easy | `IIS 6.0 WebDAV` · `CVE-2017-7269` · `Token impersonation` | [📖 Leer](./HTB/Grandpa) |
| **Granny** | 🪟 Windows | 🟢 Easy | `IIS 6.0 WebDAV` · `Subida de ficheros` · `Token impersonation` | [📖 Leer](./HTB/Granny) |
| **Jerry** | 🪟 Windows | 🟢 Easy | `Apache Tomcat` · `Credenciales por defecto` · `WAR malicioso` | [📖 Leer](./HTB/Jerry) |
| **knife** | 🐧 Linux | 🟢 Easy | `PHP 8.1.0-dev backdoor` · `Sudo (knife)` | [📖 Leer](./HTB/knife) |
| **Lame** | 🐧 Linux | 🟢 Easy | `Samba` · `CVE-2007-2447` | [📖 Leer](./HTB/Lame) |
| **Legacy** | 🪟 Windows | 🟢 Easy | `SMB` · `MS08-067 / MS17-010` | [📖 Leer](./HTB/Legacy) |
| **Nibbles** | 🐧 Linux | 🟢 Easy | `Nibbleblog` · `CVE-2015-6967` · `Sudo + script editable` | [📖 Leer](./HTB/Nibbles) |
| **Optimum** | 🪟 Windows | 🟢 Easy | `HttpFileServer 2.3` · `CVE-2014-6287` · `Kernel exploit` | [📖 Leer](./HTB/Optimum) |
| **Shocker** | 🐧 Linux | 🟢 Easy | `CGI` · `Shellshock` · `Sudo (perl)` | [📖 Leer](./HTB/Shocker) |
| **Traverxec** | 🐧 Linux | 🟢 Easy | `Nostromo` · `CVE-2019-16278` · `Clave SSH` · `journalctl` | [📖 Leer](./HTB/Traverxec) |
| **Validation** | 🐧 Linux | 🟢 Easy | `SQLi` · `Inyección de comandos` | [📖 Leer](./HTB/Validation) |

<sub>➕ La tabla se actualiza con cada nueva máquina completada.</sub>

---

## 🧩 Estructura de cada writeup

<details>
<summary><b>Pulsa para ver el formato estándar</b></summary>

<br>

1. **Resumen** · Visión general de la máquina y del camino seguido.
2. **Enumeración** · Qué se descubrió y cómo.
3. **Explotación** · Acceso inicial, paso a paso.
4. **Escalada de privilegios** · Del usuario al control total.
5. **Lecciones aprendidas** · Qué aprendí y cómo se mitiga.
6. **Referencias** · Recursos consultados.

</details>

---

## ⚠️ Aviso legal

> [!WARNING]
> Todo el contenido de este repositorio tiene **fines exclusivamente educativos**.
>
> - Solo se publican writeups de **máquinas retiradas** de Hack The Box, respetando sus normas.
> - Las técnicas se aplican únicamente en **entornos autorizados**.
> - No me hago responsable del uso indebido de esta información.
>
> Atacar sistemas sin autorización es ilegal.

---

## 📫 Contacto

<div align="center">

[![HTB](https://img.shields.io/badge/Hack_The_Box-Mi_perfil-1a1033?style=for-the-badge&logo=hackthebox&logoColor=a78bfa)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectemos-5b21b6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

</div>

---

<div align="center">

⭐ **Si este repositorio te resulta útil, dale una estrella.** ⭐

<sub>by <b>ph4n3s</b></sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0b1a,45:2e1065,100:8b5cf6&height=100&section=footer" width="100%" alt=""/>

</div>
