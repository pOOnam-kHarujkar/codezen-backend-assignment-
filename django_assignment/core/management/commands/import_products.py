# myapp/management/commands/import_products.py

from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from core.models import Product

class Command(BaseCommand):
    help = 'Import products from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The file path to the Excel file.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            raise CommandError(f'Error reading the Excel file: {e}')

        for index, row in df.iterrows():
            product_name = row['name']
            product_amount = row['amount']

            if not Product.objects.filter(name=product_name).exists():
                Product.objects.create(name=product_name, amount=product_amount)
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product_name}'))
