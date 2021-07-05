from django.urls import path
from django.conf.urls import url
from .views import (set_test, add_question, add_answer, delete_answer, set_correct_answer,
                    slug_edit_test_section, set_user_answer, delete_question)

app_name = "elearning"

urlpatterns = [
    path('set_test/', set_test, name='set_test'),
    path('slug_edit_test_section/<slug:slug>/<slug:slug_section>/', slug_edit_test_section,
         name='slug_edit_test_section'),
    path('add_question/<slug:slug_section>/', add_question,name='add_question'),
    path('delete_question/<int:id>/', delete_question, name='delete_question'),
    path('add_answer/<int:id>/', add_answer, name='add_answer'),
    path('delete_answer/<int:id>/', delete_answer, name='delete_answer'),
    path('set_correct_answer/', set_correct_answer, name='set_correct_answer'),

    # path('set_question', set_question, name='set_question'),
    # path('set_answer', set_answer, name='set_answer'),
    # path('remove_answer', remove_answer, name='remove_answer'),
    # path('get_question_data', get_question_data, name='get_question_data'),
    path('set_user_answer', set_user_answer, name='set_user_answer'),
    # path('delete_question', delete_question, name='delete_question')
]

