import sqlite3

conn = sqlite3.connect('app.db')
cur = conn.cursor()
cur.execute("SELECT * FROM item WHERE type = 5;")
results = cur.fetchall()
for op in results:
    print("/static/images/item/operator/large/{}.png".format(op[1].lower()))
