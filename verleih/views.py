from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, Asset, Ausleihe, Rueckgabe
from .forms import PersonForm, AusleiheForm, RueckgabeForm
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib import messages
from collections import defaultdict
from django.db.models import Q
import csv
from io import StringIO
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required

def generate_next_id():
    count = Person.objects.count() + 1
    return f"TEILI-{count:03d}"

@login_required
def person_anlegen(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.teilnehmer_id = generate_next_id()
            person.save()
            return redirect('index')
    else:
        form = PersonForm()
    return render(request, 'verleih/person_anlegen.html', {'form': form})

@login_required
def ausleihen(request):
    if request.method == 'POST':
        form = AusleiheForm(request.POST)
        if form.is_valid():
            pid = form.cleaned_data['teilnehmer_id']
            asset_code = form.cleaned_data['asset_input'].replace("https://assets.alpacabunt.de/ht/", "")
            try:
                person = Person.objects.get(teilnehmer_id=pid)
            except Person.DoesNotExist:
                messages.error(request, "Teilnehmer*in mit dieser ID existiert nicht.")
                return redirect('ausleihe')
            try:
                asset = Asset.objects.get(asset_tag=asset_code)
            except Asset.DoesNotExist:
                messages.error(request, "Dieses Asset existiert nicht.")
                return redirect('ausleihe')
            if asset.checked_out_to is not None:
                messages.error(request, f"Asset {asset.asset_tag} ist bereits an {asset.checked_out_to} ausgeliehen.")
                return redirect('ausleihe')
            anzahl_ausleihen = Ausleihe.objects.filter(person=person, rueckgabe__isnull=True).count()
            if anzahl_ausleihen >= 2:
                messages.warning(request, f"{person.name} hat bereits {anzahl_ausleihen} Geräte ausgeliehen.")
                return redirect('ausleihe')

            asset.checked_out_to = person
            asset.save()
            messages.success(request, f"Asset {asset_code} erfolgreich ausgeliehen.")
            Ausleihe.objects.create(person=person, asset=asset, user=request.user.username)
            return redirect('ausleihe')
    else:
        form = AusleiheForm()
    return render(request, 'verleih/ausleihe.html', {'form': form})

@login_required
def rueckgabe(request):
    if request.method == 'POST':
        form = RueckgabeForm(request.POST)
        if form.is_valid():
            pid = form.cleaned_data['teilnehmer_id']
            asset_code = form.cleaned_data['asset_input'].replace("https://assets.alpacabunt.de/ht/", "")
            try:
                person = Person.objects.get(teilnehmer_id=pid)
            except Person.DoesNotExist:
                messages.error(request, "Teilnehmer*in mit dieser ID existiert nicht.")
                return redirect('rueckgabe')
            try:
                asset = Asset.objects.get(asset_tag=asset_code)
            except Asset.DoesNotExist:
                messages.error(request, "Dieses Asset existiert nicht.")
                return redirect('rueckgabe')

            #ausleihe = get_object_or_404(Ausleihe, person=person, asset=asset)
            ausleihe = Ausleihe.objects.filter(asset=asset, rueckgabe__isnull=True).first()
            if not ausleihe:
                messages.error(request, "Dieses Asset ist aktuell nicht ausgeliehen.")
                return redirect('rueckgabe')

            if ausleihe.person != person:
                messages.error(request, f"Asset {asset.asset_tag} wurde nicht an {person.name} ausgegeben, sondern an {ausleihe.person.name} ({ausleihe.person.teilnehmer_id}).")
                return redirect('rueckgabe')

            Rueckgabe.objects.create(
                ausleihe=ausleihe,
                zustand=form.cleaned_data['zustand'],
                kommentar=form.cleaned_data['kommentar'],
                user=request.user.username
            )
            
            def clean(self):
                cleaned_data = super().clean()
                zustand = cleaned_data.get("zustand")
                kommentar = cleaned_data.get("kommentar")

                if zustand == 'Defekt' and not kommentar:
                    self.add_error('kommentar', "Kommentar ist erforderlich, wenn der Zustand 'Defekt' ist.")
            offene = Ausleihe.objects.filter(person=person, rueckgabe__isnull=True).count()
            messages.success(request, f"Asset {asset.asset_tag} erfolgreich zurückgenommen. {person.name} hat noch {offene} Asset(s) ausgeliehen.")

            asset.checked_out_to = None
            asset.save()
            messages.success(request, f"Asset {asset.asset_tag} erfolgreich zurückgenommen.")
            return redirect('index')
    else:
        form = RueckgabeForm()
    return render(request, 'verleih/rueckgabe.html', {'form': form})


@login_required
def verfuegbare_assets(request):
    assets = Asset.objects.filter(checked_out_to__isnull=True).order_by('category')
    return render(request, 'verleih/verfuegbar.html', {'assets': assets})


@login_required
def ausgegebene_assets(request):
    ausleihen = Ausleihe.objects.filter(rueckgabe__isnull=True)
    return render(request, 'verleih/ausgegeben.html', {'ausleihen': ausleihen})

@login_required
def beenden(request):
    offene_ausleihen = Ausleihe.objects.filter(rueckgabe__isnull=True)
    if offene_ausleihen.exists():
        messages.warning(request, f"Achtung: {offene_ausleihen.count()} Assets sind noch ausgeliehen. Möchtest du die Veranstaltung wirklich beenden?")
        return render(request, 'verleih/beenden_bestaetigen.html', {'anzahl_offen': offene_ausleihen.count()})
    return export_csv()

@login_required
def beenden_force(request):
    return export_csv()
    return redirect('index')

def export_csv():
    import csv
    from io import StringIO

    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=';')

    writer.writerow([
        "Asset", "Ausgegeben an", "Teilnehmer-ID", "Bestellnummer",
        "Ausgegeben am", "Zurueck am", "Status",
        "Ausgegeben von", "Zurueck von", "Zustand", "Kommentar"
    ])

    alle_ausleihen = Ausleihe.objects.select_related('person', 'asset').all()

    for ausleihe in alle_ausleihen:
        rueckgabe = Rueckgabe.objects.filter(ausleihe=ausleihe).first()
        person = ausleihe.person

        if rueckgabe:
            zustand = rueckgabe.zustand
            kommentar = rueckgabe.kommentar
            rueckgabezeit = rueckgabe.timestamp.strftime("%d.%m.%Y %H:%M")
            rueck_user = rueckgabe.user

            status = "DEFECT" if zustand == "Defekt" else "BACK"

            writer.writerow([
                ausleihe.asset.asset_tag,
                person.name,
                person.teilnehmer_id,
                person.bestellnummer,
                ausleihe.timestamp.strftime("%d.%m.%Y %H:%M"),
                rueckgabezeit,
                status,
                ausleihe.user,
                rueck_user,
                zustand,
                kommentar
            ])
        else:
            writer.writerow([
                ausleihe.asset.asset_tag,
                person.name,
                person.teilnehmer_id,
                person.bestellnummer,
                ausleihe.timestamp.strftime("%d.%m.%Y %H:%M"),
                "",
                "MISSING",
                ausleihe.user,
                "",
                "",
                ""
            ])

    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=verleih.csv'
    return response



def startseite(request):
    return render(request, 'verleih/index.html')