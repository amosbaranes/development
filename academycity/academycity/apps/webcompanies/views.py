from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _, get_language


def home(request):
    title = _('Web Companies App')
    return render(request, 'webcompanies/home.html', {'title': title})

