<div align="center">

# 🧠 hacking-journey

### My road through Hack The Box — one machine, one writeup, no skipped steps.

Enumeration → exploitation → privilege escalation → **how to actually fix it**.
Written the way I solve them: dead ends included, so you learn the process, not just the flag.

<br>

[![Hack The Box](https://img.shields.io/badge/Hack_The_Box-profile-9FEF00?style=for-the-badge&logo=hackthebox&logoColor=black&labelColor=1a1033)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=1a1033)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

![Machines](https://img.shields.io/badge/machines-14-8b5cf6?style=flat-square&labelColor=1a1033)
![Linux](https://img.shields.io/badge/Linux-7-a78bfa?style=flat-square&labelColor=1a1033&logo=linux&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-7-a78bfa?style=flat-square&labelColor=1a1033&logo=windows&logoColor=white)
![Difficulty](https://img.shields.io/badge/difficulty-Easy-6d28d9?style=flat-square&labelColor=1a1033)
![Updated](https://img.shields.io/badge/status-actively_updated-8b5cf6?style=flat-square&labelColor=1a1033)

<br>

[**Writeups**](#-writeups) · [**How I work**](#-how-i-work) · [**Layout**](#-repository-layout) · [**What's next**](#-whats-next) · [**Legal**](#-legal)

</div>

---

> [!NOTE]
> I'm a cybersecurity student documenting every HTB machine I solve. These writeups are built to be **read**, not just archived — clear steps, real reasoning, and a mitigation note on every box. If that's useful to you, a ⭐ keeps me going.

---

## 📂 Writeups

Each machine links to its own folder with the full writeup and screenshots.

| # | Machine | OS | Difficulty | What makes it tick | Writeup |
|:-:|:--|:-:|:-:|:--|:-:|
| 01 | **Lame** | 🐧 Linux | 🟢 Easy | Samba `username map script` — `CVE-2007-2447` | [→](./HTB/machines/easy/Lame) |
| 02 | **Legacy** | 🪟 Windows | 🟢 Easy | SMB on Windows XP — `MS08-067` | [→](./HTB/machines/easy/Legacy) |
| 03 | **Blue** | 🪟 Windows | 🟢 Easy | EternalBlue — `MS17-010` | [→](./HTB/machines/easy/Blue) |
| 04 | **Devel** | 🪟 Windows | 🟢 Easy | Anonymous FTP → ASPX webshell → kernel exploit | [→](./HTB/machines/easy/Devel) |
| 05 | **Grandpa** | 🪟 Windows | 🟢 Easy | IIS 6.0 WebDAV — `CVE-2017-7269` + Churrasco | [→](./HTB/machines/easy/Grandpa) |
| 06 | **Granny** | 🪟 Windows | 🟢 Easy | IIS 6.0 WebDAV → `NETWORK SERVICE` → SYSTEM | [→](./HTB/machines/easy/Granny) |
| 07 | **Optimum** | 🪟 Windows | 🟢 Easy | Rejetto HFS 2.3 RCE — `CVE-2014-6287` + `MS16-032` | [→](./HTB/machines/easy/Optimum) |
| 08 | **Jerry** | 🪟 Windows | 🟢 Easy | Tomcat default creds → malicious WAR | [→](./HTB/machines/easy/Jerry) |
| 09 | **Shocker** | 🐧 Linux | 🟢 Easy | Shellshock over CGI — `CVE-2014-6271` → sudo perl | [→](./HTB/machines/easy/Shocker) |
| 10 | **Knife** | 🐧 Linux | 🟢 Easy | PHP 8.1.0-dev backdoor → sudo `knife` | [→](./HTB/machines/easy/Knife) |
| 11 | **Bashed** | 🐧 Linux | 🟢 Easy | Exposed `phpbash` webshell → cron sudo | [→](./HTB/machines/easy/Bashed) |
| 12 | **Nibbles** | 🐧 Linux | 🟢 Easy | Nibbleblog upload — `CVE-2015-6967` → editable script | [→](./HTB/machines/easy/Nibbles) |
| 13 | **Traverxec** | 🐧 Linux | 🟢 Easy | Nostromo RCE — `CVE-2019-16278` → `journalctl`+`less` | [→](./HTB/machines/easy/Traverxec) |
| 14 | **Validation** | 🐧 Linux | 🟢 Easy | UNION SQLi → `INTO OUTFILE` webshell → password reuse | [→](./HTB/machines/easy/Validation) |

<div align="center"><sub>Ordered roughly by when I tackled them · updated with every new box.</sub></div>

---

## 🛠 How I work

Same loop on every machine — predictable on purpose, so the writeups are easy to follow:

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#2e1065','primaryTextColor':'#ede9fe','primaryBorderColor':'#8b5cf6','lineColor':'#a78bfa','secondaryColor':'#1a1033','tertiaryColor':'#0d0b1a','fontFamily':'ui-sans-serif,system-ui'}}}%%
flowchart LR
    A[Recon] --> B[Enumeration]
    B --> C[Exploitation]
    C --> D[Initial access]
    D --> E[Privilege escalation]
    E --> F[Flags]
    F --> G[Fix / mitigation]
```

<table>
<tr>
<td width="50%" valign="top">

**What every writeup gives you**
- The exact commands, with their output
- *Why* each step works, not just *what* to type
- The rabbit holes I fell into (and why)
- A mitigation note: how the box should've been secured

</td>
<td width="50%" valign="top">

**Skills I'm building**
- Service enumeration & attack-surface mapping
- Mapping versions → known CVEs
- Linux privesc (`sudo`, cron, GTFOBins)
- Windows privesc (tokens, kernel exploits, Metasploit)
- Clean, repeatable technical documentation

</td>
</tr>
</table>

---

## 🗂 Repository layout

Machines live under `HTB/machines/`, split by difficulty. Every machine is a self-contained folder: the writeup is its `README.md`, so GitHub renders it the moment you open the folder.

```
HTB/
└── machines/
    └── easy/
        ├── Blue/          README.md + screenshots
        ├── Bashed/
        ├── Knife/
        ├── Traverxec/
        └── ...            (14 machines)
```

> `medium/`, `hard/` and `insane/` folders will appear here as I climb — the structure is already waiting for them.

---

## 🚀 What's next

- [x] Clear every classic **Easy** box (14 done)
- [ ] Move into **Medium** machines
- [ ] Add an Active Directory track
- [ ] Short "lessons learned" index across all boxes

<div align="center"><sub>Writeups are bilingual-friendly: written in English (Cambridge C1) so they're useful to anyone.</sub></div>

---

## ⚖ Legal

> [!WARNING]
> Everything here is for **educational purposes only**.
> - Only **retired** Hack The Box machines are published, per HTB's rules.
> - Techniques are used strictly in **authorised** lab environments.
> - Attacking systems without permission is illegal — the author takes no responsibility for misuse.

---

<div align="center">

### If these writeups helped you, drop a ⭐ — it's the only metric that tells me to keep writing.

[![Hack The Box](https://img.shields.io/badge/Hack_The_Box-4011018-9FEF00?style=for-the-badge&logo=hackthebox&logoColor=black&labelColor=1a1033)](https://app.hackthebox.com/users/4011018)
[![LinkedIn](https://img.shields.io/badge/Francisco_Guti%C3%A9rrez-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=1a1033)](https://www.linkedin.com/in/francisco-gutierrez-garcia)

<sub>Made by <b>Francisco Gutiérrez García</b> · <code>ph4n3s</code></sub>

</div>
