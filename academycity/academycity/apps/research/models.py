from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, get_language

class InputFiles(models.Model):
    class Meta:
        verbose_name = _('inputfile')
        verbose_name_plural = _('inputfiles')
        ordering = ['-id']
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                             related_name='input_files')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='research/potential')
    file_result = models.CharField(max_length=218, null=True)
    created_at = models.DateTimeField(auto_now_add=True)