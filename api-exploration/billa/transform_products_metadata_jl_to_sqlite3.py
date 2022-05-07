import json
import sqlite3
from typing import Any, Dict, Tuple

def json_to_tuple(product: Dict[str, Any]) -> Tuple:
    return (
        product['articleId'],
        product['name'],
        product['description'],
        product['brand'],
        product['category'],
        product['product_group_id'],
        product['grammage'],
        product['vatCode'],
        product['rank'],
        json.dumps(product['attributes']),
        json.dumps(product['eanCodes'])
    )

db = sqlite3.connect('products_billa.sqlite3')

db.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        brand TEXT,
        category TEXT,
        product_group_id TEXT,
        grammage TEXT,
        vatCode TEXT,
        rank TEXT,
        attributes TEXT,
        eanCodes TEXT)
    ''')

with open('../../crawler_downloads/billa/products_metadata_20220504_201010.jl', 'r') as file:
    
    db.execute('BEGIN')
    
    for line in file:
        product = json_to_tuple(json.loads(line))
        db.execute('''
            INSERT INTO products (id, name, description, brand, category, product_group_id, grammage, vatCode, rank, attributes, eanCodes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            product)

    db.execute('COMMIT')

db.close()
