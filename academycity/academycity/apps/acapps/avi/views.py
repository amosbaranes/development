from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from django.http import HttpResponse
from .objects import DataProcessing
import os
import json


def home(request):
    company_obj_id_ = 0
    app_ = "avi"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    app_upload_file_link_ = reverse(app_+':upload_file', kwargs={})
    return render(request, app_+'/home.html', {"atm_name": app_+"_default_atm",
                                               "app": app_,
                                               "app_activate_function_link": app_activate_function_link_,
                                               "app_upload_file_link": app_upload_file_link_,
                                               "company_obj_id": company_obj_id_,
                                               "title": "Avi"}
                  )


def app_id(request, app_name, company_obj_id):
    company_obj_id_ = company_obj_id
    app_ = "avi"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "title": app_}
                  )


def app(request, app_name):
    return app_id(request, app_name, 0)


def upload_file(request):
    # print("9015", "\n", "-"*30)
    upload_file_ = request.FILES['drive_file']
    ret = {}
    if upload_file_:
        d = DataProcessing({"topic_id": "world_bank"})
        target_folder = d.TO_EXCEL
        # rtime = str(int(time.time()))
        filename = request.POST['filename']
        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file_.chunks():
                dest.write(c)

        app_ = request.POST['app']
        function_name_ = request.POST['function_name']
        obj_name_ = request.POST['obj_name']

        print("9015\n", app_, "\n", "-"*30)
        print("9016\n", function_name_, "\n", "-"*30)
        print("9017\n", obj_name_, "\n", "-"*30)
        ret['file_remote_path'] = target
    else:
        return HttpResponse(status=500)
    return HttpResponse(json.dumps(ret))

