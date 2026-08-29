from pathlib import Path

FILES = [Path('index.html'), Path('purograne.html')]

OLD = '''function productImage(product) {
  // Imagens reais pesquisadas na web por nome do produto.
  // O endpoint do Bing retorna uma miniatura compatível com a busca e mantém
  // o catálogo leve, sem incorporar dezenas de arquivos pesados no HTML.
  if (productImageCache.has(product.id)) return productImageCache.get(product.id);
  const query = encodeURIComponent(`${product.name} a granel produto natural`);
  const imageUrl = `https://tse2.mm.bing.net/th?q=${query}&w=900&h=700&c=7&rs=1&p=0`;
  productImageCache.set(product.id, imageUrl);
  return imageUrl;
}'''

NEW = '''const PRODUCT_IMAGE_SEARCH = {
  "arroz-integral": "arroz integral cru a granel grãos soltos sem embalagem loja natural",
  "feijao-carioca": "feijão carioca cru a granel grãos soltos sem embalagem loja natural",
  "aveia-em-flocos": "aveia em flocos a granel solta sem embalagem loja natural",
  "quinoa": "quinoa branca a granel sementes soltas sem embalagem loja natural",
  "lentilha": "lentilha crua a granel grãos soltos sem embalagem loja natural",
  "grao-de-bico": "grão de bico cru a granel sem embalagem loja natural",
  "castanha-do-para": "castanha do pará a granel sem embalagem castanhas soltas loja natural",
  "amendoas": "amêndoas a granel sem embalagem amêndoas soltas loja natural",
  "chia": "semente de chia a granel sem embalagem sementes soltas loja natural",
  "linhaca": "linhaça dourada a granel sem embalagem sementes soltas loja natural",
  "camomila": "camomila flores secas a granel sem embalagem loja natural",
  "hibisco": "hibisco seco a granel pétalas sem embalagem loja natural",
  "erva-doce": "erva doce sementes a granel sem embalagem loja natural",
  "torradas-integrais": "torradas integrais a granel cesta sem embalagem loja natural",
  "batata-doce-temperada": "chips de batata doce a granel sem embalagem loja natural",
  "amendoim-sabor-barbecue": "amendoim barbecue a granel sem embalagem petisco",
  "amendoim-sabor-alho-e-ervas": "amendoim alho e ervas a granel sem embalagem petisco",
  "oregano": "orégano seco a granel tempero sem embalagem loja natural",
  "paprica-defumada": "páprica defumada em pó a granel tempero sem embalagem",
  "curcuma-em-po": "cúrcuma em pó açafrão da terra a granel sem embalagem",
  "morango-liofilizado": "morango liofilizado a granel sem embalagem frutas secas",
  "banana-liofilizada": "banana liofilizada a granel sem embalagem frutas secas",
  "manga-liofilizada": "manga liofilizada a granel sem embalagem frutas secas"
};

function productImage(product) {
  // Busca direcionada para fotos do alimento solto/a granel, evitando embalagens e marcas.
  if (productImageCache.has(product.id)) return productImageCache.get(product.id);
  const search = PRODUCT_IMAGE_SEARCH[product.id] || `${product.name} a granel sem embalagem produto solto`;
  const query = encodeURIComponent(`${search} close up recipiente pote concha`);
  const imageUrl = `https://tse2.mm.bing.net/th?q=${query}&w=900&h=700&c=7&rs=1&p=0`;
  productImageCache.set(product.id, imageUrl);
  return imageUrl;
}'''

for path in FILES:
    text = path.read_text(encoding='utf-8')
    if OLD not in text:
        raise SystemExit(f'Bloco esperado não encontrado em {path}')
    path.write_text(text.replace(OLD, NEW), encoding='utf-8')
    print(f'Atualizado: {path}')
