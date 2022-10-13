from django.http import JsonResponse
from ..corporatevaluation.xbrl_obj import AcademyCityXBRL, TDAmeriTrade
from ...apps.acapps.dl.utilities.algos import AlgoDL


# This function should be defined for every app
def activate_obj_function(request):
    try:
        dic_ = request.POST.get('dic')
        dic_ = eval(dic_)
        # print('9088 dic_ activate_obj_function')
        # print(dic_)
        # print('90881 dic_')
        obj_ = dic_['obj']
        fun_ = dic_['fun']
        params = dic_["params"]
        # print('9082 params')
        # print(params)
        # print('9083 params')
        s_ = obj_+'().' + fun_ + '(params)'
        # print('9090 s_')
        # print(s_)
        # print('9091 s_')
        dic = eval(s_)
        # print(dic)
        return JsonResponse({'status': 'ok', 'result': dic})
    except Exception as ex:
        # print(ex)
        return JsonResponse({'status': 'ko: activate_obj_function'})
