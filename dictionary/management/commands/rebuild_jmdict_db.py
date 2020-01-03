import gzip
import logging
import xml.etree.ElementTree as et

from django.core.management.base import BaseCommand
from dictionary.models import Entry


log_format = "[%(asctime)s] %(filename)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class Command(BaseCommand):
    """
    Downloads and rebuilds the dataset of dictionary entries.
    """
    help = "Rebuilds the JMdict Database"

    def handle(self, *args, **kwargs):

        # Drop all entries from the table
        logging.info("Removing old entries from the database table...")
        Entry.objects.all().delete()

        # Store entries in a list for bulk creation to improve run time.
        bulk_entries = []

        # TODO: Download dictionary files automatically

        logging.info("Unzipping JMdict dictionary...")
        with gzip.open('assets/JMdict.gz', 'rb') as gz:
            root = et.fromstring(gz.read().decode('utf-8'))

        logging.info("Parsing all entries found...")
        matches = root.findall('entry')

        for match in matches:
            seq_id = match.find('ent_seq').text
            entry = Entry(seq_id=seq_id)

            if match.find('k_ele'):
                entry.japanese = match.find('k_ele').find('keb').text

                bulk_entries.append(entry)

        Entry.objects.bulk_create(bulk_entries)
        logging.info(f"{len(matches)} entries were added to the dictionary.")
