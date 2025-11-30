from django.core.serializers import serialize
from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import BasePermission


from .models import (
    Weekday, Room, Attendence,
    Group, StudentGroup, Lesson,
    Homework, 
)
from .serializers import (
    WeekDaySerializer, RoomSerializer,
    AttendenceSerailizer, GroupSerializer,
    StudentGroupSerializer, LessonSerializer,
    HomeworkSerializer
)

from account.models import (
    CustomUser, AdminTeacher, Student,
    CourseType, Course
)
from account.serializers import (
    CourseSerializer, CourseTypeSerializer,
    AdminTeacherSerializer, StudentSerializer,
    CustomUserSerializer
)



# Create your views here.

# ADMIN

class AdminEnterPermission(BasePermission):
    def has_permission(self, request, view):
        return AdminTeacher.objects.filter(user__id = request.user.id).exists()

class AdminHomeView(viewsets.ViewSet):

    permission_classes = [AdminEnterPermission]

    def list(self, request):
        info = get_list_or_404(AdminTeacher)
        info = AdminTeacherSerializer(info, many=True).data
        print(info)
        for data in info:
            data['user'] = CustomUserSerializer(get_object_or_404(CustomUser, pk=data['user'])).data

        return Response(info)

    def retrieve(self, request, pk):
        info = get_object_or_404(AdminTeacher, pk=pk)
        info = AdminTeacherSerializer(info).data
        info['user'] = CustomUserSerializer(get_object_or_404(CustomUser, pk=info['user'])).data
        return Response(info, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        print(data)




# class


