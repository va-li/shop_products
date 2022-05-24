import sqlite3

db_file= './products_billa.sqlite3'
schema_creation_script_file = './products_billa_schema.sql'

print('Creating or updating database...')
print(f'Using database {db_file}')
print(f'Using schema {schema_creation_script_file}')

con = sqlite3.connect(db_file)

schema_creation_script = None
with open('./products_billa_schema.sql', 'r') as file:
    schema_creation_script = file.read()

with con:
    res = con.executescript(schema_creation_script)
print(res.fetchall())
