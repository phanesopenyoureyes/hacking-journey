# Auditoría E0 — hacking-journey

- **Fecha:** 2026-11-07
- **Rama de trabajo:** `auditoria-e0` (solo lectura salvo `auditoria/` y la copia de seguridad).
- **Commit base (`main`):** `c1002fb`.
- **Copia de seguridad:** rama remota **`backup/pre-e0-20261107`** (apunta a `c1002fb`, cubre todo
  el código fuente y el generador). El *tag* `backup-e0-20261107` existe en local pero **no se pudo
  subir** por un corte de red del remoto; la rama de respaldo ya cumple la función. **A comprobar
  por ti:** que ves la rama de respaldo en GitHub → *branches*.

> Metodología: en este informe **solo se señala fichero:línea**, nunca el valor de un secreto, flag
> o credencial. Nada se ha modificado fuera de `auditoria/` y la rama de respaldo.

---

## 0. Corrección del "estado conocido" del encargo (verificado)

El encargo asumía cosas que **no coinciden** con el repo real; conviene partir de los hechos:

| Supuesto del encargo | Realidad verificada |
| --- | --- |
| "main solo muestra HTB/ y un README de una línea" | `main` es el repo completo: `maquinas/`, `scripts/`, `docs/`, `certificaciones/`, `preparacion/`, `herramientas/`, `mkdocs.yml`, `README.md` (212 líneas), CI y workflows. |
| "el generador puede estar sin versionar o fuera del repo" | El generador **está versionado** en `scripts/` y el CI lo ejecuta y valida. No hay riesgo de pérdida. |
| "22 máquinas (21 fáciles, 1 media)" | ✅ Correcto: 21 fáciles + 1 media **publicadas**. Además hay 2 borradores (`grandpa`, `jerry`) en `estado: pendiente` (fuera del sitio). |
| "1 certificación" | ✅ eJPT. |
| "secciones vacías en el menú" | ✅ **Herramientas** está vacía (0) y aparece en el nav y en la portada. |
| "Discord como contacto" | ✅ En `mkdocs.yml` y en `docs/sobre-mi.md`. |

---

## 1. Hallazgos por gravedad

### 🔴 ALTA

1. **Flags publicadas en texto completo en 18 de 22 writeups.**
   Incumple la regla 4 ("Nada de flags"), la política de HTB para writeups públicos y **tu propia
   práctica**: `validation`, `blue`, `granny` y `buff` ya las censuran (y en `validation` tú mismo
   escribes *"las dejo censuradas, HTB pide no publicarlas completas"*). El resto no.
   - Ejemplos (fichero, líneas con `FLAG ->`): `maquinas/htb/facil/delivery/README.md`,
     `.../broker/README.md`, `.../sau/README.md`, `.../pilgrimage/README.md`, `.../bank/README.md`,
     `.../antique/README.md`, `.../servmon/README.md`, `.../irked/README.md`, `.../nibbles/README.md`,
     `.../optimum/README.md`, `.../devel/README.md`, `.../bashed/README.md`, `.../knife/README.md`,
     `.../traverxec/README.md`, `.../validation` (no), `.../lame/README.md`, `.../legacy/README.md`,
     `maquinas/htb/media/cronos/README.md`.
   - **Autocrítica:** los writeups que añadí yo en este chat (antique, bank, servmon, irked, cronos,
     pilgrimage, broker, delivery) incluyen las flags completas. **Incumplí la regla 4 al redactarlos.**
   - **Acción propuesta (E1):** redactar/censurar **todas** las flags de forma uniforme
     (p. ej. `USER FLAG -> [censurada]`) y añadir la nota de por qué.

2. **Credenciales y hashes de máquina en texto plano.**
   Muchos writeups muestran contraseñas/hashes que forman parte de la máquina. `CLAUDE.md` los
   permite ("credenciales de la propia máquina"), pero la **regla 4 del encargo los prohíbe**
   ("contraseñas, hashes"). **Conflicto a decidir por ti** (ver `preguntas.md`).
   - Ficheros con más coincidencias: `.../servmon/README.md`, `.../delivery/README.md`,
     `.../validation/README.md`, `.../irked/README.md`, `.../antique/README.md`,
     `.../traverxec/README.md`, `.../nibbles/README.md`, `maquinas/htb/media/cronos/README.md`.
   - Nota: `.gitleaks.toml` tiene una *allowlist* específica para estos casos (líneas 10-16), así
     que el escáner no los marca **por diseño**.

### 🟠 MEDIA

3. **Discord como contacto** (reglas de contacto E1 → quitar).
   - `mkdocs.yml:83-85` (bloque `social`).
   - `docs/sobre-mi.md:22`.

