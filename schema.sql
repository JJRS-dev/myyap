PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS customers (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL CHECK (length(trim(name)) >= 2),
  phone TEXT NOT NULL,
  normalized_phone TEXT NOT NULL UNIQUE,
  email TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL CHECK (category IN ('cereais', 'leguminosas', 'sementes', 'chas', 'snaks', 'temperos', 'liofilizados')),
  price_per_kg_cents INTEGER NOT NULL CHECK (price_per_kg_cents >= 0),
  swatch TEXT NOT NULL,
  serving TEXT NOT NULL,
  calories INTEGER NOT NULL CHECK (calories >= 0),
  protein TEXT NOT NULL,
  carbohydrates TEXT NOT NULL,
  fiber TEXT NOT NULL,
  benefits TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  customer_id TEXT,
  customer_name TEXT NOT NULL,
  customer_phone TEXT NOT NULL,
  customer_email TEXT,
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  receiving_method TEXT NOT NULL CHECK (receiving_method IN ('Retirada na loja', 'Entrega')),
  address TEXT,
  payment_method TEXT NOT NULL CHECK (payment_method IN ('Pix', 'Cartão', 'Dinheiro')),
  status TEXT NOT NULL DEFAULT 'Novo' CHECK (status IN ('Novo', 'Em preparo', 'Pronto', 'Concluido', 'Cancelado')),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
  CHECK (receiving_method = 'Retirada na loja' OR length(trim(address)) > 0)
);

CREATE TABLE IF NOT EXISTS order_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id TEXT NOT NULL,
  product_id INTEGER,
  product_name TEXT NOT NULL,
  grams INTEGER NOT NULL CHECK (grams IN (100, 250, 500, 1000)),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
  subtotal_cents INTEGER NOT NULL CHECK (subtotal_cents >= 0),
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

INSERT OR IGNORE INTO products
  (name, category, price_per_kg_cents, swatch, serving, calories, protein, carbohydrates, fiber, benefits)
VALUES
  ('Arroz integral', 'cereais', 890, 'rice', '100g', 111, '2,6g', '23g', '1,8g', 'Rico em fibras;Baixo indice glicemico;Fonte de magnesio e selenio'),
  ('Feijao carioca', 'leguminosas', 950, 'bean', '100g', 127, '8,7g', '23g', '8,5g', 'Alto teor de proteina vegetal;Rico em ferro;Ajuda no controle do colesterol'),
  ('Aveia em flocos', 'cereais', 620, 'oat', '100g', 389, '16,9g', '66g', '10,6g', 'Reduz o colesterol LDL;Prolonga a saciedade;Fonte de energia de digestao lenta'),
  ('Quinoa', 'cereais', 1890, 'quinoa', '100g', 368, '14,1g', '64g', '7g', 'Proteina completa;Sem gluten;Rica em antioxidantes'),
  ('Lentilha', 'leguminosas', 1140, 'lentil', '100g', 116, '9g', '20g', '7,9g', 'Fonte de ferro e folato;Ajuda a estabilizar a glicemia;Rica em fibras soluveis'),
  ('Grao-de-bico', 'leguminosas', 1280, 'chickpea', '100g', 164, '8,9g', '27g', '7,6g', 'Rico em proteina e fibras;Ajuda na saude intestinal;Fonte de manganes e folato'),
  ('Castanha-do-para', 'snaks', 3490, 'nut', '30g', 199, '4,3g', '3,6g', '2,3g', 'Fonte natural de selenio;Antioxidante;Boa para a tireoide'),
  ('Amendoas', 'snaks', 2950, 'almond', '30g', 174, '6,4g', '6,1g', '3,6g', 'Rica em vitamina E;Gorduras boas para o coracao;Ajuda no controle do apetite'),
  ('Torradas integrais', 'snaks', 1490, 'toast', '30g', 115, '3,2g', '21g', '2,4g', 'Crocantes e leves;Fonte de fibras;Perfeitas com pastas e pates'),
  ('Batata-doce temperada', 'snaks', 2600, 'sweet-potato', '30g', 105, '1,5g', '20g', '3g', 'Assada e crocante;Temperada com ervas;Opcao pratica para um lanche'),
  ('Amendoim sabor barbecue', 'snaks', 1990, 'peanut', '30g', 170, '7g', '6g', '2,5g', 'Sabor barbecue marcante;Fonte de proteina vegetal;Ideal para petiscar'),
  ('Amendoim sabor alho e ervas', 'snaks', 1990, 'peanut', '30g', 170, '7g', '6g', '2,5g', 'Temperado com alho e ervas;Crocante e saboroso;Ideal para compartilhar'),
  ('Oregano', 'temperos', 3200, 'spice', '5g', 13, '0,4g', '3,4g', '1,6g', 'Aroma intenso;Ideal para massas e molhos;Combina com legumes e saladas'),
  ('Paprica defumada', 'temperos', 3800, 'spice', '5g', 14, '0,7g', '2,5g', '1,2g', 'Sabor defumado;Realca carnes e legumes;Pode ser usada em molhos'),
  ('Curcuma em po', 'temperos', 2900, 'turmeric', '5g', 16, '0,5g', '3,4g', '0,9g', 'Cor dourada natural;Versatil em receitas salgadas;Combina com arroz e sopas'),
  ('Morango liofilizado', 'liofilizados', 8900, 'dried-fruit', '20g', 68, '1,4g', '15g', '3,2g', 'Crocancia e sabor natural;Sem necessidade de refrigeracao;Ideal para iogurtes e cereais'),
  ('Banana liofilizada', 'liofilizados', 7200, 'dried-banana', '20g', 72, '0,8g', '17g', '2g', 'Textura crocante;Sabor naturalmente adocicado;Pratica para lanches'),
  ('Manga liofilizada', 'liofilizados', 8400, 'dried-fruit', '20g', 70, '0,6g', '17g', '1,5g', 'Sabor tropical;Crocante e leve;Combina com granolas e sobremesas'),
  ('Chia', 'sementes', 2200, 'chia', '30g', 137, '4,7g', '12g', '10,2g', 'Rica em omega-3;Alta concentracao de fibras;Ajuda na saciedade'),
  ('Linhaca', 'sementes', 1550, 'linhaca', '30g', 150, '5,1g', '9,7g', '8,2g', 'Fonte vegetal de omega-3;Rica em lignanas;Ajuda na regulacao intestinal');

COMMIT;
