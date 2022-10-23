from django.http import JsonResponse
from .objects import SystemMaintenance


# This function should be defined for every app
# in the view. For example:
# from ...core.apps_general_functions import activate_obj_function
def activate_obj_function(request):
    try:
        dic_ = request.POST.get('dic')
        dic_ = eval(dic_)
        # print('9080 dic_ activate_obj_function dic=', '\n', dic_, '\n', '-'*10)
        app_ = dic_["app"]
        obj_ = dic_['obj']
        fun_ = dic_['fun']
        s = 'from ..'
        if app_ != "corporatevaluation" and app_ != "core":
            s += 'acapps.'
        s += app_+'.objects import '+obj_
        # print('9081 dic_ activate_obj_function s=', '\n', s, '\n', '-'*10)
        exec(s)
        params = dic_["params"]
        # print('9082 dic_ activate_obj_function params=', '\n', params, '\n', '-'*10)
        s_ = obj_+'().' + fun_ + '(params)'
        # print('9084 dic_ activate_obj_function s_=', '\n', s_, '\n', '-'*10)
        try:
            dic = eval(s_)
            # print(dic)
        except Exception as ex:
            print(ex)
        return JsonResponse({'status': 'ok', 'result': dic})
    except Exception as ex:
        # print(ex)
        return JsonResponse({'status': 'ko: activate_obj_function'})
