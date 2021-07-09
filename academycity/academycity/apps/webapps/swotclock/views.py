from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
import json
from .models import SWOTClockData, SWOTClock


def index(request):
    title = _('SWOT clock App')
    return render(request, 'swotclock/index.html', {'title': title})


def save_data(request):
    is_new = request.POST.get('is_new')
    if int(is_new) == 1:
        file_name_ = request.POST.get('file_name')
    else:
        swot_clock_id = request.POST.get('swot_clock_id')
        obj = SWOTClock.objects.get(id=swot_clock_id)
        file_name_ = obj.file_name
        obj.delete()
    obj = SWOTClock.objects.create(swot_user=request.user, file_name=file_name_)
    # print('obj')
    # print(obj)
    # print('obj')
    data = request.POST.get('data')
    # print('data')
    # print(data)
    # print('data')

    json_data = json.loads(data)

    # print('json_data')
    # print(json_data)
    # print('json_data')

    for k in json_data:
        # print('k, json_data[k]')
        # print(k, json_data[k])
        # print('k, json_data[k]')
        SWOTClockData.objects.create(swot_clock=obj, field_id=k, field_value=json_data[k])

    dic = {'status': 'File was saved'}
    return JsonResponse(dic)


def get_data(request):
    swot_clock_id = request.POST.get('swot_clock_id')
    dic_ = SWOTClockData.objects.filter(swot_clock__id=swot_clock_id)
    # dic = json.dumps(list(dic_))
    obj = {}
    for q in dic_:
        obj[q.field_id] = q.field_value
    return JsonResponse(obj)


def get_user_swot(request):
    # print(request.user)
    dic_ = SWOTClock.objects.filter(swot_user=request.user)
    obj = {}
    for q in dic_:
        obj[q.id] = q.file_name
    # print(obj)
    return JsonResponse(obj)


def delete_data(request):
    swot_clock_id = request.POST.get('swot_clock_id')
    print(swot_clock_id)
    try:
        SWOTClock.objects.filter(id=swot_clock_id).delete()
    except Exception as ex:
        print(ex)
    dic = {'status': 'File was deleted'}
    return JsonResponse(dic)

