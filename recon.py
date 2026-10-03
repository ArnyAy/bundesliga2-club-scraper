"""Разведка: ищем реальные страницы календаря матчей клуба."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

CANDIDATES = [
    "https://www.herthabsc.de/",
    "https://www.herthabsc.de/profis/",
    "https://www.herthabsc.de/profis/termine/",
    "https://www.herthabsc.de/profis/spielplan/",
    "https://www.herthabsc.de/profis/testspiele/",
    "https://www.herthabsc.com/en/teams/fixtures/fixtures",
]

KEYWORDS = ["testspiel", "freundschaft", "spielplan", "termine", "anstoss", "anstoß"]

print("=== ПРОВЕРКА URL ===")
saved = []
for url in CANDIDATES:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        low = r.text.lower()
        hits = {k: low.count(k) for k in KEYWORDS if low.count(k)}
        print(f"HTTP {r.status_code} | {len(r.text):>8} байт | {url}")
        print(f"    keywords: {hits} | final: {r.url}")
        if r.status_code == 200 and len(r.text) > 10000:
            fname = "debug_" + str(len(saved)) + ".html"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(r.text)
            saved.append((fname, url))
    except Exception as e:
        print(f"ERR  | {url} | {e}")

print()
print("=== ССЫЛКИ НА КАЛЕНДАРЬ С ГЛАВНОЙ ===")
try:
    r = requests.get("https://www.herthabsc.de/", headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "lxml")
    found = set()
    for a in soup.find_all("a", href=True):
        h = a["href"].lower()
        if any(k in h for k in ("termin", "spielplan", "testspiel", "fixture", "match")):
            found.add(a["href"])
    for h in sorted(found):
        print("LINK:", h)
    if not found:
        print("(ничего не найдено)")
except Exception as e:
    print("ERR:", e)

print()
print("=== СОХРАНЁННЫЕ ФАЙЛЫ ===")
for fname, url in saved:
    print(f"{fname} <- {url}")
