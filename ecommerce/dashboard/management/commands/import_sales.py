from django.core.management.base import BaseCommand
from dashboard.models import Sale  # change app name if needed
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Import sales data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    Sale.objects.create(
                        transaction_id=row['Transaction ID'],
                        date=datetime.strptime(row['Date'], '%Y-%m-%d').date(),  # change format if needed
                        customer_id=row['Customer ID'],
                        gender=row['Gender'],
                        age=int(row['Age']),
                        product_category=row['Product Category'],
                        quantity=int(row['Quantity']),
                        price_per_unit=float(row['Price per Unit']),
                        total_amount=float(row['Total Amount'])
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error in row: {row} -> {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} sales records successfully!"))
