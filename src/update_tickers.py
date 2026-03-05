import pandas as pd

WIKI_URL = "https://es.wikipedia.org/wiki/IBEX_35"

def main():
    # Lee tablas de la página; una de ellas contiene las empresas y el ticker
    tables = pd.read_html(WIKI_URL)
    # Buscamos una tabla que tenga una columna tipo "Ticker" o "Símbolo"
    candidates = []
    for t in tables:
        cols = [c.lower() for c in t.columns.astype(str)]
        if any("ticker" in c or "símbolo" in c or "simbolo" in c for c in cols):
            candidates.append(t)

    if not candidates:
        raise RuntimeError("No encontré una tabla con tickers en la página.")

    df = candidates[0].copy()
    df.columns = [c.strip() for c in df.columns.astype(str)]

    # Intentamos localizar la columna de ticker
    ticker_col = None
    for c in df.columns:
        cl = c.lower()
        if "ticker" in cl or "símbolo" in cl or "simbolo" in cl:
            ticker_col = c
            break
    if ticker_col is None:
        raise RuntimeError("No encontré la columna de ticker.")

    tickers = (
        df[ticker_col]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", "", regex=True)
        .str.upper()
    )

    # Convertimos a formato Yahoo (Madrid): <TICKER>.MC
    # Ej: SAN -> SAN.MC
    tickers = tickers[tickers != "NAN"].tolist()
    tickers = [t + ".MC" if not t.endswith(".MC") else t for t in tickers]

    out = pd.DataFrame({"Ticker": tickers})
    out.to_csv("data/tickers.csv", index=False)
    print(f"Actualizado data/tickers.csv con {len(out)} tickers.")

if __name__ == "__main__":
    main()
