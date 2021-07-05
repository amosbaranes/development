from django.db import models
from django.db import connection
from .fields import OrderField


class ModifyModel(object):

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {} RESTART IDENTITY CASCADE'.format(cls._meta.db_table))


class Adjectives(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.adjective


class AdjectiveManager(models.Manager):
    def get_queryset(self, adjective_title):
        return super(AdjectiveManager, self).get_queryset().filter(adjective__title=adjective_title).orderby(self.order)


class AdjectivesValues(models.Model):
    adjective = models.ForeignKey(Adjectives, on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=[], default=1)
    value = models.CharField(max_length=50)

    objects = models.Manager()  # The default manager.
    adjectives = AdjectiveManager()  # Our custom manager.

    def __str__(self):
        return self.value


class Numbers(models.Model):
    SOURCES = (
        (0, 'Other'),
        (1, 'General Ledger'),
    )
    source = models.IntegerField(default=1, choices=SOURCES)
    number = models.PositiveIntegerField()

    def __str__(self):
        return str(self.source) + str(self.number)


class Debug(models.Model):
    value = models.CharField(max_length=512)

    def __str__(self):
        return self.value