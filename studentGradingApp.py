import tkinter as tk
from functools import partial
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

largeFont = ("Verdana",20)
mediumFont = font = ("Verdana",15)

class backEnd(tk.Tk): # pass in Tk module of tk

    def __init__(self, *args, **kwargs): # unlimited arguments and dicts passed
        tk.Tk.__init__(self, *args, **kwargs) # initialise Tk module
        container = tk.Frame(self) # like root?
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        container.pack(fill = tk.BOTH, expand = True)

        self.frames = {} # empty dict to store frames - when needed the frame is
        # brought to the top

        # Storing StartPage frame - (Key: StartPage, value: StartPage object)
        self.frames[StartPage] = StartPage(parent = container, controller = self)
        # parent is container to store all pages in same area
        # controller is self (instance of backEnd class) to allow new pages access 
        # methods in this class (e.g. showFrame)
        self.frames[StartPage].grid(row = 0, column = 0, sticky = 'nesw')

        self.frames[TeacherMenu] = TeacherMenu(parent = container, controller = self)
        self.frames[TeacherMenu].grid(row = 0, column = 0, sticky = 'nesw')

        self.frames[AddClass] = AddClass(parent = container, controller = self)
        self.frames[AddClass].grid(row = 0, column = 0, sticky = 'nesw')

        # must be called in __init__ function to open StartPage as soon as program run
        self.showFrame(StartPage)

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()
        


class StartPage(tk.Frame): # we inherit from tk.Frame to use all widgets related to Frame (e.g. rowconfigure)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # creates StartPage's own Frame object which stores all its widgets
        self.controller = controller    # its Frame object is stored in 'container' (along with all other pages in the app)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        teacherButton = tk.Button(self, text = 'Teacher', font = largeFont,
         borderwidth = 5,command = lambda:self.controller.showFrame(TeacherMenu))
        teacherButton.grid(row = 0, column = 0, sticky = 'nesw', padx = (10, 25), pady = 50)
        # padx can take a tuple to pad left and right by different amounts (left, right)

        studentButton = tk.Button(self, text = 'Student', font = largeFont, borderwidth = 5)
        studentButton.grid(row = 0, column = 1, sticky = 'nesw', padx = (25, 10), pady = 50)

class TeacherMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        addClass = tk.Button(self, text = 'Add new class', height = 3, width = 60, command = lambda: self.controller.showFrame(AddClass))
        addClass.pack(side = tk.TOP, pady = (175,20))
        addStudent = tk.Button(self, text = 'Add new student', height = 3, width = 60)
        addStudent.pack(side = tk.TOP, pady = 20)
        addGrades = tk.Button(self, text = 'Add new grades', height = 3, width = 60)
        addGrades.pack(side = tk.TOP, pady = 20)
        analyse = tk.Button(self, text = 'Analyse Grades', height = 3, width = 60)
        analyse.pack(side = tk.TOP, pady = 20)
        viewAll = tk.Button(self, text = 'View all students', height = 3, width = 60)
        viewAll.pack(side = tk.TOP, pady = 20)
        changes = tk.Button(self, text = 'Make Changes', height = 3, width = 60)
        changes.pack(side = tk.TOP, pady = 20)


class AddClass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        years = ['Year 7', 'Year 8', 'Year 9', 'Year 10', 'Year 11', 'Year 12', 'Year 13']
        classSize = list(range(1,31))
        self.yearOptionsLabel = tk.StringVar(self)
        self.yearOptionsLabel.set('Year')
        self.sizeOptionsLabel = tk.StringVar(self)
        self.sizeOptionsLabel.set('Size')

        self.classNameLabel = tk.Label(self, text = 'Class Name:', font = largeFont)
        self.classNameLabel.grid(column = 1, row = 1, padx = (50,10), pady = (50,25), sticky = 'w')
        self.classNameBox = tk.Entry(self,width = 30, font = mediumFont)
        self.classNameBox.grid(column = 2, row = 1, pady = (50,25))

        self.yearGroupLabel = tk.Label(self, text  = 'Year Group:', font = largeFont)
        self.yearGroupLabel.grid(column = 1, row = 3, padx = (50,0), pady = 25, sticky = 'w')
        self.yearGroupOptions = tk.OptionMenu(self,self.yearOptionsLabel,*years)
        self.yearGroupOptions.config(font = mediumFont)
        self.yearGroupOptions.grid(column = 2, row = 3, pady = 25, sticky = 'w')

        self.maxClassSizeLabel = tk.Label(self, text = 'Maximum Class Size:', font = largeFont)
        self.maxClassSizeLabel.grid(column = 1, row = 5, padx = (50,0), pady = 25, sticky = 'w')
        self.maxClassSizeOptions = tk.OptionMenu(self, self.sizeOptionsLabel, *classSize)
        self.maxClassSizeOptions.config(font = mediumFont)
        self.maxClassSizeOptions.grid(column = 2, row = 5, pady = 25, sticky = 'w')

        self.submitButton = tk.Button(self, text = 'Submit', font = mediumFont,
         command = self.addValues)
        self.submitButton.grid(column = 1, row = 7, padx = (50,0), pady = 25, sticky = 'w')

    def addValues(self):
        className, yearGroup, maxSize = self.classNameBox.get(), self.yearOptionsLabel.get(), self.sizeOptionsLabel.get()
        # assigns multiple variables together
        # self.yearOptionsLabel.get() returns current value of year drop down list
        print(className, yearGroup, maxSize+' are the values')

        if (className == '' or yearGroup == 'Year' or maxSize == 'Size'):
            print('Do not leave values empty.')

        # use try except structure for creating a class with an existing primary key
        # error: sqlite3.IntegrityError


        with conn:
            cursor.execute("INSERT INTO classes VALUES (?,?,?)", (className, yearGroup, maxSize))










app = backEnd() # equivilant of root = Tk (since backEnd() inherits from Tk)
app.state('zoomed') # makes window fullscreen
app.mainloop()