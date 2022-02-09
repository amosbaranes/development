from django.db import models


class DataTabs(models.Model):

    tab_name = models.CharField(max_length=100, null=True)
    tab_text = models.TextField(null=True)

    def __str__(self):
        return self.tab_name
# Create your models here.
