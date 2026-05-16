# Platzi Downloader

Descarga cursos de Platzi automáticamente utilizando:

- Docker
- Playwright
- yt-dlp
- ffmpeg

El proyecto detecta automáticamente los streams `.m3u8`, descarga los videos y organiza las clases por curso.

---

# Características

- Descarga cursos completos
- Detecta automáticamente videos HLS (`m3u8`)
- Organización automática por carpetas
- Numeración automática de clases
- Evita descargar archivos repetidos
- Funciona dentro de Docker
- Compatible con cursos privados usando cookies reales

---

# Requisitos

- Docker Desktop
- Cuenta de Platzi con acceso al curso

---

# Estructura del proyecto

```text
platzi-downloader/
│
├── cookies/
│   ├── cookies.json
│   └── cookies.txt
│
├── downloads/
│
├── app.py
├── convert_cookies.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

# Configurar cookies

## 1. Inicia sesión en Platzi

Abre:

```text
https://platzi.com
```

e inicia sesión normalmente.

---

## 2. Instala la extensión

Instala:

[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

---

## 3. Exporta las cookies

Con Platzi abierto:

1. Abre la extensión
2. Presiona **"Copy"**
3. Copia el contenido generado

---

## 4. Guarda las cookies

Crea el archivo:

```text
cookies/cookies.json
```

y pega el contenido copiado.

---

# Configurar el curso

En `app.py` cambia:

```python
COURSE_URL = "https://platzi.com/cursos/docker-avanzado/"
```

por el curso que deseas descargar.

---

# Ejecutar el proyecto

```bash
docker compose up --build
```

---

# Resultado

Los videos descargados aparecerán automáticamente en:

```text
downloads/nombre-del-curso/
```

Ejemplo:

```text
downloads/docker-avanzado/

├── Clase01-optimizacion-avanzada-de-docker.mp4
├── Clase02-docker-productivo-vs-comandos-basicos.mp4
├── Clase03-docker-multi-stage.mp4
```

---

# Cómo funciona

El flujo de la aplicación es:

```text
Cookies
   ↓
Playwright abre Platzi
   ↓
Detecta tráfico m3u8
   ↓
yt-dlp descarga segmentos HLS
   ↓
ffmpeg une audio + video
   ↓
MP4 final
```

---

# Tecnologías utilizadas

- Python
- Playwright
- yt-dlp
- ffmpeg
- Docker
- BeautifulSoup

---

# Notas

- Algunos cursos pueden tener clases sin video.
- Si una clase falla, el proceso continúa automáticamente.
- Los archivos existentes no se sobrescriben.
- El proyecto requiere cookies válidas para acceder a contenido premium.

---

# Uso educativo

Este proyecto fue creado con fines educativos y de automatización personal.
