from pathlib import Path
from decimal import Decimal
import csv
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog_bulk.csv"
HTML_FILES = [ROOT / "index.html", ROOT / "purograne.html"]
APPS_SCRIPT = ROOT / "CadastroUnificado.gs"
README = ROOT / "README.md"

CATEGORY_LABELS = {
    "cereais": "Cereais e grãos",
    "leguminosas": "Leguminosas",
    "sementes": "Sementes",
    "chas": "Chás",
    "ervas": "Ervas e raízes",
    "temperos": "Temperos",
    "farinhas": "Farinhas e farelos",
    "oleaginosas": "Castanhas e oleaginosas",
    "frutas": "Frutas e vegetais secos",
    "snacks": "Snacks",
    "chocolates": "Chocolates e drágeas",
    "funcionais": "Funcionais e superalimentos",
    "suplementos": "Suplementos a granel",
    "adocantes": "Açúcares e adoçantes",
    "cogumelos": "Cogumelos secos",
    "culinarios": "Ingredientes culinários",
}

IMAGE_CATEGORY_TERMS = {
    "cereais": "grãos e flocos soltos em pote transparente",
    "leguminosas": "grãos secos soltos em recipiente",
    "sementes": "sementes soltas em pote ou concha",
    "chas": "folhas flores ou ervas secas soltas em pote",
    "ervas": "ervas e raízes secas soltas em pote",
    "temperos": "tempero solto em pó grãos ou flocos em pote",
    "farinhas": "farinha farelo ou pó solto em recipiente",
    "oleaginosas": "castanhas e oleaginosas soltas em pote",
    "frutas": "fruta ou vegetal seco desidratado solto em recipiente",
    "snacks": "snack solto a granel em pote ou cesta",
    "chocolates": "chocolate gotas trufas ou drágeas soltas a granel",
    "funcionais": "superalimento em pó sementes ou grãos soltos em pote",
    "suplementos": "suplemento em pó solto a granel em pote sem marca",
    "adocantes": "cristais ou pó solto a granel em recipiente",
    "cogumelos": "cogumelos secos soltos em recipiente",
    "culinarios": "ingrediente culinário solto a granel em recipiente",
}

VALID_CATEGORIES = set(CATEGORY_LABELS)

def normalize(value):
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", text.upper()).strip()

def slugify(value):
    text = normalize(value).lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")

def category_for(name, current):
    n = normalize(name)
    c = (current or "").strip().lower()
    if n.startswith(("TRUFA", "DRAGEA", "GOTAS", "MINI GOTAS", "CHOCOLATE ", "CACAU ")):
        return "chocolates"
    if any(k in n for k in ["ASHWAGANDHA", "MACA PERUANA", "PSYLLIUM", "SPIRULINA", "ESPIRULINA", "CHLORELLA", "FENO GREGO", "TRIBULUS", "MORINGA", "ORA PRO NOBIS", "MARAPUAMA", "GINSENG", "CATUABA", "GUARANA EM PO", "GLUCOMANAN", "GARCINIA", "SHOT VITAL", "FIBRA DE MACA", "BERINJELA PO"]):
        return "funcionais"
    if any(k in n for k in ["WHEY", "CREATINA", "GLUTAMINA", "BCAA", "ALBUMINA", "COLAGENO", "PROTEINA ISOLADA", "VITAMINA D3"]):
        return "suplementos"
    if n.startswith("ACUCAR ") or n in {"ERITRITOL", "STEVIA", "XYLITOL CRYSTAL"}:
        return "adocantes"
    if any(k in n for k in ["COGUMELO", "SHITAKE"]):
        return "cogumelos"
    if "FARINHA" in n or "FARELO" in n or any(k in n for k in ["POLVILHO", "FECULA", "AMIDO DE MILHO", "GOMA XANTANA"]):
        return "farinhas"
    if any(k in n for k in ["LENTILHA", "GRAO DE BICO", "ERVILHA TORRADA", "PROTEINA TEXT. SOJA GRANULADA"]):
        return "leguminosas"
    if any(k in n for k in ["AVEIA EM FLOCOS", "AVEIA FLOCOS", "GRANOLA", "FLOCAO", "FLOCOS DE CENTEIO", "FLOCOS DE CEVADA", "FLOCOS DE ARROZ", "CANJICA", "COUSCOUS", "PAINCO", "QUINOA", "QUINUA", "SAGU", "MIX DE QUINOA"]):
        return "cereais"
    if any(k in n for k in ["GERGELIM", "LINHACA", "CHIA", "SEMENTE ABOBORA", "SEMENTE GIRASSOL", "MIX DE SEMENTES"]):
        return "sementes"
    if any(k in n for k in ["CASTANHA", "AMENDOIM", "AMENDOA", "AVEL", "MACADAMIA", "NOZES", "PISTACHE", "MIX DE CASTANHAS"]):
        return "oleaginosas"
    if any(k in n for k in ["CHIPS", "BISCOITO", "FAROFA DE SOJA", "PROVOLONE DESIDRATADO", "MILHO ESPANHOL", "BANANINHA FITNESS"]):
        return "snacks"
    return c if c in VALID_CATEGORIES else "culinarios"

