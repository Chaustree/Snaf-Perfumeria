import os
import json
from urllib.parse import quote
from flask import Flask, render_template, request, jsonify, session, send_from_directory, redirect, url_for

app = Flask(__name__)
app.secret_key = 'perfume_secret_key_store'

# Catálogo ampliado con metadata útil para filtros y UI
PERFUMES = [
    {
        "id": 1,
        "brand": "Afnan 9 AM Pour Femme",
        "name": "Elegancia fresca y luminosa para iniciar el día.",
        "category": "Mujer",
        "notes": "Cítrico - Floral - Afrutado",
        "price": 180000,
        "rating": 4.7,
        "image":"Afnan 9 AM Pour Femme.jpg",
        "description": "Una fragancia vibrante con notas de mandarina, bergamota y un fondo suave de almizcle."
    },
    {
        "id": 2,
        "brand": "Afnan 9 PM Night Out",
        "name": "Seducción nocturna dulce y envolvente.",
        "category": "Hombre",
        "notes": "Dulce - Ambarado - Especiado",
        "price": 195000,
        "rating": 4.9,
        "image": "Afnan 9 PM Night Out.jpg",
        "description": "Intenso aroma a manzana, canela y vainilla ideal para destacar en salidas nocturnas."
    },
    {
        "id": 3,
        "brand": "Afnan 9 PM Rebel",
        "name": "Carácter audaz y moderno con presencia única.",
        "category": "Hombre",
        "notes": "Frutal - Amaderado - Cuero",
        "price": 210000,
        "rating": 4.8,
        "image": "Afnan 9 PM Rebel.jpg",
        "description": "Mezcla de piña, piña ahumada y maderas oscuras para un perfil rebelde y elegante."
    },
    {
        "id": 4,
        "brand": "Afnan 9 PM",
        "name": "El clásico moderno de la perfumería oriental.",
        "category": "Hombre",
        "notes": "Vainilla - Especiado - Cálido",
        "price": 185000,
        "rating": 4.9,
        "image": "Afnan 9 PM.JPG",
        "description": "Un perfume icónico reconocido por su excelente proyección y fijación dulce amaderada."
    },
    {
        "id": 5,
        "brand": "Al Haramain Amber Oud Gold Edition",
        "name": "Lujo opulento y aura dorada inolvidable.",
        "category": "Unisex",
        "notes": "Dulce - Tropical - Ambarado",
        "price": 310000,
        "rating": 5.0,
        "image": "Al Haramain Amber Oud Gold Edition.jpg",
        "description": "Exquisita combinación de notas frutales, melón, ámbar y vainilla de alta sofisticación."
    },
    {
        "id": 6,
        "brand": "Armaf Club de Nuit Maleka",
        "name": "Sofisticación femenina digna de la realeza.",
        "category": "Mujer",
        "notes": "Floral - Especiado - Amaderado",
        "price": 220000,
        "rating": 4.8,
        "image": "Armaf — Club de Nuit Maleka.jpg",
        "description": "Aroma exclusivo con toques florales intensos y un fondo cálido de maderas preciosas."
    },
    {
        "id": 7,
        "brand": "Armaf Club de Nuit Milestone",
        "name": "Frescura marina sofisticada y metálica.",
        "category": "Unisex",
        "notes": "Marino - Cítrico - Amaderado",
        "price": 200000,
        "rating": 4.7,
        "image": "Armaf — Club de Nuit Milestone.jpg",
        "description": "Notas de sal marina, frutos rojos y maderas blancas con una estela limpia y lujosa."
    },
    {
        "id": 8,
        "brand": "Armaf Club de Nuit Sillage",
        "name": "Pureza cristalina y presencia radiante.",
        "category": "Unisex",
        "notes": "Cítrico - Fresco - Almizclado",
        "price": 210000,
        "rating": 4.8,
        "image": "Armaf — Club de Nuit Sillage.jpg",
        "description": "Combinación helada de bergamota, grosella negra y rosa sobre una base de almizcle."
    },
    {
        "id": 9,
        "brand": "Armaf Club de Nuit Untold",
        "name": "Un elixir misterioso de ámbar y azafrán.",
        "category": "Unisex",
        "notes": "Ambarado - Amaderado - Especiado",
        "price": 260000,
        "rating": 4.9,
        "image": "Armaf — Club de Nuit Untold.jpg",
        "description": "Notas hipnóticas de azafrán, resina de abeto y madera de cedro de gran intensidad."
    },
    {
        "id": 10,
        "brand": "Armaf Club de Nuit Woman",
        "name": "Elegancia floral clásica con matices frutales.",
        "category": "Mujer",
        "notes": "Floral - Cítrico - Pachulí",
        "price": 170000,
        "rating": 4.6,
        "image": "Armaf — Club de Nuit Woman.jpg",
        "description": "Mezcla atemporal de naranja, rosa, jazmín y pachulí de carácter refinado."
    },
    {
        "id": 11,
        "brand": "Armaf Club de Nuit Iconic",
        "name": "Frescura azul intensa y moderna.",
        "category": "Hombre",
        "notes": "Cítrico - Especiado - Amaderado",
        "price": 230000,
        "rating": 4.9,
        "image": "Armaf Club de Nuit Iconic.jpg",
        "description": "Aroma vibrante con toronja, menta, jengibre y maderas oscuras muy versátil."
    },
    {
        "id": 12,
        "brand": "Armaf Club de Nuit Impériale",
        "name": "Delicadeza oriental dulce y cautivadora.",
        "category": "Mujer",
        "notes": "Floral - Dulce - Ambarado",
        "price": 240000,
        "rating": 4.9,
        "image": "Armaf Club de Nuit Impériale.jpg",
        "description": "Notas de lichi, rosa turca, vainilla y incienso de alta perfumería."
    },
    {
        "id": 13,
        "brand": "Armaf Club de Nuit Intense Man",
        "name": "La fragancia masculina por excelencia.",
        "category": "Hombre",
        "notes": "Cítrico - Ahumado - Amaderado",
        "price": 185000,
        "rating": 5.0,
        "image": "Armaf Club de Nuit Intense Man.jpg",
        "description": "Apertura potente de limón y piña con un fondo ahumado de abedul y almizcle."
    },
    {
        "id": 14,
        "brand": "Armaf Delights Yum Yum",
        "name": "Divertida tentación gourmand y frutal.",
        "category": "Mujer",
        "notes": "Dulce - Gourmand - Frutal",
        "price": 160000,
        "rating": 4.5,
        "image": "Armaf Delights Yum Yum.JPG",
        "description": "Deliciosa mezcla de notas dulces, vainilla y frutas tropicales muy jugosa."
    },
    {
        "id": 15,
        "brand": "Armaf Odyssey Mandarin Sky",
        "name": "Dulzor cítrico y acaramelado irresistible.",
        "category": "Hombre",
        "notes": "Cítrico - Dulce - Caramelo",
        "price": 190000,
        "rating": 4.8,
        "image": "Armaf Odyssey Mandarin Sky.JPG",
        "description": "Explosión de mandarina madura, caramelo cremoso y haba tonka."
    },
    {
        "id": 16,
        "brand": "Badee Al Oud Collection Discovery Set",
        "name": "Set exclusivo con las joyas de Lattafa.",
        "category": "Unisex",
        "notes": "Ambarado - Especiado - Oud",
        "price": 260000,
        "rating": 4.9,
        "image": "Badee Al Oud Collection (Discovery Set).jpg",
        "description": "Colección de miniaturas con los aromas más icónicos a base de Oud de la casa Lattafa."
    },
    {
        "id": 17,
        "brand": "Carolina Herrera Very Good Girl",
        "name": "Pasión y audacia en un aroma inolvidable.",
        "category": "Mujer",
        "notes": "Frutal - Floral - Vainilla",
        "price": 500000,
        "rating": 4.9,
        "image": "Carolina Herrera — Very Good Girl.jpg",
        "description": "Acordes impactantes de grosella roja, lichi, rosa silvestre y vainilla."
    },
    {
        "id": 18,
        "brand": "Carolina Herrera Good Girl Miniature Set",
        "name": "Colección de lujo con los iconos taconcitos.",
        "category": "Mujer",
        "notes": "Dulce - Floral - Gourmand",
        "price": 340000,
        "rating": 5.0,
        "image": "Carolina Herrera (Good Girl Miniature Set).jpg",
        "description": "Set de miniaturas coleccionables con las versiones más famosas de Good Girl."
    },
    {
        "id": 19,
        "brand": "Carolina Herrera 212 VIP Men",
        "name": "La energía de la noche neoyorquina.",
        "category": "Hombre",
        "notes": "Fresco - Especiado - Amaderado",
        "price": 440000,
        "rating": 4.7,
        "image": "Carolina Herrera 212 VIP Men.jpg",
        "description": "Cóctel efervescente de lima, pimienta negra, vodka y madera de rey."
    },
    {
        "id": 20,
        "brand": "Carolina Herrera 212 VIP Rosé",
        "name": "Glamour y frescura de fiesta exclusiva.",
        "category": "Mujer",
        "notes": "Champaña - Frutal - Amaderado",
        "price": 460000,
        "rating": 4.8,
        "image": "Carolina Herrera 212 VIP Rosé.jpg",
        "description": "Notas efervescentes de champaña rosada, flor de durazno y madera de reina."
    },
    {
        "id": 21,
        "brand": "Dior Sauvage Eau de Toilette",
        "name": "El icono de frescura salvaje y nobleza.",
        "category": "Hombre",
        "notes": "Fresco - Especiado - Amaderado",
        "price": 540000,
        "rating": 5.0,
        "image": "Dior — Sauvage (Eau de Toilette).jpg",
        "description": "Bergamota de Reggio di Calabria y ambroxan en una composición rotundamente fresca."
    },
    {
        "id": 22,
        "brand": "Dolce & Gabbana Exclusive Miniature Set",
        "name": "Viaje sensorial por la alta perfumería italiana.",
        "category": "Unisex",
        "notes": "Cítrico - Floral - Mediterráneo",
        "price": 360000,
        "rating": 4.8,
        "image": "Dolce & Gabbana (Travel Retail Exclusive Miniature Set)v.jpg",
        "description": "Set exclusivo de viaje con las mejores creaciones mediterráneas de D&G."
    },
    {
        "id": 23,
        "brand": "Dumont Nitro Red Intensely",
        "name": "Potencia frutal y frescura magnética.",
        "category": "Hombre",
        "notes": "Frutal - Acuático - Ambarado",
        "price": 220000,
        "rating": 4.8,
        "image": "Dumont — Nitro Red Intensely.jpg",
        "description": "Mezcla intensa de manzana roja, sandía, notas marinas y ámbar de larga duración."
    },
    {
        "id": 24,
        "brand": "Dumont Nitro Red",
        "name": "Energía desbordante y presencia moderna.",
        "category": "Hombre",
        "notes": "Frutal - Fresco - Amaderado",
        "price": 200000,
        "rating": 4.7,
        "image": "Dumont Nitro Red.JPG",
        "description": "Notas vibrantes de bergamota, lavanda y maderas suaves para uso diario."
    },
    {
        "id": 25,
        "brand": "Giorgio Armani Acqua Di Giò Pour Homme",
        "name": "La frescura marina más legendaria del mundo.",
        "category": "Hombre",
        "notes": "Marino - Cítrico - Acuático",
        "price": 480000,
        "rating": 4.9,
        "image": "Giorgio Armani Acqua Di Giò Pour Homme.jpg",
        "description": "Inspirada en el mar mediterráneo con notas de bergamota, jazmín y romero."
    },
    {
        "id": 26,
        "brand": "Giorgio Armani Acqua Di Giò Profondo",
        "name": "Inmersión en la intensidad del océano.",
        "category": "Hombre",
        "notes": "Marino - Aromático - Especiado",
        "price": 520000,
        "rating": 4.9,
        "image": "Giorgio Armani Acqua Di Giò Profondo.jpg",
        "description": "Notas marinas profundas, esencias aromáticas y pachulí mineral intensos."
    },
    {
        "id": 27,
        "brand": "Jean Paul Gaultier Miniatures Set",
        "name": "Iconos de la moda en frascos de colección.",
        "category": "Unisex",
        "notes": "Dulce - Orientales - Florales",
        "price": 380000,
        "rating": 4.9,
        "image": "Jean Paul Gaultier (Miniatures Set).jpg",
        "description": "Set exclusivo con los torsos clásicos de Jean Paul Gaultier en versión miniatura."
    },
    {
        "id": 28,
        "brand": "Lattafa Liam Blue Shine",
        "name": "Frescura azul refinada de estilo árabe.",
        "category": "Unisex",
        "notes": "Cítrico - Marino - Especiado",
        "price": 150000,
        "rating": 4.6,
        "image": "Lattafa — Liam Blue Shine.jpg",
        "description": "Combinación limpia de bergamota, pimienta marina y maderas claras."
    },
    {
        "id": 29,
        "brand": "Lattafa Yara (Pink)",
        "name": "Dulzura atalcada y femenina irresistible.",
        "category": "Mujer",
        "notes": "Dulce - Atalcado - Vainilla",
        "price": 140000,
        "rating": 4.9,
        "image": "Lattafa — Yara (Pink).jpg",
        "description": "Famoso aroma cremoso con orquídea, heliotropo, frutas tropicales y vainilla."
    },
    {
        "id": 30,
        "brand": "Lattafa Asad Bourbon",
        "name": "Calidez especiada y carácter viril.",
        "category": "Hombre",
        "notes": "Especiado - Ambarado - Vainilla",
        "price": 160000,
        "rating": 4.8,
        "image": "Lattafa Asad Bourbon.JPG",
        "description": "Intensas notas de pimienta negra, café, tabaco y vainilla borbónica."
    },
    {
        "id": 31,
        "brand": "Lattafa Bade'e Al Oud Noble Blush",
        "name": "Sofisticación dulce y floral rosada.",
        "category": "Mujer",
        "notes": "Floral - Dulce - Gourmand",
        "price": 180000,
        "rating": 4.8,
        "image": "Lattafa Bade'e Al Oud Noble Blush.JPG",
        "description": "Una mezcla delicada de merengue, leche de almendras y rosas orientales."
    },
    {
        "id": 32,
        "brand": "Lattafa Pride Al Qiam Gold",
        "name": "Riqueza dorada con toques de cuero y madera.",
        "category": "Unisex",
        "notes": "Ambarado - Especiado - Cuero",
        "price": 190000,
        "rating": 4.7,
        "image": "Lattafa Pride Al Qiam Gold.JPG",
        "description": "Aroma cálido de azafrán, frambuesa, cuero suave y madera de oud."
    },
    {
        "id": 33,
        "brand": "Lattafa Yara (Rosa)",
        "name": "Encanto floral y cremoso de alta proyección.",
        "category": "Mujer",
        "notes": "Dulce - Floral - Almizclado",
        "price": 140000,
        "rating": 4.9,
        "image": "Lattafa Yara (Rosa).JPG",
        "description": "Edición especial del clásico Yara con énfasis en notas florales rosadas."
    },
    {
        "id": 34,
        "brand": "Louis Vuitton Imagination",
        "name": "Vuelo creativo de cítricos y té negro.",
        "category": "Hombre",
        "notes": "Cítrico - Ambergris - Té",
        "price": 1280000,
        "rating": 5.0,
        "image": "Louis Vuitton Imagination.jpg",
        "description": "Magistral fusión de cidra de Sicilia, té negro de China y ambrox de lujo."
    },
    {
        "id": 35,
        "brand": "Louis Vuitton L'Immensité",
        "name": "Horizontes infinitos de jengibre y frescura.",
        "category": "Hombre",
        "notes": "Especiado - Cítrico - Amaderado",
        "price": 1280000,
        "rating": 4.9,
        "image": "Louis Vuitton L'Immensité.jpg",
        "description": "Jengibre fresco, toronja y ládano para un aroma vibrante y sofisticado."
    },
    {
        "id": 36,
        "brand": "Louis Vuitton Ombre Nomade",
        "name": "El perfume supremo de Oud y rosa mística.",
        "category": "Unisex",
        "notes": "Oud - Incensado - Rosa",
        "price": 1520000,
        "rating": 5.0,
        "image": "Louis Vuitton Ombre Nomade .jpg",
        "description": "Una obra maestra de madera de agar, lágrimas de incienso y frambuesa."
    },
    {
        "id": 37,
        "brand": "Montale Paris Arabians Tonka",
        "name": "Potencia oriental de haba tonka y oud.",
        "category": "Unisex",
        "notes": "Dulce - Especiado - Oud",
        "price": 580000,
        "rating": 4.9,
        "image": "Montale Paris — Arabians Tonka.jpg",
        "description": "Mezcla fascinante de azafrán, rosa, haba tonka y madera de oud ultrapotente."
    },
    {
        "id": 38,
        "brand": "Montale Paris Crazy in Love",
        "name": "Torbellino de rosas silvestres y ámbar.",
        "category": "Mujer",
        "notes": "Floral - Ambarado - Dulce",
        "price": 560000,
        "rating": 4.8,
        "image": "Montale Paris — Crazy in Love.jpg",
        "description": "Notas apasionadas de rosa silvestre, violeta, azafrán y ámbar cálido."
    },
    {
        "id": 39,
        "brand": "Moschino Toy Miniature Collection",
        "name": "Set divertido de los icónicos ositos Moschino.",
        "category": "Mujer",
        "notes": "Floral - Frutal - Fresco",
        "price": 300000,
        "rating": 4.7,
        "image": "Moschino (Toy Miniature Collection).JPG",
        "description": "Colección de miniaturas con las distintas fragancias Toy 2 y Toy Boy."
    },
    {
        "id": 40,
        "brand": "Yara Collection Discovery Set",
        "name": "Trilogía completa de las fragancias Yara.",
        "category": "Mujer",
        "notes": "Dulce - Gourmand - Atalcado",
        "price": 220000,
        "rating": 4.9,
        "image": "Yara Collection (Discovery Set).jpg",
        "description": "Set de descubrimiento que incluye las versiones Pink, Tous y Moi de la línea Yara."
    }
]

