# Generated by Django 3.1.2 on 2021-01-11 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210111_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherprofile',
            name='student_classes',
        ),
    ]