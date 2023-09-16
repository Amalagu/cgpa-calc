from django.contrib import admin
from .models import Year, Course, Student, Enrollment  # , CGPA
# Register your models here.
admin.site.register(Year)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Enrollment)
# admin.site.register(CGPA)
