from django.utils.translation import ugettext_lazy as _, get_language
from django.shortcuts import render, get_object_or_404, redirect
import random
from django.forms.models import modelform_factory
from django.apps import apps

from django.views.generic.base import TemplateResponseMixin, View
from .forms import CourseScheduleFormSet, CourseScheduleEmailForm

from django.utils.text import slugify
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
#
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
# import weasyprint
from io import BytesIO
#
from django.utils.translation import get_language
from django.views.generic import ListView, DetailView

from django.views.generic.edit import UpdateView

from parler.views import TranslatableSlugMixin
from django.contrib.contenttypes.models import ContentType
#
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.core.files.storage import FileSystemStorage
#
import braintree
#
from .models import (Department, Course, Syllabus, Section, SubSection, CourseSchedule, CourseScheduleUser, Order,
                     OrderItem, Coupon, Assignment, AssignmentUser, Team, AssignmentUserContent)

from ..core.email import email_message
from ..core.accounting import post_gl
from ..core.utils import is_role
from ..core.sql import SQL
from ..actions.utils import create_action
from .tasks import asy_email_message
from ..globsim.views import configure_globsim_game
from ..corporatevaluation.views import configure_corporatevaluation_project
# -----------------------------------
from ..cart.cart import Cart
from ..cart.forms import CartAddProductForm
# from .basecart import BaseCart
# from ..core.basecartforms import CartAddProductForm

from parler.utils.context import switch_language
from datetime import datetime
from django.contrib.auth import get_user_model


def home(request):
    # print('courses view')
    # this is temporary

    if not request.user.is_authenticated:
        return redirect('allauth:account_login')

    is_instructor = is_role(request.user, 'instructors')
    if is_instructor:
        return redirect('/my-account')

    title = _('Courses by Fields')

    # for course in department.department_courses.all():
    #     for cs in course.course_schedules():
    #         for cs.c
    #
    # course_schedule_ = get_object_or_404(CourseSchedule, slug=slug)
    # user = request.user
    # s_name = user.first_name + ' ' + str(user.id) + ' ' + course_schedule_.name
    # s_slug = slugify(s_name)
    # # s_slug1 = slugify(s_name+str(random.randint(0, 10**9)))
    # print('------')
    # # print(s_slug1)
    # print('-------')
    #
    # new = False
    # if not CourseScheduleUser.objects.filter(slug=s_slug).count() > 0:
    #     #if not CourseScheduleUser.objects.filter(slug=s_slug).count() > 0:
    #     new = True
    # if new:
    #     coupon = request.POST.get('coupon')
    #     print(coupon)
    #     now = timezone.now()
    #     try:
    #         coupon_obj = Coupon.objects.get(code__iexact=coupon,
    #                                         product=course_schedule_,
    #                                         valid_from__lte=now,
    #                                         valid_to__gte=now,
    #                                         active=True)
    #     except Coupon.DoesNotExist:
    #         coupon_obj = None

    departments = Department.objects.all().filter(active=True).filter(translations__language_code=get_language()).order_by('order')
    user_courses_schedule = request.user.course_schedule_users.all()
    # user_courses_schedule = request.user.objects.filter(course_schedule__active=True).all()

    user_courses = []
    user_courses_ = {}
    for scu in user_courses_schedule:
        if scu.course_schedule.active:
            # print('-'*10)
            # print(scu.course_schedule.active)
            # print(scu.course_schedule.name)
            # print('-'*10)
            user_courses.append(scu.course_schedule.course)
            if scu.course_schedule.course.link_app:
                user_courses_[scu.course_schedule.course.name] = scu.course_schedule.get_simulation_url()
    return render(request, 'courses/home.html', {'title': title, 'departments': departments,
                                                 'user_courses': user_courses,
                                                 'user_courses_': user_courses_})


def course_detail_instructor(request, slug, slug_course_schedule):
    # print('='*100)
    # print(slug)
    # print(slug_course_schedule)
    # print('='*100)
    # add form to add sections, post and get functions. Add placeholder
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    request.session['course_id'] = course.id
    request.session['course_name'] = course.name

    course_schedule_ = CourseSchedule.objects.filter(slug=slug_course_schedule)[0]
    is_instructor = True
    chat_room_id = course_schedule_.id
    if not chat_room_id:
        chat_room_name = 'general'
    chat_room_name = course_schedule_.name
    sub_section = course.course_sections.filter(translations__language_code=get_language())[0].section_sub_sections.filter(translations__language_code=get_language())[0]
    section = sub_section.section

    return render(request, 'courses/course_detail.html', {'course': course, 'sub_section': sub_section,
                                                          'section': section, 'questions': None,
                                                          'chat_room_id': chat_room_id,
                                                          'chat_room_name': chat_room_name,
                                                          'is_instructor': is_instructor
                                                          })


