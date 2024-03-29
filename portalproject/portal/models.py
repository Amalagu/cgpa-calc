from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Year(models.Model):
    levels = [
        ('Year One', 'YR1'),
        ('Year Two', 'YR2'),
        ('Year Three', 'YR3'),
        ('Year Four', 'YR4'),
        ('Year Five', 'YR5')
    ]

    name = models.CharField(max_length=10, choices=levels)

    @property
    def gpa(self):
        tnu = self.course_set.all()

    def __str__(self):
        return self.name


class Course(models.Model):
    semesterlist = (('Harmattan', 'Harmattan'), ('Rain', 'Rain'))
    semester = models.CharField(
        max_length=50, choices=semesterlist, null=True, blank=True)
    code = models.CharField(max_length=7, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    level = models.ForeignKey(
        Year, null=False, blank=False, on_delete=models.CASCADE)
    unit = models.IntegerField()

    def __str__(self):
        return self.code


class Student(models.Model):
    def makedict():
        newdict = dict()
        sampledict = {'Year One': {'tnu': 0, 'tgp': 0, 'gp': 0},
                      'Year Two': {'tnu': 0, 'tgp': 0, 'gp': 0},
                      'Year Three': {'tnu': 0, 'tgp': 0, 'gp': 0},
                      'Year Four': {'tnu': 0, 'tgp': 0, 'gp': 0},
                      'Year Five': {'tnu': 0, 'tgp': 0, 'gp': 0}
                      }
        newdict = sampledict.copy()
        return newdict
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20)
    result = models.JSONField(default=makedict)
    cgpa = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


class Enrollment(models.Model):
    gradelist = [('A', 'A'), ('B', 'B'), ('C', 'C'),
                 ('D', 'D'), ('E', 'E'), ('F', 'F')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollment")
    grade = models.CharField(max_length=1, choices=gradelist)
    # level = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.code} )"


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(
            user=instance, registration_number="YourDefaultValueHere")


@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    instance.student.save()


post_save.connect(create_student_profile, sender=User)
post_save.connect(save_student_profile, sender=User)


""" class CGPA(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    cgpa = models.DecimalField(
        max_digits=4, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - CGPA: {self.cgpa}"
 """

"""
from django.db import models
from django.contrib.auth.models import User

# Define the Course model
class Course(models.Model):
    course_code = models.CharField(max_length=10)
    course_title = models.CharField(max_length=100)
    credit_hours = models.PositiveIntegerField()

    def __str__(self):
        return self.course_code

# Define the Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    batch_session = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

# Define the Enrollment model as an intermediary table
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.course_code} ({self.semester})"

# Define the CGPA model
class CGPA(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - CGPA: {self.cgpa}"
"""
