from django.db import models


class Entry(models.Model):
    ent_seq = models.IntegerField("Sequencial Id", default=0)
    keb = models.TextField("Kanji")
    ke_inf = models.TextField("Kanji Information")
    ke_pre = models.TextField("Kanji Priority")

    def __str__(self):
        return self.keb


class Reading(models.Model):
    entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
    reb = models.TextField("Reading")
    re_nokanji = models.TextField("No Kanji")
    re_restr = models.TextField("Reading Restrictions")
    re_inf = models.TextField("Reading Information")
    re_pri = models.TextField("Reading Priority")

    def __str__(self):
        return self.reb


class Definition(models.Model):
    reading_id = models.ForeignKey(Reading, on_delete=models.CASCADE)
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
        return f"Reading ID: {self.reading_id}"


class Translation(models.Model):
    definition_id = models.ForeignKey(Definition, on_delete=models.CASCADE)
    gloss = models.TextField("Glossary")
    lang = models.TextField("Language")

    def __str__(self):
        return self.gloss

