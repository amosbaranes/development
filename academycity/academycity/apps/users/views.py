from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, reverse_lazy
from .models import (Institution, Profile,)
from ..webapps.education.models import ReceivedMessages
from ..courses.models import (Department, GeneralLedger, TrialBalance, Order,
                              OrderItem, CourseSchedule, CourseScheduleUser)
from .forms import (ProfileEditForm, UserEditForm, RegistrationForm)
from ..actions.models import Action
from ..courses.models import (CourseScheduleUser, Order, TrialBalance,
                              Course, Section, SubSection)
from ..core.accounting import update_trial_balance
from django.utils.translation import ugettext_lazy as _, get_language
from django.db.models import Q

import pandas as pd
from ..core.sql import SQL
from ..core.email import email_message
from ..courses.models import Coupon, CourseScheduleUser
from ..core.sql import SQL
from ..core.filesystem import FS
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..webcompanies.WebCompanies import WebSiteCompany
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# from allauth.account.forms import SignupForm
from django.core.mail import EmailMessage


def show_sub_content(request):
    sub_page = request.POST.get('sub_page')

    if sub_page == "process_trial_balance":
        period_type = request.POST.get('period_type')
        update_trial_balance(period_type)
        period_type_ = 1
        if '3' in period_type:
            period_type_ = 3
        elif '2' in period_type:
            period_type_ = 2

        trial_balance_1 = TrialBalance.objects.filter(flow_type=1).filter(period_type=period_type_)
        trial_balance_2 = TrialBalance.objects.filter(flow_type=2).filter(period_type=period_type_)
        return render(request, 'users/_process_trial_balance.html',
                      {'period_type': period_type,
                       'trial_balance_1': trial_balance_1,
                       'trial_balance_2': trial_balance_2,
                       })
    elif sub_page == "admin_role_management_courses":
        report = request.POST.get('report')
        departments = Department.objects.all().filter(translations__language_code=get_language()).order_by('order')
        return render(request, 'users/_admin_role_management_courses.html', {'departments': departments})
    elif sub_page == "instructor_role_management_courses":
        report = request.POST.get('report')
        ics = CourseSchedule.objects.filter(instructors=request.user).all()
        print(ics)
        return render(request, 'users/_instructor_role_management_courses.html', {'course_schedules': ics})
    elif sub_page == "student_role_management_courses":
        report = request.POST.get('report')
        if report == 'courses':
            my_course_schedule_user = \
                CourseScheduleUser.objects.filter(user=request.user).filter(course_schedule__active=True)
            my_course_schedule_user_completed = \
                CourseScheduleUser.objects.filter(user=request.user).filter(course_schedule__active=False)

            my_orders = Order.objects.filter(user=request.user)
            return render(request, 'users/_student_role_management_courses.html',
                          {'my_course_schedule_user': my_course_schedule_user,
                           'my_orders': my_orders,
                           'my_course_schedule_user_completed': my_course_schedule_user_completed
                           })
    elif sub_page == "admin_role_management_maintenance":
        report = request.POST.get('report')
        print(report)
        general_ledger = GeneralLedger.objects.all()
        trial_balance = TrialBalance.objects.all()
        order = Order.objects.all()
        order_item = OrderItem.objects.all()
        course_schedule = CourseSchedule.objects.all()
        course_schedule_user = CourseScheduleUser.objects.all()
        coupon = Coupon.objects.all()
        return render(request, 'users/_admin_role_management_maintenance.html',
                      {'general_ledger': general_ledger,
                       'trial_balance': trial_balance,
                       'order': order,
                       'order_item': order_item,
                       'course_schedule': course_schedule,
                       'course_schedule_user': course_schedule_user,
                       'coupon': coupon,
                       })
    elif sub_page == "admin_role_management_clean_accounting_registrations":
        print(1111)
        # report = request.POST.get('report')
        # print(report)
        # sql = SQL()
        # print('-1-')
        # sql.exc_sql("""truncate table courses_trialbalance""", ())
        # print('-12-')
        # sql.exc_sql("""truncate table courses_generalledger""", ())
        # print('-13-')
        # sql.exc_sql("""
        #             truncate table courses_coupon, courses_orderitem,
        #             courses_order, courses_coursescheduleuser, courses_courseschedule_instructors,
        #             courses_courseschedule""", ())
        print('-15-')
        return render(request, 'users/_admin_role_management_car.html', {'results': 'ok'})
    elif sub_page == "admin_role_management_registered_users":
        report = request.POST.get('report')
        User = get_user_model()
        if report == 'signed_up':
            users = User.objects.order_by('-date_joined')
        elif report == 'not_registered_for_course':
            users = User.objects.filter(course_schedule_users__isnull = True).order_by('-date_joined')
        return render(request, 'users/_admin_role_management_registered_users.html', {'users': users})

    elif sub_page == "admin_role_management_file_system":
        report = request.POST.get('report')
        fs = FS()
        if report == 'file_system':
            fs_info = fs.get_info_for(path="/")
            return render(request, 'users/_admin_role_management_file_system.html', {'fs_info': fs_info})
        if report == 'backup':
            path = settings.DBBACKUP_STORAGE_OPTIONS['location']
            files = fs.get_files_in(path)
            return render(request, 'users/_admin_role_management_backup.html', {'path': path, 'files': files})


    elif sub_page == "admin_role_management_documentations":
        report = request.POST.get('report')
        if report == 'academycity':
            return render(request, 'users/_admin_role_management_documentations.html', {})
    elif sub_page == "admin_role_management_research":
        report = request.POST.get('report')
        if report == 'all':
            return render(request, 'users/_admin_role_management_research.html', {'report': report})

    return render(request, 'users/_show_content.html', {'page': sub_page})


