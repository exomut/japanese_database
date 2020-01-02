import gzip
import xml.etree.ElementTree as et

from django.core.management.base import BaseCommand
from dictionary.models import Entry


class Command(BaseCommand):
    help = 'Rebuilds the JMdict Database'

    def handle(self, *args, **kwargs):
        Entry.objects.all().delete()

        es = []

        with gzip.open('assets/JMdict.gz', 'rb') as gz:
            root = et.fromstring(gz.read().decode('utf-8'))
            entries = root.findall('entry')

            for entry in entries:
                if entry.find('k_ele'):
                    print(entry.find('k_ele').find('keb').text)
                    es.append(Entry(japanese=entry.find('k_ele').find('keb').text))

        Entry.objects.bulk_create(es)
