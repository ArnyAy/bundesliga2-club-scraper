from datetime import date

# Список клубов 2. Bundesliga 2026/27
# URL пока ориентировочные — уточним для каждого клуба при написании парсера
CLUBS = [
    {"name": "Hertha BSC", "city": "Berlin"},
    {"name": "Hannover 96", "city": "Hannover"},
    {"name": "1. FC Kaiserslautern", "city": "Kaiserslautern"},
    {"name": "1. FC Magdeburg", "city": "Magdeburg"},
    {"name": "1. FC Nürnberg", "city": "Nürnberg"},
    {"name": "Karlsruher SC", "city": "Karlsruhe"},
    {"name": "SV Darmstadt 98", "city": "Darmstadt"},
    {"name": "Dynamo Dresden", "city": "Dresden"},
    {"name": "SpVgg Greuther Fürth", "city": "Fürth"},
    {"name": "FC Schalke 04", "city": "Gelsenkirchen"},
    {"name": "SC Paderborn 07", "city": "Paderborn"},
    {"name": "VfL Bochum", "city": "Bochum"},
    {"name": "Fortuna Düsseldorf", "city": "Düsseldorf"},
    {"name": "Holstein Kiel", "city": "Kiel"},
    {"name": "Eintracht Braunschweig", "city": "Braunschweig"},
    {"name": "SV 07 Elversberg", "city": "Spiesen-Elversberg"},
    {"name": "Preußen Münster", "city": "Münster"},
    {"name": "SSV Ulm 1846", "city": "Ulm"},
]

END_DATE = date(2026, 12, 31)
