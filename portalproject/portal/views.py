from django.shortcuts import render
from .serializers import CourseSerializer
from .models import Year, Course, Student, Enrollment, CGPA
from rest_framework import routers, serializers, viewsets
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        # Get the JSON data from the request
        courses_data = request.data

        # Create a list to hold created course objects
        created_courses = []

        # Iterate through the data and create course instances
        for course_data in courses_data:
            serializer = CourseSerializer(data=course_data)
            if serializer.is_valid():
                serializer.save()
                created_courses.append(serializer.data)

        return Response(created_courses, status=status.HTTP_201_CREATED)






def cgpa_calc(user):
	tgp = 0
	tnu =0
	cgpa = 0.0
	student_course_list = Enrollment.objects.filter(student=user.student)
	for course in student_course_list:
		tgp+= course.grade*course.course.unit
		tnu += course.course.unit
	if tnu:
		cgpa = tgp/tnu
	return cgpa
	

def home(request):
	user=request.user
	#print(user.student)
	cgpa = cgpa_calc(user)
	context ={'cgpa':cgpa}
	return render(request, 'home.html', context)
	
	
	