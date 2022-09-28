from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from django.apps import apps
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from ..actions.utils import create_action
from .AdvancedTabes import AdvancedTabs
from ..acapps.accounting.models import Locations, TimeDim
from ..core.utils import log_debug
from .accounting_obj import AccountingObj
from django.db.models.fields.related import ForeignKey, ManyToManyField, ManyToManyRel


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


def update_field_model_by_id(request, foreign=None):
    # log_debug("update_field_model_by_id 0")
    dic_ = request.POST["dic"]
    # print('-1'*50)
    # print('update_field_model_by_id: dic_')
    # print(dic_)
    # print('-1'*50)
    log_debug(dic_)
    # print('dic_')
    dic_ = eval(dic_)
    app_ = dic_['app']
    model_ = dic_['model']
    pkey_ = dic_['pkey']
    fields_ = dic_['fields']
    type_ = dic_['type']
    company_obj_id_ = dic_['company_obj_id']
    parent_model_ = dic_['parent_model']
    parent_model = apps.get_model(app_label=app_, model_name=app_+"web")
    company_obj = parent_model.objects.get(id=company_obj_id_)
    model = apps.get_model(app_label=app_, model_name=model_)
    if pkey_ == "new":
        s = ""
        if model.model_field_exists(app_+'_web') and isinstance(model._meta.get_field("businesssim_web"), ForeignKey):
            # print("it is a foreign key")
            s = "model.objects.create("
            s += app_ + '_web=company_obj '
        if parent_model_ != "":
            # print('9040\n', s)
            if s == "":
                s = "model.objects.create("
            parent_pkey_ = dic_['parent_pkey']
            parent_model__ = apps.get_model(app_label=app_, model_name=parent_model_)
            parent_model_fk_name = parent_model_[:-1]
            parent_obj__ = parent_model__.objects.get(id=parent_pkey_)
            s += ", "+parent_model_fk_name+'=parent_obj__'
        try:
            # print('9045')
            space_ = ", "
            if s == "":
                s = "model.objects.create("
                space_ = ""
            # print("9045 ")
            foreign_keys = dic_["foreign_keys"]
            # print("9046 ")
            for k in foreign_keys:
                t_obj = apps.get_model(app_label=app_, model_name=foreign_keys[k]["foreign_table"])
                obj__ = t_obj.objects.get(id=int(foreign_keys[k]["value"]))
                # print("=6"*10)
                # print(obj__)
                # print("=6"*10)
                try:
                    myVars = vars()
                except Exception as ex:
                    print("err800: "+str(ex))
                try:
                    myVars[k] = obj__
                except Exception as ex:
                    log_debug("err900: "+str(ex))
                s += space_+k+'='+k
                space_ = ", "
        except Exception as ex:
            pass
            # print("save with fkey error " + str(ex))
        s += ')'
        try:
            # print("9050\n" + s)
            obj = eval(s)
            # print("9051\n" + s)

            # print("9042 "+str(model._meta.get_field("businesssim_web")))

            if model.model_field_exists(app_ + '_web') and isinstance(model._meta.get_field("businesssim_web"), ManyToManyField):
                s = "obj."+app_ + '_web.add(company_obj)'
                # print("9035\n", s)
                eval(s)
                # print("9052")
                obj.save()
                # print("9055")
        except Exception as ex:
            print("error701 "+str(ex))
            log_debug("error701 "+str(ex))
    else:
        try:
            obj_slug = request.POST.get('obj_slug')
            # print(obj_slug)
            obj = \
            model.objects.filter(translations__language_code=get_language()).filter(translations__slug=obj_slug).all()[0]
        except Exception as er:
            obj = model.objects.get(id=pkey_)

    # print('9088  obj')
    # print(obj)
    # print('9088  obj')

    try:
        for f in fields_:
            value_ = fields_[f]
            # print("9071 ", f, value_)
            try:
                if isinstance(model._meta.get_field(f), ManyToManyRel):
                    l_ = value_.split(",")
                    for z in l_:
                        print(z)
                        model__ = apps.get_model(app_label=app_, model_name=f.split("_")[1])
                        model__v = model__.objects.get(id=int(z))
                        print(model__v)
                        try:
                            print("model__v." + f.split("_")[0] + "_web.add(obj)")
                            exec("model__v." + f.split("_")[0] + "_web.add(obj)")
                            model__v.save()
                        except Exception as ex:
                            print("Error 9072 " + ex)

                    print(9089)
                    return JsonResponse({'status': 'ok', "record_id": obj.id})
            except Exception as ex:
                print("Error 450: "+str(ex))

            # print("f", f, "fields_[f]", fields_[f])
            if type_ == "checkbox":
                if value_ == 'true':
                    value_ = True
                else:
                    value_ = False
            elif type_ == "date":
                try:
                    v_ = parse_date(value_)
                    if v_:
                        value_ = v_
                except Exception as exx:
                    print(exx)
            elif type_ == "multiple_select":
                # need to fix this part
                # need to fix this part
                value_ = value_.split(",")
                for k in obj.instructors.all():
                    obj.instructors.remove(k)
                for i in value_:
                    u_ins = User.objects.get(id=int(i))
                    obj.instructors.add(u_ins)
                # need to fix this part
                # need to fix this part
                return JsonResponse({'status': 'ok'})
            try:
                try:
                    foreign_keys = dic_["foreign_keys"]
                    # print(foreign_keys, f)
                    model_f = apps.get_model(app_label=app_, model_name=foreign_keys[f]["foreign_table"])
                    # print(model_f)
                    # print("9011 ", value_)
                    value_ = model_f.objects.get(id=value_)
                    # print("9012 ", value_)
                except Exception as ex:
                    pass
                    # print("Error 600: "+str(ex))
                setattr(obj, f, value_)
            except Exception as ex:
                print("Error 800: "+str(ex))
        try:
            obj.save()
        except Exception as eex:
            print("Error 850: "+str(eex))
        return JsonResponse({'status': 'ok', "record_id": obj.id})
    except Exception as e:
        log_debug("erro600 " + str(e))
        return JsonResponse({'status': 'ko'})