# --- Función auxiliar para obtener los datos completos del carrito actual ---
def get_cart_details():
    cart = session.get('cart', {})
    cart_items = []
    total = 0.0
    total_count = 0

    for item_id, qty in cart.items():
        product = next((p for p in PERFUMES if str(p['id']) == str(item_id)), None)
        if product:
            item_total = product['price'] * qty
            total += item_total
            total_count += qty
            cart_items.append({
                **product,
                "quantity": qty,
                "item_total": item_total
            })
            
    return cart_items, total, total_count


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').lower()
    
    filtered = PERFUMES
    if category != 'all':
        filtered = [p for p in filtered if p['category'].lower() == category.lower()]
    if search:
        filtered = [p for p in filtered if search in p['name'].lower() or search in p['brand'].lower()]
        
    return jsonify(filtered)


@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def cart_actions():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if request.method == 'POST':
        data = request.json or {}
        product_id = str(data.get('id'))
        cart[product_id] = cart.get(product_id, 0) + 1
        session.modified = True

    elif request.method == 'DELETE':
        data = request.json or {}
        product_id = str(data.get('id'))
        if product_id in cart:
            del cart[product_id]
            session.modified = True

    cart_items, total, total_count = get_cart_details()

    return jsonify({
        "items": cart_items,
        "total": round(total, 2),
        "total_count": total_count
    })


