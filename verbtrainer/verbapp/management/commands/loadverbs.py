import csv

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from ...models import IrregularVerb


class Command(BaseCommand):
    help = 'Load verbs from CSV into the db'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str)

    def handle(self, *args, **options):

        with open(options['csv_file_path'], newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                try:
                    verb = IrregularVerb.objects.create(
                        base=row[0],
                        translation=row[1],
                        past_simple=row[2],
                        past_participle=row[3]
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully added verb: {verb}'))
                except ValidationError as e:
                    self.stdout.write(self.style.WARNING(f'Failed to add verb {row[0]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
        self.stdout.write(self.style.SUCCESS('Success'))