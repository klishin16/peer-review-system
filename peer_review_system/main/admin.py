from django.contrib import admin

from .models import (
	Task, 
	TaskExecutor,
	TaskInspection,
	TaskSolution,
	Criterion, 
	Group,
	SolutionInspection,
)


# class StudentsInline(admin.TabularInline):
# 	model = StudentProfile


class TaskAdmin(admin.ModelAdmin):
	list_display = ['title', 'teacher']

	#inlines = [
	# 	CriterionInline,
	# ]

# class StudentInline(admin.TabularInline):
#     model = CustomUser

class GroupAdmin(admin.ModelAdmin):
	list_display = ['title']
	# inlines = [
	# 	StudentsInline
	# ]

class TaskExecutorAdmin(admin.ModelAdmin):
	list_display = ['task', 'id']

class SolutionInspectionAdmin(admin.ModelAdmin):
	list_display = ['solution', 'inspector', 'score']


admin.site.register(Task, TaskAdmin)
admin.site.register(Criterion)
admin.site.register(TaskExecutor, TaskExecutorAdmin)
admin.site.register(TaskInspection)
admin.site.register(TaskSolution)
admin.site.register(Group, GroupAdmin)
admin.site.register(SolutionInspection, SolutionInspectionAdmin)

# admin.site.register(StudentProfile)
