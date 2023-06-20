from django.db import models

# Create your models here.

class capteur(models.Model):
    nom = models.CharField(max_length=40, default = 'Nouveau capteur')
    piece = models.CharField(max_length=40)
    emplacement = models.TextField()
    def __str__(self):
        return f"capteur {self.nom} {self.piece}"
    def dic(self):
        return {"nom":self.nom, "piece":self.piece, "emplacement":self.emplacement}

class donnees(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    capteur = models.ForeignKey('capteur', on_delete=models.CASCADE)
    date = models.DateField()
    heure =models.TimeField()
    temp = models.FloatField()
    def __str__(self):
        return f"id {self.id}, le {self.date} à {self.heure} : température {self.temp}°C"
    def dic(self):
        return {"id":self.id, "capteur":self.capteur, "date":self.date, "heure":self.heure, "temp":self.temp}