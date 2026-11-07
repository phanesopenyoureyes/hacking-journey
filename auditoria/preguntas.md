# Auditoría E0 — Preguntas para ti

Reunidas todas aquí (no he interrumpido antes). Responde a lo que puedas y con eso arranco E1.
Las marcadas con ⚠️ **bloquean** decisiones de E1.

## Seguridad / contenido

1. ⚠️ **Flags.** La regla 4 dice "nada de flags" y tú ya las censuras en algunos writeups.
   ¿Confirmo que **censuro todas** las flags de todos los writeups (dejando algo como
   `USER FLAG -> [censurada]` + nota)? (recomiendo: **sí**.)

2. ⚠️ **Credenciales y hashes de máquina.** Aquí hay un conflicto: `CLAUDE.md` permite mostrar las
   credenciales/hashes que son **parte de la máquina** (la contraseña por defecto que se explota, el
   hash que se crackea), pero la **regla 4** del encargo dice "nada de contraseñas, hashes". ¿Qué hago?
   - (a) Dejarlas (son públicas y de laboratorio; es lo habitual en writeups), **o**
   - (b) Enmascararlas también (p. ej. `Pass****` o `[credencial de la máquina]`).
   Afecta a muchos writeups y a algunas capturas; dime el criterio y lo aplico a todos por igual.

3. **Capturas.** ¿Quieres que haga un repaso visual fino de las capturas buscando pestañas del
   navegador, emails reales o *hostnames* privados? (riesgo que veo: bajo, pero es tu decisión).

## Contacto (E1)

4. ⚠️ **Email profesional.** Necesito un email para la sección de contacto (la regla pide LinkedIn
   principal + GitHub + HTB + email profesional). ¿Cuál pongo? Recomiendo uno tipo
   `nombre.apellido@gmail.com` dedicado, **no** tu email personal actual si no quieres exponerlo.
   (Tu email de la cuenta no lo publico salvo que me lo digas explícitamente.)

5. **Discord.** Confirmo que lo quito de **toda** la web (mkdocs.yml + sobre-mi). ¿Correcto?

## Certificaciones (E1)

6. La única certificación publicada es **eJPT** (INE), con fecha `2026-10-30` y enlace de
   verificación de INE. ¿Es correcta la fecha y el enlace? ¿Hay alguna **otra** certificación real
   que deba añadir (con fecha y enlace verificable)? No añado nada que no me confirmes.

## Portada / estado (E2)

7. **"Estado actual".** ¿Confirmo el texto *"preparando CPTS (objetivo 2027), después OSCP"*?
   ¿Y la frase de 2–3 líneas de quién eres / qué estudias / qué buscas la redacto yo y tú la
   apruebas, o me pasas tú el texto?

8. **Nota de transparencia sobre Claude Code.** La regla E2 me pide preguntarte: ¿quieres una nota
   breve y honesta diciendo que usas Claude Code como herramienta de apoyo para redactar/organizar
   el portfolio? (sin exagerar; tú decides sí/no).

## Autenticidad (E3)

9. Varios writeups los redacté yo a partir de tus notas (ver `writeups.md`, columna "Autoría").
   Para los **3 destacados** (propongo Validation + Optimum + Sau/Delivery) te haré preguntas
   concretas en E3 ("qué probé primero, qué falló, qué me costó, qué aprendí") para añadir tu voz.
   ¿Te parece bien esa terna o prefieres destacar otras?

   **Actualización E3 (2026-11-07):** la terna que está **publicada** en la portada ahora es
   `validation`, `optimum` y `buff` (ver `scripts/generar-sitio.py`, lista `DESTACADOS`).
   Y la auditoría de autenticidad ha encontrado que **buff** es el que menos material tuyo
   tiene (su escalada la completé yo «con el método conocido de la máquina»). Esto convierte
   la pregunta 9 en urgente → pasa a ser la **pregunta 13**.

## Autenticidad (E3) — preguntas nuevas

Estas son las nuevas de E3 (10 a 16) y bloquean el cierre de la etapa. Las que ya había
antes de E3, sobre higiene del repo y despliegue, se han renumerado al final (17 a 19) para
que no se solaparan. El detalle completo está en `auditoria/autenticidad.md`.

### Las cuatro preguntas, writeup por writeup destacado

Para cada uno de los tres destacados necesito estas cuatro respuestas. Con las de
validation y optimum ya he escrito la sección usando **solo frases que están en tu
writeup actual** (que es texto tuyo verificado contra el original): te las pongo para que
**me corrijas lo que no cuadre** y para añadir lo que falte. Con buff no tengo nada tuyo,
así que ahí la sección **no existe todavía** y la escribo con tus respuestas.

**Validation** (ya escrito, pendiente de tu corrección)

1. ¿Qué probaste **primero** y falló? Yo tengo: el formulario de registro a pelo, y el
   intento de inyectar en el desplegable de país (imposible sin Burp).
2. ¿Qué fue lo que más te **costó**? Yo tengo: el campo `<select>`, el `base64` para leer
   el `config.php`, y el SSH que falló tres veces.
3. ¿Qué **aprendiste** que no sea una regla de seguridad? Yo tengo tu reflexión final:
   abrir Burp con Intercept desde el principio.
4. ¿Quieres que añada algo que sé que pasó pero no está escrito?

**Optimum** (ya escrito, pendiente de tu corrección)

1. ¿Qué probaste primero y falló? Yo tengo: editar el exploit sin `sudo`, el
   `nmap --script vuln` (falsos positivos), y el binario `41020.exe` que daba `404`.
2. ¿Qué fue lo que más te costó? Yo tengo: el `404` del binario, y la búsqueda del PoC
   alternativo hasta dar con `Invoke-MS16032.ps1`.
