from django import forms
from .models import Person, Asset, Rueckgabe

class PersonForm(forms.ModelForm):
    teilnehmer_id = forms.CharField(label="Teilnehmer*innen Code", help_text="Bitte den Teilnehmer*innen Code scannen.", required=True)
    name = forms.CharField(label="Name", help_text="Bitte den Namen eingeben.", required=True)
    projekt = forms.CharField(label="Projekt", help_text="An welchem Projekt arbeitet die Teilnehmer*in?.", required=False)
    class Meta:
        model = Person
        fields = ['teilnehmer_id', 'name', 'projekt']

class AusleiheForm(forms.Form):
    teilnehmer_id = forms.CharField(label="Teilnehmer*innen Code", help_text="Bitte den Teilnehmer*innen Code scannen oder eingeben. Beispiel: TEILI-001")
    asset_input = forms.CharField(label="Asset Tag", help_text="Bitte den Asset Tag scannen oder eingeben. Beispiel: AINV-00001")

class RueckgabeForm(forms.Form):
    teilnehmer_id = forms.CharField(label="Teilnehmer*innen Code", help_text="Bitte den Teilnehmer*innen Code scannen oder eingeben. Beispiel: TEILI-001")
    asset_input = forms.CharField(label="Asset Tag", help_text="Bitte den Asset Tag scannen oder eingeben. Beispiel: AINV-00001")
    zustand = forms.ChoiceField(label="Asset Zustand", help_text="Bitte wähle den Asset Zustand aus", choices=[('Gleich', 'Gleich'), ('Schlechter', 'Schlechter'), ('Defekt', 'Defekt')])
    kommentar = forms.CharField(label="Kommentar", help_text="Wenn du irgendetwas zum Zustand oder Asset kommentieren willst kannst du das hier tun.", widget=forms.Textarea, required=False)
    
class MeinGeraetForm(forms.Form):
    teilnehmer_id = forms.CharField(label="Teilnehmer*innen Code", help_text="Scanne deinen Code", required=True)
    asset_input = forms.CharField(label="Asset Tag", help_text="Scanne das Gerät", required=True)