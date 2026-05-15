import json
from pathlib import Path

INPUT_FILE = "/cookies/cookies.json"
OUTPUT_FILE = "/cookies/cookies.txt"

HEADER = """# Netscape HTTP Cookie File
# This file was generated automatically.

"""

def bool_to_str(value):
    return "TRUE" if value else "FALSE"

def convert():
    input_path = Path(INPUT_FILE)

    if not input_path.exists():
        print("cookies.json no existe")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    lines = [HEADER]

    for cookie in cookies:
        domain = cookie.get("domain", "")
        include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
        path = cookie.get("path", "/")
        secure = bool_to_str(cookie.get("secure", False))
        expiration = int(cookie.get("expirationDate", 0))
        name = cookie.get("name", "")
        value = cookie.get("value", "")

        line = "\t".join([
            domain,
            include_subdomains,
            path,
            secure,
            str(expiration),
            name,
            value
        ])

        lines.append(line + "\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"cookies.txt generado en {OUTPUT_FILE}")

if __name__ == "__main__":
    convert()