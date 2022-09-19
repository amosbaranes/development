from django.http import JsonResponse
from ..corporatevaluation.xbrl_obj import AcademyCityXBRL


# This function should be defined for every app
def activate_obj_function(request):
    try:
        dic_ = request.POST.get('dic')
        dic_ = eval(dic_)
        # print('dic_')
        # print(dic_)
        # print('dic_')
        obj_ = dic_['obj']
        fun_ = dic_['fun']
        params = dic_["params"]
        # print(params)
        s_ = obj_+'().' + fun_ + '(params)'
        # print(s_)
        dic = eval(s_)
        return JsonResponse({'status': 'ok', 'result': dic})
    except Exception as ex:
        # print(ex)
        return JsonResponse({'status': 'ko: activate_obj_function'})
