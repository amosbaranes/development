from django.urls import path
from .views import (home, course_detail, course_detail_instructor, sub_section_detail, syllabus_detail,
                    course_schedule, course_schedule_user, get_diploma_pdf,
                    course_schedule_edit, CourseScheduleAssignmentEdit, updated_successfully, TeamEditView,
                    course_schedule_random_group_assignment, course_schedule_simulation_edit,
                    course_schedule_send_email, course_schedule_send_email_user,
                    register_form, register, activate_register, activate_graduate,get_registered_list0_,
                    get_registered_list, get_registered_list0, get_registered_list1,
                    get_registered_short_list1, set_new_model_instance, set_new_schedule_course,
                    SectionOrderView, SubSectionOrderView,
                    cart_detail, cart_add, cart_remove,
                    order_create, course_schedule_random_group_assignment_,
                    ContentCreateUpdateView, ContentDeleteView, ContentView,
                    payment_process, payment_process_, payment_done, payment_canceled, get_invoice_pdf,
                    get_team_list1, get_team_list2, add_me_to_team, class_schedule_delete)

app_name = "courses"

urlpatterns = [
    path('', home, name='home'),
    path('section/<slug:slug>/<slug:slug_section>', course_detail, name='slug_section'),
    path('course_detail/<slug:slug>', course_detail, name='course_detail'),
    path('course_detail/<slug:slug>/<slug:slug_course_schedule>', course_detail_instructor,
         name='course_detail_instructor'),
    path('sub_section_detail', sub_section_detail, name='sub_section_detail'),
    path('syllabus_detail/<slug:slug>', syllabus_detail, name='syllabus_detail'),

    path('course_schedule/<slug:slug>', course_schedule, name='course_schedule'),
    path('course_schedule_user/<slug:slug>', course_schedule_user, name='course_schedule_user'),

    path('register_form/<slug:slug>', register_form, name='register_form'),
    path('register', register, name='register'),
    path('activate_register', activate_register, name='activate_register'),
    path('activate_graduate', activate_graduate, name='activate_graduate'),

    path('set_new_model_instance', set_new_model_instance, name='set_new_model_instance'),
    path('set_new_schedule_course', set_new_schedule_course, name='set_new_schedule_course'),

    path('get_registered_list/<slug:slug>', get_registered_list, name='get_registered_list'),
    path('get_registered_short_list1/<slug:slug>', get_registered_short_list1, name='get_registered_short_list1'),
    path('get_registered_list0/<slug:slug>', get_registered_list0, name='get_registered_list0'),
    path('get_registered_list0_', get_registered_list0_, name='get_registered_list0_'),

    path('get_registered_list1', get_registered_list1, name='get_registered_list1'),

    path('get_team_list1/<slug:slug>', get_team_list1, name='get_team_list1'),
    path('get_team_list2/<slug:slug>', get_team_list2, name='get_team_list2'),
    path('add_me_to_team', add_me_to_team, name='add_me_to_team'),

    path('class_schedule_delete', class_schedule_delete, name='class_schedule_delete'),

    # Formset to be removed
    # path('<pk>/course_schedule_update/', CourseScheduleUpdateView.as_view(), name='course_schedule_update'),

    path('cs_send_email/<slug:slug>', course_schedule_send_email, name='course_schedule_send_email'),
    path('course_schedule_send_email_user', course_schedule_send_email_user, name='course_schedule_send_email_user'),

    path('csrga/<slug:slug>', course_schedule_random_group_assignment, name='course_schedule_random_group_assignment'),
    path('csrga/<slug:slug>', course_schedule_random_group_assignment_, name='course_schedule_random_group_assignment_'),
    path('csrga/', course_schedule_random_group_assignment_, name='course_schedule_random_group_assignment_'),

    path('csse/<slug:slug>', course_schedule_simulation_edit, name='course_schedule_simulation_edit'),

    path('<pk>/course_schedule_edit', course_schedule_edit, name='course_schedule_edit'),

    # path('<pk>/course_schedule_edit/', CourseScheduleEditView.as_view(), name='course_schedule_edit'),


    path('<pk>/course_schedule_assignment_edit/', CourseScheduleAssignmentEdit.as_view(),
         name='course_schedule_assignment_edit'),

    path('<pk>/team_edit/', TeamEditView.as_view(), name='team_edit'),
    path('updated_successfully/', updated_successfully, name='updated_successfully'),
    #
    path('assignment/<int:assignment_user_id>/content/<model_name>/create/', ContentCreateUpdateView.as_view(),
         name='assignment_user_content_create'),
    path('assignment/<int:assignment_user_id>/content/<model_name>/<id>/', ContentCreateUpdateView.as_view(),
         name='assignment_user_content_update'),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(), name='assignment_user_content_delete'),
    path('content/<int:id>/', ContentView.as_view(), name='assignment_user_content'),
    #
    path('section/order/', SectionOrderView.as_view(), name='section_order'),
    path('sub_section/order/', SubSectionOrderView.as_view(), name='sub_section_order'),

    path('cart_detail', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/<str:coupon>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),

    path('payment_process1/', order_create, name='order_create'),

    path('payment_process/', payment_process, name='payment_process'),
    path('payment_process/<int:order_id>/', payment_process_, name='payment_process_'),
    path('payment_done/', payment_done, name='payment_done'),
    path('payment_canceled/', payment_canceled, name='payment_canceled'),

    path('get_invoice_pdf/<int:order_id>/pdf/', get_invoice_pdf, name='get_invoice_pdf'),
    path('get_diploma_pdf/<slug:slug>', get_diploma_pdf, name='get_diploma_pdf'),
    #
]

