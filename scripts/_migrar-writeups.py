#!/usr/bin/env python3
# Migra los writeups antiguos: añade front-matter y las secciones Resumen,
# Mitigación y Qué he aprendido. Conserva el cuerpo original tal cual; no lo
# reescribe. Donde falta info, deja PENDIENTE.
import re, os, unicodedata

def pelar(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    return re.sub(r"\s+"," ",s).strip()

# titulo, fecha, so, dificultad, estado, tecnicas, herramientas, resumen, mitigacion
M = {
"bashed": dict(t="Bashed", fecha="2026-10-21", so="linux", est="publicado",
  tec=["enumeracion-web","exposicion-de-herramienta","sudo-misconfig","cron-abuse"],
  her=["nmap","ffuf","nc"],
  res="Servidor Apache con el blog de desarrollo de «Arrexel», que dejó expuesta públicamente una pseudo-shell PHP (`phpbash`) en `/dev/`. Desde ahí se obtiene ejecución de comandos como `www-data`, se salta a `scriptmanager` por un `sudo` mal configurado y se llega a root abusando de un cron que ejecuta un script escribible.",
  mit="No exponer herramientas de pruebas como `phpbash` en un directorio accesible: deben quedar fuera del *document root* o protegidas con autenticación. Restringir las reglas `NOPASSWD` de `sudo` al mínimo imprescindible. Revisar que las carpetas ejecutadas por cron (`/scripts`) no sean escribibles por usuarios sin privilegios."),
"blue": dict(t="Blue", fecha="2026-10-16", so="windows", est="publicado",
  tec=["enumeracion-smb","ms17-010","eternalblue"], her=["nmap","metasploit"],
  res="Máquina Windows vulnerable a EternalBlue (MS17-010) en el servicio SMBv1. La explotación del fallo concede directamente una shell con privilegios de `NT AUTHORITY\\SYSTEM`, por lo que no hace falta escalada posterior.",
  mit="Aplicar el parche MS17-010 y, en general, mantener el sistema actualizado. Deshabilitar SMBv1, que está obsoleto y es el protocolo explotado. Segmentar la red para que el puerto 445 no sea accesible desde fuera de la red de confianza."),
"devel": dict(t="Devel", fecha="2026-10-23", so="windows", est="publicado",
  tec=["ftp-anonimo","carga-de-archivos","iis","kernel-exploit"], her=["nmap","msfvenom"],
  res="Servidor IIS cuyo FTP permite acceso anónimo con escritura sobre la misma raíz que sirve la web. Se sube una webshell `.aspx` que da ejecución como el usuario del *application pool*, y después un exploit de kernel eleva a `SYSTEM`.",
  mit="Desactivar el acceso anónimo al FTP y, sobre todo, no permitir escritura sobre el directorio que sirve IIS. Mantener el sistema parcheado para cerrar el exploit de kernel usado en la escalada. Aplicar el principio de mínimo privilegio al *application pool*."),
"grandpa": dict(t="Grandpa", fecha="2026-10-19", so="windows", est="pendiente",
  tec=["iis","webdav","buffer-overflow","token-impersonation"], her=["nmap","metasploit"],
  res="Servidor IIS 6.0 con WebDAV habilitado, vulnerable a un desbordamiento de búfer (CVE-2017-7269). La explotación da una shell de bajos privilegios y, mediante abuso de tokens (Churrasco), se eleva a `SYSTEM`.",
  mit="Retirar IIS 6.0 y WebDAV, software sin soporte desde hace años. Si el servicio es imprescindible, aislarlo y aplicar los parches disponibles. Limitar los privilegios de la cuenta de servicio para dificultar el abuso de tokens."),
"granny": dict(t="Granny", fecha="2026-10-18", so="windows", est="publicado",
  tec=["iis","webdav","buffer-overflow","token-impersonation"], her=["nmap","metasploit"],
  res="Servidor IIS 6.0 con WebDAV, de la misma familia que Grandpa. Se sube contenido mediante los métodos WebDAV y se explota el servicio para obtener una shell, que luego se eleva a `SYSTEM` mediante abuso de tokens.",
  mit="Retirar IIS 6.0 y WebDAV por falta de soporte. Deshabilitar los métodos HTTP de escritura (PUT, MOVE) si no se usan. Mantener el sistema parcheado y limitar los privilegios de la cuenta de servicio."),
"jerry": dict(t="Jerry", fecha="2026-10-14", so="windows", est="publicado",
  tec=["tomcat","credenciales-por-defecto","war-malicioso"], her=["nmap","msfvenom"],
  res="Servidor Apache Tomcat cuyo panel de gestión usa credenciales por defecto. Con ellas se despliega un `.war` malicioso que da una shell con privilegios de `SYSTEM`, ya que Tomcat corre como servicio.",
  mit="Cambiar siempre las credenciales por defecto del panel de gestión de Tomcat y usar contraseñas robustas. Restringir el acceso a `/manager` por IP. Ejecutar Tomcat con una cuenta de servicio de privilegios mínimos, no como `SYSTEM`."),
"knife": dict(t="Knife", fecha="2026-10-19", so="linux", est="publicado",
  tec=["enumeracion-web","php-backdoor","sudo-misconfig","gtfobins"], her=["nmap"],
  res="Servidor web que corre una versión de PHP (8.1.0-dev) con una puerta trasera conocida en la cabecera `User-Agentt`. Da ejecución como `james`, y un `sudo` sobre el binario `knife` permite escalar a root vía GTFOBins.",
  mit="No desplegar nunca versiones *dev* o no oficiales de PHP en producción: esta llevaba una puerta trasera introducida en el repositorio. Restringir las reglas de `sudo` y evitar permitir binarios que, como `knife`, pueden ejecutar código arbitrario (ver GTFOBins)."),
"lame": dict(t="Lame", fecha="2026-10-15", so="linux", est="publicado",
  tec=["enumeracion-smb","samba","rce"], her=["nmap","metasploit"],
  res="Máquina Linux antigua con un Samba 3.0.20 vulnerable a `usermap_script` (CVE-2007-2447), que permite inyección de comandos. La explotación da directamente una shell como root.",
  mit="Actualizar Samba a una versión con soporte: el fallo está parcheado desde hace años. Deshabilitar la opción `username map script` si no se usa. Exponer SMB solo en redes de confianza."),
"legacy": dict(t="Legacy", fecha="2026-10-16", so="windows", est="publicado",
  tec=["enumeracion-smb","ms08-067","ms17-010"], her=["nmap","metasploit"],
  res="Windows XP vulnerable a fallos clásicos de SMB (MS08-067 / MS17-010). La explotación concede directamente una shell con privilegios de `SYSTEM`.",
  mit="Retirar Windows XP, sin soporte desde 2014. Aplicar los parches MS08-067 y MS17-010 y deshabilitar SMBv1. Aislar en la red cualquier sistema heredado que no pueda actualizarse."),
"nibbles": dict(t="Nibbles", fecha="2026-10-22", so="linux", est="publicado",
  tec=["enumeracion-web","fuzzing","carga-de-archivos","sudo-misconfig"], her=["nmap","ffuf","hydra","nc"],
  res="Servidor web con Nibbleblog, vulnerable a subida de ficheros (CVE-2015-6967). Tras acceder al panel se sube una shell que da ejecución como `nibbler`, y un `sudo` sobre un script escribible (`monitor.sh`) permite escalar a root.",
  mit="Mantener Nibbleblog actualizado para cerrar la subida de ficheros. Usar credenciales robustas en el panel de administración. Revisar las reglas de `sudo` y que los scripts ejecutables como root no sean escribibles por el usuario."),
"optimum": dict(t="Optimum", fecha="2026-10-24", so="windows", est="publicado",
  tec=["http-file-server","rce","kernel-exploit"], her=["nmap","metasploit","powershell"],
  res="Servidor HttpFileServer (HFS) 2.3 vulnerable a ejecución remota de código (CVE-2014-6287). Da una shell como `kostas`, y un exploit de kernel (MS16-032) eleva a `SYSTEM`.",
  mit="Actualizar HFS: la versión 2.3 tiene un fallo de RCE conocido. Mantener el sistema parcheado para cerrar la escalada de kernel. No exponer servicios de terceros sin mantenimiento directamente a la red."),
"shocker": dict(t="Shocker", fecha="2026-10-20", so="linux", est="publicado",
  tec=["enumeracion-web","fuzzing","shellshock","sudo-misconfig","gtfobins"], her=["nmap","ffuf","nc"],
  res="Servidor web con un script CGI vulnerable a Shellshock (CVE-2014-6271). La inyección en la cabecera da ejecución como `shelly`, y un `sudo` sobre `perl` permite escalar a root vía GTFOBins.",
  mit="Parchear Bash para cerrar Shellshock. Deshabilitar CGI si no es imprescindible y evitar que los scripts CGI invoquen el shell. Restringir las reglas de `sudo`, en especial sobre intérpretes como `perl` (ver GTFOBins)."),
"traverxec": dict(t="Traverxec", fecha="2026-10-25", so="linux", est="publicado",
  tec=["enumeracion-web","rce","crackeo-de-hash","sudo-misconfig","gtfobins"], her=["nmap","john","nc"],
  res="Servidor web nostromo vulnerable a RCE (CVE-2019-16278). Da ejecución como `www-data`; desde ahí se obtiene un `.htpasswd` y una clave SSH cifrada que, crackeada, da acceso como `david`. Un `sudo` sobre `journalctl` permite escalar a root vía GTFOBins.",
  mit="Actualizar nostromo para cerrar el RCE. No almacenar hashes de contraseñas ni claves privadas en rutas accesibles por el servicio web, y proteger las claves SSH con passphrases robustas. Restringir `sudo`, en especial sobre `journalctl`, que puede lanzar un shell (ver GTFOBins)."),
"validation": dict(t="Validation", fecha="2026-10-12", so="linux", est="publicado",
  tec=["inyeccion-sql","webshell","reutilizacion-de-credenciales"], her=["nmap","burpsuite"],
  res="Aplicación web vulnerable a inyección SQL en un formulario de registro. A través de una `UNION` se escribe una webshell que da ejecución como `www-data`, y la reutilización de la contraseña de la base de datos permite pasar a root con `su`.",
  mit="Usar consultas parametrizadas (*prepared statements*) para eliminar la inyección SQL. No reutilizar contraseñas entre servicios: la de la base de datos no debería servir para la cuenta de root del sistema. Aplicar privilegios mínimos a la cuenta de base de datos."),
}

APREND = re.compile(r"^(#{2,3})\s+(.*)$")
def es_aprendido(h):
    p = pelar(h)
    return any(k in p for k in ["resumen rapido","conclusion","lo que me llevo"])

for k, d in M.items():
    f = f"maquinas/htb/{k}/README.md"
    raw = open(f, encoding="utf-8").read()
    # Quitar front-matter previo (grandpa) o preámbulo hasta la primera H2.
    txt = raw
    if txt.startswith("---"):
        fin = txt.find("\n---", 3)
        if fin != -1:
            txt = txt[fin+4:]
    lineas = txt.split("\n")
    # índice de la primera H2
    i0 = next((i for i,l in enumerate(lineas) if re.match(r"##\s+", l)), len(lineas))
    cabecera = lineas[:i0]
    cuerpo = lineas[i0:]
    # prosa de intro: líneas antes de la primera H2 que no sean metadatos/reglas/H1
    intro = []
    for l in cabecera:
        s = l.strip()
        if not s or s=="---" or s.startswith("#") or s.startswith("**") or s.startswith(">") or s.startswith("- **"):
            continue
        intro.append(l)
    resumen = "\n".join(intro).strip() if intro else d["res"]
    # renombrar la sección de cierre a "Qué he aprendido"
    cuerpo2 = []
    tiene_aprendido = False
    for l in cuerpo:
        m = APREND.match(l)
        if m and es_aprendido(m.group(2)):
            cuerpo2.append("## Qué he aprendido")
            tiene_aprendido = True
        else:
            cuerpo2.append(l)
    cuerpo = "\n".join(cuerpo2).rstrip()
    # insertar Mitigación antes de "Qué he aprendido"; si no hay, al final + aprendido
    bloque_mit = f"## Mitigación\n\n{d['mit']}\n"
    if tiene_aprendido:
        cuerpo = re.sub(r"\n## Qué he aprendido", f"\n{bloque_mit}\n## Qué he aprendido", cuerpo, count=1)
    else:
        cuerpo = cuerpo + f"\n\n{bloque_mit}\n## Qué he aprendido\n\nPENDIENTE\n"
    fm = (
        "---\n"
        f'titulo: "{d["t"]}"\n'
        f'fecha: {d["fecha"]}\n'
        "plataforma: htb\n"
        f'so: {d["so"]}\n'
        "dificultad: Easy\n"
        f'estado: {d["est"]}\n'
        f'tecnicas: [{", ".join(d["tec"])}]\n'
        f'herramientas: [{", ".join(d["her"])}]\n'
        "---\n\n"
        f'# {d["t"]}\n\n'
        f"## Resumen\n\n{resumen}\n\n"
    )
    open(f,"w",encoding="utf-8").write(fm + cuerpo.lstrip("\n") + "\n")
    print("migrado", k, "estado="+d["est"], "aprendido="+("sí" if tiene_aprendido else "PENDIENTE"))
