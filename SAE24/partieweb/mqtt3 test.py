import mysql.connector


print("tentative de connection à MySQL")
mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="toto", database="mqtt", connect_timeout=3)
print("connecté à MySQL")

query = """
CREATE TABLE niquetamere(azerty VARCHAR(40),chaine VARCHAR(100));
INSERT INTO niquetamere(azerty, chaine) VALUES ('azerty','qrgtq');
"""
#query = 'create table partieweb_temp(id INT PRIMARY KEY AUTO_INCREMENT,a VARCHAR(40),b VARCHAR(40),chaine VARCHAR(100))'
curseur = mydb.cursor()
curseur.execute(query)