from pathlib import Path

FILES = [Path('index.html'), Path('purograne.html')]

OLD = '''  const visibleProducts = filter === "todos"
    ? Object.keys(CATEGORY_LABELS)
        .map(category => PRODUCTS.find(p => (p.categories || [p.cat]).includes(category)))
        .filter(Boolean)
    : PRODUCTS.filter(p => (p.categories || [p.cat]).includes(filter));'''

NEW = '''  const visibleProducts = filter === "todos"
    ? Object.keys(CATEGORY_LABELS)
        .map(category => PRODUCTS.find(p => (p.categories || [p.cat]).includes(category)))
        .filter(Boolean)
        .slice(0, 10)
    : PRODUCTS.filter(p => (p.categories || [p.cat]).includes(filter));'''

for path in FILES:
    text = path.read_text(encoding='utf-8')
    if OLD not in text:
        raise SystemExit(f'Bloco esperado não encontrado em {path}')
    path.write_text(text.replace(OLD, NEW), encoding='utf-8')
    print(f'Atualizado: {path}')
