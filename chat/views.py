from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from courses.models import Course


# Create your views here.
@login_required
def cours_chat_room(request, course_id):
    try:
        # User = request.user
        course = request.user.courses_joined.get(id = course_id)
        
    except Course.DoesNotExist:
        print(f"User {request.user.username} is NOT enrolled in course {course_id}")
        return HttpResponseForbidden()
    latest_messages = course.chat_messages.select_related('user').order_by('-id')[:5]
    latest_messages = reversed(latest_messages)
    return render(request, 'chat/room.html', {'course': course, 'latest_messages': latest_messages})