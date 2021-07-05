from django.conf.urls import url
from django.urls import path, include
from .views import (show_content, show_sub_content,
                    DeleteInstitution, InstitutionsView, InstitutionView, CreateInstitution, UpdateInstitution,
                    edit_user_profile, user_delete)

app_name = "users"

urlpatterns = [
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
]