4. **Sección "Herramientas" vacía** visible en nav y portada.
   - Portada generada: `docs/index.md` → "0 herramientas propias publicadas" (tarjeta con contador 0).
   - `herramientas/` solo tiene `README.md` (0 herramientas).
   - **Acción (E1):** ocultar del nav y de la portada las secciones vacías y los contadores a 0.
   - El cambio debe ir en **`scripts/generar-sitio.py`** (regla 5), no en `docs/` generado.

5. **Contador en singular/plural incorrecto.**
   - `docs/index.md`: "**1 certificaciones** publicadas" → debe ser "1 certificación publicada".
   - Origen: `scripts/generar-sitio.py` (texto del contador de la portada).

6. **Inconsistencia en el tratamiento de flags, plantillas y campo `dificultad`** (ver `writeups.md`).
   Tres estilos de plantilla y el campo `dificultad` mezcla `Easy`/`Fácil`. No rompe nada, pero
   resta profesionalidad. (E4.)

### 🟡 BAJA

7. **Ramas sin limpiar:** ~28 ramas de *feature* ya fusionadas siguen en `origin` (`writeup-*`,
   `fix-*`, etc.). Ensucian el repo. **Acción:** borrarlas (no borra contenido; son historia ya
   fusionada). *Pregunta incluida.*

8. **`docs/_auditoria.md`** es una auditoría antigua (fase 0, 2026-10-27) ya obsoleta, excluida del
   sitio vía `exclude_docs`. Candidata a borrar (su sitio es ahora `auditoria/`).

9. **Nota de ética ausente en la web.** El *Aviso legal* existe en `README.md:113-121` (GitHub)
   pero **no** en el sitio publicado (`docs/sobre-mi.md` solo menciona "máquinas retiradas").
   La regla E1 pide una nota breve de ética en la web.

10. **Rendimiento de imágenes** (números base para comparar en E4):
    - 14 capturas pesan **> 500 KB** (máximas: `optimum-04-preparando-privesc.png` 1,4 MB;
      `traverxec-06-…` 1,4 MB; `traverxec-05-…` 1,2 MB; `nibbles-02-…` 1,1 MB).
    - `.git` pesa **98 MB** (histórico cargado de imágenes).
    - **Acción (E4):** comprimir/redimensionar capturas (objetivo < ~300 KB) en origen.

---

## 2. Generador y despliegue

- **Qué se edita a mano (fuente, versionado):** `maquinas/**/README.md`, `certificaciones/**`,
  `preparacion/**`, `herramientas/**`, `mkdocs.yml`, `docs/assets/`, `docs/stylesheets/extra.css`,
  `docs/sobre-mi.md`, `docs/404.md`, `scripts/*`, `.plantillas/*`.
- **Qué se genera (NO editar a mano; `.gitignore`):** `docs/index.md`, `docs/maquinas/`,
  `docs/certificaciones/`, `docs/herramientas/`, `docs/preparacion/`, `site/`. Lo construye
  `scripts/generar-sitio.py` a partir del front-matter de cada `README.md` (`estado: publicado`).
- **Índices** (`README.md` raíz y `maquinas/htb/README.md`) los genera `scripts/generar-indice.py`
  entre marcadores; el CI comprueba que están al día.
- **Despliegue:** `.github/workflows/pages.yml` → en push a `main` ejecuta `generar-sitio.py` +
  `mkdocs build --strict` + `upload-pages-artifact` + `deploy-pages`. **No hay rama `gh-pages`**:
  el origen de Pages es GitHub Actions. La URL no cambia.
- **CI** (`.github/workflows/ci.yml`): valida writeups, enlaces, secretos propios, índice al día,
  gitleaks y `mkdocs build --strict`.
- **Cómo versionar el código fuente sin romper el despliegue:** **ya está versionado y protegido
  por CI.** Propuestas de higiene (no urgentes): borrar las ramas fusionadas, borrar
  `docs/_auditoria.md`, y añadir `auditoria/` a `exclude_docs`/fuera de `docs/` (ya está fuera de
  `docs/`, así que **no se publica**).

---

## 3. Seguridad (detalle)

- **Secretos propios:** no se encuentran. No hay `*.ovpn`, `*.pem`, `id_rsa`, `.env` (bloqueados en
  `.gitignore`). `scripts/buscar-secretos.sh` pasa. **No aparece tu email** en el contenido, ni IPs
  privadas de casa/instituto (`192.168.x`, `10.0.x`) — la única coincidencia `192.168` está en
  `CLAUDE.md:50` como **regla**, no como dato.
- **Flags / credenciales de máquina:** ver hallazgos ALTA 1 y 2.
- **IPs de laboratorio** (`10.129.x`, `10.10.1x.x`): presentes y **permitidas** por `CLAUDE.md`
  (son privadas y reasignables). Sin hallazgo.
- **Metadatos de imágenes (EXIF/chunks):** **0 imágenes** con metadatos sospechosos (autor,
  software, comentario, XMP). Limpio.
