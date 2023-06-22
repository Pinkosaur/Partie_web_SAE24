import mysql.connector


print("tentative de connection à MySQL")
mydb = mysql.connector.connect(host="10.252.10.198", user="root", password="root", database="mqtt", connect_timeout=3)
print("connecté à MySQL")