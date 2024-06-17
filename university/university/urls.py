from django.contrib import admin
from django.urls import path

from university.apps.views import (
    page_views,
    content_views
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls),
    path(
        '',
        page_views.welcome,
        name='authorisation'
    ),
    path(
        'registration',
        page_views.registration,
        name='registration'
    ),
    path(
        'student',
        page_views.student,
        name='student'
    ),
    path(
        'teacher',
        page_views.teacher,
        name='teacher'
    ),
    path(
        'my_account',
        page_views.my_account,
        name='my_account'
    ),
    path(
        'logout',
        page_views.logout,
        name='logout'
    ),
    path(
        'update_user_data',
        page_views.update_user_data,
        name='update_user_data'
    ),

    path(
        'student_lessons',
        content_views.student_lessons,
        name='student_lessons'
    ),
    path(
        'student_marks',
        content_views.student_marks,
        name='student_marks'
    ),
    path(
        'teacher_schedule',
        content_views.teacher_schedule,
        name='teacher_schedule'
    ),
    path(
        'teacher_groups',
        content_views.teacher_groups,
        name='teacher_groups'
    ),

    path(
        'student_diagram',
        content_views.student_diagram,
        name='student_diagram'
    ),
    path(
        'teacher_diagram',
        content_views.teacher_diagram,
        name='teacher_diagram'
    ),
]
