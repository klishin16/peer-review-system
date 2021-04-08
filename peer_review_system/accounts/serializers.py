from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

# from django.contrib.auth.models import User

from .models import (
	CustomUser,
	StudentProfile, TeacherProfile,
)


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = ['id', 'email', 'name', 'surname', 'is_teacher']
		ref_name = "Custom user"


class UserRegistrationSerializer(UserCreateSerializer):

	class Meta(UserCreateSerializer.Meta):
		fields = ('email', 'password', 'is_teacher')

