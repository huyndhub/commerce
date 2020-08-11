from django.db import models


class Greeting(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_greeting'