- **Contenido visible en capturas:** se revisaron a alto nivel; aparecen el alias `ph4n3s@kali`,
  *prompts* de las máquinas (`activemq@broker`, `maildeliverer@Delivery`…) e IPs de laboratorio —
  todo aceptable. **A comprobar por ti (TODO):** un repaso visual fino por si en alguna captura se
  colara una pestaña del navegador, un email real o un *hostname* privado. Riesgo estimado: bajo.
- **Historial reciente de git:** los commits recientes son de contenido (writeups, fixes del
  generador); no se observan secretos propios introducidos. (gitleaks corre en CI con el historial
  completo.)

---

## 4. Los 3 mejores writeups (justificados)

1. **Validation** — el más honesto y didáctico: narra los atascos reales (el `<select>` de país,
   el lío 302/blind), intentos fallidos (SSH), el *porqué* de cada decisión y una reflexión
   metodológica final. Además **ya censura las flags**. Es el que mejor demuestra proceso real.
2. **Optimum** — documenta un **intento fallido** ("41020.exe no llegó a servirse") y la alternativa
   que sí funcionó, con un "concepto clave aprendido" valioso. Muestra criterio, no solo comandos.
3. **Sau / Delivery** (empate) — las cadenas más interesantes técnicamente (SSRF+inyección;
   osTicket↔Mattermost) y bien ilustradas. **Matiz:** su redacción es de Claude a partir de tus
   notas; para destacarlas en portada conviene que añadas tu voz (E3).

---

## 5. NO VERIFICADO

- **Autoría real de parte de los writeups.** Los de "Autoría: Claude (de tus notas)" en
  `writeups.md` fueron **ensamblados por Claude Code** a partir de tus notas/capturas; su redacción
  (Resumen, Mitigación, Qué he aprendido) no es tuya. Para cumplir las reglas 2 y 3 debes
  revisarlos y hacerlos tuyos (E3). **NO VERIFICADO** que cada paso refleje exactamente tu proceso.
- **Cronos:** la escalada se **completó desde las capturas** porque tus notas de texto se cortaban
  en el crontab. Verifica el payload exacto que usaste.
- **`sau`** se añadió fuera de las sesiones que controlo; **NO VERIFICADO** quién lo redactó.
- **Máquinas retiradas:** todas las publicadas son clásicas y retiradas (Blue, Lame, Legacy,
  Devel, Optimum, Granny, Nibbles, Bashed, Shocker, Knife, Traverxec, Validation, Bank, Antique,
  Irked, Buff, ServMon, Pilgrimage, Sau, Broker, Delivery, Cronos). No he podido **confirmar en
  vivo** el estado "retirada" de cada una contra HTB desde aquí → **NO VERIFICADO**; confírmalo tú
  (lo normal es que lo estén todas).

---

## 6. Números base (para comparar en E4)

| Métrica | Valor actual |
| --- | --- |
| Páginas HTML generadas | 36 |
| Peso de `site/` | 29 MB |
| Nº de imágenes | 113 |
| Imágenes > 500 KB | 14 |
| Peso de `maquinas/` | 23 MB |
| Peso de `.git` | 98 MB |
| `mkdocs build --strict` | ✅ sin avisos |
| Enlaces relativos rotos | 0 |
| Writeups publicados | 22 (21 fáciles + 1 media) |

---

## 7. Plan priorizado (propuesta de etapas)

1. **E1 (seguridad y arreglos seguros):** censurar flags (ALTA-1); decidir creds/hashes (ALTA-2);
   quitar Discord (MEDIA-3); ocultar sección vacía y contador 0 (MEDIA-4); arreglar plural
   (MEDIA-5); nota de ética en la web (BAJA-9). Todo en `scripts/generar-sitio.py`/fuente.
2. **E2 (portada, README, About de GitHub).**
3. **E3 (autenticidad):** tu voz en los 3 destacados + revisar los ensamblados por Claude.
4. **E4 (plantilla única, tags, versión EN, meta/OG/favicon/alt, comprimir imágenes).**
5. **Higiene (cuando quieras):** borrar ramas fusionadas y `docs/_auditoria.md`.

---

## 8. Autocrítica contra las reglas

- **Regla 4 (flags):** la incumplí al añadir en sesiones anteriores writeups con las flags
  completas (antique, bank, servmon, irked, cronos, pilgrimage, broker, delivery). Se corrige en E1.
- **Regla 2/3 (autenticidad):** varios writeups los redacté yo; su *Resumen/Mitigación/Qué he
  aprendido* son míos, no tuyos. Lo marco como NO VERIFICADO y lo abordamos en E3.
- Resto de reglas de E0 (solo lectura, respaldo, informes solo con fichero:línea, `auditoria/`
  fuera de lo publicado): respetadas.
