# from django.views.generic import TemplateView
from django.shortcuts import render


# class VideoCall(TemplateView):
#     template_name = 'videocall/video_call.html'

def video_call(request):
    return render(request, 'videocall/video_call.html', {'user_id': request.user.id})


def video_simple(request):
    return render(request, 'videocall/video_simple.html', {'user_id': request.user.id})
