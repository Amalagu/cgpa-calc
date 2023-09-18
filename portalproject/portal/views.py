from django.shortcuts import render, redirect
from .serializers import CourseSerializer
from .models import Year, Course, Student, Enrollment  # , CGPA
from rest_framework import routers, serializers, viewsets
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


def studentcgpa(student):
    tnu = 0
    tgp = 0
    for key in student.result.keys():
        tnu += student.result[key]['tnu']
        tgp += student.result[key]['tgp']
    if tnu:
        return tgp/tnu
    return 0.0


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


def enrollment_view(request, level):
    year = Year.objects.get(id=level)
    student = Student.objects.get(user=request.user)
    courses = Course.objects.filter(level=level)
    enrollments_objects = Enrollment.objects.filter(
        student=student, course__level=year)
    enrolled_courses = [
        enrolled.course for enrolled in enrollments_objects]
    context = {
        'enrolled_courses': enrolled_courses,
        'courses': courses,
        'enrollments_objects': enrollments_objects,
        'level': year.id

    }
    if request.method == 'POST':
        # this matches the course codes
        coursescode = [course.code for course in courses]
        enrolled_coursescode = [course.code for course in enrolled_courses]
        for code in request.POST.keys():
            # if (code not in enrolled_coursescode) & (code in coursescode):
            if code in coursescode:
                course = Course.objects.get(code=code)
                enroll = Enrollment.objects.create(
                    student=student, course=course, grade=5)
                enroll.save()

        return redirect('enrollment_view', level=year.id)
    return render(request, 'enrollment.html', context)


def calc(request, level):
    user = request.user
    student = Student.objects.get(user=user)
    level_id = level
    level_name = Year.objects.get(id=level)
    courses = Course.objects.filter(level=level_id)
    # enrolled_objects = Enrollment.objects.filter(student=user.student)
    # course_list = [course.code for course in courses]
    # retrieves a list of courses that the current user is enrolled for
    # enrolled_courses = [course.course.code for course in enrolled_objects]
    gpa = student.result[f'{level_name}']['gp']

    # getting the student's new enrollment selection
    if request.method == 'POST':
        entry_list = []
        tnu = 0
        tgp = 0
        for entry in request.POST:
            if entry in courses and request.POST[entry] != '':
                entry_list.append(entry)
                entry_course = Course.objects.get(code=entry)
                tnu += entry_course.unit
                tgp += entry_course.unit * int(request.POST[entry])
        if tnu:
            gpa = tgp/tnu
        student.result[f'{level_name}']['tnu'] = tnu
        student.result[f'{level_name}']['tgp'] = tgp
        student.result[f'{level_name}']['gp'] = gpa
        student.cgpa = studentcgpa(student)
        student.save()

    context = {
        'level': level,
        'level_name': level_name,
        'gpa': gpa,
        'cgpa': student.cgpa,
        'courses': courses,
    }
    return render(request, 'calc.html', context)


def home(request):
    user = request.user
    student_cgpa = studentcgpa(Student.objects.get(user=user))
    if request.method == 'POST':
        level = request.POST['level']
        level = Year.objects.get(name=level).id
        courses = Course.objects.filter(level=level)
        return redirect(calc, level)

    return render(request, 'home.html', {'cgpa': student_cgpa})
