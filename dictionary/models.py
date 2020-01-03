from django.db import models


class Entry(models.Model):
    seq_id = models.IntegerField("Sequencial Id", default=0)
    japanese = models.CharField("Kanji", max_length=1000)

    def __str__(self):
        return self.japanese
