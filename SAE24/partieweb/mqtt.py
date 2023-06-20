import paho.mqtt.client as mqtt
import json
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion. Code de retour : {rc}")
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
    with open(f"./messages/temp_{data[1]}_hms={heure}.json", "w") as f:  # Remplacer ./messages/ par le chemin adapté sur le serveur
        json.dump(data, f)



broker_address = "test.mosquitto.org"
client_id = "bb43543d-adac-4736-9cac-cba1331053f2"

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()