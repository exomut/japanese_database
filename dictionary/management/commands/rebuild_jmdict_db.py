import gzip
import logging
from xml.etree import ElementTree

from django.core.management.base import BaseCommand
from dictionary.models import Kanji, Reading, Sense, Translation

from toolkit.xml_tools import find_element_text, findall_to_csv, get_element_text

log_format = "[%(asctime)s] %(filename)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class Command(BaseCommand):
    """
    Downloads and rebuilds the dataset of dictionary entries.
    """
    help = "Rebuilds the JMdict Database"
    bulk_kanji = []
    bulk_readings = []
    bulk_senses = []
    bulk_translations = []

    def handle(self, *args, **kwargs):
        # Drop all entries from the table
        logging.info("Removing old entries from the database table...")
        Kanji.objects.all().delete()
        Reading.objects.all().delete()
        Sense.objects.all().delete()
        Translation.objects.all().delete()

        # TODO: Download dictionary files automatically

        logging.info("Unzipping JMdict dictionary...")
        with gzip.open('assets/JMdict.gz', 'rb') as gz:
            root = ElementTree.fromstring(gz.read().decode('utf-8'))
            self.get_entries(root)

        Kanji.objects.bulk_create(self.bulk_kanji)
        logging.info(f"{len(self.bulk_kanji)} kanji were added.")

        Reading.objects.bulk_create(self.bulk_readings)
        logging.info(f"{len(self.bulk_readings)} readings were added.")

        Sense.objects.bulk_create(self.bulk_senses)
        logging.info(f"{len(self.bulk_senses)} senses were added.")

        Translation.objects.bulk_create(self.bulk_translations)
        logging.info(f"{len(self.bulk_translations)} translations were added.")

    def build_kanji(self, entry: ElementTree.Element, entry_id: int):
        k_eles = entry.findall('k_ele')
        for kanji_num, k_ele in enumerate(k_eles):
            kanji = Kanji()
            kanji.entry_id = entry_id
            kanji.kanji_num = kanji_num
            kanji.keb = find_element_text(k_ele, 'keb')
            kanji.ke_inf = findall_to_csv(k_ele, 'ke_inf')
            kanji.ke_pre = findall_to_csv(k_ele, 'ke_pre')

            self.bulk_kanji.append(kanji)

    def build_reading(self, entry: ElementTree.Element, entry_id: int):
        r_eles = entry.findall('r_ele')
        for reading_num, r_ele in enumerate(r_eles):
            reading = Reading()
            reading.entry_id = entry_id
            reading.reading_num = reading_num
            reading.reb = find_element_text(r_ele, 'reb')
            reading.re_nokanji = find_element_text(r_ele, 're_nokanji') or ''
            reading.re_inf = findall_to_csv(r_ele, 're_inf')
            reading.re_pri = findall_to_csv(r_ele, 're_pri')

            self.bulk_readings.append(reading)

    def build_sense(self, entry: ElementTree.Element, entry_id: int):
        s_eles = entry.findall('sense')
        for sense_num, s_ele in enumerate(s_eles):
            sense = Sense()
            sense.entry_id = entry_id
            sense.sense_num = sense_num

            self.bulk_senses.append(sense)

            self.build_translation(s_ele, entry_id, sense_num)

    def build_translation(self, entry: ElementTree.Element, entry_id: int, sense_num: int):
        g_eles = entry.findall('gloss')
        for translation_num, g_ele in enumerate(g_eles):
            translation = Translation()
            translation.entry_id = entry_id
            translation.sense_num = sense_num
            translation.translation_num = translation_num

            gloss = get_element_text(g_ele)
            translation.gloss = gloss or ''

            translation.lang = 'eng'
            for k, v in g_ele.attrib.items():
                if 'lang' in k:
                    translation.lang = v

            translation.g_gend = g_ele.attrib.get('g_gend', '')
            translation.g_type = g_ele.attrib.get('g_type', '')

            self.bulk_translations.append(translation)

    def get_entries(self, root: ElementTree.Element):
        logging.info("Parsing all entries found...")
        entries = root.findall('entry')

        for entry_id, entry in enumerate(entries):

            self.build_kanji(entry, entry_id)
            self.build_reading(entry, entry_id)
            self.build_sense(entry, entry_id)
