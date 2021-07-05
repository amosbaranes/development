from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings


class ActionCategory(models.Model):
    name = models.CharField(max_length=25)


class ActionSubCategory(models.Model):
    name = models.CharField(max_length=25)
    category = models.ForeignKey(ActionCategory, default=None, on_delete=models.CASCADE, related_name='sub_categories')


class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ActionSubCategory, null=True, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

