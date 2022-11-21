drop table if exists products;
drop table if exists categories;
drop table if exists union_table;
-- для упрощения работы программы и скрипта заполнения данными,
-- таблицы в БД пересоздаются при каждом запуске main.py
CREATE TABLE IF NOT EXISTS products(
                                       product_id INTEGER PRIMARY KEY,
                                       product_name TEXT
);
CREATE TABLE IF NOT EXISTS categories(
                                         category_id INTEGER PRIMARY KEY,
                                         category_name TEXT
);

CREATE TABLE IF NOT EXISTS union_table(
                                          product_id REFERENCES products(product_id),
                                          category_id REFERENCES categories(category_id),
                                          PRIMARY KEY (product_id,category_id)
);
