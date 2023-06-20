import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion. Code de retour : {rc}")
def on_message(client, userdata, message):
    print(f"Message reçu : {message.payload}")

broker_address = "test.mosquitto.org"
client_id = "bb43543d-adac-4736-9cac-cba1331053f2"

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()