@app.route('/favicon.ico')
def favicon():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Si viene por POST desde un formulario que envía el JSON directamente
    if request.method == 'POST' and request.form.get('cart_data'):
        cart_data = request.form.get('cart_data', '[]')
        cart_items = json.loads(cart_data)
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)
        return render_template('checkout.html', cart=cart_items, total=total)
    
    # Si viene por GET o recarga de página, recupera los datos desde session['cart']
    cart_items, total, _ = get_cart_details()
    return render_template('checkout.html', cart=cart_items, total=total)


@app.route('/confirmar-pedido', methods=['POST'])
def confirmar_pedido():
    # 1. Recibir datos del cliente desde checkout.html
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')
    metodo = request.form.get('payment_method')

    # 2. Obtener productos y total actual desde la sesión
    cart_items, total, _ = get_cart_details()

    if not cart_items:
        return redirect(url_for('home'))

    cliente = {
        'nombre': nombre,
        'telefono': telefono,
        'direccion': direccion,
        'metodo': metodo
    }

    # 3. Formatear mensaje para WhatsApp con el nombre de marca SNAF
    metodo_texto = 'Nequi / Daviplata' if metodo == 'nequi_daviplata' else 'Pago Contra Entrega'
    
    resumen_productos = ""
    for item in cart_items:
        resumen_productos += f"• {item['brand']} (x{item['quantity']}) - ${item['item_total']:,.0f}\n"

    texto_raw = (
        f"¡Hola SNAF! Realicé un nuevo pedido en la tienda.\n\n"
        f" *Cliente:* {nombre}\n"
        f" *Teléfono:* {telefono}\n"
        f" *Dirección:* {direccion}\n"
        f" *Método de Pago:* {metodo_texto}\n\n"
        f" *Detalle del Pedido:*\n{resumen_productos}\n"
        f" *Total A Pagar:* ${total:,.0f} COP\n\n"
        f"Quedo atento para coordinar el envío."
    )
    
    # Codificar el texto para que los saltos de línea y caracteres especiales funcionen en la URL de WhatsApp
    mensaje_wa = quote(texto_raw, safe='')

    # 4. Vaciar la sesión del carrito tras confirmar el pedido
    session.pop('cart', None)

    # 5. Renderizar vista final de agradecimiento
    return render_template('gracias.html', cliente=cliente, total=total, mensaje_wa=mensaje_wa)


if __name__ == '__main__':
    app.run(debug=True)