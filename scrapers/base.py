import re
import logging
import requests
from datetime import date
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


class BaseClubScraper:
    """Базовый класс для парсера официального сайта клуба.

    Наследник обязан задать CLUB_NAME, CLUB_URL, SOURCE
    и реализовать метод scrape().
    """

    CLUB_NAME = ""
    CLUB_URL = ""
    SOURCE = ""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.log = logging.getLogger(self.CLUB_NAME or self.__class__.__name__)

    # ---------- загрузка страницы ----------
    def fetch(self, url: str = None, timeout: int = 25) -> str:
        r = self.session.get(url or self.CLUB_URL, timeout=timeout)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
        return r.text

    def soup(self, url: str = None):
        return BeautifulSoup(self.fetch(url), "lxml")

    # ---------- разбор даты/времени (немецкие форматы) ----------
    @staticmethod
    def parse_date_de(text: str):
        m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", text)
        if not m:
            return None
        try:
            return date(int(m[3]), int(m[2]), int(m[1]))
        except ValueError:
            return None

    @staticmethod
    def parse_time_de(text: str) -> str:
        m = re.search(r"\b(\d{1,2}:\d{2})\b", text)
        return m[1] if m else ""

    # ---------- фильтры ----------
    FRIENDLY_HINTS = ("testspiel", "freundschaft", "friendly", "test match")
    SKIP_HINTS = ("u17", "u19", "u21", "u23", "frauen", "women",
                  "legenden", "traditionself", "allstars")

    def is_friendly(self, *texts: str) -> bool:
        t = " ".join(texts).lower()
        if any(h in t for h in self.SKIP_HINTS):
            return False
        return any(h in t for h in self.FRIENDLY_HINTS)

    # ---------- сборка матча ----------
    def make_match(self, d: date, home: str, away: str,
                   time_str: str = "", venue: str = "") -> dict:
        return {
            "date": d.isoformat(),
            "time": time_str,
            "home": home.strip(),
            "away": away.strip(),
            "venue": venue.strip(),
            "source": self.SOURCE or self.CLUB_NAME,
            "url": self.CLUB_URL,
        }

    # ---------- обязательный метод наследника ----------
    def scrape(self) -> list:
        raise NotImplementedError
