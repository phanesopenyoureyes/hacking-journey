---
titulo: "Escáner de red de contenedores"
fecha: 2026-11-12
tipo: "script"
estado: publicado
repo: ""
temas: [enumeracion, pivoting, docker]
---

# Escáner de red de contenedores

## Qué hace

Es un **script pequeño en bash** que me hice para **enumerar los hosts vivos de la red interna de
un contenedor**. Lo usé resolviendo **Reddish**: en esa máquina acabas dentro de un contenedor
Docker y, para avanzar, tienes que **pivotar** hacia los otros contenedores, que viven en redes
internas (`172.18.0.0/24`, `172.19.0.0/24`…). Lo que hace el script es un **barrido de ping** a todas
las IPs de esas redes y me dice cuáles responden, para saber a qué contenedores puedo llegar.

No tiene ningún misterio —es un `ping` en bucle— pero lanzado **en paralelo** barre una `/24` en un
par de segundos, que es justo lo que quieres cuando estás pivotando y no tienes `nmap` a mano dentro
del contenedor.

## Uso

Las redes a escanear están en el array `networks`, al principio del script, así que **se editan ahí**
según la máquina. Luego solo hay que ejecutarlo:

```bash
chmod +x escaner-red-contenedores.sh
./escaner-red-contenedores.sh
```

Salida de ejemplo:

```
[+] Enumerando el network 172.18.0:
[+] Host 172.18.0.1 - Activo.
[+] Host 172.18.0.2 - Activo.
...
```

## El script

```bash
#!/bin/bash

function ctrl_c(){
    echo -e "\n\n[!] Saliendo...\n"
    tput cnorm; exit 1
}

# Ctrl+C
trap ctrl_c INT

networks=(172.18.0 172.19.0)

tput civis
for network in "${networks[@]}"; do
    echo -e "\n[+] Enumerando el network $network:"
    for i in $(seq 1 254); do
        (timeout 1 bash -c "ping -c 1 $network.$i" &>/dev/null && echo "[+] Host $network.$i - Activo.") &
    done; wait
done
tput cnorm
```

## Notas

- **El rango se cambia en el array `networks`**: pon ahí las redes que te interese barrer
  (`172.18.0`, `172.19.0`, `10.10.10`…), sin el último octeto, que lo recorre el script del 1 al 254.
- El barrido va **en paralelo** (cada ping en segundo plano, con un `wait` al final de cada red), así
  que una `/24` completa tarda poco.
- `tput civis` / `tput cnorm` solo ocultan y restauran el cursor mientras corre; el `trap` de
  `Ctrl+C` se asegura de volver a mostrarlo si lo cortas a medias.
- Es para **redes pequeñas y rápidas** (contenedores, laboratorios). Para algo serio, `nmap` o
  `fping` hacen esto mejor; esto es para cuando estás dentro de un contenedor pelado y solo tienes
  `bash` y `ping`.
