import sqlite3

conn = sqlite3.connect('app.db')
cur = conn.cursor()
cur.execute("SELECT * FROM item WHERE type = 6;")
results = cur.fetchall()
for item in results:
    print("/static/images/item/organisation/small/{}.png".format(item[1].lower()))
