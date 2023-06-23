from django.db import models

# Create your models here.

class capteur(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    nom = models.CharField(max_length=40, unique = True)
    piece = models.CharField(max_length=40)
    emplacement = models.TextField()
    def __str__(self):
        return f"capteur {self.id}: {self.nom}, {self.piece}"
    def dic(self):
        return {"nom":self.nom, "piece":self.piece, "emplacement":self.emplacement}

class donnees(models.Model):
    capteur = models.ForeignKey('capteur', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temp = models.FloatField()
    def __str__(self):
        return f"mesure du {self.timestamp} : {self.temp}°C"
    def dic(self):
        return {"id":self.id, "capteur":self.capteur, "timestamp":self.timestamp, "temp":self.temp}

class temp(models.Model):
    chaine = models.CharField(max_length=100, primary_key=True)