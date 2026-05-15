@echo off

set URL=%1

if "%URL%"=="" (
    echo Debes pasar una URL
    pause
    exit
)

docker compose run --rm downloader yt-dlp ^
--cookies /cookies/cookies.txt ^
-o "/downloads/%%(title)s.%%(ext)s" ^
"%URL%"

pause