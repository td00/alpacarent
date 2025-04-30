from django import forms
from .models import Person, Asset, Rueckgabe

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'bestellnummer']

class AusleiheForm(forms.Form):
    teilnehmer_id = forms.CharField(label="Teilnehmer*innen Code", help_text="Bitte den Teilnehmer*innen Code scannen oder eingeben. Beispiel: TEILI-001")
    asset_input = forms.CharField(label="Asset Tag", help_text="Bitte den Asset Tag scannen oder eingeben. Beispiel: AINV-00001")

class RueckgabeForm(forms.Form):
    teilnehmer_id = forms.CharField(label="Teilnehmer*innen Code", help_text="Bitte den Teilnehmer*innen Code scannen oder eingeben. Beispiel: TEILI-001")
    asset_input = forms.CharField(label="Asset Tag", help_text="Bitte den Asset Tag scannen oder eingeben. Beispiel: AINV-00001")
    zustand = forms.ChoiceField(label="Asset Zustand", help_text="Bitte wähle den Asset Zustand aus", choices=[('Gleich', 'Gleich'), ('Schlechter', 'Schlechter'), ('Defekt', 'Defekt')])
    kommentar = forms.CharField(label="Kommentar", help_text="Wenn du irgendetwas zum Zustand oder Asset kommentieren willst kannst du das hier tun.", widget=forms.Textarea, required=False)
    