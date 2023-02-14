from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...users.forms import (RegistrationForm, ACAuthenticationForm)
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from ...core.utils import log_debug, clear_log_debug

dic = {10: {"title": "War Training", "type": 1, "color": "#ffffe6", "sub_tests":{"type":3, "data":{}}},
       20: {"title": "Fitness", "type": 1, "color": "#e6ffff", "sub_tests":{"type":2, "data":{}}},
       30: {"title": "Hitting", "type": 1, "color": "#e6e6ff", "sub_tests":{"type":2, "data":{}}}}

# War Training
dic[10]["sub_tests"]["data"][100010]={"title": "Single War Strip"}
dic[10]["sub_tests"]["data"][100010]["grade_conversion"]={
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}
dic[10]["sub_tests"]["data"][100020]={"title": "Single Practice", "grade_conversion": {}}
dic[10]["sub_tests"]["data"][100020]["grade_conversion"]={
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}
dic[10]["sub_tests"]["data"][100030]={"title": "Field craft", "grade_conversion": {}}
dic[10]["sub_tests"]["data"][100030]["grade_conversion"]={
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}

# # #  Physical Fitness
dic[20]["sub_tests"]["data"][2010] = {"title": "Physical Fitness", "type": 2, "color": "blue", "sub_tests": {"type": 3, "data": {}}}
dic[20]["sub_tests"]["data"][2010]["sub_tests"]["data"][201010] = {"title": "Run 300", "grade_conversion":{
    "from":[25,41,46,51,56,61,66,71,76,81],
    "to":[40,45,50,55,60,65,70,75,80,1000],
    "grade":[100,90,80,70,60,50,0,0,0,0],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2010]["sub_tests"]["data"][201020] = {"title": "Run 3000","grade_conversion":{
    "from":[8,11.31,12.01,12.31,13.01,13.31,14.01,14.31,15.01,16.01],
    "to":[11.3,12,12.3,13,13.3,14,14.3,15,16,1000],
    "grade":[100,90,80,70,60,50,0,0,0,0],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2010]["sub_tests"]["data"][201030] = {"title": "Run 5000","grade_conversion":{
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2010]["sub_tests"]["data"][201040] = {"title": "Run 10000","grade_conversion":{
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2010]["sub_tests"]["data"][201050] = {"title": "Pushups","grade_conversion":{
    "from":[40,35,30,25,20,15,0,0,0,0],
    "to":[80,39,34,29,24,19,14,0,0,0,],
    "grade":[100,90,80,70,60,50,0,0,0,0],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2010]["sub_tests"]["data"][201060] = {"title": "Pullups","grade_conversion":{
    "from":[20,17,14,10,8,6,0,0,0,0,],
    "to":[60,19,16,13,9,7,5,0,0,0],
    "grade":[100,90,80,70,60,50,0,0,0,0],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}

# Combat Fitness
dic[20]["sub_tests"]["data"][2020] = {"title": "Combat Fitness", "type": 2, "color": "blue", "sub_tests": {"type": 3, "data": {}}}
dic[20]["sub_tests"]["data"][2020]["sub_tests"]["data"][202010] = {"title": "Fighting combat", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2020]["sub_tests"]["data"][202020] = {"title": "Obstacle course", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}

#
dic[20]["sub_tests"]["data"][2030] = {"title": "Combat Fitness", "type": 2, "color": "blue", "sub_tests": {"type": 3, "data": {}}}
dic[20]["sub_tests"]["data"][2030]["sub_tests"]["data"][203010] = {"title": "Getting the weapon", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[],
    "rank":[10,9,8,7,6,5,4,3,2,1]
}}
dic[20]["sub_tests"]["data"][2030]["sub_tests"]["data"][203020] = {"title": "Getting the gun", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[20]["sub_tests"]["data"][2030]["sub_tests"]["data"][203030] = {"title": "Pre-Commando", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[20]["sub_tests"]["data"][2030]["sub_tests"]["data"][203040] = {"title": "grade for Week no 7", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[20]["sub_tests"]["data"][2030]["sub_tests"]["data"][203050] = {"title": "grade for Final preparing", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[20]["sub_tests"]["data"][2030]["sub_tests"]["data"][203060] = {"title": "Final", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}

dic[30]["sub_tests"]["data"][3010] = {"title": "Weapon", "type": 2, "color": "blue", "sub_tests": {"type": 3, "data": {}}}
dic[30]["sub_tests"]["data"][3010]["sub_tests"]["data"][301010] = {"title": "Professional use", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[30]["sub_tests"]["data"][3010]["sub_tests"]["data"][301020] = {"title": "Final Hitting test", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}

dic[30]["sub_tests"]["data"][3010]["sub_tests"]["data"][301030] = {"title": "Safety", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}

dic[30]["sub_tests"]["data"][3020] = {"title": "Gun", "type": 2, "color": "blue", "sub_tests": {"type": 3, "data": {}}}
dic[30]["sub_tests"]["data"][3020]["sub_tests"]["data"][302010] = {"title": "Professional use", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[30]["sub_tests"]["data"][3020]["sub_tests"]["data"][302020] = {"title": "Final Hitting test", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}
dic[30]["sub_tests"]["data"][3020]["sub_tests"]["data"][302030] = {"title": "Safety", "grade_conversion":{
    "from":[],
    "to":[],
    "grade":[]
}}

def home(request):
    if request.method == "POST":
        form_login = ACAuthenticationForm(request, data=request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return home_logged(request)
        else:
            return signup_login_form(request, error_message="Invalid username or password.")
    elif request.user.is_authenticated:
        home_logged(request)
    return signup_login_form(request, error_message='')

def signup_login_form(request, error_message=''):
    form_login = ACAuthenticationForm()
    form_signup = RegistrationForm()
    arg = {'form_login': form_login, 'form_signup': form_signup, 'error_message': error_message,
           'redirect_field_name': "next", 'redirect_field_value': reverse('training:home')
           }
    return render(request, 'training/login_page.html', arg)

def home_logged(request):
    log_debug("home_logged")
    # try:
    #     logout()
    # except Exception as ex:
    #     pass
    wsc = WebSiteCompany(request, web_company_id=20)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id

    # print(request.user.groups.all().values()) #  .filter(name=group_name).exists()
    app_name = "default"
    if request.user.groups.filter(name="t_senior_manager").exists():
        app_name = "senm"
    elif request.user.groups.filter(name="t_admin").exists():
        app_name = "admin"
    log_debug(app_name)
    return app_id(request, app_name, company_obj_id_)

def homet(request):
    if not request.user.is_authenticated:
        return signup_login_form(request, error_message='You need to login')
    wsc = WebSiteCompany(request, web_company_id=20, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_name = "default"
    return app_id(request, app_name, company_obj_id_)

def app_id(request, app_name, company_obj_id):
    if not request.user.is_authenticated:
        return signup_login_form(request, error_message='You need to login')
    company_obj_id_ = company_obj_id
    app_ = "training"
    log_debug("app_id " + app_name + " "  + app_ + " " + str(company_obj_id))
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "title": app_}
                  )

def appt(request, app_name):
    if not request.user.is_authenticated:
        return signup_login_form(request, error_message='You need to login')
    wsc = WebSiteCompany(request, web_company_id=20, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    if request.user.groups.filter(name="admins").exists():
        return app_id(request, app_name, company_obj_id_)
    else:
        return home(request)

def app(request, app_name):
    if not request.user.is_authenticated:
        return signup_login_form(request, error_message='You need to login')
    wsc = WebSiteCompany(request, web_company_id=20)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    if request.user.groups.filter(name="admins").exists():
        return app_id(request, app_name, company_obj_id_)
    elif request.user.is_authenticated():
        return home_logged(request)
