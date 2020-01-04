from django.db import models


class Kanji(models.Model):
    entry_id = models.IntegerField(default=0)
    kanji_num = models.IntegerField(default=0)
    keb = models.TextField("Kanji")
    ke_inf = models.TextField("Kanji Information")
    ke_pre = models.TextField("Kanji Priority")

    def __str__(self):
        return self.keb


class Reading(models.Model):
    entry_id = models.IntegerField(default=0)
    reading_num = models.IntegerField(default=0)
    reb = models.TextField("Reading")
    re_nokanji = models.TextField("No Kanji", default='')
    re_restr = models.TextField("Reading Restrictions")
    re_inf = models.TextField("Reading Information")
    re_pri = models.TextField("Reading Priority")

    def __str__(self):
        return self.reb


class Sense(models.Model):
    entry_id = models.IntegerField(default=0)
    sense_num = models.IntegerField(default=0)
    stagk = models.TextField()
    stagr = models.TextField()
    xref = models.TextField("Cross Reference")
    ant = models.TextField("Antonym")
    pos = models.TextField("Part of Speech")
    field = models.TextField()
    misc = models.TextField("Miscellaneous")
    lsource = models.TextField("Language Source")
    dial = models.TextField("Dialect")
    pri = models.TextField()
    s_inf = models.TextField("Sense Information")

    def __str__(self):
        return f"Reading ID: {self.entry_id}"


class Translation(models.Model):
    entry_id = models.IntegerField(default=0)
    sense_num = models.IntegerField(default=0)
    translation_num = models.IntegerField(default=0)
    gloss = models.TextField("Glossary", default='')
    lang = models.TextField("Language", default='eng')
    g_gend = models.TextField("Gender")
    g_type = models.TextField("Type")

    def __str__(self):
        return self.gloss
