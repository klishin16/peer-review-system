from django.contrib import admin
from django.urls import path, include, re_path

from .views import (
	CriterionListView, MyExecutionTaskListView, MyInspectionTaskListView, SolutionInspectionsListView, 
	StudentsClassListView, StudentsClassDetailView,
	TaskListView, TaskDetialView, TaskExecutorsListView, TaskInspectorsListView, TaskSolutionsListView, TeacherStudentsListView,
	TeacherTasksListView
)

from accounts.views import (
	StudentListView, StudentDetailView, TeacherDetailView, TeacherListView,
)


urlpatterns = [
    path('tasks/', TaskListView.as_view()),
	path('task/<int:pk>/', TaskDetialView.as_view()),
	path('task/<int:pk>/executors/', TaskExecutorsListView.as_view()),
	path('task/<int:pk>/inspectors/', TaskInspectorsListView.as_view()),
	path('task/<int:pk>/solutions/', TaskSolutionsListView.as_view()),
	path('my_execution_tasks/', MyExecutionTaskListView.as_view()),
	path('my_inspection_tasks/', MyInspectionTaskListView.as_view()),
	path('students_classes/', StudentsClassListView.as_view()),
	path('students_class/<int:pk>/', StudentsClassDetailView.as_view()),
	path('students/', StudentListView.as_view()),
	path('student/<int:pk>/', StudentDetailView.as_view()),
	path('teachers/', TeacherListView.as_view()),
	path('teacher/<int:pk>/', TeacherDetailView.as_view()), # используется user id
	path('teacher/<int:user_id>/tasks/', TeacherTasksListView.as_view()),
	path('teacher/<int:user_id>/students/', TeacherStudentsListView.as_view()),
	path('criterions/', CriterionListView.as_view()),
	path('solution_inspections/<int:solution_id>/', SolutionInspectionsListView.as_view())

]