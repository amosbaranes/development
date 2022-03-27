from django.shortcuts import render


def home(request):
    return render(request, 'businesssim/home.html', {"atm_name": "batm", "app": "businesssim", "title": "Business Sim"})
