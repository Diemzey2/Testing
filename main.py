from flask import Flask, request, jsonify
import os
from bs4 import BeautifulSoup  # Importa BeautifulSoup aquí para poder usarlo en la detección
from extractors import amazon, mercadolibre, promodescuentos

app = Flask(__name__)

# Asegúrate de que el directorio de archivos HTML existe
directory = "html_files"
if not os.path.exists(directory):
    os.makedirs(directory)

@app.route('/submit-html', methods=['POST'])
def receive_html():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    html_content = data.get('html')
    if not html_content:
        return jsonify({"error": "No HTML provided"}), 400

    # Usa BeautifulSoup para buscar en el contenido HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup.find("a", class_="cept-tt thread-link linkPlain thread-title--list js-thread-title"):
        response = promodescuentos.process_promodescuentos(html_content, directory)
    elif 'amazon.com' in html_content:
        response = amazon.process_amazon(html_content, directory)
    elif 'mercadolibre.com.mx' in html_content:
        response = mercadolibre.process_mercadolibre(html_content, directory)
    else:
        response = {"error": "Unknown HTML source"}, 500

    return jsonify(response), response[1]

if __name__ == '__main__':
    app.run(debug=True, port=8000)
