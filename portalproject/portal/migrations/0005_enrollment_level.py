# Generated by Django 4.2.5 on 2023-09-15 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_alter_cgpa_cgpa_alter_year_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='portal.year'),
        ),
    ]
