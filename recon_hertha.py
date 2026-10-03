"""Разведка страницы календаря Hertha BSC."""
import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

URL = "https://www.herthabsc.com/de/mannschaften/spielplaene/spielplan"

print(f"=== ЗАГРУЗКА {URL} ===")
r = requests.get(URL, headers=HEADERS, timeout=20)
print(f"HTTP {r.status_code} | {len(r.text)} байт")

if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    
    print("\n=== ПОИСК СТРУКТУРЫ МАТЧЕЙ ===")
    
    # Ищем все элементы с классами, содержащими "match", "game", "fixture"
    for tag in soup.find_all(["div", "article", "li", "section"]):
        classes = " ".join(tag.get("class", []))
        if any(kw in classes.lower() for kw in ["match", "game", "fixture", "spiel"]):
            print(f"\n--- Найдено: {tag.name} class='{classes}' ---")
            print(tag.prettify()[:1000])
            break
    
    print("\n=== ПОИСК JSON/API ДАННЫХ ===")
    # Ищем встроенный JSON (React/Vue часто кладут данные в скрипты)
    for script in soup.find_all("script"):
        if script.string and ("matches" in script.string or "fixtures" in script.string or "games" in script.string):
            print(f"\n--- Скрипт с данными ---")
            print(script.string[:500])
    
    print("\n=== ВСЕ ССЫЛКИ НА МАТЧИ ===")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "match" in href.lower() or "spiel" in href.lower() or "fixture" in href.lower():
            text = a.get_text(strip=True)[:50]
            print(f"{text} -> {href}")
    
    # Сохраняем HTML для детального анализа
    with open("hertha_spielplan.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("\n✓ Сохранено: hertha_spielplan.html")

else:
    print("✗ Не удалось загрузить")
