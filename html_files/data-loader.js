const jsonFiles = [
    { file: "amazon.json", type: "amazon", table: "#amazonTable" },
    { file: "mercadolibre.json", type: "mercadolibre", table: "#mercadolibreTable" },
    { file: "promodescuentos.json", type: "promodescuentos", table: "#promodescuentosTable" }
];

async function loadAndDisplayProducts() {
    for (let entry of jsonFiles) {
        try {
            const response = await fetch(entry.file);
            const products = await response.json();
            const tbody = document.querySelector(entry.table + ' tbody');

            products.forEach(product => {
                const row = document.createElement('tr');
                const data = formatProductData(product, entry.type);
                row.innerHTML = data;
                tbody.appendChild(row);
            });

            $(entry.table).DataTable({
                "order": [[1, "desc"]]
            });
        } catch (error) {
            console.error('Error loading or parsing JSON:', error);
        }
    }
}

function formatProductData(product, type) {
    switch (type) {
        case 'amazon':
            return `
                <td>${product.titulo}</td>
                <td>${product.precio || 'No disponible'}</td>
                <td><a href="${product.enlace}">Ver</a></td>
                <td>${product.calificacion || 'No disponible'}</td>
            `;
        case 'mercadolibre':
            return `
                <td>${product.titulo}</td>
                <td>${product.precio}</td>
                <td><a href="${product.enlace}">Ver</a></td>
                <td>${product.envio_gratis || 'No'}</td>
                <td>${product.calificacion}</td>
            `;
        case 'promodescuentos':
            return `
                <td>${product.title}</td>
                <td>${product.price}</td>
                <td><a href="${product.link}">Ver</a></td>
                <td>${new Date(product.published_at * 1000).toLocaleDateString()}</td>
                <td>${product.temperature}°</td>
            `;
    }
}

window.onload = loadAndDisplayProducts;
