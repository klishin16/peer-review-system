import random
import time

from django.http.response import Http404
from rest_framework.response import Response
from main.models import Group
from main.serializers import GroupSerializer, TeacherSerializer, StudentSerializer
from .models import StudentProfile, CustomUser, TeacherProfile
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerProfileOrReadOnly
#from .serializers import UserProfileSerializer


# class UserProfileListCreateView(ListCreateAPIView):
#     queryset=UserProfile.objects.all()
#     serializer_class=UserProfileSerializer
#     # permission_classes=[IsAuthenticated]

#     def perform_create(self, serializer):
#         user=self.request.user
#         serializer.save(user=user)


# class userProfileDetailView(RetrieveUpdateDestroyAPIView):
#     queryset=UserProfile.objects.all()
#     serializer_class=UserProfileSerializer
#     permission_classes=[IsAuthenticated]

class StudentListView(generics.ListAPIView):
	queryset = StudentProfile.objects.all()
	serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateAPIView): # используем id CustomUser (НЕ Student!!!)

	serializer_class = StudentSerializer

	def get_object(self):
		pk = self.kwargs.get('pk')
		userProfile = CustomUser.objects.filter(id=pk).first()
		print("student pk:", pk)
		print("User Profile:", userProfile.student_profile.first())

		return userProfile.student_profile.first()

	def patch(self, request, pk, format='json'): # патчим только group
		newGroup = Group.objects.filter(pk=request.data['student_class']['id']).first()
		print(newGroup)
		studentProfile = request.user.student_profile.first()
		studentProfile.student_class = newGroup
		studentProfile.save()
		return Response({"Updated!"}, status=status.HTTP_201_CREATED)
		
		return Response({"Error!"}, status=status.HTTP_400_BAD_REQUEST)

	def dispatch(self, request, *args, **kwargs):
		time.sleep(1)
		
		return super(StudentDetailView, self).dispatch(request, *args, **kwargs)


class TeacherListView(generics.ListAPIView):
	queryset = TeacherProfile.objects.all()
	serializer_class = TeacherSerializer


class TeacherDetailView(generics.RetrieveUpdateAPIView):

	serializer_class = TeacherSerializer

	def get_object(self):
		pk = self.kwargs.get('pk')
		try:
			user = CustomUser.objects.filter(pk=pk).first().teacher_profile
			print("TeacherDetail -> get_object -> user: {}".format(user))
			return user
		except CustomUser.DoesNotExist:
			raise Http404
	
	def patch(self, request, pk, format='json'): # патчим только group
		newGroups = Group.objects.filter(pk__in=[g['id'] for g in request.data['student_classes']]).all()
		# newGroup = Group.objects.filter(pk=request.data['student_class']['id']).first()
		teacherProfile = request.user
		print(teacherProfile.groups.all())
		teacherProfile.groups.clear()
		for newGroup in newGroups:
			newGroups.update(teacher=teacherProfile)
		teacherProfile.save()
		return Response({"Updated!"}, status=status.HTTP_201_CREATED)
		# print('patch teacher', newGroups)
		
		return Response({"Error!"}, status=status.HTTP_400_BAD_REQUEST)
