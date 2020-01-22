import gzip
import re
import logging
from xml.etree import ElementTree

from django.core.management.base import BaseCommand
from dictionary.models import Entry, Kanji, Reading, Sense, Translation

from toolkit.xml_tools import find_element_text, findall_to_csv, get_element_text, is_element

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
        Entry.objects.all().delete()
        Kanji.objects.all().delete()
        Reading.objects.all().delete()
        Sense.objects.all().delete()
        Translation.objects.all().delete()

        # TODO: Download dictionary files automatically

        logging.info("Unzipping JMdict dictionary...")
        with gzip.open('assets/JMdict.gz', 'rb') as gz:
            root = ElementTree.fromstring(gz.read().decode('utf-8'))
            self.get_entries(root)

        logging.info("Building Database...")

        Kanji.objects.bulk_create(self.bulk_kanji)
        logging.info(f"1/4: {len(self.bulk_kanji)} kanji were added...")

        Reading.objects.bulk_create(self.bulk_readings)
        logging.info(f"2/4: {len(self.bulk_readings)} readings were added...")

        Sense.objects.bulk_create(self.bulk_senses)
        logging.info(f"3/4: {len(self.bulk_senses)} senses were added...")

        Translation.objects.bulk_create(self.bulk_translations)
        logging.info(f"4/4: {len(self.bulk_translations)} translations were added...")

        logging.info(f"Cleaning up...")

    def build_kanji(self, entry: ElementTree.Element, foreign_key):
        k_eles = entry.findall('k_ele')
        for kanji_num, k_ele in enumerate(k_eles):
            kanji = Kanji()
            kanji.entry = foreign_key
            kanji.kanji_num = kanji_num
            kanji.keb = find_element_text(k_ele, 'keb')
            kanji.ke_inf = findall_to_csv(k_ele, 'ke_inf', '|')
            kanji.ke_pri = findall_to_csv(k_ele, 'ke_pri', '|')

            self.bulk_kanji.append(kanji)

    def build_reading(self, entry: ElementTree.Element, foreign_key):
        r_eles = entry.findall('r_ele')
        for reading_num, r_ele in enumerate(r_eles):
            reading = Reading()
            reading.entry = foreign_key
            reading.reading_num = reading_num
            reading.reb = find_element_text(r_ele, 'reb')
            reading.re_nokanji = is_element(r_ele.find('re_nokanji'))
            reading.re_restr = findall_to_csv(r_ele, 're_restr')
            reading.re_inf = findall_to_csv(r_ele, 're_inf', '|')
            reading.re_pri = findall_to_csv(r_ele, 're_pri', '|')

            self.bulk_readings.append(reading)

    def build_sense(self, entry: ElementTree.Element, foreign_key):
        s_eles = entry.findall('sense')
        for sense_num, s_ele in enumerate(s_eles):
            sense = Sense()
            sense.entry = foreign_key
            sense.sense_num = sense_num
            sense.stagk = findall_to_csv(s_ele, 'stagk', '|')
            sense.stagr = findall_to_csv(s_ele, 'stagr', '|')
            # Remove the Japanese Katakana dot as a csv delimiter and replace with a pipe
            sense.xref = findall_to_csv(s_ele, 'xref', '|').replace('\u30fb', "|")
            sense.ant = findall_to_csv(s_ele, 'ant', '|')
            sense.pos = findall_to_csv(s_ele, 'pos', '|')
            sense.field = findall_to_csv(s_ele, 'field', '|')
            sense.misc = findall_to_csv(s_ele, 'misc', '|')
            sense.lsource = findall_to_csv(s_ele, 'lsource', '|')
            sense.dial = findall_to_csv(s_ele, 'dial', '|')
            sense.pri = findall_to_csv(s_ele, 'pri', '|')
            sense.s_inf = findall_to_csv(s_ele, 's_inf', '|')

            self.bulk_senses.append(sense)

            self.build_translation(s_ele, sense_num, foreign_key)

    def build_translation(self, entry: ElementTree.Element, sense_num: int, foreign_key):
        g_eles = entry.findall('gloss')
        for translation_num, g_ele in enumerate(g_eles):
            translation = Translation()
            translation.entry = foreign_key
            translation.sense_num = sense_num
            translation.translation_num = translation_num

            gloss = get_element_text(g_ele)
            translation.gloss = gloss or ''

            translation.lang = 'eng'
            for k, v in g_ele.attrib.items():
                if 'lang' in k:
                    translation.lang = v

            if translation.lang == 'eng':
                simple = re.sub(r'[ ]?\([^\(]*\)[ ]?', '', translation.gloss)
                simple = re.sub(r'^to be ', '', simple)
                simple = re.sub(r'^to ', '', simple)
                translation.simple = simple
            else:
                translation.simple = translation.gloss

            translation.g_gend = g_ele.attrib.get('g_gend', '')
            translation.g_type = g_ele.attrib.get('g_type', '')

            self.bulk_translations.append(translation)

    def get_entries(self, root: ElementTree.Element):
        entries = root.findall('entry')

        logging.info("Building Entry Table for Foreign Keys...")
        bulk_entries = []
        for entry_id, ele in enumerate(entries):
            entry = Entry(id=entry_id, ent_seq=ele.find('ent_seq').text)
            bulk_entries.append(entry)

        Entry.objects.bulk_create(bulk_entries)
        total = len(bulk_entries)
        del bulk_entries

        logging.info(f"Parsing {total} found entries...")

        for entry_id, entry in enumerate(entries):

            # Update user on current progress
            if entry_id % 10000 == 0:
                if entry_id != 0:
                    print(f"{entry_id}/{total} parsed...")

            foreign_key = Entry.objects.get(id=entry_id)

            self.build_kanji(entry, foreign_key)
            self.build_reading(entry, foreign_key)
            self.build_sense(entry, foreign_key)
