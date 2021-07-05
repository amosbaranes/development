from django.shortcuts import render
from django.http import JsonResponse
from .models import Whiteboard, WhiteboardData
from ..courses.models import CourseSchedule, Section, CourseScheduleUser
from django.contrib.auth import get_user_model


def index(request, username):
    return render(request, 'chat/index.html', {})


def get_or_create_wb(request):
    try:
        wb_id = request.POST.get('wb_id')
        section_id = request.POST.get('section_id')
        board_name_ = request.POST.get('board_name')
        course_schedule_id_ = request.POST.get('course_schedule_id')
        # print('-'*100)
        # print(wb_id)
        # print(section_id)
        # print(course_schedule_id_)
        # print('-'*100)
        # User = get_user_model()
        # u = User.objects.get(id=creator_id)
        # course_schedule_id = request.POST.get('course_schedule_id')
        creator = request.user # request.POST.get('creator_id')
        section = Section.objects.get(id=section_id)

        # print('-'*100)
        # print(section)
        # print('-'*100)

        # course_schedule_user = CourseScheduleUser.objects.get(user=creator, course_schedule__course__id = section.course.id)
        # course_schedule = course_schedule_user.course_schedule

        course_schedule = CourseSchedule.objects.get(id=course_schedule_id_)

        # print('-'*100)
        # print('-'*100)
        # print(course_schedule)
        # print('-'*100)
        # print('-'*100)

        if wb_id == "-1":
            # print('-'*100)
            # print('-'*100)
            wb = Whiteboard.objects.create(course_schedule = course_schedule, section = section, creator = creator,
                                           board_name = board_name_)
            # print('-'*100)
            # print('-'*100)
            # print(161)
        else:
            wb = Whiteboard.objects.get(id=wb_id)
    except Exception as e:
        print("200 :" + e)
    rr = {'wb_id': wb.id, 'course_schedule_id':course_schedule.id, 'section_id': section.id, 'creator_id': creator.id, 'board_name':board_name_}
    return JsonResponse(rr)


def get_wb_of_section(request):
    data = {}
    try:
        # user_ = request.user # request.POST.get('creator_id')
        section_id = request.POST.get('section_id')
        course_schedule_id = request.POST.get('course_schedule_id')
        section = Section.objects.get(id=section_id)
        # course_schedule_user = CourseScheduleUser.objects.get(user=user_, course_schedule__course__id = section.course.id)
        # course_schedule = course_schedule_user.course_schedule

        course_schedule = CourseSchedule.objects.get(id=course_schedule_id)

        wbs = Whiteboard.objects.filter(section=section, course_schedule=course_schedule).all()
        for wb in wbs:
            data[wb.id] = {'creator': wb.creator.username, 'board_name': wb.board_name}
            wbds = WhiteboardData.objects.filter(whiteboard=wb).all()
            data[wb.id]['data'] = {}
            for wbd in wbds:
                data[wb.id]['data'][wbd.id] = {}
                data[wb.id]['data'][wbd.id]['painter'] = wbd.painter.username
                data[wb.id]['data'][wbd.id]['color'] = wbd.color
                data[wb.id]['data'][wbd.id]['xf'] = wbd.xf
                data[wb.id]['data'][wbd.id]['yf'] = wbd.yf
                data[wb.id]['data'][wbd.id]['xt'] = wbd.xt
                data[wb.id]['data'][wbd.id]['yt'] = wbd.yt
                data[wb.id]['data'][wbd.id]['mode'] = wbd.mode
                data[wb.id]['data'][wbd.id]['pen_size'] = wbd.pen_size
        # print('--13--')
        # print(data)
        # print('--13--')
    except Exception as e:
        print(e)
    return JsonResponse(data)



