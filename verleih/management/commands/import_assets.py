import csv
from django.core.management.base import BaseCommand
from verleih.models import Asset

class Command(BaseCommand):
    help = 'Importiere Assets aus einer CSV-Datei'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['csv_file'], newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Asset Tag']:
                    Asset.objects.update_or_create(
                        asset_tag=row['Asset Tag'],
                        defaults={
                            'asset_name': row['Asset Name'],
                            'serial': row['Serial'],
                            'model': row['Model'],
                            'category': row['Category'],
                            'status': row['Status'],
                            'location': row['Location'],
                            'purchase_cost': row['Purchase Cost'],
                            'current_value': row['Current Value'],
                        }
                    )
        self.stdout.write(self.style.SUCCESS("CSV import abgeschlossen."))