3. ¿Qué aprendiste? Yo tengo tu «concepto clave aprendido» (buscar otra implementación de
   la misma CVE).
4. ¿Usaste Metasploit para la escalada en el final, o solo lo dejas como alternativa?

**Buff** (sin escribir — necesito tus respuestas)

1. ¿Qué probaste primero? ¿Gym Management lo viste en el pie de página o lo encontraste de
   otra forma?
2. ¿Qué falló antes de funcionar? (En el writeup no hay ni un intento fallido: es el
   primero que no documenta ni un callejón.)
3. ¿Qué te costó? (el pivoting con chisel, la shellcode, los *bad chars*…)
4. ¿Qué aprendiste?



10. **Buff — ¿qué hiciste tú exactamente?** Es el writeup destacado que más importa. De sus
    capturas y notas tengo: subida de ficheros sin auth (CVE-2020-25223) → shell como
    `shaun` → servicio CloudMe solo en `127.0.0.1:8888` → pivoting con chisel → exploit
    48389. Pero el **final** de la escalada lo completé yo. Concretamente:
    - ¿Hiciste tú el pivoting con chisel, o lo hizo otra persona?
    - ¿Usaste el `48389.py` con shellcode de `msfvenom` (como está escrito), o el método
      que tú usaste fue otro (exploit de Metasploit, otro PoC, otro debugger)?
    - ¿Hubo pasos intermedios que hice falta y se me quedaron fuera?
    - ¿Lo reescribes tú, o prefieres que lo saque de la portada y pongamos otro?

11. **Cronos — la escalada no la ejecutaste tú (al menos, no está en tus notas).** El
    commit dice que la completé a partir de las capturas. Además, tal como está escrita, el
    payload **no funcionaría**: se mete una línea de bash en `Kernel.php`, pero el cron
    ejecuta `php .../artisan schedule:run`, o sea PHP. Necesita el envoltorio
    `<?php system(...); ?>`. ¿Cuál fue el payload real que usaste? (Pégamelo tal cual y lo
    pongo; si no lo recuerdas, lo marco como NO VERIFICADO y lo reescribo con el envoltorio
    correcto diciéndolo.)

12. **ServMon, Pilgrimage, Sau y los demás del bloque B — ¿me pasas tus notas?** Tengo tus
    capturas, pero no tus textos: no puedo contrastar frase por frase qué es tuyo. Si me
    pasas el texto original (o me dices dónde está), lo comparo y te digo qué difiere. Sin
    eso, los writeups que redacté yo se quedan como están, con mi prosa.

13. ⚠️ **La terna de destacados de la portada.** Ahora mismo son `validation`, `optimum`,
    `buff`. Dado que buff es el que menos material tuyo tiene, ¿lo cambiamos por `sau` o
    `delivery` (que sí tienen capturas y notas tuyas), o lo rehaces tú y lo mantenemos?
    Recomiendo: **cambiarlo por `delivery`** hasta que lo rehagas, porque ahora mismo el
    writeup más visible de la portada es el menos tuyo. Y la terna que propuse en la
    pregunta 9 era precisamente `validation` + `optimum` + `sau`/`delivery`.

14. **Los seis con más problemas técnicos.** En `auditoria/autenticidad.md` §4 tienes la
    lista con línea exacta. Son errores comprobables, no de estilo:
    `cronos:236` (payload PHP), `servmon:141` (ruta macOS en máquina Windows),
    `pilgrimage:182/185` (nombres de fichero que no coinciden), `buff:63-64` (tres CVEs mal
    atribuidas y ninguna usada después), `sau:107` (falta el comando de lanzar el exploit),
    `legacy:8,129` (MS17-010 no aplica a XP).
    - ¿Quieres que **arregle yo** los mecánicos (los que no dependen de tus notas:
      servmon, pilgrimage, sau, legacy) y te deje los dos que sí dependen de tus notas
      (cronos, buff) para que los rehagas?
    - ¿O prefieres revisarlos tú todos y que solo prepare las correcciones propuestas?

15. **Los writeups sin una sola marca de primera persona.** Son 16 de 24. El que más me
    preocupa no es el estilo, es `buff` (0 marcas, 100% impersonal, y está en la portada).
    ¿Quieres que en E4 reescriba **todos** los writeups del bloque B en primera persona
    (con lo que hay en tus capturas, marcando lo que no sé), o lo dejamos así y que solo
    los destacados lleven voz propia?

16. **Nota de transparencia (recuerda la pregunta 8).** Si acabas publicando writeups
    redactados por mí a partir de tus notas, ¿quieres una nota breve y honesta en el
    README o en «Sobre mí» diciendo que los writeups se documentan con apoyo de Claude Code
    para redactar y organizar, y que el trabajo técnico es tuyo? Mi opinión: **sí**, es
    mejor que lo diga yo a que lo pille un técnico leyendo el repo. Pero es tu decisión y no
    la tomo por mi cuenta.

## Higiene del repo (cualquier momento)

17. ¿Borro las ~28 **ramas ya fusionadas** de `origin` (`writeup-*`, `fix-*`, …)? No borra
    contenido (es historia ya en `main`), solo limpia la lista de ramas.

18. ¿Borro `docs/_auditoria.md` (auditoría vieja de fase 0, ya excluida del sitio)? Su función la
    cumple ahora `auditoria/`.

## Despliegue / versiones

19. Las dependencias están fijadas (`mkdocs 1.6.1`, `mkdocs-material 9.8.0`,
    `awesome-pages 2.10.1`). No las tocaré sin tu permiso. ¿Quieres que las deje tal cual? (recomiendo **sí**).