def course_detail(request, slug, slug_section=None, questions=None):
    # print('-'*100)
    # print(slug)
    # print(slug_section)
    # print(questions)
    # print('-'*100)
    # add form to add sections, post and get functions. Add placeholder
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    request.session['course_id'] = course.id
    request.session['course_name'] = course.name

    is_instructor = False
    for g in request.user.groups.all():
        if g.name == "admins" or g.name == "staff" or g.name == "instructors":
            is_instructor = True
            break

    chat_room_name = 'general'
    chat_room_id = 1
    registered_courses = request.user.course_schedule_users.all()
    for csu in registered_courses:
        if csu.course_schedule.course.name == course.name:
            chat_room_id = csu.course_schedule.id
            chat_room_name = csu.course_schedule.name

    if slug_section:
        sub_section = get_object_or_404(SubSection, translations__slug=slug_section)
    else:
        sub_section = course.course_sections.filter(translations__language_code=get_language())[0].section_sub_sections.filter(translations__language_code=get_language())[0]
    section = sub_section.section
    # print(section)

    return render(request, 'courses/course_detail.html', {'course': course, 'sub_section': sub_section,
                                                          'section': section, 'questions': questions,
                                                          'chat_room_id': chat_room_id,
                                                          'chat_room_name': chat_room_name,
                                                          'is_instructor': is_instructor
                                                          })


def course_schedule(request, slug):
    course_schedule_ = CourseSchedule.objects.filter(slug=slug)[0]
    return render(request, 'courses/course_schedule.html', {'course_schedule': course_schedule_})


def course_schedule_user(request, slug):
    course_schedule_user_ = CourseScheduleUser.objects.filter(slug=slug)[0]
    return render(request, 'courses/course_schedule_user.html', {'course_schedule_user': course_schedule_user_})


def sub_section_detail(request):
    slug=request.POST.get('slug')
    # sub_section = SubSection.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    sub_section = get_object_or_404(SubSection, translations__slug=slug)
    s_course = sub_section.section.course.name
    result = False

    course_schedule_ = None
    registered_courses = request.user.course_schedule_users.all()
    for csu in registered_courses:
        if csu.course_schedule.course.name == s_course:
            course_schedule_ = csu.course_schedule
            result = True
    # this is temporary I should remove it
    result = True
    #
    if result:
        assignment = None
        assignment_user = None
        try:
            with switch_language(sub_section, 'en'):
                # print('--0020--------sub section name--------------')
                atsn = sub_section.name.lower()
                if atsn == 'homework' or atsn == 'assignment':
                    # print('--00320-----cases of assignments and homework-------------------')
                    assignment = get_object_or_404(Assignment, sub_section=sub_section, course_schedule=course_schedule_)
                    assignment_user = assignment.get_assignment_user()
        except Exception as ee:
            print(ee)
        create_action(request.user, 'view subsection', sub_section)
        return render(request, 'courses/_sub_section_detail.html', {'sub_section': sub_section,
                                                                    'assignment': assignment,
                                                                    'assignment_user': assignment_user})
    else:
        create_action(request.user, 'attempt view subsection', sub_section)
        return render(request, 'courses/_sub_section_detail_blocked.html', {'sub_section': sub_section})


# ------------
# Register
# ------------
def register_form(request, slug):
    # print('register_form')
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    course_schedules = course.course_schedules.filter(active=True)

    # just for testing
    # messages.info(request, 'try to register')

    return render(request, 'courses/register_form.html', {'course_schedules': course_schedules})


