import os
import json
from bs4 import BeautifulSoup
import uuid

def normalize_value(value):
    return value.strip() if value else ""

def extract_information_amazon(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    resultados = []
    
    productos = soup.find_all('div', {'data-cy': 'title-recipe'})

    for producto in productos:
        titulo_elemento = producto.find('h2', {'class': 'a-size-mini'})
        if titulo_elemento:
            titulo = normalize_value(titulo_elemento.find('span', {'class': 'a-text-normal'}).text)
            link_element = titulo_elemento.find('a', {'class': 'a-link-normal'})
            enlace = "https://www.amazon.com" + link_element.get('href') if link_element else ""
        
        # Extracción de la calificación usando el selector específico
        calificacion_elemento = producto.find('i', {'data-cy': 'reviews-ratings-slot'})
        calificacion_span = calificacion_elemento.find('span', {'class': 'a-icon-alt'}) if calificacion_elemento else None
        calificacion = normalize_value(calificacion_span.text) if calificacion_span else ""

        precio_elemento = producto.find('span', {'class': 'a-price-whole'})
        if precio_elemento:
            simbolo_precio = precio_elemento.parent.find('span', {'class': 'a-price-symbol'})
            decimal_precio = precio_elemento.find('span', {'class': 'a-price-decimal'})
            fraccion_precio = precio_elemento.parent.find('span', {'class': 'a-price-fraction'})

            simbolo = normalize_value(simbolo_precio.text) if simbolo_precio else "$"
            entero = normalize_value(precio_elemento.text) if precio_elemento else ""
            decimal = normalize_value(decimal_precio.text) if decimal_precio else "."
            fraccion = normalize_value(fraccion_precio.text) if fraccion_precio else "00"

            precio = f"{simbolo}{entero}{decimal}{fraccion}"
        else:
            precio = ""
        
        resultados.append({
            "titulo": titulo,
            "enlace": enlace,
            "calificacion": calificacion,
            "precio": precio
        })

    return resultados

def process_amazon(html_content, directory):
    productos = extract_information_amazon(html_content)
    if productos:
        filename = os.path.join(directory, "amazon.json")
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