def get_data_link(request):
    dic_ = request.POST["dic"]
    dic_ = eval(dic_)
    # print('get_data_link dic_= ')
    # print(dic_)
    # print(dic_["fields"])
    # print('dic_')
    multiple_select_fields = None
    if "multiple_select_fields" in dic_:
        if len(dic_["multiple_select_fields"]) > 0:
            multiple_select_fields = dic_["multiple_select_fields"]
    if "id" not in dic_["fields"]:
        dic_["fields"].insert(0, "id")

    app_ = dic_['app']
    model_ = dic_['model']
    # print("model_: "+model_)
    if model_ == "":
        dic = {'status': 'ko', "dic": {}}
        return JsonResponse(dic)

    fields_str = '"'
    for f in dic_["fields"]:
        try:
            exec(f + ' = []')
            fields_str += f + '","'
        except Exception as ex:
            print("error 400"+str(ex))
    fields_str = fields_str[:len(fields_str)-2]

    # print("=2"*50)
    # print(fields_str)
    # print("=2"*50)

    model = apps.get_model(app_label=app_, model_name=model_)

    # fields_ = model._meta.get_fields(include_parents=True, include_hidden=True)
    # print(fields_)

    number_of_rows_ = 2
    try:
        number_of_rows_ = dic_['number_of_rows']
        number_of_rows_ = int(number_of_rows_)
    except Exception as ex:
        pass
        # print(ex)
    parent_id_ = -1
    try:
        parent_id_ = int(dic_['parent_id'])
    except Exception as ex:
        # print("error 500 "+str(ex))
        pass
    company_obj_id_ = dic_['company_obj_id']
    filters = dic_['filters']

    # print(dic_['order_by'])
    if len(dic_['order_by']) > 0:
        order_by = dic_['order_by']
    else:
        order_by = ""
    if company_obj_id_ != "-1":
        parent_model = apps.get_model(app_label=app_, model_name=app_+"web")
        # print(parent_model)
        company_obj = parent_model.objects.get(id=company_obj_id_)
        s = 'model.objects'
        s_ = ''
        if model.model_field_exists(app_+'_web') and isinstance(model._meta.get_field(app_+'_web'),
                                                                    ForeignKey):
                s_ += app_ + '_web=company_obj '

        if parent_id_ > -1:
            parent_model_ = dic_['parent_model']
            parent_pkey_ = parent_id_
            parent_model__ = apps.get_model(app_label=app_, model_name=parent_model_)
            parent_model_fk_name = parent_model_[:-1]
            parent_obj__ = parent_model__.objects.get(id=parent_pkey_)
            s_ += ', ' + parent_model_fk_name+'=parent_obj__'
        if s_ != '':
            s += '.filter('+s_+')'
        # print('s00')
        # print(s)
        # print('s00')
    else:
        if parent_id_ > -1:
            parent_model_ = dic_['parent_model']
            parent_pkey_ = parent_id_
            parent_model__ = apps.get_model(app_label=app_, model_name=parent_model_)
            parent_model_fk_name = parent_model_[:-1]
            parent_obj__ = parent_model__.objects.get(id=parent_pkey_)
            s = 'model.objects.filter(' + parent_model_fk_name+'=parent_obj__)'
        else:
            s = 'model.objects'
        # print('500 s '+s)
        # print('500 s '+s)
        # print('500 s '+s)
    try:
        for f in filters:
            filter_field_ = f
            filter_value_ = filters[f]["value"]
            foreign_table_ = ""
            try:
                foreign_table_ = filters[f]["foreign_table"]
            except Exception as exx:
                pass
                # print(exx)
            if filter_value_ != "":
                if foreign_table_ != "":
                    s += '.filter('+foreign_table_+'__id__icontains='+filter_value_+')'
                else:
                    s += '.filter('+filter_field_+'__icontains="'+filter_value_+'")'
        if order_by != "":
            s += '.order_by("'+order_by["field"]+'")'
            if order_by["direction"] == "descending":
                s += '.reverse()'
        if multiple_select_fields:
            ss__ = s+'.all()[:number_of_rows_]'
            # print('ss__')
            # print(ss__)
            # print('ss__')
            data__ = eval(ss__)
        s += '.all()[:number_of_rows_].values('+fields_str+')'
        # print('s111')
        # print(s)
        # print('s11')
        data = eval(s)
    except Exception as ex:
        print("error 300 "+str(ex))
        # pass

    dic = {}
    if multiple_select_fields:
        for z in multiple_select_fields:
            dic[z] = []
            for q in data__:
                qs = eval('q.'+z+'.all()')
                s = ""
                for q_ in qs:
                    if s != "":
                        s += ","
                    s += str(q_.id)
                dic[z].append(s)
    # print('data')
    # print(data)
    # print('data')

    try:
        for q in data:
            for f in dic_["fields"]:
                # print(f+'.append(q[\''+f+'\'])')
                eval(f+'.append(q[\''+f+'\'])')
                # print(eval(f))

        for ff in dic_["fields"]:
            dic[ff] = eval(ff)
    except Exception as ex:
        pass
        print(ex)

    # print("=2"*50)
    # print(dic)
    # print("=2"*50)

    dic = {'status': 'ok', "dic": dic}
    # print(dic)
    return JsonResponse(dic)

