INSERT INTO categories (name) VALUES
  ('Books'), ('Stationery'), ('Kitchen'), ('Gifts')
ON CONFLICT (name) DO NOTHING;

INSERT INTO products (name, description, price) VALUES
  ('Ceramic mug', 'Hand-glazed ceramic mug, 350 ml', 12.50),
  ('Hardcover notebook', '240 lined pages, elastic band closure', 24.00),
  ('Gel pen', NULL, 3.20),
  ('Espresso cup set', 'Set of four porcelain cups with saucers', 38.90),
  ('Pocket sketchbook', 'A6, 120 gsm paper, 80 pages', 9.75),
  ('Tea infuser', 'Stainless steel, fits most mugs', 6.40);

INSERT INTO product_categories (product_id, category_id)
SELECT p.id, c.id FROM products p JOIN categories c ON (p.name, c.name) IN (
  ('Ceramic mug', 'Kitchen'),
  ('Ceramic mug', 'Gifts'),
  ('Hardcover notebook', 'Books'),
  ('Hardcover notebook', 'Stationery'),
  ('Gel pen', 'Stationery'),
  ('Espresso cup set', 'Kitchen'),
  ('Espresso cup set', 'Gifts'),
  ('Pocket sketchbook', 'Stationery'),
  ('Tea infuser', 'Kitchen')
)
ON CONFLICT DO NOTHING;
