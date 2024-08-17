import os
import json
from bs4 import BeautifulSoup

def normalize_value(value):
    return value.strip() if value else ""

def extract_information_mercadolibre(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    productos = soup.find_all('div', {'class': 'ui-search-result__content-wrapper'})
    resultados = []
    for producto in productos:
        titulo_elemento = producto.find('a', {'class': 'ui-search-link'})
        precio_elemento = producto.find('span', {'role': 'img'})
        mensualidades_elemento = producto.find('span', {'class': 'ui-search-installments ui-search-color--LIGHT_GREEN'})
        envio_gratis_elemento = producto.find('span', {'class': 'ui-pb-highlight'})
        precio_anterior_elemento = producto.find('s', {'class': 'andes-money-amount ui-search-price__part ui-search-price__part--small ui-search-price__original-value'})
        calificacion_elemento = producto.find('div', {'class': 'ui-search-reviews'})

        if titulo_elemento and precio_elemento:
            titulo = normalize_value(titulo_elemento.find('h2', {'class': 'ui-search-item__title'}).text)
            precio = normalize_value(precio_elemento.get('aria-label', '').split()[-2]).replace(',', '')
            enlace = normalize_value(titulo_elemento.get('href'))
            
            mensualidades = normalize_value(mensualidades_elemento.text) if mensualidades_elemento else ""
            envio_gratis = normalize_value(envio_gratis_elemento.text) if envio_gratis_elemento else ""
            precio_anterior = normalize_value(precio_anterior_elemento.text) if precio_anterior_elemento else ""
            calificacion = normalize_value(calificacion_elemento.text) if calificacion_elemento else ""
            
            resultados.append({
                "titulo": titulo,
                "precio": precio,
                "enlace": enlace,
                "mensualidades": mensualidades,
                "envio_gratis": envio_gratis,
                "precio_anterior": precio_anterior,
                "calificacion": calificacion
            })
    return resultados

def process_mercadolibre(html_content, directory):
    productos = extract_information_mercadolibre(html_content)
    if productos:
        filename = os.path.join(directory, "mercadolibre.json")
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
