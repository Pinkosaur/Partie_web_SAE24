from paho.mqtt import client as mqtt
import random, os, csv
import mysql.connector
import pandas as pd


csvfilename = "./messages/cache.csv"
if not os.path.exists(csvfilename):
    print("Fichier CSV n'existe pas, création")
    with open(csvfilename, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id","piece","temp","timestamp"])

id_file = "id.txt"
if not os.path.exists(id_file):
    with open(id_file, 'w', newline="") as f:
        f.write("")


def traitement(data, mydb):
    with open(id_file, 'r') as f:
        lines = f.readlines()
        if lines == []:
            with open(id_file, 'a') as f:
                f.write(f"{data[0]}, 'Capteur {data[1]} {data[0]}'" + "\n")
            mycursor = mydb.cursor()
            query = "INSERT INTO partieweb_capteurs (id, nom, piece) VALUES (%s, %s, %s)"
            values = (dict_capteur["id"], nom, dict_capteur["piece"])
            mycursor.execute(query, values)
            mydb.commit()
    with open(id_file, 'r') as f:
        lines = f.readlines()
        for attribute in lines:
            attribute = attribute.split(",")[0]
            liste.append(attribute)
        if not dict_capteur["id"] in liste:
            with open(id_file, 'a') as f:
                f.write(f"{id_capteur},{nom}" + "\n")
                mycursor = mydb.cursor()
                query = "INSERT INTO partieweb_capteurs (id, nom, piece) VALUES (%s, %s, %s)"
                values = (dict_capteur["id"], nom, dict_capteur["piece"])
                mycursor.execute(query, values)
                mydb.commit()
        mycursor = mydb.cursor()
        query = f"INSERT INTO partieweb_donnees (timestamp, temp, capteur_id) VALUES (%s, %s, %s)"
        values = (dict["timestamp"], dict["temp"], dict_capteur["id"])
        mycursor.execute(query, values)
        mydb.commit()

def on_connect(client, userdata, flags, rc):
        print("Connexion établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")


def on_message(client, userdate, msg):
    temp = str(msg.payload).split('\'')[1].split(',')
    data = []
    data.append(temp[0].split('=')[1])
    data.append(temp[1].split('=')[1])
    data.append(temp[2].split('=')[1])
    heure = temp[3].split('=')[1].split(':')
    heure = f"{heure[0]}-{heure[1]}-{heure[2]}"
    data.append(heure)
    data.append(temp[4].split('=')[1])
    try:
        print('Connexion ...')
        mydb = mysql.connector.connect( host="127.0.0.1",
            user="root",
            password="toto",
            database="mqtt",
            connect_timeout= 2
        )
        connected= True
        print("Connecté")
    except:
        print("Connexion échouée, ajout des infos au cache")
        connected = False
        with open(csvfilename, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data)

    if connected == True:
        print("Envoi des infos vers le serveur MySQL")
        traitement(data, mydb)
        df = pd.read_csv(csvfilename)
        if df.empty == False:
            print("Ajout des infos du cache dans le serveur MySQL")
            df = pd.read_csv(csvfilename, header=None)
            with open(csvfilename, "r+") as csvfile:
                reader = csv.reader(csvfile)
                for data in reader:
                    print(data)
                    traitement(data, mydb)
                    df.drop(df.index[1], inplace=True)
                    df.to_csv(csvfilename, index=False, header=False)




broker_address = "test.mosquitto.org"
client_id = "bb43543d-adac-4736-9cac-cba1331053f2"

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()






