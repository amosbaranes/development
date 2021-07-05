from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _, get_language
from django.shortcuts import render
from .models import Question, Answer, UserAnswer
from ..courses.models import Course, Section
from django.http import JsonResponse
import random


def set_correct_answer(request):
    pkey_ = request.POST.get('pkey_')
    value_ = request.POST.get('value_')
    if value_ == 'true':
        value_ = True
    else:
        value_ = False
    a = Answer.objects.get(id=pkey_)
    a.correct = value_
    a.save()
    # print(a.correct)
    return JsonResponse({'status': 'ok'})


def delete_answer(request, id):
    a = Answer.objects.get(id=id)
    section = a.question.section
    a.delete()
    return slug_edit_test_section(request, section.course.slug, slug_section=section.slug)


def delete_question(request, id):
    q = Question.objects.get(id=id)
    section = q.section
    q.delete()
    return slug_edit_test_section(request, section.course.slug, slug_section=section.slug)


def add_question(request, slug_section):
    section_ = get_object_or_404(Section, translations__slug=slug_section)
    q = Question.objects.create(section_id=section_.id)
    q.save()
    is_correct_num = random.randint(1, 4)
    for k in range(1, 5):
        if k == is_correct_num:
            a = Answer.objects.create(question_id=q.id, correct=True)
        else:
            a = Answer.objects.create(question_id=q.id, correct=False)
    section_ = q.section
    course = q.section.course
    questions = section_.questions.all()
    sub_section = None
    return render(request, 'courses/course_detail.html', {'course': course, 'sub_section': sub_section,
                                                          'section': section_, 'questions': questions})


def add_answer(request, id):
    q = Question.objects.get(id=id)
    a = Answer.objects.create(question_id=q.id)
    return slug_edit_test_section(request, q.section.course.slug, slug_section=q.section.slug)


def slug_edit_test_section(request, slug, slug_section=None):
    # add form to add sections, post and get functions. Add placeholder
    course = Course.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    request.session['course_id'] = course.id
    request.session['course_name'] = course.name
    section_ = get_object_or_404(Section, translations__slug=slug_section)
    questions = section_.questions.all()
    if questions.count() < 1:
        return add_question(request, slug_section)
    sub_section = None
    return render(request, 'courses/course_detail.html', {'course': course, 'sub_section': sub_section,
                                                          'section': section_, 'questions': questions})


def set_test(request):
    id_ = request.POST.get('id')
    section = Section.objects.filter(translations__language_code=get_language()).filter(id=id_)[0]
    return render(request, 'elearning/_set_test_student.html', {'section': section})


def set_user_answer(request):
    ppkey_ = request.POST.get('ppkey')
    pkey_ = request.POST.get('pkey')
    q = Question.objects.get(id=ppkey_)
    aa = Answer.objects.get(id=pkey_)
    try:
        a = UserAnswer.objects.get(question=q, user=request.user)
    except UserAnswer.DoesNotExist:
        a = UserAnswer.objects.create(question=q, user=request.user, answer=aa)
    a.answer = aa
    a.save()
    return JsonResponse({'status': 'ok'})
