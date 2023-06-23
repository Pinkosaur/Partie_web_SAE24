from paho.mqtt import client as mqtt
import random, os, csv
import mysql.connector
import pandas as pd


cache = "./messages/cache.csv"
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion au broker établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion au broker. Code de retour : {rc}")
def on_message(client, userdata, message):
    temp = str(message.payload).split('\'')[1].split(',')
    date = temp[2].split('=')[1].split("/")
    date = f"{date[2]}-{date[1]}-{date[0]}"
    heure = temp[3].split('=')[1].split(':')
    heure = f"{heure[0]}.{heure[1]}.{heure[2]}"
    data = f"{temp[0].split('=')[1]}_{temp[1].split('=')[1]}_{date}_{heure}_{temp[4].split('=')[1]}"
    print("données reçues :", data)
    try:
        print('Connexion à MySQL')
        mydb = mysql.connector.connect(host="127.0.0.1",
                                       user="root",
                                       password="toto",
                                       database="mqtt",
                                       connect_timeout=2
                                       )
        connected = True
        print("Connecté")
    except:
        print("Connexion à MySQL échouée, ajout des infos au cache")
        connected = False
        with open(cache, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data)

    if connected == True:
        print("Envoi des infos vers le serveur MySQL")
        ajout(data, mydb)
        if os.path.exists(cache):
            with open(cache, "w") as f:
                for data in cache:
                    ajout(data, mydb)
            os.remove(cache)

def ajout(data, mydb):
    query = f"INSERT INTO partieweb_temp (chaine) VALUES ('{data}')"
    print ("commande :", query)
    try:
        curseur = mydb.cursor()
        curseur.execute(query)
        mydb.commit()
        print("commande exécutée")
    except:
        print("échec")

broker_address = "test.mosquitto.org"
client_id = "bb43543d-adac-4736-9cac-cba1331053f2"

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()