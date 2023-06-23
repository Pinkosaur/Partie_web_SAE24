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


def traitement(dict, mydb):
    dict_capteur = {}
    liste = []
    print(dict["id"])
    dict_capteur["id"], dict_capteur["piece"] = dict["id"], dict["piece"]
    id_capteur = dict_capteur["id"]
    nom = "capteur "+ dict_capteur["piece"] + str(random.randint(0,10))
    del dict["id"]
    del dict["piece"]
    with open(id_file, 'r') as f:
        lines = f.readlines()
        if lines == []:
            with open(id_file, 'a') as f:
                f.write(f"{id_capteur},{nom}" + "\n")
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
    val = str(msg.payload).split(",")
    print(msg.payload)
    dict = {}
    for valeurs in val:
        key, valeur = valeurs.split("=")
        if key == "b'Id":
            key = "id"
        if key == 'temp':
            valeur = valeur[0:-1]
        dict[key]= valeur
    jour, mois, annee = str(dict["date"]).split("/")
    if dict.get("time")==None:
        time = dict["heure"]
        del dict["heure"]
    else:
        time = dict["time"]
        del dict["time"]
    timestamp = f"{annee}-{mois}-{jour} {time}"
    dict["timestamp"] = timestamp
    del dict["date"]
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
            writer.writerow([dict["id"], dict["piece"], dict["temp"], dict["timestamp"]])

    if connected == True:
        print("Envoi des infos vers le serveur MySQL")
        traitement(dict, mydb)
        df = pd.read_csv(csvfilename)
        if df.empty == False:
            print("Ajout des infos du cache dans le serveur MySQL")
            df = pd.read_csv(csvfilename, header=None)
            with open(csvfilename, "r+") as csvfile:
                reader = csv.DictReader(csvfile)
                print("voici le reader :", reader)
                for dict in reader:
                    print(dict)
                    traitement(dict, mydb)
                    df.drop(df.index[1], inplace=True)
                    df.to_csv(csvfilename, index=False, header=False)




broker_address = "test.mosquitto.org"
client_id = "bb43543d-adac-4736-9cac-cba1331053f2"

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()






