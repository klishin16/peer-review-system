from django.views import generic
from rest_framework.schemas import inspectors
from accounts.models import CustomUser, StudentProfile
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import (
	Criterion, SolutionInspection, Task, 
	TaskExecutor,
	Group, TaskInspection,
	TaskSolution
)

from .serializers import (
	CriterionSerializer, 
	GroupSerializer, InspectionSerializer, 
	TaskSerializer, TaskShortSerializer,
	SolutionSerializer,
	PatchSolutionSerializer,
	StudentSerializer,
)

from accounts.serializers import (
	UserSerializer,
)


class CriterionListView(generics.ListCreateAPIView):
	queryset = Criterion.objects.all()
	serializer_class = CriterionSerializer


# view для задач
class TaskListView(generics.ListCreateAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def post(self, request, *args, **kwargs):
		print("Task -> POST {}".format(request.user))
		return super().post(request, *args, **kwargs)


class TaskDetialView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def patch(self, request, pk):
		task = Task.objects.filter(pk=pk).first()
		print("Patch task task", task)
		serializer = TaskSerializer(task, data=request.data, partial=True)
		if (serializer.is_valid()):
			serializer.save()
			return Response({"Updated!"}, status=status.HTTP_201_CREATED)
		else:
			print("invalid")

		return Response({"Error!"}, status=status.HTTP_400_BAD_REQUEST)


class TaskSolutionsListView(APIView):

	def get(self, request, pk ,format=None):
		currentTask = Task.objects.get(pk=pk)
		solutions = currentTask.task_solutions.all()

		serializer = SolutionSerializer(solutions, many=True)

		return Response(serializer.data)
	
	def post(self, request, pk):
		currentTask = Task.objects.get(pk=pk)
		currentUser = CustomUser.objects.get(email = request.data['user']['email'])

		TaskSolution.objects.create(
			data = request.data['data'],
			task = currentTask,
			executor = currentUser,
			)

		return Response({"Work!"}, status=status.HTTP_201_CREATED)
	
	def patch(self, request, pk, format='json'):
		serializer = PatchSolutionSerializer(data=request.data, many=True)
		if serializer.is_valid():
			for item in request.data:
				currentSolution = TaskSolution.objects.get(pk=item['id'])
				currentSolution.score = item['score']
				currentSolution.save()
				return Response({"Updated!"}, status=status.HTTP_201_CREATED)
		
		return Response({"Error!"}, status=status.HTTP_400_BAD_REQUEST)


class TaskExecutorsListView(APIView):

	def get(self, request, pk, format=None):
		currentTask = Task.objects.get(pk=pk)
		executors = currentTask.executors.all()

		serializer = UserSerializer(executors, many=True)

		return Response(serializer.data)
	
	def patch(self, request, pk, format='json'):
		currentTask = Task.objects.filter(pk=pk).first()
		newExecutors = CustomUser.objects.filter(pk__in=request.data).all()
		oldExecutors = currentTask.executors.all()
		for newExecutor in newExecutors:
			if (newExecutor not in oldExecutors):
				currentTask.executors.add(newExecutor)
		for oldExecutor in oldExecutors:
			if (oldExecutor not in newExecutors):
				currentTask.executors.remove(oldExecutor)
		return Response({"Updated!"}, status=status.HTTP_201_CREATED)


class TaskInspectorsListView(APIView):

	def get(self, request, pk, format=None):
		currentTask = Task.objects.get(pk=pk)
		inspectors = currentTask.inspections.all()

		serializer = UserSerializer(inspectors, many=True)

		return Response(serializer.data)
	
	def patch(self, request, pk, format='json'):
		currentTask = Task.objects.filter(pk=pk).first()
		newInspectors = CustomUser.objects.filter(pk__in=request.data).all()
		oldInspections = currentTask.inspections.all()
		for newInspector in newInspectors:
			if (newInspector not in oldInspections):
				currentTask.inspections.add(newInspector)
		for oldInspector in oldInspections:
			if (oldInspector not in newInspectors):
				currentTask.inspections.remove(oldInspector)
		return Response({"Updated!"}, status=status.HTTP_202_ACCEPTED)


class MyExecutionTaskListView(generics.ListAPIView):

	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user

		return user.tasks_to_execute.all()
	
	serializer_class = TaskSerializer


class MyInspectionTaskListView(generics.ListAPIView):

	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user

		return user.tasks_to_inspect.all()
	
	serializer_class = TaskSerializer


class StudentsClassListView(generics.ListAPIView):

	queryset = Group.objects.all()
	serializer_class = GroupSerializer


class StudentsClassDetailView(APIView):

	def get_object(self, pk):
		try:
			return Group.objects.get(pk=pk)
		except Group.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		studentClass = self.get_object(pk=pk)
		studentsInClass = StudentProfile.objects.filter(student_class=studentClass).all()

		classSerializer = GroupSerializer(studentClass)
		studentSerializer = StudentSerializer(studentsInClass, many=True)

		return Response({
			"Main info": classSerializer.data,
			"Students": studentSerializer.data
		})


class StudentsInClassListView(generics.ListAPIView):

	def get_queryset(self):
		pass


class TeacherTasksListView(generics.ListAPIView):

	def get_queryset(self):
		user_id = self.kwargs.get("user_id")
		user = CustomUser.objects.filter(pk=user_id).first()

		return user.tasks.all()
	
	serializer_class = TaskShortSerializer


class TeacherStudentsListView(generics.ListAPIView):

	def get_queryset(self):
		user_id = self.kwargs.get("user_id")
		user_profile = CustomUser.objects.filter(pk=user_id).first()

		return StudentProfile.objects.filter(student_class__in=user_profile.groups.all()).all()
	
	serializer_class = StudentSerializer

class SolutionInspectionsListView(generics.ListCreateAPIView):
	
	def get_queryset(self):
		solution_id = self.kwargs.get("solution_id")
		solution = TaskSolution.objects.filter(pk=solution_id).first()
		inspections = SolutionInspection.objects.filter(solution=solution)

		return inspections

	serializer_class = InspectionSerializer

	def post(self, request, solution_id):
		print("Solution inspection -> POST", request.data)
		try:
			inspector = CustomUser.objects.get(pk=request.data["inspector"])
			solution = TaskSolution.objects.get(pk=request.data["solution"])
		except CustomUser.DoesNotExist:
			return Response({"Inspector doesn't exist!"}, status=status.HTTP_400_BAD_REQUEST)
		except TaskSolution.DoesNotExist:
			return Response({"Solution doesn't exist!"}, status=status.HTTP_400_BAD_REQUEST)
		
		SolutionInspection.objects.create(
				solution=solution,
				score = request.data["score"],
				inspector = inspector
			)

		return Response({"Created!"}, status=status.HTTP_201_CREATED)
		


