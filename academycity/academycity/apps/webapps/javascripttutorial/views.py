from django.shortcuts import render


def home(request):
    return render(request, 'javascripttutorial/home.html', {})


def motion(request):
    return render(request, 'javascripttutorial/js_motion.html', {})


def whiteboard(request):
    return render(request, 'javascripttutorial/whiteboard.html', {})


def lists(request):
    return render(request, 'javascripttutorial/lists.html', {})


def data_tab(request):
    return render(request, 'javascripttutorial/data_vertical_tab.html', {})


def tab(request):
    return render(request, 'javascripttutorial/at.html', {"atm_name": "atm"})