def adjusted_prices(price_kg):
    raw = str(price_kg).strip().replace("R$", "").replace(" ", "")
    if "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    kg = Decimal(raw)
    base_100g = kg / Decimal("10")
    whole = int(base_100g)
    price_100g = Decimal(whole) + Decimal("0.99")
    adjusted_kg = price_100g * Decimal("10")
    return price_100g, adjusted_kg

def br(value):
    return f"{value:.2f}".replace(".", ",")

with CATALOG.open(encoding="utf-8", newline="") as fh:
    source = list(csv.DictReader(fh))

products = []
for row in source:
    name = (row.get("name") or "").strip()
    if not name or normalize(name).startswith("SEM DESCRICAO") or "PERCARBONATO" in normalize(name):
        continue
    p100, pkg = adjusted_prices(row.get("price") or row.get("priceKgAdjusted") or "0")
    products.append({
        "name": name,
        "category": category_for(name, row.get("cat")),
        "price100g": p100,
        "priceKg": pkg,
        "id": slugify(name),
    })

if len(products) < 300:
    raise SystemExit(f"Catálogo parece incompleto: apenas {len(products)} produtos")

product_lines = []
for p in products:
    benefits = [
        "Vendido a granel na quantidade que você escolher",
        "Preço calculado automaticamente conforme o peso",
        "Consulte a loja para disponibilidade e informações do produto",
    ]
    product_lines.append(
        "  { name: %s, price: %s, swatch: \"generic\", cat: %s, nutri: { serving: \"100g\", cal: \"—\", protein: \"—\", carbs: \"—\", fiber: \"—\" }, benefits: %s },"
        % (json.dumps(p["name"], ensure_ascii=False), json.dumps(br(p["priceKg"])), json.dumps(p["category"]), json.dumps(benefits, ensure_ascii=False))
    )
products_block = "const PRODUCTS = [\n" + "\n".join(product_lines) + "\n];"

labels_block = "const CATEGORY_LABELS = " + json.dumps(CATEGORY_LABELS, ensure_ascii=False, indent=2) + ";"
terms_block = "const IMAGE_CATEGORY_TERMS = " + json.dumps(IMAGE_CATEGORY_TERMS, ensure_ascii=False, indent=2) + ";"

filter_lines = ['      <button class="filter-btn active" data-filter="todos">Todos</button>']
for key, label in CATEGORY_LABELS.items():
    if any(p["category"] == key for p in products):
        filter_lines.append(f'      <button class="filter-btn" data-filter="{key}">{label}</button>')
filters_block = '    <div class="filter-row reveal">\n' + "\n".join(filter_lines) + '\n    </div>'

image_function = '''function productImage(product) {
  if (productImageCache.has(product.id)) return productImageCache.get(product.id);
  const categoryTerm = IMAGE_CATEGORY_TERMS[primaryCategory(product)] || "produto solto a granel em recipiente";
  const search = `${product.name} a granel sem embalagem sem marca ${categoryTerm}`;
  const query = encodeURIComponent(`${search} close up`);
  const imageUrl = `https://tse2.mm.bing.net/th?q=${query}&w=900&h=700&c=7&rs=1&p=0`;
  productImageCache.set(product.id, imageUrl);
  return imageUrl;
}'''

