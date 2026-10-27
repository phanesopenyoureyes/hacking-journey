# Mantenimiento

Guía para mantener el repositorio. Para leer cuando haga falta, no para memorizar.

## El día a día

Añadir un writeup son tres pasos:

1. `scripts/nuevo-writeup.sh <nombre-maquina> <dificultad>` crea la carpeta con la
   plantilla dentro de `maquinas/htb/<dificultad>/` (dificultad: `facil`, `media`,
   `dificil` o `insane`).
2. Escribir el texto en el `README.md` que acaba de aparecer, respetando las secciones.
   Las capturas van en `capturas/`. Pon `estado: publicado` cuando esté listo.
3. `git add . && git commit -m "writeup: <nombre>" && git push`.

Para certificaciones y herramientas es igual, con `scripts/nueva-certificacion.sh
<nombre>` y `scripts/nueva-herramienta.sh <nombre>`. Cada una aparece en su propia
sección del sitio en cuanto la marcas como publicada y haces push.

El índice y el sitio se regeneran solos. No hay ningún comando de publicación que
recordar: el workflow de Pages se dispara con el push a `main`.

Si el commit se rechaza, el hook de `pre-commit` dice qué falta: casi siempre un campo
del front-matter sin rellenar, un enlace roto o una sección obligatoria vacía. Se
arregla y se vuelve a commitear.

Para que los hooks se ejecuten, una vez por máquina: `pip install pre-commit && pre-commit install`.

## Qué hace cada pieza

| Pieza | Para qué sirve | ¿Se toca? |
| --- | --- | --- |
| `.plantillas/writeup.md` | El molde de cada writeup | Sí, si cambian las secciones |
| `scripts/nuevo-writeup.sh` | Crea la carpeta y copia la plantilla | Rara vez |
| `scripts/validar-writeups.py` | Comprueba metadatos y secciones | No |
| `scripts/generar-indice.py` | Rellena las tablas de índice | No |
| `scripts/generar-sitio.py` | Prepara `docs/` para el sitio | No |
| `scripts/comprobar-enlaces.py` | Comprueba enlaces relativos | No |
| `scripts/buscar-secretos.sh` | Busca claves, `.ovpn` y tokens propios | No |
| `mkdocs.yml` | Título, menú y colores del sitio | Sí |
| `requirements.txt` | Versiones fijadas de MkDocs | No |
| `.github/workflows/pages.yml` | Construye y publica el sitio | No |
| `.github/workflows/ci.yml` | Comprobaciones en cada pull request | No |
| `.pre-commit-config.yaml` | Comprueba antes de dejar commitear | No |

## Si algo falla

El único síntoma habitual es «he subido algo y el sitio no se ha actualizado»:

1. Entra en la pestaña **Actions** del repo y abre el último run en rojo. El error suele
   estar en la última línea roja del log.
2. Reprodúcelo en local: `pip install -r requirements.txt` y luego `mkdocs build --strict`.
3. Arréglalo en el contenido. Los dos fallos típicos son un enlace que apunta a un
   fichero que ya no existe y un front-matter con un campo mal escrito.

Dos cosas que no hay que hacer: desactivar comprobaciones para que pase, y cambiar
versiones a ver si así tira. Las dos convierten un fallo pequeño en uno difícil de
diagnosticar.
