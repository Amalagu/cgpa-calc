from django.db import models

# Create your models here.

class Year(models.Model):
	levels= [('Year One', 'YR1'), ('Year Two', 'YR2')]
	name = models.Integerfield(max_length=10, choices=levels)
	
	
class Course(models.Model):
	gradelist=[('A', 5), ('B', 4), ('C', 3)]
	code=models.CharField(max_length=6, blank=False, null=False)
	title = models.CharField(max_length=100, blank=False, null=False)
	level = models.ForeignKey(Year, null=False, blank=False)
	unit = models.IntegerField()
	grade=models.IntegerField(choices=gradelist)
	
	
class Profile(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	