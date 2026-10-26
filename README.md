<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0b1a,45:2e1065,100:8b5cf6&height=220&section=header&text=HACK%20THE%20BOX%20WRITEUPS&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Offensive%20security%20machine%20writeups%20%C2%B7%20ph4n3s&descSize=18&descAlignY=60&animation=fadeIn" alt="Hack The Box Writeups" width="100%"/>

<br>

[![HTB](https://img.shields.io/badge/Hack_The_Box-1a1033?style=for-the-badge&logo=hackthebox&logoColor=a78bfa)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-5b21b6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

![Writeups](https://img.shields.io/badge/Writeups-14-a78bfa?style=flat-square&labelColor=1a1033)
![Status](https://img.shields.io/badge/Status-Active-8b5cf6?style=flat-square&labelColor=1a1033)
![Scope](https://img.shields.io/badge/Scope-Educational-6d28d9?style=flat-square&labelColor=1a1033)

**[Writeups](#writeups)** · **[Skills](#skills-practised)** · **[Repository layout](#repository-layout)** · **[Legal notice](#legal-notice)** · **[Contact](#contact)**

</div>

---

## About this repository

A collection of Hack The Box writeups documenting my training in offensive security. Each writeup covers the full process — enumeration, exploitation, privilege escalation and lessons learned — with special attention to how each vulnerability is mitigated.

I write them as I actually solve the machines, dead ends included, because I think that reflects the real workflow better than a clean "command → result → flag" list.

---

## Methodology

Every writeup follows the same workflow:

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#2e1065','primaryTextColor':'#ede9fe','primaryBorderColor':'#8b5cf6','lineColor':'#a78bfa','secondaryColor':'#1a1033','tertiaryColor':'#0d0b1a','fontFamily':'ui-sans-serif,system-ui'}}}%%
flowchart LR
    A[Recon] --> B[Enumeration]
    B --> C[Exploitation]
    C --> D[Initial access]
    D --> E[Privilege escalation]
    E --> F[Flags]
    F --> G[Lessons learned]
```

---

## Writeups

**14 machines completed** · 7 Linux · 7 Windows · all Easy difficulty

| Machine | OS | Difficulty | Key techniques | Writeup |
|:--|:-:|:-:|:--|:-:|
| **Bashed** | Linux | Easy | `Web fuzzing` · `Exposed webshell` · `Sudo misconfig` | [Read](./HTB/machines/easy/Bashed) |
| **Blue** | Windows | Easy | `SMB` · `MS17-010 (EternalBlue)` | [Read](./HTB/machines/easy/Blue) |
| **Devel** | Windows | Easy | `Anonymous FTP` · `ASPX upload` · `Kernel exploit` | [Read](./HTB/machines/easy/Devel) |
| **Grandpa** | Windows | Easy | `IIS 6.0 WebDAV` · `CVE-2017-7269` · `Token impersonation` | [Read](./HTB/machines/easy/Grandpa) |
| **Granny** | Windows | Easy | `IIS 6.0 WebDAV` · `File upload` · `Token impersonation` | [Read](./HTB/machines/easy/Granny) |
| **Jerry** | Windows | Easy | `Apache Tomcat` · `Default credentials` · `Malicious WAR` | [Read](./HTB/machines/easy/Jerry) |
| **Knife** | Linux | Easy | `PHP 8.1.0-dev backdoor` · `Sudo (knife)` | [Read](./HTB/machines/easy/Knife) |
| **Lame** | Linux | Easy | `Samba` · `CVE-2007-2447` | [Read](./HTB/machines/easy/Lame) |
| **Legacy** | Windows | Easy | `SMB` · `MS08-067 / MS17-010` | [Read](./HTB/machines/easy/Legacy) |
| **Nibbles** | Linux | Easy | `Nibbleblog` · `CVE-2015-6967` · `Sudo + editable script` | [Read](./HTB/machines/easy/Nibbles) |
| **Optimum** | Windows | Easy | `HttpFileServer 2.3` · `CVE-2014-6287` · `Kernel exploit` | [Read](./HTB/machines/easy/Optimum) |
| **Shocker** | Linux | Easy | `CGI` · `Shellshock` · `Sudo (perl)` | [Read](./HTB/machines/easy/Shocker) |
| **Traverxec** | Linux | Easy | `Nostromo` · `CVE-2019-16278` · `SSH key` · `journalctl` | [Read](./HTB/machines/easy/Traverxec) |
| **Validation** | Linux | Easy | `SQLi` · `Command injection` | [Read](./HTB/machines/easy/Validation) |

<sub>The table is updated with every new machine completed.</sub>

---

## Skills practised

- Service enumeration and attack-surface reconnaissance (SMB, FTP, HTTP, WebDAV).
- Identification and analysis of known vulnerabilities by their CVE.
- Privilege escalation on Linux (`sudo` misconfigurations) and Windows (token impersonation, kernel exploits).
- Review of insecure configurations: default credentials, exposed services and excessive permissions.
- Structured technical documentation, with mitigation measures in every case.

---

## Repository layout

Machines are organised by difficulty under `HTB/machines/`. Every machine has its own folder with a `README.md` writeup and its screenshots. Higher-difficulty folders (`medium`, `hard`, `insane`) will be added as I complete machines at those tiers.

```
HTB/
└── machines/
    └── easy/
        ├── Bashed/        README.md + screenshots
        ├── Blue/
        ├── Devel/
        ├── ...
        └── Validation/
```

<details>
<summary><b>Standard writeup format</b></summary>

<br>

1. **Summary** — overview of the machine and the path taken.
2. **Enumeration** — what was found and how.
3. **Exploitation** — initial access, step by step.
4. **Privilege escalation** — from user to full control.
5. **Lessons learned** — conclusions and mitigation measures.
6. **References** — resources consulted.

</details>

---

## Legal notice

> [!WARNING]
> All content in this repository is for **educational purposes only**.
>
> - Only writeups of **retired** Hack The Box machines are published, in line with their rules.
> - The techniques are applied exclusively in **authorised environments**.
> - The author is not responsible for any misuse of this information.
>
> Attacking systems without authorisation is illegal.

---

## Contact

<div align="center">

[![HTB](https://img.shields.io/badge/Hack_The_Box-Profile-1a1033?style=for-the-badge&logo=hackthebox&logoColor=a78bfa)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-5b21b6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

</div>

---

<div align="center">

If you find the content useful, a star on the repository is always appreciated.

<sub>Author: Francisco Gutiérrez García (ph4n3s)</sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0b1a,45:2e1065,100:8b5cf6&height=100&section=footer" width="100%" alt=""/>

</div>
