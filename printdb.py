import sqlite3
connection = sqlite3.connect("pw_us_drop.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM log") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)

connection.commit()
connection.close()
