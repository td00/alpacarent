from django.db import models
from django.utils import timezone

class Person(models.Model):
    teilnehmer_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    projekt = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} - ({self.projekt})"
    class Meta:
        verbose_name = "Teilnehmer*in"
        verbose_name_plural = "Teilnehmer*innen"

class Asset(models.Model):
    asset_name = models.CharField(max_length=100, blank=True)
    asset_tag = models.CharField(max_length=20, unique=True)
    serial = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    purchase_cost = models.CharField(max_length=50, blank=True)
    current_value = models.CharField(max_length=50, blank=True)
    checked_out_to = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.category} - {self.asset_tag} ({self.asset_name})"
    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

class Ausleihe(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.asset} - {self.person} - {self.timestamp}"
    class Meta:
        verbose_name = "Ausleihe"
        verbose_name_plural = "Ausleihen"

class Rueckgabe(models.Model):
    ausleihe = models.OneToOneField(Ausleihe, on_delete=models.CASCADE)
    zustand = models.CharField(max_length=20, choices=[('Gleich', 'Gleich'), ('Schlechter', 'Schlechter'), ('Defekt', 'Defekt')])
    kommentar = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.ausleihe} - {self.zustand} - {self.timestamp}"
    class Meta:
        verbose_name = "Rückgabe"
        verbose_name_plural = "Rückgaben"
