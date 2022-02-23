from django.shortcuts import render


def home(request):
    return render(request, 'businesssim/home.html', {"atm_name": "batm", "title": "Business Sim"})
