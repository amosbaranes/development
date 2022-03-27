from django.shortcuts import render


def home(request):
    return render(request, 'macroeconomics/home.html', {"atm_name": "matm", "app": "businesssim", "title": "Macro Economics"})
