import json
from flask import Flask
import sqlite3
import sys
import os

app = Flask(__name__)
script_dir = os.path.dirname(sys.argv[0])
db = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = db.cursor()

# создание таблиц в БД
with open(os.path.join(script_dir, 'create_db.sql'), 'r') as file:
    scr = file.read()
    cur.executescript(scr)
    db.commit()

# заполнение БД
with open(os.path.join(script_dir, 'fill_db.sql'), 'r') as file:
    scr = file.read()
    cur.executescript(scr)
    db.commit()


@app.route('/', methods=["GET"])
def default_page():
    return json.dumps({"available requests": ["get_products", "get_categories", "get_pairs"]})


# получить список всех продуктов с их категориями
@app.route('/get_products', methods=["GET"])
def get_products():
    cur.execute(f"select product_name, group_concat(categoty_name) as category from "
                f"(select products.product_name as product_name, c.category_name as categoty_name "
                f"from products left join union_table ut on products.product_id = ut.product_id "
                f"left join categories c on ut.category_id = c.category_id) group by product_name;")
    res = cur.fetchall()
    dict_res = {"products": [{i[0]:i[1] if i[1] is None else [j for j in i[1].split(",")]} for i in res]}
    return json.dumps(dict_res, ensure_ascii=False)


# получить список категорий с продуктами
@app.route('/get_categories', methods=["GET"])
def get_categories():
    cur.execute(f"select category_name, group_concat(p.product_name) from categories "
                f"left join union_table ut on categories.category_id = ut.category_id "
                f"left join products p on p.product_id = ut.product_id group by category_name;")
    res = cur.fetchall()
    dict_res = {"categories": [{i[0]:i[1] if i[1] is None else [j for j in i[1].split(",")]} for i in res]}
    return json.dumps(dict_res, ensure_ascii=False)


# получить список всех пар «Имя продукта – Имя категории»
# возвращает список пар, а так же список продуктов без категории и список категорий без продуктов
@app.route('/get_pairs', methods=["GET"])
def get_pairs():
    cur.execute(f"select p.product_name, c.category_name from union_table "
                f"join categories c on c.category_id = union_table.category_id "
                f"join products p on p.product_id = union_table.product_id;")
    res = cur.fetchall()
    dict_res = {"pairs": [{i[0]:i[1]} for i in res]}
    cur.execute(f"select product_name from products "
                f"left join union_table on union_table.product_id = products.product_id "
                f"where union_table.product_id is null;")
    dict_res["products_without_categories"] = [i[0] for i in cur.fetchall()]
    cur.execute(f"select category_name from categories "
                f"left join union_table on union_table.category_id = categories.category_id "
                f"where union_table.category_id is null;")
    dict_res["categories_without_products"] = [i[0] for i in cur.fetchall()]
    return json.dumps(dict_res, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
