import os
import json
import uuid
from bs4 import BeautifulSoup

def normalize_value(value):
    return value.strip() if value else ""

def extract_information_promodescuentos(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    results = []
    articles = soup.find_all("article")

    for article in articles:
        try:
            img_data = json.loads(article.select_one('div[class*="image"]').find("div", {"data-vue2": True})["data-vue2"])
            url = img_data["props"]["threadImageUrl"]
            data_vue2 = article.find("div", {"data-vue2": True})["data-vue2"]
            data = json.loads(data_vue2)

            if data["props"]["thread"]["isExpired"] or not data["props"]["thread"].get("link"):
                continue  # Si el thread está expirado o falta el link, se salta el artículo

            if not url.startswith("http"):  # Comprueba si la URL de la imagen parece válida
                continue  # Salta este artículo si la URL de la imagen no es válida

            promo_article = {
                "title": data["props"]["thread"]["title"],
                "temperature": data["props"]["thread"]["temperature"],
                "link": data["props"]["thread"]["link"],
                "merchant_name": data["props"]["thread"]["merchant"]["merchantName"],
                "published_at": data["props"]["thread"]["publishedAt"],
                "old_price": data["props"]["thread"]["nextBestPrice"],
                "price": data["props"]["thread"]["price"],
                "imgurl": url
            }

            results.append(promo_article)
        except Exception as e:
            print(f"Error parsing article data: {e}")

    return results

def process_promodescuentos(html_content, directory):
    productos = extract_information_promodescuentos(html_content)
    if productos:
        filename = os.path.join(directory, "promodescuentos.json")
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(productos, file, ensure_ascii=False, indent=4)
            return {"message": f"JSON saved to {filename}"}, 200
        except Exception as e:
            return {"error": f"Error saving JSON to file: {e}"}, 500
    else:
        filename = os.path.join(directory, f"{uuid.uuid4()}.html")
        try:
            with open(filename, 'w') as file:
                file.write(html_content)
            return {"message": f"HTML saved to {filename}"}, 200
        except Exception as e:
            return {"error": f"Error saving HTML to file: {e}"}, 500