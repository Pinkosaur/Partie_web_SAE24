import paho.mqtt.client as mqtt
import json, os, csv, mysql.connector
import pandas as pd

if not os.path.exists("./messages/cache.csv"):
    with open("./messages/cache.csv", 'w', newline="") as f:
        f.write("")

if not os.path.exists("./messages/id.csv"):
    with open("./messages/id.csv", 'w', newline="") as f:
        f.write("")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion MQTT établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion au MQTT. Code de retour : {rc}")
def on_message(client, userdata, message):
    temp = str(message.payload).split('\'')[1].split(',')
    data = []
    data.append(temp[0].split('=')[1])
    data.append(temp[1].split('=')[1])
    data.append(temp[2].split('=')[1])
    heure = temp[3].split('=')[1].split(':')
    heure = f"{heure[0]}-{heure[1]}-{heure[2]}"
    data.append(heure)
    data.append(temp[4].split('=')[1])
    print (data)
    try:
        print("tentative de connection à MySQL")
        mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="toto",database="mqtt",connect_timeout=3)
        print("connecté à MySQL")
        connected = True
    except:
        print("échec")
        connected = False
        with open(f"./messages/cache.csv", "a", newline="") as f:  # Remplacer ./messages/ par le chemin adapté sur le serveur
            writer = csv.writer(f)
            writer.writerow(data)
            print ("enregistré dans le cache")
    if connected==True:
        print("envoi des données")
        envoi(data, mydb)
        cache = pd.read_csv("./messages/cache.csv")
        if cache.empty == False:
            cache=pd.read_csv("./messages/cache.csv", header=None)
            with open("./messages/cache.csv", "r+") as f:
                reader=csv.reader(f)
                for data in reader:
                    envoi(data, mydb)
                    cache.drop(cache.index[0], inplace=True)
                    cache.to_csv("./messages/cache.csv", index=False, header=False)


def envoi(data, mydb):
    existencecapteur = f"SELECT * FROM partieweb_capteur WHERE id={data[0]}"
#    if not mydb.cursor.execute(existencecapteur):
#        querycapteur = f"INSERT INTO partieweb_capteur (id, nom, piece) VALUES ('{data[0]}', 'Capteur {data[1]} {data[0]}', '{data[1]}')"
#        print(querycapteur)
#        mydb.cursor().execute(querycapteur)
#        mydb.commit()
    date = data[2].split('/')
    heure = data[3].split('-')
    timestamp = f"{date[2]}-{date[1]}-{date[0]} {heure[0]}:{heure[1]}:{heure[2]}"
    querydonnees = f"INSERT INTO partieweb_donnees (timestamp, temp, capteur_id) VALUES ('{timestamp}', '{data[4]}', '{data[0]}')"

    print(querydonnees)
    mycursor = mydb.cursor()
    try :
        mycursor.execute(querydonnees)
        print("requête exécutée")
    except:
        print('échec de l\'envoi de la requête SQL')



broker_address = "test.mosquitto.org"
client_id = "bb43543d-adac-4736-9cac-cba1331053f2"

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()