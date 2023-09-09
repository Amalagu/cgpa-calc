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
            else:
                print(f"Validation errors: {serializer.errors}")

        return Response(created_courses, status=status.HTTP_201_CREATED)

	

def home(request):
	user=request.user
	courses = Course.objects.all()
	enrolled_objects = Enrollment.objects.filter(student=user.student)
	course_list = [course.code for course in courses ]
	enrolled_courses =[course.course.code for course in enrolled_objects ] #retrieves a list of courses that the current user is enrolled for
	cgpa = 0.0

	#getting the student's new enrollment selection
	if request.method == 'POST':
		print(request.POST)
		entry_list=[]
		tnu = 0
		tgp = 0
		for entry in request.POST:
			if entry in course_list and request.POST[entry] != '':
				entry_list.append(entry)
				entry_course =  Course.objects.get(code=entry)
				tnu += entry_course.unit
				tgp += entry_course.unit * int(request.POST[entry])
		if tnu:
			cgpa = tgp/tnu

	context ={
		'cgpa':cgpa, 
		'courses':courses, 
		'enrolled_courses': enrolled_courses
	}
	return render(request, 'home.html', context)

	
	
""" def enroll(request):
      return render(request, 'enrollment') """