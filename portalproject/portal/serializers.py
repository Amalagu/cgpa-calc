from django.urls import path, include
from .models import Course
from rest_framework import routers, serializers, viewsets

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"