def show_content(request):
    page=request.POST.get('page')
    if page == "student_role_management":
        return render(request, 'users/_student_role_management.html', {})
    elif page == "admin_role_management":
        return render(request, 'users/_admin_role_management.html', {})

    # elif page == "my_courses":
    #     my_course_schedule_user = \
    #         CourseScheduleUser.objects.filter(user=request.user).filter(course_schedule__active=True)
    #     my_course_schedule_user_completed = \
    #         CourseScheduleUser.objects.filter(user=request.user).filter(course_schedule__active=False)
    #     my_orders = Order.objects.filter(user=request.user)
    #     return render(request, 'users/_my_course_schedule_user.html',
    #                   {'my_course_schedule_user': my_course_schedule_user,
    #                    'my_orders': my_orders,
    #                    'my_course_schedule_user_completed': my_course_schedule_user_completed
    #                    })
    elif page == "my_actions":
        my_actions = Action.objects.filter(user=request.user)
        return render(request, 'users/_my_actions.html', {'my_actions': my_actions})
    elif page == "all_actions":
        # all_actions = Action.objects.all()
        verbs_ = list(Action.objects.values_list('verb', flat=True))
        verbs_ = list(set(verbs_))
        print(verbs_)
        Action.objects.filter(object_id__isnull=False)
        print('users/_all_actions.html')

        return render(request, 'users/_all_actions.html', {
            'verbs': verbs_
            # 'all_actions': all_actions
        })
    elif page == "courses_actions":
        page = request.POST.get('page')
        by = 'a.created'
        filter = ''
        if request.POST.get('filter') is not None:
            filter = request.POST.get('filter')
            if filter == '':
                by = request.POST.get('by')
            else:
                filter_where = request.POST.get('filter_where')
                filter = ' and ' + filter_where + ' = ' + request.POST.get('filter')
        # print('-----')
        # print(page)
        # print(filter)
        # print(by)
        # print('-----')
        sql = SQL()
        squery = '''
                SELECT a.created, a.verb, ss.id, s.id, c.id, cs.id, au.id
                FROM actions_Action a, courses_SubSection ss, courses_Section s, courses_course c, auth_user au,
                courses_CourseScheduleUser csu, courses_CourseSchedule cs
                WHERE a.object_id = ss.id
                and ss.section_id = s.id
                and s.course_id = c.id
                and a.user_id = au.id
                and cs.course_id = c.id                
                and csu.course_schedule_id = cs.id                
                and csu.user_id = au.id
                ''' + filter + " order by " + by
        # print(squery)
        results = sql.exc_sql(squery, [], verb='select')
        results = pd.DataFrame(results, columns=['created', 'verb', 'SubSection', 'Section', 'Course', 'Class', 'User'])
        return render(request, 'users/_courses_actions.html', {
            'df': results
        })

    elif page == "accountant_close_the_books":
        return render(request, 'users/_accountant_close_the_books.html', {})
    elif page == "active_courses":
        return render(request, 'users/_instructor_active_courses.html', {})

    return render(request, 'users/_show_content.html', {'page': page})


# Institutions views
class InstitutionsView(ListView):
    template_name = 'institution_list.html'
    model = Institution


class InstitutionView(DetailView):
    template_name = 'users/institutions_detail.html'
    model = Institution


# https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/
class CreateInstitution(CreateView):
    model = Institution
    fields = ['name', 'type']
    #institution_form.html


class UpdateInstitution(UpdateView):
    model = Institution
    fields = ['name', 'type']
    template_name_suffix = '_update_form'
    #institution_update_form.html


class DeleteInstitution(DeleteView):
    model = Institution
    success_url = reverse_lazy('users:list_institution')
    #Institution_confirm_delete.html


def user_delete(request):
    id = request.POST.get('id')
    print('---------')
    print(id)
    print('---------')
    try:
        User = get_user_model()
        count = User.objects.filter(id=id).delete()
        rr = {'status': 'ok'}
    except Exception as ee:
        count = 0
        rr = {'status': 'ko'}
    return JsonResponse(rr)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'users/authentication/profile.html', args)


# See https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
def create_profile(sender, **kwargs):
    print('-'*20)
    print('create_profile')
    print('-'*20)
    if not kwargs['created']:
        user = kwargs['instance']
        profile = Profile.objects.filter(user=user)
        if not profile:
            profile = Profile.objects.create(user=user)
            profile.save()


