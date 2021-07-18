from django.conf.urls import url
from django.urls import path, include
from .views import (show_content, show_sub_content,
                    DeleteInstitution, InstitutionsView, InstitutionView, CreateInstitution, UpdateInstitution,
                    edit_user_profile, user_delete, my_account,
                    MyPasswordResetView,MyPasswordResetConfirmView,MyPasswordResetCompleteView,MyPasswordResetDoneView,
                    login_page, signup_page, view_profile,
                    change_password, logout_request, contact_us
                    )

from django.urls import reverse

app_name = "users"

urlpatterns = [
    path('contact_us', contact_us, name='contact_us'),
    path('my_account', my_account, name='my_account'),
    path('show_content', show_content, name='show_content'),
    path('show_sub_content', show_sub_content, name='show_sub_content'),
    path('institutions', InstitutionsView.as_view(), name='list_institution'),
    path('CreateInstitutions/', CreateInstitution.as_view(), name='create_institution'),
    path('edit_user_profile/', edit_user_profile, name='edit_user_profile'),
    path('user_delete/', user_delete, name='user_delete'),

    # url(r'^institutions$', InstitutionsView.as_view(), name='list_institution'),

    url(r'^institutions/(?P<pk>\d+)/$', InstitutionView.as_view(), name='detailed_institution'),
    # url(r'^CreateInstitutions/$', CreateInstitution.as_view(), name='create_institution'),
    url(r'^UpdateInstitutions/(?P<pk>\d+)/$', UpdateInstitution.as_view(), name='update_institution'),
    url(r'^DeleteInstitutions/(?P<pk>\d+)/$', DeleteInstitution.as_view(), name='delete_institution'),

    # url(r'^edit_user_profile/$', edit_user_profile, name='edit_user_profile'),
    #

    # path('login_page', login_page, name='login_page'),
    # path('signup_page', signup_page, name='signup_page'),

    url(r'signup/$', signup_page, name='signup'),
    url(r'login/$', login_page, name='login'),

    # url(r'login/$', LoginView.as_view(template_name='users/authentication/login.html'), name='login'),
    # url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^logout/$', logout_request, name='logout'),

    url(r'^profile/$', view_profile, name='view_profile'),
    # url(r'^profile/(?P<pk>\d+)/$', view_profile, name='view_profile_with_pk'),
    # url(r'^profile/edit/user/$', edit_user_profile, name='edit_user_profile'),

    url(r'^change-password/$', change_password, name='change_password'),
    url(r'^reset-password/$', MyPasswordResetView.as_view(), name='reset_password'),
    url(r'^reset-password/done/$', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset-password/complete/$', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
