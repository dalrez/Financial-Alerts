import pandas as pd
import requests
from io import StringIO

URLS = [
    "https://es.wikipedia.org/wiki/IBEX_35",
    "https://en.wikipedia.org/wiki/IBEX_35",
]

HEADERS = {
    # Un User-Agent “real” para evitar 403
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

def fetch_html():
    last_err = None
    for url in URLS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            return r.text, url
        except Exception as e:
            last_err = e
    raise RuntimeError(f"No pude descargar ninguna página de Wikipedia. Último error: {last_err}")

def extract_tickers_from_tables(tables):
    # Buscamos una columna que parezca ticker/symbol
    for t in tables:
        cols = [str(c).strip() for c in t.columns]
        cols_l = [c.lower() for c in cols]

        # posibles nombres de columna
        candidates = []
        for i, c in enumerate(cols_l):
            if "ticker" in c or "símbolo" in c or "simbolo" in c or "symbol" in c:
                candidates.append(cols[i])

        if not candidates:
            continue

        ticker_col = candidates[0]
        tickers = (
            t[ticker_col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", "", regex=True)
            .str.upper()
        )

        # limpia valores raros
        tickers = [x for x in tickers.tolist() if x and x != "NAN"]

        # formato Yahoo Madrid: .MC
        tickers = [x if x.endswith(".MC") else f"{x}.MC" for x in tickers]

        # quita duplicados manteniendo orden
        seen = set()
        tickers_unique = []
        for x in tickers:
            if x not in seen:
                seen.add(x)
                tickers_unique.append(x)

        # un IBEX35 debería rondar 35 (puede variar si la tabla cambia)
        if len(tickers_unique) >= 20:
            return tickers_unique

    raise RuntimeError("No encontré una tabla válida con tickers en Wikipedia.")

def main():
    html, used_url = fetch_html()
    tables = pd.read_html(StringIO(html))

    tickers = extract_tickers_from_tables(tables)
    out = pd.DataFrame({"Ticker": tickers})
    out.to_csv("data/tickers.csv", index=False)

    print(f"OK: actualizado data/tickers.csv con {len(out)} tickers desde {used_url}")

if __name__ == "__main__":
    main()
