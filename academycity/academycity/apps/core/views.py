from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from django.apps import apps
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from ..actions.utils import create_action
from .AdvancedTabes import AdvancedTabs


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


def activate_function(request):
    # var dic_ = {"obj": "AdvancedTabs", "atm": atm_.my_name, "app": atm_.my_app, "fun": "add_tab",
    #             "params": {"tab_name": tab_name_}}
    try:
        dic_ = request.POST["dic"]
        dic_ = eval(dic_)
        # print(dic_)

        obj_ = dic_["obj"]
        atm_ = dic_["atm"]
        app_ = dic_["app"]
        fun_ = dic_["fun"]
        params_ = dic_["params"]

        # print('-1'*20)
        s = obj_ + "('"+atm_+"', '"+app_+"')." + fun_ + "(params_)"
        # print(s)
        # print('-1'*20)
        result = eval(s)
        # print('-3'*20)
        dic = {'status': 'ok', 'result': result}
        # print(dic)
    except Exception as ex:
        dic = {'status': 'ko', 'result': "{}"}
    return JsonResponse(dic)


def update_field_model_by_id(request):
    dic_ = request.POST["dic"]
    print('dic_')
    print(dic_)
    print('dic_')
    dic_ = eval(dic_)
    app_ = dic_['app']
    model_ = dic_['model']
    pkey_ = dic_['pkey']
    value_ = dic_['value']
    field_ = dic_['field']
    type_ = dic_['type']
    company_obj_id_ = dic_['company_obj_id']
    parent_model_ = dic_['parent_model']
    # print('1-'*20)
    # print(value_)
    # print(model_)
    # print(pkey_)
    # print('1-'*20)
    # print('2-'*20)
    # print(field_)
    # print('2-'*20)
    # print(company_obj_id_)
    # print('2-'*20)
    # print(parent_model_)
    # print('2-'*20)

    parent_model = apps.get_model(app_label=app_, model_name=app_+"web")
    # print(parent_model)
    company_obj = parent_model.objects.get(id=company_obj_id_)

    model = apps.get_model(app_label=app_, model_name=model_)
    # try:
    #     model.truncate()
    # except Exception as ex:
    #     print(ex)
    # Students

    if pkey_ == "new":
        print("1"*20)
        print(parent_model_)
        print("1"*20)
        if parent_model_ != "":
            parent_pkey_ = dic_['parent_pkey']
            print(parent_pkey_)
            print("2"*20)
            parent_model__ = apps.get_model(app_label=app_, model_name=parent_model_)
            print("3"*20)
            parent_model_fk_name = parent_model_[:-1]
            print("4"*20)
            print(parent_model_fk_name)
            parent_obj__ = parent_model__.objects.get(id=parent_pkey_)
            s = 'model.objects.create('+app_+'_web=company_obj, '+parent_model_fk_name+'=parent_obj__)'
        else:
            s = 'model.objects.create('+app_+'_web=company_obj)'
        print(s)
        obj = eval(s)
        # print(obj)
        # print('2'*30)
    else:
        try:
            obj_slug = request.POST.get('obj_slug')
            # print(obj_slug)
            obj = \
            model.objects.filter(translations__language_code=get_language()).filter(translations__slug=obj_slug).all()[0]
        except Exception as er:
            obj = model.objects.get(id=pkey_)

    # print('6'*30)
    # print(obj)
    # print('7-'*20)
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
        # print('-'*30)
        # print(s)
        # print('-'*30)
        exec(s)
        obj.save()
        # print(obj.id)
        return JsonResponse({'status': 'ok', "record_id": obj.id})
    except Exception as e:
        # print('-'*30)
        # print("err")
        # print(e)
        # print("err")
        # print('-'*30)
        # pass
        return JsonResponse({'status': 'ko'})


def get_data_link(request):
    dic_ = request.POST["dic"]
    dic_ = eval(dic_)
    # print('dic_')
    # print(dic_)
    # print(dic_["fields"])
    # print('dic_')
    dic_["fields"].insert(0, "id")
    app_ = dic_['app']
    model_ = dic_['model']
    # print(model_)
    if model_ == "":
        dic = {'status': 'ko', "dic": {}}
        return JsonResponse(dic)

    fields_str = '"'
    for f in dic_["fields"]:
        try:
            exec(f + ' = []')
            fields_str += f + '","'
        except Exception as ex:
            print(ex)
    fields_str = fields_str[:len(fields_str)-2]
    model = apps.get_model(app_label=app_, model_name=model_)
    # print(model)

    number_of_rows_ = int(dic_['number_of_rows'])
    parent_id_ = -1
    try:
        parent_id_ = int(dic_['parent_id'])
    except Exception as ex:
        pass
    # print(parent_id_)
    company_obj_id_ = dic_['company_obj_id']
    # print(company_obj_id_)
    if company_obj_id_ != "-1":
        parent_model = apps.get_model(app_label=app_, model_name=app_+"web")
        # print(parent_model)
        company_obj = parent_model.objects.get(id=company_obj_id_)
        if parent_id_ > -1:
            parent_model_ = dic_['parent_model']
            parent_pkey_ = parent_id_
            parent_model__ = apps.get_model(app_label=app_, model_name=parent_model_)
            parent_model_fk_name = parent_model_[:-1]
            parent_obj__ = parent_model__.objects.get(id=parent_pkey_)
            s = 'model.objects.filter(accounting_web=company_obj, ' + parent_model_fk_name
            s += '=parent_obj__).all()[:number_of_rows_].values(' + fields_str + ')'
        else:
            s = 'model.objects.filter(accounting_web=company_obj).all()[:number_of_rows_].values('+fields_str+')'
    else:
        if parent_id_ > -1:
            parent_model_ = dic_['parent_model']
            parent_pkey_ = parent_id_
            parent_model__ = apps.get_model(app_label=app_, model_name=parent_model_)
            parent_model_fk_name = parent_model_[:-1]
            parent_obj__ = parent_model__.objects.get(id=parent_pkey_)
            s = 'model.objects.filter(' + parent_model_fk_name
            s += '=parent_obj__).all()[:number_of_rows_].values(' + fields_str + ')'
        else:
            s = 'model.objects.all()[:number_of_rows_].values('+fields_str+')'
    try:
        # print(s)
        data = eval(s)
    except Exception as ex:
        # print(ex)
        pass

    # print(1000)

    for q in data:
        for f in dic_["fields"]:
            # print(f+'.append(q[\''+f+'\'])')
            eval(f+'.append(q[\''+f+'\'])')
            # print(eval(f))

    dic = {}
    for ff in dic_["fields"]:
        dic[ff] = eval(ff)
    dic={'status': 'ok', "dic": dic}
    # print(dic)
    return JsonResponse(dic)


# def get_adjective_link(request):
#     dic_ = request.POST["dic"]
#     dic_ = eval(dic_)
#     # print('dic_')
#     # print(dic_)
#     # print('dic_')
#     app_ = dic_['app']
#     adjective_ = dic_['adjective']
#     model = apps.get_model(app_label=app_, model_name="AdjectivesValues")
#
#     data = model.adjectives.adjectives(adjective_title=adjective_)
#
#     dic = {}
#     for q in data:
#         dic[q.id] = q.value
#
#     dic = {'status': 'ok', "dic": dic}
#     # print(dic)
#     return JsonResponse(dic)

