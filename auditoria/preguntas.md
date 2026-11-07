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

## Higiene del repo (cualquier momento)

10. ¿Borro las ~28 **ramas ya fusionadas** de `origin` (`writeup-*`, `fix-*`, …)? No borra
    contenido (es historia ya en `main`), solo limpia la lista de ramas.

11. ¿Borro `docs/_auditoria.md` (auditoría vieja de fase 0, ya excluida del sitio)? Su función la
    cumple ahora `auditoria/`.

## Despliegue / versiones

12. Las dependencias están fijadas (`mkdocs 1.6.1`, `mkdocs-material 9.8.0`,
    `awesome-pages 2.10.1`). No las tocaré sin tu permiso. ¿Quieres que las deje tal cual? (recomiendo **sí**).
