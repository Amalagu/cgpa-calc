# Generated by Django 4.2.5 on 2023-09-18 14:11

from django.db import migrations, models
import django.db.models.deletion
import portal.models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_remove_enrollment_level_student_cgpa_student_result_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='portal.course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='result',
            field=models.JSONField(default=portal.models.Student.makedict),
        ),
    ]