def edit_user_profile(request):
    company_obj = WebSiteCompany(request, web_company_id=7).site_company()
    profile = Profile.objects.filter(user=request.user)
    if not profile:
        profile = Profile.objects.create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.academics, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.academics)
    return render(request, 'users/authentication/edit_user_profile.html', {'user_form': user_form,
                                                                           'profile_form': profile_form,
                                                                           'institution_obj': company_obj})


def my_account(request):
    company_obj = WebSiteCompany(request, web_company_id=7).site_company()
    return render(request, 'user_home.html', {'institution_obj': company_obj})


def login_page(request):
    company_obj = WebSiteCompany(request, web_company_id=7).site_company()
    if request.method == "POST":
        form_login = AuthenticationForm(request, data=request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("education:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    return signup_login_form(request, error_message='')


def signup_login_form(request, error_message=''):
    company_obj = WebSiteCompany(request, web_company_id=7).site_company()
    form_login = AuthenticationForm()
    form_signup = RegistrationForm()
    arg = {'form_login': form_login, 'form_signup': form_signup,
           'redirect_field_name': "next", 'redirect_field_value': reverse('education:home'),
           'error_message': error_message, 'institution_obj': company_obj
           }
    return render(request, 'users/authentication/login_page.html', arg)


def signup_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        test = request.POST['test']
        try:
            if int(test) != 1:
                return signup_login_form(request, error_message='You must enter test number')
        except Exception as ex:
            return signup_login_form(request, error_message='You must enter test number')

        if form.is_valid():
            cd = form.cleaned_data
            s_email = cd['email']
            try:
                user_ = User.objects.get(email=s_email)
                if user_:
                    return signup_login_form(request, error_message='This email already registered.')
            except Exception as ex:
                return signup_login_form(request, error_message='You must enter test number')

            email_message(s_email, subject='registeration', body='Your registration was completed.')
            form.save()
            wsc = WebSiteCompany(request, web_company_id=7)
            if wsc.is_registered_domain():
                # print('wsc.is_registered_domain():wsc.is_registered_domain()')
                return wsc.get_redirect_link()
            else:
                # print('-----3333----')
                # print(request.POST['next'])
                # print('-----3333----')
                return redirect(request.POST['next'])
    else:
        return signup_login_form(request, error_message='')   #'must enter test number'

    #
    # if request.method == 'POST':
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         print('-----')
    #         print(cd)
    #         print('-----')
    #         semail = cd['email']
    #
    #         # email_message(semail, 'register')
    #         form.save(request)
    #         wsc = WebSiteCompany(request, web_company_id=7)
    #         if wsc.is_registered_domain():
    #             print('wsc.is_registered_domain():wsc.is_registered_domain()')
    #             return wsc.get_redirect_link()
    # else:
    #     print('11111---111')
    #     form_signup = SignupForm
    #     print('form_signup')
    #     print(form_signup)
    #     print(reverse('education:home'))
    #     print('End 11111---111')
    #
    # return render(request, 'education/signup_page.html', {
    #     'form_signup': form_signup,
    #     'redirect_field_name': "next",
    #     'redirect_field_value': reverse('education:home')
    # })


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("partners:home")

#
# class Logout(LogoutView):
#     template_name = 'users/authentication/logout.html'
#     # next_page = reverse('education:home')


def change_password(request):
    company_obj = WebSiteCompany(request, web_company_id=7).site_company()
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('education:home'))
        else:
            return redirect(reverse('users:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form, 'institution_obj': company_obj}
        return render(request, 'users/authentication/change_password.html', args)


class MyPasswordResetView(PasswordResetView):
    # form_class = PasswordResetForm
    template_name = 'users/authentication/reset_password.html'
    success_url = reverse_lazy('users:password_reset_done')
    # subject_template_name = 'accounts/emails/password-reset-subject.txt'
    email_template_name = 'users/authentication/reset_password_email.html'


class MyPasswordResetDoneView(PasswordResetDoneView):
    # form_class = PasswordResetForm
    template_name = 'users/authentication/reset_password_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    # form_class = PasswordResetForm
    template_name = 'users/authentication/reset_password_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/authentication/reset_password_complete.html'


def contact_us(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    return_message = ''
    if request.method == 'POST':
        contact_us_name = request.POST.get('name')
        contact_us_email = request.POST.get('email')
        contact_us_subject = request.POST.get('subject')
        contact_us_message = request.POST.get('message')
        if contact_us_subject == '' or contact_us_message == '':
            return_message = 'Must enter subject and a message!'
        else:
            try:
                ReceivedMessages.objects.create(institution_web=company_obj, name=contact_us_name,
                                                email=contact_us_email,
                                                subject=contact_us_subject,
                                                message=contact_us_message)
                contact_us_message = 'message received from ' + contact_us_name + ' \nEmail:' + contact_us_email + ' \nMessage:\n' + contact_us_message
                email = EmailMessage(contact_us_subject, contact_us_message, contact_us_email, [company_obj.email])
                email.send()
                return_message = 'Your message was received.\n\nThank you.'
            except Exception as ee:
                print(ee)
                return_message = 'Error in sending your message.\n\nPlease try again.'

    return render(request, 'users/contact_us/contact_us.html', {'institution_obj': company_obj,
                                                                'return_message': return_message})
