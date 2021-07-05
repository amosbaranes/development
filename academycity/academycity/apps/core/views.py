from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from django.apps import apps
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from ..actions.utils import create_action


def home(request):
    title = _('Core App')
    return render(request, 'core/home.html', {'title': title})


def post_ajax_create_action(request):
    try:
        obj = None
        if request.POST.get('model') and request.POST.get('model') != "":
            app_ = request.POST.get('app')
            model_ = request.POST.get('model')
            model = apps.get_model(app_label=app_, model_name=model_)
            try:
                obj_slug = request.POST.get('obj_slug')
                # print(obj_slug)
                obj = model.objects.filter(translations__language_code=get_language()).filter(translations__slug=obj_slug).all()[0]
            except Exception as er:
                pkey_ = request.POST.get('pkey')
                obj = model.objects.get(id=pkey_)

        verb_ = request.POST.get('verb')
        create_action(request.user, verb_, obj)
    except Exception as err:
        JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ok'})


def update_field_model(request):
    app_ = request.POST.get('app')
    model_ = request.POST.get('model')
    pkey_ = request.POST.get('pkey')
    value_ = request.POST.get('value')
    field_ = request.POST.get('field')
    type_ = request.POST.get('type')
    # print('1-'*20)
    # print(value_)
    # print(model_)
    # print(pkey_)
    # print('1-'*20)
    # print('2-'*20)
    # print(field_)
    # print('2-'*20)
    model = apps.get_model(app_label=app_, model_name=model_)
    try:
        obj_slug = request.POST.get('obj_slug')
        # print(obj_slug)
        obj = model.objects.filter(translations__language_code=get_language()).filter(translations__slug=obj_slug).all()[0]
    except Exception as er:
        obj = model.objects.get(id=pkey_)
    # print(obj)
    # print('3-'*20)
    # print(type_)
    # print('4-'*20)
    if type_ == "checkbox":
        if value_ == 'true':
            value_ = True
        else:
            value_ = False
    elif type_ == "date":
        value_ = parse_date(value_)
    elif type_ == "multiple_select":
        value_ = value_.split(",")
        for k in obj.instructors.all():
            obj.instructors.remove(k)
        for i in value_:
            u_ins = User.objects.get(id=int(i))
            obj.instructors.add(u_ins)
        return JsonResponse({'status': 'ok'})
    try:
        # print(value_)
        s = 'obj.' + field_ + ' = value_'
        # print(s)
        # print('-'*30)
        # print(s)
        # print('-'*30)
        exec(s)
        obj.save()
        if model_ == "Game" and field_ == "number_of_periods":
            obj.get_schedule_period_dates
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        # print('-'*30)
        # print("err")
        # print(e)
        # print("err")
        # print('-'*30)
        pass
        return JsonResponse({'status': 'ko'})


def create_db_backup():
    call_command('dbbackup', compress=True, clean=True)


def clean_registrations(request):
    clean_accounting_registrations()


