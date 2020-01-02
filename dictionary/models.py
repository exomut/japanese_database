from django.db import models


class Entries(models.Model):
    japanese = models.CharField(max_length=1000)

    def __str__(self):
        return self.japanese
