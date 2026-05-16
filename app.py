from yt_dlp import YoutubeDL
from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess
import requests

URLS_FILE = "urls.txt"

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
    subprocess.run(["python", "convert_cookies.py"])

def load_urls():
    path = Path(URLS_FILE)

    if not path.exists():
        print("No existe urls.txt")
        return []

    with open(path, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f.readlines()
            if line.strip()
        ]


def get_m3u8(platzi_url):

    found = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        context = browser.new_context(
            user_agent=HEADERS["User-Agent"]
        )

        page = context.new_page()

        def handle_response(response):

            url = response.url

            if ".m3u8" in url:

                if url not in found:
                    found.append(url)

                    print(f"M3U8 detectado: {url}")

        page.on("response", handle_response)

        page.goto(platzi_url)

        # esperar más tiempo
        page.wait_for_timeout(20000)

        browser.close()

    print(f"\nSe encontraron {len(found)} m3u8\n")

    valid = []

    for url in found:

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code == 200:

                print(f"VALIDO: {url}")

                valid.append(url)

            else:
                print(f"INVALIDO ({response.status_code}): {url}")

        except Exception as e:
            print(f"ERROR: {url} -> {e}")

    return valid

def main():

    convert_cookies()

    platzi_urls = load_urls()

    if not platzi_urls:
        print("No hay URLs")
        return

    ydl_opts = {
        "cookiefile": COOKIE_FILE,
        "outtmpl": DOWNLOAD_PATH,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "http_headers": HEADERS,
    }

    for platzi_url in platzi_urls:

        print(f"Abriendo: {platzi_url}")

        m3u8_links = get_m3u8(platzi_url)

        if not m3u8_links:
            print("No se encontró ningún m3u8 válido")
            continue

        video_url = m3u8_links[0]

        print(f"Descargando: {video_url}")

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

if __name__ == "__main__":
    main()