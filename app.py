from yt_dlp import YoutubeDL
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import requests
import subprocess
import re
import os
import time

BASE_URL = "https://platzi.com"

COURSE_URL = "https://platzi.com/cursos/docker-avanzado/"

DOWNLOAD_PATH = "/downloads/%(title)s.%(ext)s"

COOKIE_FILE = "/cookies/cookies.txt"

HEADERS = {
    "Referer": "https://platzi.com/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}


def convert_cookies():

    print("\nConvirtiendo cookies...")

    subprocess.run(
        ["python", "convert_cookies.py"],
        check=True
    )

    print("cookies.txt generado")


def get_course_classes(course_url):

    print("\nObteniendo clases del curso:")
    print(course_url)

    response = requests.get(
        course_url,
        headers=HEADERS
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    classes = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        # detectar clases reales
        if re.match(r"^/cursos/.+/.+/$", href):

            if "opiniones" in href:
                continue

            if "faq" in href:
                continue

            full_url = BASE_URL + href

            if full_url not in classes:
                classes.append(full_url)

    print(f"\nClases encontradas: {len(classes)}")

    return classes


def parse_netscape_cookies(path):

    cookies = []

    if not os.path.exists(path):
        raise Exception("No existe cookies.txt")

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            if line.startswith("#"):
                continue

            if not line.strip():
                continue

            parts = line.strip().split("\t")

            if len(parts) != 7:
                continue

            domain, flag, path_, secure, expiration, name, value = parts

            cookies.append({
                "domain": domain,
                "path": path_,
                "name": name,
                "value": value,
                "secure": secure.upper() == "TRUE",
                "httpOnly": False
            })

    print(f"\nCookies cargadas: {len(cookies)}")

    return cookies


def get_m3u8(platzi_url):

    found = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--autoplay-policy=no-user-gesture-required"
            ]
        )

        context = browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={
                "width": 1920,
                "height": 1080
            }
        )

        # cargar cookies REALES
        cookies = parse_netscape_cookies(COOKIE_FILE)

        context.add_cookies(cookies)

        page = context.new_page()

        # bloquear cosas innecesarias
        page.route(
            "**/*",
            lambda route: (
                route.abort()
                if route.request.resource_type in [
                    "image",
                    "font",
                    "stylesheet"
                ]
                else route.continue_()
            )
        )

        def handle_response(response):

            url = response.url

            if ".m3u8" not in url:
                return

            if "mediastream" not in url:
                return

            if url not in found:

                found.append(url)

                print("\nM3U8 REAL:")
                print(url)

        page.on("response", handle_response)

        print(f"\nAbriendo: {platzi_url}")

        try:

            # IMPORTANTE:
            # domcontentloaded en vez de networkidle
            # porque Platzi deja conexiones abiertas
            page.goto(
                platzi_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

        except Exception as e:

            print("\nWARNING EN GOTO:")
            print(e)

        # esperar reproductor
        try:

            page.wait_for_selector(
                "video",
                timeout=20000
            )

            print("\nVideo encontrado")

        except:

            print("\nNo apareció el video")

        # intentar reproducir
        try:

            page.evaluate("""
                async () => {

                    const video = document.querySelector("video");

                    if(video){

                        video.muted = true;

                        try{
                            await video.play();
                        }catch(e){}

                    }
                }
            """)

        except Exception as e:

            print("\nError reproduciendo video")
            print(e)

        # esperar requests del stream
        print("\nEsperando stream...")

        page.wait_for_timeout(15000)

        browser.close()

    print(f"\nSe encontraron {len(found)} m3u8 reales")

    return found

def get_course_slug(course_url):

    # docker-avanzado
    return course_url.rstrip("/").split("/")[-1]


def get_lesson_slug(lesson_url):

    # optimizacion-avanzada-de-docker-para-clo
    return lesson_url.rstrip("/").split("/")[-1]


def create_course_folder(course_slug):

    folder = f"/downloads/{course_slug}"

    os.makedirs(folder, exist_ok=True)

    return folder


def build_video_path(course_slug, lesson_slug, index):

    folder = create_course_folder(course_slug)

    filename = f"Clase{index:02d}-{lesson_slug}.mp4"

    full_path = os.path.join(folder, filename)

    return full_path


def download_video(video_url, output_path):

    ydl_opts = {

        "cookiefile": COOKIE_FILE,

        # nombre FINAL
        "outtmpl": output_path,

        "format": "bestvideo+bestaudio/best",

        "merge_output_format": "mp4",

        "ignoreerrors": True,

        "http_headers": HEADERS,

        "concurrent_fragment_downloads": 10,

        "retries": 20,

        "fragment_retries": 20,

        "nopart": True,

        "quiet": False,

        "no_warnings": False,

        "hls_prefer_native": False,

        "downloader": "ffmpeg",

        "downloader_args": {
            "ffmpeg": [
                "-loglevel", "warning"
            ]
        }
    }

    print("\nDescargando:")
    print(video_url)

    print("\nGuardando en:")
    print(output_path)

    with YoutubeDL(ydl_opts) as ydl:

        ydl.download([video_url])

def main():

    convert_cookies()

    lessons = get_course_classes(COURSE_URL)

    if not lessons:

        print("\nNo se encontraron clases")
        return

    print("\nIniciando descarga del curso completo...\n")

    downloaded = set()

    for index, lesson_url in enumerate(lessons, start=1):

            course_slug = get_course_slug(COURSE_URL)

    for index, lesson_url in enumerate(lessons, start=1):

        print("\n" + "=" * 60)
        print(f"Clase {index}/{len(lessons)}")
        print("=" * 60)

        try:

            lesson_slug = get_lesson_slug(lesson_url)

            output_path = build_video_path(
                course_slug,
                lesson_slug,
                index
            )

            # verificar si ya existe
            if os.path.exists(output_path):

                print("\nEl archivo ya existe:")
                print(output_path)

                continue

            m3u8_links = get_m3u8(lesson_url)

            if not m3u8_links:

                print("\nNo se encontró ningún m3u8 válido")
                continue

            video_url = m3u8_links[-1]

            if video_url in downloaded:

                print("\nVideo ya descargado")
                continue

            downloaded.add(video_url)

            download_video(
                video_url,
                output_path
            )

            print("\nEsperando siguiente clase...\n")

            time.sleep(3)

        except Exception as e:

            print("\nERROR GENERAL:")
            print(e)

    print("\nCurso descargado")


if __name__ == "__main__":
    main()