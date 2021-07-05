from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
# from .documents import InstitutionWebDocument
from django.http import JsonResponse


def home(request):
    title = _('Search App')
    return render(request, 'search/home.html', {'title': title})


def search(request):
    rr = {}

    # q = request.POST.get('q')
    # # print('q')
    # # print(q)
    # # print('q')
    #
    # if q:
    #     inst = InstitutionWebDocument.search().query('match', institution_name=q)
    # else:
    #     inst = ''
    #
    # for hit in inst:
    #     # print('-'*50)
    #     # print(
    #     #     "Inst name : {}, description {} - {}".format(hit.institution_name, hit.institution_short_description,
    #     #                                                  hit.email)
    #     # )
    #     rr[str(hit.id)] = {'institution_name': hit.institution_name,
    #                        'institution_short_description': hit.institution_short_description,
    #                        'email': hit.email}

    return JsonResponse(rr)
