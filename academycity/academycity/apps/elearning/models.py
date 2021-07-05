# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, get_language
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404


# https://pypi.org/project/django-currentuser/
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)

from filer.fields.image import FilerImageField
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields
from parler.utils.context import switch_language

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from ..core.fields import OrderField
from ..courses.models import Section


# @python_2_unicode_compatible
class Question(models.Model):
    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, related_name='questions', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    question_text = PlaceholderField('question_text')

    def __str__(self):
        return str(self.id)


# @python_2_unicode_compatible
class Answer(models.Model):
    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    answer_text = PlaceholderField('answer_text')

    def __str__(self):
        return str(self.id)


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'user', )

