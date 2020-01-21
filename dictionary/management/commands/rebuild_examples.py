import gzip
import logging

from django.core.management.base import BaseCommand

from dictionary.models import Example

log_format = "[%(asctime)s] %(filename)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logging.info("Removing old entries from the database table...")
        Example.objects.all().delete()

        bulk_examples = []

        logging.info("Unzipping Examples dictionary...")
        with gzip.open("assets/examples.gz", 'rb') as z:
            for line in z.readlines():
                parts = line.rstrip().decode('euc-jp').split('\t')

                # Prevent overly perverted examples from being added
                # Replace with the below if statement if you would like to include them
                # if len(parts) == 4:
                if len(parts) == 4 and '[XXX]' not in line:
                    example = Example()

                    example.example_id = parts[0]
                    example.english = parts[1]
                    example.japanese = parts[2]
                    example.break_down = parts[3]

                    bulk_examples.append(example)

        logging.info("Building Database...")
        Example.objects.bulk_create(bulk_examples)
        logging.info(f"{len(bulk_examples)} examples were added...")
        logging.info(f"Cleaning up...")

