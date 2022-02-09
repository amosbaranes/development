from django.shortcuts import render
from django.http import JsonResponse
from .models import DataTabs


def home(request):
    return render(request, 'javascripttutorial/home.html', {})


def motion(request):
    return render(request, 'javascripttutorial/js_motion.html', {})


def whiteboard(request):
    return render(request, 'javascripttutorial/whiteboard.html', {})


def lists(request):
    return render(request, 'javascripttutorial/lists.html', {})


def tab(request):
    return render(request, 'javascripttutorial/vertical_tab.html', {})


def data_tab(request):
    return render(request, 'javascripttutorial/data_vertical_tab.html', {})


def add_tab(request):
    tab_name_ = request.POST["tab_name"]
    new_tab, is_new_row = DataTabs.objects.get_or_create(tab_name=tab_name_)
    # print(new_tab, is_new_row)
    dic = {'status': 'ok', 'tab_id': new_tab.id}
    return JsonResponse(dic)


def get_tabs_from_table(request):
    tabs = DataTabs.objects.all()
    dic = {}
    for t in tabs:
        dic[t.id] = {"tab_name": t.tab_name, "tab_text": t.tab_text}
    return JsonResponse(dic)


def delete_tab(request):
    try:
        tab_name_ = request.POST["tab_name"]
        tab_to_delete = DataTabs.objects.get(tab_name=tab_name_)
        tab_id_ = tab_to_delete.id
        tab_to_delete.delete()
        dic = {'status': 'ok', 'tab_id': tab_id_}
    except Exception as ex:
        dic = {'status': 'ko', 'tab_id': "-1"}
    return JsonResponse(dic)


def update_text_tab(request):
    try:
        tab_id_ = request.POST["tab_id"]
        tab_value_ = request.POST["value"]
        tab_to_update = DataTabs.objects.get(id=tab_id_)
        tab_to_update.tab_text = tab_value_
        tab_to_update.save()
        dic = {'status': 'ok'}
    except Exception as ex:
        dic = {'status': 'ko'}
    return JsonResponse(dic)