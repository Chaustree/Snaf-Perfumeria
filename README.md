Markdown# 💎 Aura - Perfumería de Lujo

**Aura** es una aplicación web e-commerce interactiva y moderna para la exhibición y gestión de compras de fragancias exclusivas. Construida con un backend en Python (Flask) y un frontend con JavaScript nativo y CSS personalizado con estética *Dark Luxury*.

---

## 🚀 Características Principales

* **Backend Dinámico (Flask):**
  * Catálogo estructurado de productos con metadata (marca, categoría, notas olfativas, precio, valoración).
  * API RESTful para consulta de productos y filtrado interactivo.
  * Gestión de carrito de compras almacenado en sesión de usuario (`Flask Session`).
  * Cálculo dinámico y formateado de totales e ítems acumulados.

* **Frontend Interactivo y Moderno:**
  * **Filtros en tiempo real:** Búsqueda por texto y filtrado por categoría (Hombre, Mujer, Todos) sin recargar la página.
  * **Panel de Carrito Deslizable (Slide-over Cart):** Experiencia de usuario fluida mediante consumo de la API vía `fetch`.
  * **Diseño Dark Luxury:** Paleta de colores oscura con acentos dorados (`#d4af37`), bordes sutiles, efectos *glassmorphism* y animaciones suaves.

---

## 📂 Estructura del Proyecto

```text
perfume-store/
├── app.py                 # Servidor Flask y endpoints API
├── static/
│   ├── css/
│   │   └── style.css      # Estilos UI (Dark Luxury Theme)
│   └── img/               # Imágenes del catálogo de perfumes
└── templates/
    └── index.html         # Plantilla principal y cliente JS
🛠️ Tecnologías UtilizadasBackend: Python 3.x, FlaskFrontend: HTML5, CSS3 (Variables CSS, Flexbox, Grid), JavaScript (ES6+ Fetch API)Iconos y Fuentes: FontAwesome 6, Font Stack del sistema (Segoe UI, sans-serif)📋 Requisitos PreviosAsegúrate de tener instalado en tu sistema:Python 3.8+pip (gestor de paquetes de Python)⚙️ Instalación y ConfiguraciónClonar o descargar el repositorio:Bashgit clone [https://github.com/tu-usuario/aura-perfumery.git](https://github.com/tu-usuario/aura-perfumery.git)
cd aura-perfumery
Crear y activar un entorno virtual (recomendado):Bash# En Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# En Windows:
python -m venv venv
venv\Scripts\activate
Instalar dependencias:Bashpip install flask
Estructura de imágenes:Asegúrate de colocar las imágenes del catálogo dentro de la carpeta static/img/ (por ejemplo: bleu.png).🏁 Ejecución del ProyectoPara iniciar el servidor de desarrollo local:Bashpython app.py
Accede desde tu navegador web a la siguiente dirección:Plaintext[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
📡 Endpoints de la APIMétodoEndpointDescripciónParámetros Query / BodyGET/Renderiza la vista principal (index.html)N/AGET/api/productsObtiene la lista filtrada de perfumescategory (all, hombre, mujer)search (texto a buscar)GET/api/cartObtiene el estado actual del carrito de la sesiónN/APOST/api/cartAñade una unidad del producto al carrito{ "id": 1 }DELETE/api/cartElimina un producto por completo del carrito{ "id": 1 }🎨 Capturas de Pantalla / PrevisualizaciónHome & Grid: Visualización responsiva de fragancias con tarjetas flotantes.Carrito Deslizable: Despliegue lateral dinámico con badge de conteo en la barra superior.