def register(request):
    # print('register')
    slug = request.POST.get('slug')  # of course_schedule
    course_schedule_ = get_object_or_404(CourseSchedule, slug=slug)
    user = request.user
    s_name = user.first_name + ' ' + str(user.id) + ' ' + course_schedule_.name
    s_slug = slugify(s_name)
    # s_slug1 = slugify(s_name+str(random.randint(0, 10**9)))
    # print('------')
    # print(s_slug1)
    # print('-------')

    show_checkout = 0
    new = False
    if not CourseScheduleUser.objects.filter(slug=s_slug).count() > 0:
        #if not CourseScheduleUser.objects.filter(slug=s_slug).count() > 0:
        new = True
    if new:
        coupon = request.POST.get('coupon')
        print(coupon)
        now = timezone.now()
        try:
            coupon_obj = Coupon.objects.get(code__iexact=coupon,
                                            product=course_schedule_,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
        except Coupon.DoesNotExist:
            coupon_obj = None
        message = ""
        if course_schedule_.price > 0:
            cart = Cart(request, 'courses', 'courseschedule')
            cart.add(product=course_schedule_,
                     quantity=1,
                     update_quantity=False,
                     slug=s_slug,
                     s_name=s_name,
                     coupon_obj=coupon_obj)
            message = "You need to click on the check out Button to complete the registration."
            show_checkout = 1
        else:
            cu = CourseScheduleUser.objects.create(course_schedule=course_schedule_, paid=True,
                                                   active=True, user=request.user, slug=s_slug)
            # print(cu.active)
        message = 'Your registration for the course ' + course_schedule_.name + ' was successful. ' + message
        create_action(request.user, 'added course to cart', course_schedule_)
    else:
        message = 'you already have been registered for the course ' + course_schedule_.name

    return render(request, 'courses/_register.html', {'message': message,
                                                      'schedule': course_schedule_,
                                                      'showCheckOut': show_checkout})

    # try:
    #     # print('00000')
    #     # print(s_slug)
    #     if not CourseScheduleUser.objects.objects.filter(slug=s_slug).exist() \
    #             or CourseScheduleUser.objects.objects.filter(slug=s_slug1).exist():
    #         new = True
    #
    #     uu = CourseScheduleUser.objects.get(slug=s_slug)
    #     message = 'you already have been registered for the course ' + course_schedule_.name
    # except CourseScheduleUser.DoesNotExist as ee:
    #     coupon = request.POST.get('coupon')
    #     print(coupon)
    #     now = timezone.now()
    #     try:
    #         coupon_obj = Coupon.objects.get(code__iexact=coupon,
    #                                         product=course_schedule_,
    #                                         valid_from__lte=now,
    #                                         valid_to__gte=now,
    #                                         active=True)
    #     except Coupon.DoesNotExist:
    #         coupon_obj = None
    #
    #     cart = Cart(request, 'courses', 'courseschedule')
    #     cart.add(product=course_schedule_,
    #              quantity=1,
    #              update_quantity=False,
    #              slug=s_slug,
    #              s_name=s_name,
    #              coupon_obj=coupon_obj)
    #     message = 'Your registration for the course ' + course_schedule_.name + ' was successful.'
    #     create_action(request.user, 'added course to cart', course_schedule_)
    # return render(request, 'courses/_register.html', {'message': message})


def class_schedule_delete(request):
    slug = request.POST.get('slug')
    print('---------')
    print(slug)
    print('---------')
    try:
        count = CourseScheduleUser.objects.filter(slug=slug).delete()
        rr = {'status': 'ok'}
    except Exception as ee:
        count = 0
        rr = {'status': 'ko'}

    return JsonResponse(rr)


def activate_register(request):
    slug = request.POST.get('slug')
    action = request.POST.get('action')
    # course_schedule_user = get_object_or_404(CourseScheduleUser, slug=slug)
    if slug and action:
        try:
            csu = CourseScheduleUser.objects.get(slug=slug)
            if action == "activate":
                csu.active = True
            else:
                csu.active = False
            csu.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


def activate_graduate(request):
    slug = request.POST.get('slug')
    action = request.POST.get('action')
    # course_schedule_user = get_object_or_404(CourseScheduleUser, slug=slug)
    if slug and action:
        try:
            csu = CourseScheduleUser.objects.get(slug=slug)
            if action == "degraduated":
                csu.graduated = True
            else:
                csu.graduated = False
            csu.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


def syllabus_detail(request, slug):
    # add form to add sections, post and get functions. Add placeholder
    # syllabus = get_object_or_404(Syllabus, slug=slug)
    syllabus = Syllabus.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    create_action(request.user, 'view syllabus', syllabus)
    return render(request, 'courses/syllabus_detail.html', {'syllabus': syllabus})


def get_registered_list(request, slug):
    # add form to add sections, post and get functions. Add placeholder
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    return render(request, 'courses/course_schedule_detail.html', {'course': course})


def get_registered_list0(request, slug):
    # print(slug)
    course_schedule_ = CourseSchedule.objects.filter(slug=slug)[0]
    # print(course)
    return render(request, 'users/_admin_role_management_courses_schedule_user.html',
                  {'course_schedule': course_schedule_})


def get_registered_list0_(request):
    slug=request.POST.get('slug')
    return get_registered_list0(request, slug)


def get_registered_list1(request):
    slug=request.POST.get('slug')
    # add form to add sections, post and get functions. Add placeholder
    # print(slug)
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    # print(course)
    return render(request, 'users/_admin_role_management_courses_schedule_user1.html', {'course': course})


def course_schedule_send_email_user(request):
    if request.method == 'POST':
        id_ = request.POST.get('id')
        print(id_)
        user_model = get_user_model()
        user = user_model.objects.get(id=id_)
        subject = 'Complete your profile data'
        message = 'Your profile data are missing. Please complete your information by going to your account and edit your profile. When done, click update.'
        email = EmailMessage(subject, message, request.user.email, [user.email])
        email.send()
        return JsonResponse({'status': 'ok'})


def course_schedule_send_email(request, slug):
    if request.method == 'POST':
        form_ = CourseScheduleEmailForm(request.POST)
        print(form_.is_valid())

        cd = form_.cleaned_data
        subject = cd['subject']
        message = cd['message']
        slug = cd['slug']
        course_schedule_ = get_object_or_404(CourseSchedule, slug=slug)

        if 'file' in request.FILES:
            file = request.FILES['file']
            if int(file.size) <= 1500000:
                fs = FileSystemStorage()
                filename = fs.save(settings.MEDIA_ROOT + '/email/attachments/' + file.name, file)
        else:
            file = None

        csu = CourseScheduleUser.objects.filter(course_schedule=course_schedule_).all()
        for c in csu:
            email = EmailMessage(subject, message, request.user.email, [c.user.email])
            if file:
                email.attach_file(filename)
            # print('-----')
            # print(email.recipients())
            # print('-----')
            email.send()

        # email = EmailMessage(subject, message, request.user.email, recipients)
        # if 'file' in request.FILES:
        #     file = request.FILES['file']
        #     if int(file.size) <= 1500000:
        #         fs = FileSystemStorage()
        #         filename = fs.save(settings.MEDIA_ROOT + '/email/attachments/' + file.name, file)
        #         email.attach_file(filename)
        # print('-----')
        # print(email.recipients())
        # print('-----')
        # email.send()
        return render(request, 'courses/course_schedule/operation_successfully.html',
                      {'operation': 'send email to class'})
    else:
        form_ = CourseScheduleEmailForm(initial={'slug': slug})
        course_schedule_ = get_object_or_404(CourseSchedule, slug=slug)
    return render(request, 'courses/course_schedule_send_email.html',
                  {'form': form_, 'course_schedule': course_schedule_})


def course_schedule_random_group_assignment(request, slug):
    # print('------ran--------------')
    course_schedule_ = get_object_or_404(CourseSchedule, slug=slug)
    # print(course_schedule_)
    csu = CourseScheduleUser.objects.filter(course_schedule=course_schedule_).filter(team__isnull=True).all()
    # print(csu)
    # print('1----------')

    teams_ = course_schedule_.schedule_teams.all()
    # print(teams_)
    # print('2----------')

    for u in csu:
        # print('3----------')
        if course_schedule_.number_of_teams < course_schedule_.min_number_of_teams:
            new_team = Team.objects.create(course_schedule=course_schedule_,
                                           name='Team ' + str(course_schedule_.number_of_teams + 1))
            u.team = new_team

        # print(teams_)
        # print('4----------')
        if not u.team:
            teams_ = course_schedule_.schedule_teams.all()
            # print('40----------')
            for t in teams_:
                if t.number_of_members < course_schedule_.min_students_per_team:
                    u.team = t
                    break

        # print(teams_)
        # print('5----------')
        if not u.team:
            if course_schedule_.number_of_teams < course_schedule_.max_number_of_teams:
                # print('51----------')
                csu_ = CourseScheduleUser.objects.filter(course_schedule=course_schedule_).filter(team__isnull=True).all()
                # print('=============')
                # print(csu_.count())
                # print('=============')
                if csu_.count() <= course_schedule_.min_students_per_team:
                    # print('512----------')
                    new_team = None
                    z = 10000
                    for tt in teams_:
                        if tt.number_of_members < course_schedule_.max_number_of_teams:
                            z = tt.number_of_members
                            new_team = tt
                    # print('5123----------')
                    if new_team.number_of_members <= course_schedule_.max_students_per_team:
                        u.team = new_team
                # print('51234----------')
                if not u.team:
                    u.team = Team.objects.create(course_schedule=course_schedule_,
                                                 name='Team ' + str(course_schedule_.number_of_teams+1))
        # print(teams_)
        # print('6----------')
        if not u.team:
            print("error")
        u.save()
    return get_team_list2(request, slug, admin=True)


# def course_schedule_random_group_assignment_(request):
#     slug = request.POST.get('slug')
#     return get_team_list1(request, slug)
#     # return course_schedule_random_group_assignment(request, slug)


def course_schedule_random_group_assignment_(request, slug=None):
    if slug == None:
        slug = request.POST.get('slug')
    return get_team_list1(request, slug)
    # return course_schedule_random_group_assignment(request, slug)


def course_schedule_simulation_edit(request, slug):
    course_schedule_ = get_object_or_404(CourseSchedule, slug=slug)

    fields = ['course', 'name', 'owner', 'instructors', 'assignment_method',
              'min_students_per_team', 'max_students_per_team', 'min_number_of_teams', 'max_number_of_teams',
              'start_date', 'end_date', 'active', 'price']

    return render(request, 'users/_course_schedule_simulation_edit.html',
                  {'course_schedule': course_schedule_})


def course_schedule_edit(request, pk):
    course_schedule_ = CourseSchedule.objects.filter(id=pk).all()[0]
    target_ = course_schedule_.target
    return render(request, 'courses/course_schedule/_course_schedule.html',
                  {'course_schedule': course_schedule_,
                   'target': target_})


# should be deleted
class CourseScheduleEditView(UpdateView):
    model = CourseSchedule
    fields = ['course', 'name', 'owner', 'instructors', 'assignment_method',
              'min_students_per_team', 'max_students_per_team', 'min_number_of_teams', 'max_number_of_teams',
              'start_date', 'end_date', 'active', 'price']

    # template_name_suffix = '_form'
    template_name = "courses/course_schedule/courseschedule_form.html"
    success_url = reverse_lazy('courses:updated_successfully')
    #coursescheduleeditview_form.html


class TeamEditView(UpdateView):
    model = Team
    fields = ['name', 'image']
    template_name = "courses/course_schedule/team_form.html"
    success_url = reverse_lazy('courses:updated_successfully')
    #coursescheduleeditview_form.html


def updated_successfully(request):
    return render(request, 'courses/course_schedule/operation_successfully.html', {})


class CourseScheduleAssignmentEdit(TemplateResponseMixin, View):
    template_name = 'courses/course_schedule/assignment_formset.html'
    course_schedule = None

    def get_formset(self, data=None):
        return CourseScheduleFormSet(instance=self.course_schedule, data=data)

    def dispatch(self, request, pk):
        self.course_schedule = get_object_or_404(CourseSchedule, id=pk)
        return super(CourseScheduleAssignmentEdit, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course_schedule': self.course_schedule, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(self.course_schedule.course.get_registered_short_list1_url())
        return self.render_to_response({'course_schedule': self.course_schedule, 'formset': formset})


# I think I should remove this:
# class CourseScheduleUpdateView(TemplateResponseMixin, View):
#     template_name = 'courses/course_schedule/formset.html'
#     course = None
#
#     def get_formset(self, data=None):
#         return ModuleFormSet(instance=self.course, data=data)
#
#     def dispatch(self, request, pk):
#         self.course = get_object_or_404(Course, id=pk)
#         return super(CourseScheduleUpdateView, self).dispatch(request, pk)
#
#     def get(self, request, *args, **kwargs):
#         formset = self.get_formset()
#         return self.render_to_response({'course': self.course, 'formset': formset})
#
#     def post(self, request, *args, **kwargs):
#         formset = self.get_formset(data=request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect(self.course.get_registered_short_list1_url())
#         return self.render_to_response({'course': self.course, 'formset': formset})


# -----
def get_registered_short_list1(request, slug):
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    # for course_schedule_1 in course.course_schedules.all():
    #     print('1==============')
    #     print(course.name)
    #     print(course_schedule_1.name)
    #     print(course_schedule_1.slug)
    #     print('1==============')
    #
    # print('==============')
    # print('==============')
    for course_schedule_ in course.course_schedules.all():
        # print('==============')
        # print(course_schedule_.name)
        # print('==============')
        for section_ in course.course_sections.all():
            sss = section_.section_sub_sections.all()
            # print('-----sub_sections-------')
            # print(course_schedule_)
            # print(sss)
            # print('---------number of sub_sections:')
            # print(sss.count())
            # z = 0
            for sub_section_ in sss:
                # z += 1
                # print('sub section number:')
                # print(z)
                # print('22--------')
                with switch_language(sub_section_, 'en'):
                    # print('--0020--------sub section name--------------')
                    atsn = sub_section_.name.lower()

                    # print('++++++++++++++++')
                    # print(course_schedule_)
                    # print(section_.name)
                    # print(atsn)
                    # print('++++++++++++++++')
                    # print('--00202--')

                    if atsn == 'homework' or atsn == 'assignment':
                        # print('--00320-----cases of assignments and homework-------------------')
                        csa = course_schedule_.course_schedules_assignments.all()
                        # print('-----------csa created--------------')
                        a = csa.get_or_create(sub_section=sub_section_, course_schedule=course_schedule_)
                        # print('--0011111111--')
                        # print(a)
                        # print(csa)
                        # print('--00111111111--')
                        if a[1]:
                            if atsn == 'homework':
                                a[0].assignment_type = 1
                            elif atsn == 'assignment':
                                a[0].assignment_type = 2
                            a[0].save()
                        # print(1900)
    return render(request, 'users/_admin_role_management_short_courses_schedule.html', {'course': course})


def get_team_list1(request, slug):
    course_schedule_ = CourseSchedule.objects.filter(slug=slug)[0]
    # print(course_schedule_)
    teams = course_schedule_.schedule_teams.all()
    # print(teams)
    csu = get_object_or_404(CourseScheduleUser, course_schedule=course_schedule_, user=request.user)
    team_ = csu.team
    return render(request, 'users/_student_role_management_teams1.html',
                  {'course_schedule': course_schedule_, 'teams': teams, 'assignment_method': 1, 'my_team': team_})


def get_team_list2(request, slug, admin=None):
    course_schedule_ = CourseSchedule.objects.filter(slug=slug)[0]
    # print(course_schedule_)
    teams = course_schedule_.schedule_teams.all()
    if admin:
        team_ = None
    else:
        csu = get_object_or_404(CourseScheduleUser, course_schedule=course_schedule_, user=request.user)
        team_ = csu.team
    # print(teams)
    return render(request, 'users/_student_role_management_teams1.html',
                  {'course_schedule': course_schedule_, 'teams': teams, 'assignment_method': 2, 'my_team': team_})


def add_me_to_team(request):
    new_team = request.POST.get('new_team')
    team_slug = request.POST.get('team_slug')
    cs_slug = request.POST.get('cs_slug')
    course_schedule_ = get_object_or_404(CourseSchedule, slug=cs_slug)
    if new_team == 'yes':
        team_ = Team.objects.create(course_schedule=course_schedule_,
                                    name='Team ' + str(course_schedule_.number_of_teams+1))
    else:
        team_ = get_object_or_404(Team, id=int(team_slug))
    # print(team_slug)
    # print(cs_slug)
    # print('--------')
    if team_.number_of_members >= course_schedule_.max_number_of_teams:
        dic = {'status': 'This team is full.\n Please chose another team'}
        return JsonResponse(dic)

    # print('--------55')
    # print(team_)
    # print('--------66')
    # print(course_schedule_)
    # print('--------')

    csu = CourseScheduleUser.objects.get(user=request.user, course_schedule=course_schedule_, active=True)
    # print(csu)
    # print('--------')
    csu.team = team_
    csu.save()
    dic = {'status': 'Your registration was successful.\n Refresh your screen, by clicking on My Team, to see your team'}
    return JsonResponse(dic)


# -----------------------------------------
def create_obj_with_parent_id(request, parent_model_name, parent_model_id, model_name, obj_name):
    parent_model = apps.get_model(app_label='courses', model_name=parent_model_name)
    parent_model_obj = parent_model.objects.get(id=parent_model_id)
    return create_obj(request, parent_model_name, parent_model_obj, model_name, obj_name)


def create_translated_obj_with_parent_id(parent_model_name, parent_model_id, model_name, obj_name):
    parent_model = apps.get_model(app_label='courses', model_name=parent_model_name)
    parent_model_obj = parent_model.objects.get(id=parent_model_id)
    return create_translated_obj(parent_model_name, parent_model_obj, model_name, obj_name)


def create_obj(request, parent_model_name, parent_model_obj, model_name, obj_name):
    print('--01---')
    print(parent_model_obj)
    print(model_name)
    print(obj_name)
    print('--01')

    obj_model = apps.get_model(app_label='courses', model_name=model_name)
    # print(obj_model)
    # # can generalize this:
    if parent_model_name == 'course':
        new_obj_en = obj_model.objects.create(name=obj_name, course=parent_model_obj, owner=request.user,
                                              start_date=timezone.now(), end_date=timezone.now()
                                              )
        if parent_model_obj.link_app and model_name == 'courseschedule':
            print(parent_model_obj.link_app)
            print(parent_model_obj.link_model)
            m_type = apps.get_model(app_label=parent_model_obj.link_app, model_name=parent_model_obj.link_model)
            new_obj = m_type.objects.create(name=obj_name, course_schedule=new_obj_en)
            new_obj_en.target = new_obj
            new_obj_en.save()
    return new_obj_en


def create_translated_obj(parent_model_name, parent_model_obj, model_name, obj_name):
    obj_model = apps.get_model(app_label='courses', model_name=model_name)
    if parent_model_name == 'department':
        new_obj_en = obj_model.objects.language('en').create(name=obj_name, department=parent_model_obj)
    elif parent_model_name == 'course':
        new_obj_en = obj_model.objects.language('en').create(name=obj_name, course=parent_model_obj)
    elif parent_model_name == 'section':
        new_obj_en = obj_model.objects.language('en').create(name=obj_name, section=parent_model_obj)
    else:
        new_obj_en = obj_model.objects.language('en').create(name=obj_name, subsection=parent_model_obj)
    sql = SQL()
    model_name_translation = model_name + '_translation'
    for l in settings.LANGUAGES:
        if l[0] != 'en':
            ssql = " INSERT INTO courses_" + model_name_translation + " (language_code, name, slug, master_id) VALUES (%s,%s,%s,%s)"
            data = (l[0], obj_name + '-' + l[0], new_obj_en.slug + '-' + l[0], new_obj_en.id)
            # print('-----------')
            # print(ssql)
            # print(data)
            count = sql.exc_sql(ssql, data)
            # print(count)
            # print(2002)
            # print('-----------')
    return [1, new_obj_en]

    # print('--')
    # print(parent_model_name)
    # print(parent_model_obj)
    # print(model_name)
    # print(obj_name)
    # print('--')


def create_translated_department(model_name, obj_name):
    # print('--')
    # print(model_name)
    # print(obj_name)
    # print('--')

    obj_model = apps.get_model(app_label='courses', model_name=model_name)
    # print('-1-')
    new_obj_en = obj_model.objects.language('en').create(name=obj_name)
    # print('-2-')

    sql = SQL()
    model_name_translation = model_name + '_translation'
    for l in settings.LANGUAGES:
        if l[0] != 'en':
            ssql = " INSERT INTO courses_" + model_name_translation + " (language_code, name, slug, master_id) VALUES (%s,%s,%s,%s)"
            data = (l[0], obj_name + '-' + l[0], new_obj_en.slug + '-' + l[0], new_obj_en.id)
            # print('-----------')
            # print(ssql)
            # print(data)
            count = sql.exc_sql(ssql, data)
            # print(count)
            # print(2002)
            # print('-----------')
    return [1, new_obj_en]


# -------------
# https://pynative.com/python-postgresql-tutorial/
def set_new_model_instance(request):
    obj_name = request.POST.get('on')
    model_name = request.POST.get('mn')
    if not request.POST.get('pmn'):
        ll = create_translated_department(model_name=model_name, obj_name=obj_name)
        create_action(request.user, 'create department', ll[1])
        return JsonResponse({'status': 'ok'})

    parent_model_name = request.POST.get('pmn')
    parent_model_id = request.POST.get('pmid')
    if not obj_name == '' and obj_name != 'Need to change':
        result = 'ko'
        try:
            count, new_obj_en = create_translated_obj_with_parent_id(parent_model_name, parent_model_id, model_name, obj_name)
            create_action(request.user, 'create ' + model_name, new_obj_en)
            if parent_model_name == 'department':
                # print(100)
                model_name_section = 'section'
                obj_name_section = 'intro for ' + obj_name
                parent_model_name_section = model_name
                count, new_obj_en_section = create_translated_obj(parent_model_name_section,
                                                                  new_obj_en, model_name_section, obj_name_section)
                create_action(request.user, 'create section', new_obj_en_section)
                # --
                model_name_sub_section = 'subsection'
                obj_name_sub_section = 'Topics for ' + obj_name
                parent_model_name = model_name_section
                count, new_obj_en_sub_section = create_translated_obj(parent_model_name, new_obj_en_section,
                                                                      model_name_sub_section, obj_name_sub_section)
                create_action(request.user, 'create subsection', new_obj_en_sub_section)
                # -- syllabus --
                model_name_syllabus = 'syllabus'
                obj_name_syllabus = 'Syllabus'
                parent_model_name_syllabus = model_name
                count, new_obj_en = create_translated_obj(parent_model_name_syllabus, new_obj_en,
                                                          model_name_syllabus, obj_name_syllabus)
                create_action(request.user, 'create syllabus', new_obj_en)
            if count > 0:
                dic = {'status': 'ok'}
                return JsonResponse(dic)
        except Exception as e:
            print(e)
            result = e
    return JsonResponse({'status': result})


def set_new_schedule_course(request):
    obj_name = request.POST.get('on')
    model_name = request.POST.get('mn')
    parent_model_name = request.POST.get('pmn')
    parent_model_id = request.POST.get('pmid')
    # print(obj_name)
    # print(model_name)
    # print(parent_model_name)
    # print(parent_model_id)
    if not obj_name == '' and obj_name != 'Need to change':
        parent_model = apps.get_model(app_label='courses', model_name=parent_model_name)
        parent_model_obj = parent_model.objects.get(id=parent_model_id)
        obj_model = apps.get_model(app_label='courses', model_name=model_name)
        new_obj_en = obj_model.objects.create(name=obj_name, course=parent_model_obj, owner=request.user,
                                              start_date=timezone.now(), end_date=timezone.now()
                                              )
        # print(parent_model_obj)
        # print(parent_model_obj.link_app)
        if parent_model_obj.link_app:
            # print(parent_model_obj.link_app)
            # print(parent_model_obj.link_model)
            m_type = apps.get_model(app_label=parent_model_obj.link_app, model_name=parent_model_obj.link_model)
            new_obj = m_type.objects.create(name=obj_name, course_schedule=new_obj_en)
            new_obj_en.target = new_obj
            new_obj_en.save()
            sql = SQL()
            model_name_translation = parent_model_obj.link_model + '_translation'
            for l in settings.LANGUAGES:
                if l[0] != 'en':
                    ssql = " INSERT INTO "+parent_model_obj.link_app+"_" + model_name_translation + " (language_code, name, slug, master_id) VALUES (%s,%s,%s,%s)"
                    data = (l[0], obj_name + '-' + l[0], new_obj.slug + '-' + l[0], new_obj.id)
                    # print('-----------')
                    # print(ssql)
                    # print(data)
                    count = sql.exc_sql(ssql, data)
                    # print(count)
                    # print(2002)
                    # print('-----------')
            s = 'configure_'+parent_model_obj.link_app+'_'+parent_model_obj.link_model+'(request, new_obj)'
            eval(s)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ko11'})


# ---------------------------------------------
# Need to complete this drg and drop
# -----
class SectionOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Section.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class SubSectionOrderView(CsrfExemptMixin,
                          JsonRequestResponseMixin,
                          View):
    def post(self, request):
        for id, order in self.request_json.items():
            SubSection.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved': 'OK'})


# ------
# Assignment User sub_content
# -------
class ContentCreateUpdateView(TemplateResponseMixin, View):
    assignment_user = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, assignment_user_id, model_name, id=None):
        # print('---1----')
        # print(assignment_user_id)
        # print(id)
        # print('-------')
        self.assignment_user = get_object_or_404(AssignmentUser, id=assignment_user_id)
        # print('-------')
        self.model = self.get_model(model_name)
        # print('---12----')
        if id:
            self.obj = get_object_or_404(self.model, id=id)

        # print('---13----')

        return super(ContentCreateUpdateView, self).dispatch(request, assignment_user_id, model_name, id)

    def get(self, request, assignment_user_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, assignment_user_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                AssignmentUserContent.objects.create(assignment_user=self.assignment_user, item=obj)
            return redirect('courses:updated_successfully')

        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(AssignmentUserContent, id=id)
        content.item.delete()
        content.delete()
        return redirect('courses:updated_successfully')


class ContentView(View):
    def get(self, request, id):
        content = get_object_or_404(AssignmentUserContent, id=id)
        # print(content)
        return render(request, 'courses/course_schedule/assignment_user_content.html', {'content': content})


# ----------------------------------
# Cart
# ---------------------------------
@require_POST
def cart_add(request, product_id, coupon):
    try:
        coupon_obj = Coupon.objects.get(code__iexact=coupon)
    except Coupon.DoesNotExist:
        coupon_obj = None
    cart_ = Cart(request, 'courses', 'courseschedule')
    product = get_object_or_404(CourseSchedule, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart_.add(product=product,
                  quantity=cd['quantity'],
                  update_quantity=cd['update'],
                  slug=None,
                  s_name=None,
                  coupon_obj=coupon_obj)
    return redirect('courses:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request, 'courses', 'courseschedule')
    product = get_object_or_404(CourseSchedule, id=product_id)
    cart.remove(product)
    return redirect('courses:cart_detail')


def cart_detail(request):
    cart = Cart(request, 'courses', 'courseschedule')
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    show_payment = False
    if len(cart.cart) > 0:
        show_payment = True
    return render(request, 'courses/course_cart_detail.html', {'cart': cart, 'show_payment': show_payment})


# ------
# Order
# ------
def order_create(request):
    print('order_create')
    cart = Cart(request, 'courses', 'courseschedule')
    gl_entries = []
    if len(cart.cart) > 0:
        order = Order.objects.create(user=request.user)
        for item in cart:
            oi = OrderItem.objects.create(order=order,
                                          product=item['product'],
                                          price=item['price'],
                                          quantity=item['quantity'],
                                          course_schedule_user_slug=item['slug'],
                                          code=item['coupon'],
                                          total_price=item['total_price'],
                                          discount=item['total_discount'],
                                          total_price_after_discount=item['total_price_after_discount']
                                          )
            print(oi)
            #
            entry = (8, oi.total_price_after_discount, oi)
            gl_entries.append(entry)
            entry = (7, -oi.total_price, oi)
            gl_entries.append(entry)
            entry = (13, oi.discount, oi)
            gl_entries.append(entry)
            #
            print('--CourseScheduleUser--0--')
            cu = CourseScheduleUser.objects.create(course_schedule=item['product'], user=request.user, slug=item['slug'])
            print(cu.active)
            print('--CourseScheduleUser--01--')
        cart.clear()
        request.session['order_id'] = order.id
        create_action(request.user, 'created order', order)

        # gl_entries = [(account, amount, obj), ]
        # print(gl_entries)
        result = post_gl(gl_entries)

        return redirect(reverse('courses:payment_process'))
    return render(request, 'courses/courses_order_cart_empty.html', {})


def send_email_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    subject = 'My Courses - Invoice no. {}'.format(order.id)
    message = 'Please, find attached the invoice for your recent course registration.'
    email = EmailMessage(subject, message, 'donotreply@drbaranes.com.com', [order.user.email])
    # generate PDF
    html = render_to_string('courses/courses_invoice_pdf.html', {'order': order})
    out = BytesIO()
    # stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/shop_pdf.css')]
    # weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
    email.send()


def get_diploma_pdf(request, slug):
    course_schedule_user_ = CourseScheduleUser.objects.filter(slug=slug)[0]

    if course_schedule_user_.course_schedule.certificate_number < 100:
        ss = "certificate"
    else:
        ss = "diploma"

    # print('-'*100)
    # print(ss)

    html = render_to_string('courses/course_schedule/courses_'+ss+'_pdf.html',
                            {'time': datetime.today(), 'course_schedule_user': course_schedule_user_,
                             "DOMAIN": settings.DOMAIN})

    # print(html)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="diploma_{}.pdf"'.format(course_schedule_user_.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/shop_pdf.css')])

    # print('-'*100)
    return response


def get_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('courses/courses_invoice_pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/shop_pdf.css')])
    return response


def payment_process_(request, order_id=None):
    request.session['order_id'] = order_id
    return redirect(reverse('courses:payment_process'))


def payment_process_0(request, order, order_id):
    gl_entries = []
    for item in order.items.all():
        course_schedule_user_ = CourseScheduleUser.objects.get(user=request.user, course_schedule=item.product,
                                                               active=False)
        course_schedule_user_.active = True
        course_schedule_user_.paid = True
        course_schedule_user_.save()
        # 5-Credit Card; 8-Account Receivable; 6 -Revenue; 7 - From Courses
        #
        entry = (5, item.total_price_after_discount, item)
        gl_entries.append(entry)
        entry = (8, -item.total_price_after_discount, item)
        gl_entries.append(entry)
        #
    result = post_gl(gl_entries)
    # create invoice e-mail
    send_email_invoice_pdf(request, order_id)
    create_action(request.user, 'paid order', order)


def payment_process(request):
    print('payment_process-1')
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    if order.get_total_price_after_discount() < 0.01:
        order.paid = True
        # store the unique transaction id
        order.braintree_id = '0'
        order.save()
        payment_process_0(request, order, order_id)
        return redirect(reverse('courses:payment_done'))

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_price_after_discount()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            payment_process_0(request, order, order_id)
            return redirect(reverse('courses:payment_done'))
        else:
            request.session['order_id'] = order_id
            return redirect(reverse('courses:payment_canceled'))
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request, 'courses/courses_payment_process.html',
                      {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'courses/courses_payment_done.html')


def payment_canceled(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'courses/courses_payment_canceled.html', {'order': order})

