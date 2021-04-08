from datetime import date
from django.db import models
from django.contrib.auth import get_user_model

import datetime


class Criterion(models.Model):
	title = models.CharField(max_length=120, default="Критерий ", verbose_name="Название критерия")
	description = models.CharField(max_length=450, default="Описание ", verbose_name="Описание критерия")
	weight = models.IntegerField(default=1)

	def __str__(self) -> str:
		return self.title


class Task(models.Model):
	title = models.CharField(max_length=120, verbose_name="Название задания")
	description = models.CharField(max_length=450, verbose_name="Текст задания")
	criterions = models.ManyToManyField(Criterion)
	executors = models.ManyToManyField(get_user_model(), through="TaskExecutor", related_name="tasks_to_execute")
	inspections = models.ManyToManyField(get_user_model(), through="TaskInspection", related_name="tasks_to_inspect")
	teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Учитель", related_name="tasks", default=1)
	status = models.IntegerField(choices=(
		(0, "Not started"),
		(1, "In progress"),
		(2, "Done")
	))

	def __str__(self) -> str:
		return self.title


class TaskExecutor(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	executor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	creation_date = models.DateField(default=datetime.date.today)
	deadline = models.DateField(default=datetime.date.today)

	def __str__(self) -> str:
		return self.task.title + " -> " + self.executor.email


class TaskInspection(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	inspector = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	
	def __str__(self) -> str:
		return self.task.title + " -> " + self.inspector.email


class TaskSolution(models.Model):
	data = models.CharField(max_length=1000)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_solutions")
	executor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	score = models.IntegerField(blank=True, null=True)

	def __str__(self) -> str:
		return self.executor.email + " -> " + self.task.title


class SolutionInspection(models.Model):
	solution = models.ForeignKey(TaskSolution, on_delete=models.CASCADE, related_name="solution_inspections", default=1)
	score = models.IntegerField()
	inspector = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="inspections")

	def __str__(self) -> str:
		return self.inspector.email + " -> " + str(self.score)	


class Group(models.Model):
	title = models.CharField(max_length=10, default="1A")
	teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="groups", null=True, blank=True)

	def __str__(self) -> str:
		return self.title


class Comments(models.Model):
	title = models.CharField(max_length=140, default="Комментарий")
	text = models.CharField(max_length=450, verbose_name="Текст комментария")
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	post_time = models.DateTimeField(default=datetime.datetime.now)



	
