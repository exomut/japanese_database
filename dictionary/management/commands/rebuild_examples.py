import gzip
import logging

from django.core.management.base import BaseCommand


log_format = "[%(asctime)s] %(filename)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with gzip.open("assets/examples.gz", 'rb') as z:
            for line in z.readlines():
                print(line.replace('\r\n', '').decode('euc-jp').split('\t'))
