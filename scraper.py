import requests
from bs4 import BeautifulSoup


def buscar_productos_ml(keyword):
    """
    Devuelve una lista de dicts con keys: title, price, url, thumbnail.
    Adaptado a la nueva estructura de Mercado Libre (clases 'poly-card', etc.).
    """
    url = f"https://listado.mercadolibre.com.ar/{keyword.replace(' ', '-')}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MiScraper/1.0)"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select("li.ui-search-layout__item")
    print(f"[DEBUG] Encontré {len(cards)} cards")  # debug

    resultados = []
    for card in cards:
        # Título y enlace
        title_link = card.select_one(
            "h3.poly-component__title-wrapper > a.poly-component__title"
        )
        # Precio actual: símbolo + fracción
        price_symbol = card.select_one(
            "div.poly-component__price span.andes-money-amount__currency-symbol"
        )
        price_fraction = card.select_one(
            "div.poly-component__price span.andes-money-amount__fraction"
        )
        # Imagen
        img = card.select_one("figure.poly-component__image-wrapper img")

        if title_link and price_symbol and price_fraction:
            title = title_link.get_text(strip=True)
            url_item = title_link["href"]
            price = f"{price_symbol.get_text(strip=True)}{price_fraction.get_text(strip=True)}"
            thumb = img["src"] if img and img.get("src") else ""

            resultados.append(
                {"title": title, "price": price, "url": url_item, "thumbnail": thumb}
            )
    return resultados