promos = '''const WEEKLY_PROMOTIONS = [
  { product: "CASTANHA DO PARA INTEIRA", discount: 15, description: "Oleaginosas selecionadas com preço especial." },
  { product: "AVEIA FLOCOS NORMAL", discount: 10, description: "Ideal para o café da manhã." },
  { product: "CAMOMILA FLOR", discount: 10, description: "Um chá suave para deixar sua rotina mais leve." },
];'''

for path in HTML_FILES:
    text = path.read_text(encoding="utf-8")
    text, n = re.subn(r"const PRODUCTS = \[.*?\n\];(?=\n\nconst WEEKLY_PROMOTIONS)", products_block, text, flags=re.S)
    if n != 1: raise SystemExit(f"Falha ao trocar produtos em {path.name}: {n}")
    text, n = re.subn(r"const WEEKLY_PROMOTIONS = \[.*?\n\];", promos, text, count=1, flags=re.S)
    if n != 1: raise SystemExit(f"Falha ao trocar promoções em {path.name}: {n}")
    text, n = re.subn(r'<div class="filter-row reveal">.*?</div>\s*(?=<div class="products-grid" id="productsGrid"></div>)', filters_block, text, count=1, flags=re.S)
    if n != 1: raise SystemExit(f"Falha ao trocar filtros em {path.name}: {n}")
    text, n = re.subn(r"const CATEGORY_LABELS = \{.*?\n\};", labels_block, text, count=1, flags=re.S)
    if n != 1: raise SystemExit(f"Falha ao trocar categorias em {path.name}: {n}")
    text, n = re.subn(r"const PRODUCT_IMAGE_SEARCH = \{.*?\n\};", "const PRODUCT_IMAGE_SEARCH = {};", text, count=1, flags=re.S)
    if n != 1: raise SystemExit(f"Falha ao limpar buscas antigas em {path.name}: {n}")
    replacement = terms_block + "\n\n" + image_function + "\n\nfunction productId(name) {"
    text, n = re.subn(r"function productImage\(product\) \{.*?\n\}\n\nfunction productId\(name\) \{", replacement, text, count=1, flags=re.S)
    if n != 1: raise SystemExit(f"Falha ao atualizar imagens em {path.name}: {n}")
    text = text.replace("Escolha o grão, escolha o peso.", "Escolha o produto, escolha o peso.")
    text = text.replace("Clique em qualquer produto para ver a composição nutricional e os benefícios para o corpo.", "Escolha uma categoria, abra o produto e selecione o peso desejado.")
    text = text.replace('<img class="product-image" src="${productImage(p)}"', '<img class="product-image" loading="lazy" decoding="async" src="${productImage(p)}"')
    path.write_text(text, encoding="utf-8")
    print(f"Atualizado {path.name}: {len(products)} produtos")

price_pairs = []
for p in products:
    cents_per_kg = int(p["priceKg"] * 100)
    price_pairs.append(f'  "{p["id"]}": {cents_per_kg}')
price_map = "const PRODUCT_PRICES_CENTS = {\n" + ",\n".join(price_pairs) + "\n};"

gs = APPS_SCRIPT.read_text(encoding="utf-8")
gs, n = re.subn(r"const PRODUCT_PRICES_CENTS = \{.*?\n\};", price_map, gs, count=1, flags=re.S)
if n != 1: raise SystemExit(f"Falha ao atualizar preços do Apps Script: {n}")
APPS_SCRIPT.write_text(gs, encoding="utf-8")

if README.exists():
    readme = README.read_text(encoding="utf-8")
    readme = re.sub(r"\b23 produtos\b", f"{len(products)} produtos", readme)
    README.write_text(readme, encoding="utf-8")

print(f"Catálogo final: {len(products)} produtos; preços exibidos por 100g terminando em ,99")
