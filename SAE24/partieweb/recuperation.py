import os, json
from .views import ajoutdonnees

repertoire = './messages'

while True:
    if os.listdir(repertoire):
        for file in os.listdir(repertoire):
            with open(os.path.join(repertoire, file), 'r') as f:
                data = json.load(f)
            ajoutdonnees(data)
            os.remove(os.path.join(repertoire, file))