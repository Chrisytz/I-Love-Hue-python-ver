import sqlite3

con = sqlite3.connect('testing.db')
cur = con.cursor()

# cur.execute('''CREATE TABLE arrays
#                 (string text, uwu text)''')

cur.execute("INSERT INTO arrays VALUES ('num1', '[(123,123,123), (234,234,234), (123,456,789)]')")

cur.execute("SELECT * FROM arrays WHERE string = 'num1'")
print(cur.fetchone()[1])


cur.execute("DELETE FROM arrays WHERE string = 'num1'")


con.commit()

con.close()