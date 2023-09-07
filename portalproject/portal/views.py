from django.shortcuts import render

from .models import Year, Course, Student, Enrollment, CGPA
# Create your views here.


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