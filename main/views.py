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
        return request.user and AdminTeacher.objects.filter(user__id = request.user.id).exists()
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

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
        user = data['user']
        user_serializer = CustomUserSerializer(data=user)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer.save()
        print(user_serializer.data)
        data['user'] = user_serializer.data['id']
        admin_teacher_serializer = AdminTeacherSerializer(data=data)

        if not admin_teacher_serializer.is_valid():
            return Response(admin_teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        admin_teacher_serializer.save()
        data = admin_teacher_serializer.data
        data['user'] = CustomUserSerializer(CustomUser.objects.get(pk=data['user'])).data
        
        return Response({"message":"success", "data":data}, status=status.HTTP_200_OK)
    

    def update(self, request, pk):

        data = request.data

        admin_teacher_instance = get_object_or_404(AdminTeacher, pk=pk)

        user = CustomUser.objects.get(id=admin_teacher_instance.user.id)
        user_data = data['user']

        if request.method == 'PUT':
            user_serializer = CustomUserSerializer(instance= user,data=user_data, partial=False)

        else:
            user_serializer = CustomUserSerializer(instance= user,data=user_data, partial=True)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        user_serializer.save()

        data['user'] = user_serializer.data['id']
        admin_serializer = AdminTeacherSerializer(instance=admin_teacher_instance ,data=data, partial=False)

        if not admin_serializer.is_valid():
            return Response(admin_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        admin_serializer.save()

        return Response(admin_serializer.data, status=status.HTTP_202_ACCEPTED)







# class


