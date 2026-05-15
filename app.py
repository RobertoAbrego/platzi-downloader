from yt_dlp import YoutubeDL
from pathlib import Path
import subprocess

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

def main():
    convert_cookies()

    urls = load_urls()

    ydl_opts = {
        "cookiefile": COOKIE_FILE,
        "outtmpl": DOWNLOAD_PATH,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "http_headers": HEADERS,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

if __name__ == "__main__":
    main()