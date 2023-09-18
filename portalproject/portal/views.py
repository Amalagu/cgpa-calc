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
    allcourses = Course.objects.filter(level=level)
    enrollments_objects = Enrollment.objects.filter(
        student=student, course__level=year)  # retrieve all the enrollments done by the student in that level
    enrolled_courses = [
        enrolled.course for enrolled in enrollments_objects]  # queryset of all the course objects the student enrolled for in that level
    context = {
        'enrolled_courses': enrolled_courses,
        'courses': allcourses,
        'enrollments_objects': enrollments_objects,
        'level': year.id,
        'year': year.name

    }
    if request.method == 'POST':
        # this retrieves the course codes only for all the courses offered
        allcoursescode = [course.code for course in allcourses]
        enrolled_coursescode = [course.code for course in enrolled_courses]
        set_of_already_enrolled_courses = set(enrolled_coursescode)
        set_of_enrollment_choices = set(
            code for code in request.POST.keys() if code in allcoursescode)
        print(set_of_enrollment_choices)
        print(set_of_already_enrolled_courses)
        for code in (set_of_enrollment_choices - set_of_already_enrolled_courses):
            course = Course.objects.get(code=code)
            enroll = Enrollment.objects.create(
                student=student, course=course, grade=5)
            enroll.save()
        for code in (set_of_already_enrolled_courses - set_of_enrollment_choices):
            enroll = Enrollment.objects.get(course__code=code, student=student)
            enroll.delete()

        return redirect('enrollment_view', level=year.id)
    return render(request, 'enrollment.html', context)


def calc(request, level):
    user = request.user
    student = Student.objects.get(user=user)
    level_id = level
    level_name = Year.objects.get(id=level)
    enrollments = Enrollment.objects.filter(
        course__level=level_id, student=student)
    courses = [enrolled.course for enrolled in enrollments]
    all_enrolled_coursecode = []
    coursestuples = []
    for course in courses:
        grade = course.enrollment.get(student=student).grade
        coursestuples.append((course, grade))
        all_enrolled_coursecode.append(course.code)
    gpa = student.result[f'{level_name}']['gp']
    gradekeys = {
        '0': 'F', '1': 'E', '2': 'D', '3': 'C', '4': 'B', '5': 'A'
    }
    context = {
        'level': level,
        'level_name': level_name,
        'gpa': gpa,
        'cgpa': student.cgpa,
        'courses': courses,
        'coursestuples': coursestuples
    }
    # getting the student's new enrollment selection
    if request.method == 'POST':
        print(request.POST)
        entry_list = []
        tnu = 0
        tgp = 0
        for entry in request.POST:
            if entry in all_enrolled_coursecode and request.POST[entry] != '':
                enroll_new_grade = Enrollment.objects.get(
                    course__code=entry, student=student)
                enroll_new_grade.grade = gradekeys[request.POST[entry]]
                enroll_new_grade.save()
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
        return redirect('calc', level=level)

    return render(request, 'calc.html', context)


def home(request):
    user = request.user
    student_cgpa = studentcgpa(Student.objects.get(user=user))
    if request.method == 'POST':
        if request.POST['level']:
            level = request.POST['level']
            level = Year.objects.get(name=level).id
            if request.POST['choice'] == 'calculate':
                return redirect('calc', level=level)
            elif request.POST['choice'] == 'enroll':
                return redirect('enrollment_view', level=level)

    return render(request, 'home.html', {'cgpa': student_cgpa})
