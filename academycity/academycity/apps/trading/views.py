from django.shortcuts import render
from .core.utilities import AlgoTrading


def home(request):
    title = "Algorithmic Trading Framework"
    return render(request, 'trading/home.html', {'title': title})

