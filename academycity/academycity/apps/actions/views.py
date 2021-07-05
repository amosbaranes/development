from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _, get_language
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib import messages
from ..core.email import email_message


def home(request):
    title = _('Actions  11')
    return render(request, 'actions/home.html', {'title': title})

