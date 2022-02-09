#-*- coding: utf-8 -*-
from django.db import models
from cms.models import CMSPlugin
from django.urls import reverse


class Poll(models.Model):

    question = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})

    def __str__(self):              # Python 3: def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):              # Python 3: def __unicode__(self):
        return self.choice_text


# Plugins --
class PollPluginModel(CMSPlugin):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.poll.question


class ToDoForSamuel(models.Model):

    task = models.CharField(max_length=500)

