---
titulo: "Creador de directorios de trabajo para HTB"
fecha: 2026-11-25
tipo: "script"
estado: publicado
repo: ""
temas: [organizacion, htb, bash]
---

# Creador de directorios de trabajo para HTB

## Qué hace

Es un **script pequeño en bash** que me monta la **estructura de carpetas** de una máquina de Hack
The Box, para empezar cada caja siempre igual de ordenado. Le paso el **nombre de la máquina** como
argumento y crea, dentro de `~/htb_boxes/<máquina>/`, cuatro subcarpetas:

- **`nmap/`** — escaneos y resultados de reconocimiento.
- **`exploits/`** — PoCs y exploits que preparo o descargo.
- **`loot/`** — credenciales, hashes y ficheros que voy sacando.
- **`generalDocumentation/`** — notas, capturas y lo que luego se convierte en el write-up.

Si la carpeta base `~/htb_boxes` no existe, la crea. Si no le paso nombre, me recuerda cómo se usa y
sale.

## Uso

```bash
chmod +x htbworkdir.sh
./htbworkdir.sh <nombre de la maquina>
```

Por ejemplo, `./htbworkdir.sh Cascade` deja listo `~/htb_boxes/Cascade/` con sus cuatro subcarpetas.

## El script

```bash
#!/bin/bash

#Create the machine directory

machine_name=$1
printf "\n [+] Creating: %s\n" "$machine_name"

if [ -z "$machine_name" ]; then
  printf "\n [!] You miss the machine name s%\n"
  sleep 1
  printf "\n Usage: chmod +x htbworkdir.sh && ./htbworkdir.sh <machine name> s%\n"
  exit 1
fi

#Check if the directory "~/htb_boxes" already exists

if [ ! -d "$HOME/htb_boxes" ]; then
  mkdir "$HOME/htb_boxes"
fi

#Create the machine main Directory

if [ "1" = "1" ]; then
  sleep 1
  cd "$HOME/htb_boxes" && mkdir -p "$HOME/htb_boxes/$machine_name"/{nmap,exploits,loot,generalDocumentation}
  sleep 1
  printf "\n [+] Directory succesfully created, you can find it in "$HOME/htb_boxes/$machine_name" s%\n"
else
  printf "\n [!] You already own a directory with that name, you can check it in "$HOME/htb_boxes/$machine_name" s%\n"
fi
```

## Notas

- La estructura (`nmap`, `exploits`, `loot`, `generalDocumentation`) es la que uso en todas las
  máquinas, así cada caja empieza con el mismo esqueleto y luego es fácil montar el write-up desde
  `generalDocumentation`.
- Para tenerlo siempre a mano, va bien dejarlo en el `PATH` o ponerle un alias en el `.bashrc`/`.zshrc`.
- Es un script de comodidad para organizarme; no hace nada "ofensivo", solo crea carpetas.
