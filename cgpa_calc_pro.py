#!
from tkinter import *
import time
from tkinter.messagebox import showinfo


"""This is a G.P.A calculator with a graphical User Interface. A selftest code is attached at the end of the code so the program can be run from an IDE or by double-clicking on the source-file Icon on a GUI Operating System"""


#List of Courses for various levels
lis1=['csc 111', 'csc 112', 'csc 113', 'csc 114' ]
lis2=['csc 211', 'csc 212', 'csc 213', 'csc 214' ]
lis3=['csc 311', 'csc 312', 'csc 313', 'csc 314' ]
lis4=['csc 411', 'csc 412', 'csc 413', 'csc 414' ]
lis5=['csc 511', 'csc 512', 'csc 513', 'csc 514' ]
dic={'Yr1':lis1, 'Yr2':lis2, 'Yr3':lis3, 'Yr4':lis4, 'Yr5':lis5}
#
grades=['A', 'B', 'C', 'D', 'E', 'F']
unit=[5,4,3,2,1,0]
grades_dict=dict(zip(grades, unit ))




class LevelSelect(Frame):
	def __init__(self, parent=None, levellist=['Yr1', 'Yr2', 'Yr3', 'Yr4', 'Yr5'], **options):
		Frame.__init__(self, parent, **options)
		self.levellist=levellist
		self.var=StringVar()
		for level in self.levellist:
			Radiobutton(self, text=level, variable=self.var, value=level, command=onpress).pack(side=LEFT)
		self.var.set(self.levellist[0])
	#def onpress(self):
#		val=self.var.get()
#		chosen=dic[val]



class CourseMenu(Frame):
	def __init__(self, checkbutton, parent=None, **options):
		Frame.__init__(self, parent, **options)
		courselist=dic[checkbutton.var.get()]
		self.var=StringVar()
		OptionMenu(self, self.var, *courselist ).pack(side=TOP)
		self.var.set(courselist[0])
		
		
class GradeMenu(Frame):
	def __init__(self, parent=None, gradelist=['A', 'B', 'C', 'D', 'E', 'F'], **options):
		Frame.__init__(self, parent, **options)
		self.gradelist=gradelist
		self.var=StringVar()
		OptionMenu(self, self.var, *self.gradelist ).pack(side=TOP)
		self.var.set(self.gradelist[0])
		
class UnitMenu(Frame):
	def __init__(self, parent=None, unitlist=[4,3,2,1,0], **options):
		Frame.__init__(self, parent, **options)
		self.unitlist=unitlist
		self.var=StringVar()
		OptionMenu(self, self.var, *self.unitlist ).pack(side=TOP)
		self.var.set(self.unitlist[0])
		






if __name__ == '__main__':
		
		root=Frame()
		root.grid(columnspan=3)
		def onpress():
			for i in range(1,6):
				courseitem=CourseMenu(levs)
				courseitem.grid(row=i, column=0, sticky=EW)
		levs=LevelSelect(root)
		levs.pack(side=TOP, fill=BOTH)
		uglist=[]
		for i in range(1,6):
			courseitem=CourseMenu(levs)
			courseitem.grid(row=i, column=0, sticky=EW)
			unititem=UnitMenu()
			unititem.grid(row=i, column=1,sticky=EW )
			gradeitem=GradeMenu()
			gradeitem.grid(row=i, column=2, sticky=EW   )
			uglist.append((unititem, gradeitem))
			xxx=lambda:oncalculate(uglist)
			Button(text='Calculate', command=xxx).grid(row=i+1, column=2)
			Button(text='Quit', command=quit).grid(row=i+1, column=1)
			
		def oncalculate(list):
				multiplesum=0
				simplesum=0
				for (x,y) in list:
					x=int(x.var.get())
					y=grades_dict[y.var.get()]
					multiplesum+= (x*y)
					simplesum+=x
				cgpa=(multiplesum/simplesum)
				showinfo(title="G.P.A", message=f"Your G.P.A is  %.2f" % cgpa )
			
		Label(root, text='GPA CALCULATOR').pack(side=TOP, fill=BOTH)
	
		
		
		mainloop()
		

		
