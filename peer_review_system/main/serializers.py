from django.http import request
from accounts.serializers import UserSerializer
from accounts.models import StudentProfile, TeacherProfile
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers

from .models import (
	SolutionInspection, Task,
	Group,
	TaskExecutor,
	TaskInspection,
	TaskSolution,
	Criterion,
)


class TaskExecutorSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.ReadOnlyField(source='executor.email')
    id = serializers.ReadOnlyField(source='executor.id')

    class Meta:
        model = TaskExecutor

        fields = ('id', 'email', )


class TaskInspectorSerializer(serializers.HyperlinkedModelSerializer):

    email = serializers.ReadOnlyField(source='inspector.email')
    id = serializers.ReadOnlyField(source='inspector.id')

    class Meta:
        model = TaskInspection

        fields = ('id', 'email', )


class SolutionSerializer(serializers.ModelSerializer):
	executor = UserSerializer()

	class Meta:
		model = TaskSolution

		fields = ("id", "executor", "data", "score", "task", )


class PatchSolutionSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = TaskSolution

		fields = ("id", "data", "score", "task", )



class CriterionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Criterion
		fields = "__all__"


class TaskSerializer(serializers.ModelSerializer): # полный сериализатор задач
	executors = TaskExecutorSerializer(source='taskexecutor_set', many=True, read_only=True)
	inspections = TaskInspectorSerializer(source='taskinspection_set', many=True, read_only=True)

	# criterions = 	TODO
	status = serializers.ChoiceField(choices=(
		(0, "Not started"),
		(1, "In progress"),
		(2, "Done"))
	)

	def create(self, validated_data):
		instance = Task.objects.create(
			title = validated_data.pop("title"),
			description = validated_data.pop("description"),
			status = validated_data.pop("status"),
			teacher = self.context['request'].user
		)
		for criterion in validated_data.pop("criterions"):
			instance.criterions.add(criterion)
		
		return instance
	
	def update(self, instance, validated_data):
		print("Task update")
		return super().update(instance, validated_data)

	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['criterions'] = CriterionSerializer(instance=instance.criterions.all(), many=True).data
		print("herer", instance.criterions.all())
		return data

	class Meta:
		model = Task
		fields = ('id', 'title', 'description', 'executors', 'inspections', 'criterions', 'status')


class TaskShortSerializer(serializers.ModelSerializer): # короткий сериализатор задач
	
	class Meta:
		model = Task
		fields = ('id', 'title', 'description', )


# сериализаторы для классов
class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	student_classes = GroupSerializer(source='user.groups', many=True)

	class Meta:
		model = TeacherProfile
		fields = ['user', 'student_classes']


class StudentSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	student_class = GroupSerializer()

	class Meta:
		model = StudentProfile
		fields = ['user', 'student_class']


class InspectionSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		data = super().to_representation(instance)
		s_data = UserSerializer(instance.inspector).data
		data['inspector'] = s_data
		data['solution']
		return data

	class Meta:
		model = SolutionInspection
		fields = "__all__"

