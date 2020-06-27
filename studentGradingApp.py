import tkinter as tk
from functools import partial

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
        yearOptionsLabel = tk.StringVar(self)
        yearOptionsLabel.set('Year')
        sizeOptionsLabel = tk.StringVar(self)
        sizeOptionsLabel.set('Size')

        classNameLabel = tk.Label(self, text = 'Class Name:', font = largeFont)
        classNameLabel.grid(column = 1, row = 1, padx = (50,10), pady = (50,25), sticky = 'w')
        classNameBox = tk.Text(self, height = 1, width = 30, font = mediumFont)
        classNameBox.grid(column = 2, row = 1, pady = (50,25))

        yearGroupLabel = tk.Label(self, text  = 'Year Group:', font = largeFont)
        yearGroupLabel.grid(column = 1, row = 3, padx = (50,0), pady = 25, sticky = 'w')
        yearGroupOptions = tk.OptionMenu(self,yearOptionsLabel,*years)
        yearGroupOptions.config(font = mediumFont)
        yearGroupOptions.grid(column = 2, row = 3, pady = 25, sticky = 'w')

        maxClassSizeLabel = tk.Label(self, text = 'Maximum Class Size:', font = largeFont)
        maxClassSizeLabel.grid(column = 1, row = 5, padx = (50,0), pady = 25, sticky = 'w')
        maxClassSizeOptions = tk.OptionMenu(self, sizeOptionsLabel, *classSize)
        maxClassSizeOptions.config(font = mediumFont)
        maxClassSizeOptions.grid(column = 2, row = 5, pady = 25, sticky = 'w')








app = backEnd() # equivilant of root = Tk (since backEnd() inherits from Tk)
app.state('zoomed') # makes window fullscreen
app.mainloop()