import sqlite3

conn = sqlite3.connect('app.db')
cur = conn.cursor()
cur.execute("SELECT * FROM item;")
results = cur.fetchall()
#print(results[0])
#print(results[0][3].replace('/static/images/item/', ''))


for item in results:
    try:
        print(item)
        cur.execute("UPDATE item SET small_image = '{}' WHERE id = {}".format(item[3].replace('/static/images/item/', ''), item[0]))    
    except AttributeError:
        continue
    try:
        cur.execute("UPDATE item SET large_image = '{}' WHERE id = {}".format(item[4].replace('/static/images/item/', ''), item[0]))
    except AttributeError:
        continue
conn.commit()
