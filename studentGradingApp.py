import tkinter as tk
from functools import partial
import sqlite3

import matplotlib
matplotlib.use("TkAgg") # backend of mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

largeFont = ("Verdana",15)
mediumFont = ("Verdana",12)
smallFont =  ("Verdana", 10)

class backEnd(tk.Tk): # pass in Tk module of tk

    def __init__(self, *args, **kwargs): # unlimited arguments and dicts passed
        tk.Tk.__init__(self, *args, **kwargs) # initialise Tk module
        container = tk.Frame(self) # like root?
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        container.pack(fill = tk.BOTH, expand = True)

        self.frames = {} # empty dict to store frames - when needed the frame is
        # brought to the top
        self.studentClass = {}
        self.allClasses = [Class[0] for Class in cursor.execute("SELECT [Class Name] FROM classes")] 
        # self.updatedList = [Name[0] for Name in cursor.execute("SELECT [Class Name] FROM classes")]   

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

        self.frames[AddStudent] = AddStudent(parent = container,controller = self)
        self.frames[AddStudent].grid(row = 0, column = 0, sticky = 'nesw')

        self.frames[AddGrades] = AddGrades(parent = container, controller = self)
        self.frames[AddGrades].grid(row = 0, column = 0, sticky = 'nesw')

        self.frames[ViewGrades] = ViewGrades(parent = container, controller = self)
        self.frames[ViewGrades].grid(row = 0, column = 0, sticky = 'nesw')


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
        addStudent = tk.Button(self, text = 'Add new student', height = 3, width = 60, command = lambda: self.controller.showFrame(AddStudent))
        addStudent.pack(side = tk.TOP, pady = 20)
        addGrades = tk.Button(self, text = 'Add new grades', height = 3, width = 60, command = lambda: self.controller.showFrame(AddGrades))
        addGrades.pack(side = tk.TOP, pady = 20)
        analyse = tk.Button(self, text = 'View Grades', height = 3, width = 60, command = lambda: self.controller.showFrame(ViewGrades))
        analyse.pack(side = tk.TOP, pady = 20)
        viewAll = tk.Button(self, text = 'View all students', height = 3, width = 60)
        viewAll.pack(side = tk.TOP, pady = 20)
        changes = tk.Button(self, text = 'Make Changes', height = 3, width = 60)
        changes.pack(side = tk.TOP, pady = 20)


class AddClass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6']
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

        self.backButton = tk.Button(self, text = 'Back', font = mediumFont, command = lambda: self.controller.showFrame(TeacherMenu))
        self.backButton.grid(column = 1, row = 7, padx = (50,0), pady = 25, sticky = 'w')
        self.submitButton = tk.Button(self, text = 'Submit', font = mediumFont,
         command = self.addValues)
        self.submitButton.grid(column = 2, row = 7, padx = (50,0), pady = 25, sticky = 'e')

    def addValues(self):
        className, yearGroup, maxSize = self.classNameBox.get(), self.yearOptionsLabel.get(), self.sizeOptionsLabel.get()
        # assigns multiple variables together
        # self.yearOptionsLabel.get() returns current value of year drop down list

        try: # prevents program crashing if exisiting class name entered
            if (className == '' or yearGroup == 'Year' or maxSize == 'Size'): # if field empty display error message
                errorMessage = tk.Label(self, text = 'Fill in all fields', font = mediumFont)
                errorMessage.grid(column = 1, padx = (50,0), row = 9, sticky = 'w')
            else:
                with conn:
                    cursor.execute("INSERT INTO classes VALUES (?,?,?)", (className, yearGroup, maxSize))
                acceptanceMessage = tk.Label(self, text = 'Class added', font = mediumFont)
                acceptanceMessage.grid(column = 1, padx = (50,0), row = 9, sticky = 'w')

                self.toAdd = tk.StringVar(self)
                self.toAdd2 = tk.StringVar(self)
                self.toAdd.set(className)
                self.toAdd2.set(className)
                self.display1 = self.controller.frames[AddStudent].classNameMenuLabel
                menu = self.controller.frames[AddStudent].classNameList['menu'] # getting dropdown list from AddStudent class
                # label = value to add to list, command = set label of dropdown list (self.var2) to the new value when this
                # value is clicked on
                # menu.add_command(label=self.toAdd.get(), command=lambda a=self.toAdd.get(): self.var2.set(a))
                menu.add_command(label=self.toAdd.get(), command= lambda: self.display1.set(self.toAdd.get()))

                self.display2 = self.controller.frames[ViewGrades].classNameMenuLabel
                menu2 = self.controller.frames[ViewGrades].classList['menu']
                menu2.add_command(label = self.toAdd2.get(), command = lambda: self.display2.set(self.toAdd2.get()))                
               # self.controller.allClasses.append(className)

        except sqlite3.IntegrityError:
            errorMessage = tk.Label(self, text = 'Enter a unique class name', font = mediumFont)
            errorMessage.grid(column = 1, padx = (50,0), row = 9, sticky = 'w')

class AddStudent(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.updatedList = [Name[0] for Name in cursor.execute("SELECT [Class Name] FROM classes")]
        self.updatedList.append(None)
 
        self.classNameMenuLabel = tk.StringVar(self)
        self.classNameMenuLabel.set('Class')

        self.firstNameLabel = tk.Label(self, text = 'First Name:', font = largeFont)
        self.firstNameLabel.grid(column = 1, row = 1, padx = (50,10), pady = (50,25), sticky = 'w')
        self.firstNameBox = tk.Entry(self,width = 30, font = mediumFont)
        self.firstNameBox.grid(column = 2, row = 1, pady = (50,25))
        self.lastNameLabel = tk.Label(self, text = 'Surname:', font = largeFont)
        self.lastNameLabel.grid(column = 1, row = 3, padx = (50,10), pady = 25, sticky = 'w')
        self.lastNameBox = tk.Entry(self,width = 30, font = mediumFont)
        self.lastNameBox.grid(column = 2, row = 3, pady = 25)
        self.classNameLabel = tk.Label(self, text = 'Class:', font = largeFont)
        self.classNameLabel.grid(column = 1, row = 5, padx = (50,0), pady = 25, sticky = 'w')
        self.classNameList = tk.OptionMenu(self, self.classNameMenuLabel,*self.updatedList)
        self.classNameList.config(font = mediumFont)
        self.classNameList.grid(column = 2, row = 5, pady = 25, sticky = 'w')

        self.submitButton = tk.Button(self, text = 'Submit', font = mediumFont, command = lambda: self.submitDetails())
        self.submitButton.grid(column = 3, row = 7, pady = 30, sticky ='w')
        self.backButton = tk.Button(self, text = 'Back', font = mediumFont, command =lambda: self.controller.showFrame(TeacherMenu))
        self.backButton.grid(column = 1, row = 7, pady = 25, padx = 10, sticky = 'w')

    def submitDetails(self):
        self.firstName = self.firstNameBox.get()
        self.lastName = self.lastNameBox.get()
        self.className = self.classNameMenuLabel.get()
      ##  try:
        with conn:
            cursor.execute('SELECT * FROM students WHERE [First Name] LIKE ? AND [Surname] LIKE ?',(self.firstName, self.lastName))
            exists = cursor.fetchall()
            if (exists != []):
                print('already exists')
                self.failureMsg = tk.Label(self, text = 'This student already exists', font = mediumFont)
                self.failureMsg.grid(column = 3, row = 9, pady = 30, sticky = 'w')
            else:
                cursor.execute("INSERT INTO students ([First Name], Surname, Class) VALUES (?,?,?)", (self.firstName, self.lastName, self.className))
                self.successMsg = tk.Label(self, text = 'Student added                ', font = mediumFont)
                self.successMsg.grid(column = 3, row = 9, pady = 30, sticky ='w')
                self.controller.studentClass[self.className] = self.firstName+" "+self.lastName
                print(self.controller.studentClass)
        
        ############################################################################
        # self.firstNameVariable is created in this class
        # firstNameVar is a tk.StringVar type from ViewGrades class.
        self.firstNameVariable = tk.StringVar(self)
        self.firstNameVariable.set(self.firstName) 
        self.firstNameDisplay = self.controller.frames[ViewGrades].firstNameVar
        firstNameMenu = self.controller.frames[ViewGrades].firstNameList['menu']
        firstNameMenu.add_command(label = self.firstNameVariable.get(), command = lambda: self.firstNameDisplay.set(self.firstNameVariable.get()))
        # Next Steps - Add same for Surname and reorder ViewGrades Page.

        self.surnameVariable = tk.StringVar(self)
        self.surnameVariable.set(self.lastName)
        self.surnameDisplay = self.controller.frames[ViewGrades].surnameVar
        surnameMenu = self.controller.frames[ViewGrades].surnameList['menu']
        surnameMenu.add_command(label = self.surnameVariable.get(), command = lambda: self.surnameDisplay.set(self.surnameVariable.get()))

class AddGrades(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.StringVar(self)
        self.label.set('Term')
        self.termList = ['Autumn1', 'Autumn2', 'Spring1', 'Spring2', 'Summer1', 'Summer2']


        self.firstNameLabel = tk.Label(self, text = 'First Name:', font = largeFont)
        self.firstNameLabel.grid(column = 1, row = 1, padx = (50,10), pady = (50,25), sticky = 'w')
        self.firstNameBox = tk.Entry(self,width = 30, font = mediumFont)
        self.firstNameBox.grid(column = 2, row = 1, pady = (50,25))

        self.lastNameLabel = tk.Label(self, text = 'Surname:', font = largeFont)
        self.lastNameLabel.grid(column = 1, row = 3, padx = (50,10), pady = 25, sticky = 'w')
        self.lastNameBox = tk.Entry(self,width = 30, font = mediumFont)
        self.lastNameBox.grid(column = 2, row = 3, pady = 25)

        self.markAchievedLabel = tk.Label(self, text = 'Mark Achieved: ', font = largeFont)
        self.markAchievedLabel.grid(column = 1, row = 5, padx = (50,10), pady = 25, sticky = 'w')
        self.markAchievedBox = tk.Entry(self, width = 3, font = mediumFont)
        self.markAchievedBox.grid(column = 2, row = 5, pady = 25, sticky = 'w')

        self.totalMarksLabel = tk.Label(self, text = 'Marks Available: ', font = largeFont)
        self.totalMarksLabel.grid(column = 1, row = 7, padx = (50,10), pady = 25, sticky = 'w')
        self.totalMarksBox = tk.Entry(self, width = 3, font =mediumFont)
        self.totalMarksBox.grid(column = 2, row = 7, pady = 25, sticky = 'w')

        self.termMenu = tk.OptionMenu(self, self.label, *self.termList)
        self.termMenu.config(font = mediumFont)
        self.termMenu.grid(column = 1, row = 9, padx = (50,10), pady = 25, sticky = 'w')

        self.backButton = tk.Button(self, text = 'Back', font = mediumFont, command = lambda: self.controller.showFrame(TeacherMenu))
        self.backButton.grid(column = 1, row = 11, padx = (50,10), pady = 25, sticky = 'w')

        self.submitButton = tk.Button(self, text = 'Submit', font = mediumFont, command = lambda: self.findPercentage())
        self.submitButton.grid(column = 2, row = 11, padx = 10, pady = 25, sticky = 'w')

    def findPercentage(self):
        markAchieved = int(self.markAchievedBox.get())
        totalMark = int(self.totalMarksBox.get())
        firstName = self.firstNameBox.get()
        lastName = self.lastNameBox.get()

        percentage = (markAchieved/totalMark)*100
        percentage = round(percentage,2)
        if percentage > 100:
            percentage = 0
            errorLabel = tk.Label(self, text = 'Enter a valid score', font = mediumFont)
            errorLabel.grid(column = 2, row = 13, padx = 50, pady = 25, sticky = 'w')

        # print(percentage, self.label.get(), firstName, lastName)

        with conn:
            cursor.execute('''SELECT [First Name], Surname FROM students WHERE [First Name] = ? AND [Surname]
            = ? ''',(firstName, lastName))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE students SET ("+ self.label.get()+") = ? WHERE [First Name] = ? AND Surname = ?",(percentage,
                firstName, lastName))
            
                successLabel = tk.Label(self, text = 'Percentage Added          ', font = mediumFont)
                successLabel.grid(column = 2, row = 13, padx = 50, pady = 25, sticky = 'w')
            else:
                
                errorLabel = tk.Label(self, text = 'Student does not exist', font = mediumFont)
                errorLabel.grid(column = 2, row = 13, padx = 50, pady = 25, sticky = 'w')


        # in future instead of 'first name' and 'surname' have 2 dropdown boxes
        # 1st: 'Class', once user chooses the class, the next dropdown ('Student') dynamically updates

class ViewGrades(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.classNameMenuLabel = tk.StringVar(self)
      #  self.classNameMenuLabel.trace('w', self.updateOptions)
        self.classNameMenuLabel.set('Class')

        self.firstNameVar = tk.StringVar(self)
        self.firstNameVar.set('First Name')

        self.surnameVar = tk.StringVar(self)
        self.surnameVar.set('Last Name')
       # self.firstNameLabel.set('First Name')
        # self.firstNameLabel.trace('w', self.updateOptions)

        self.updatedClassList = [Class[0] for Class in cursor.execute("SELECT [Class Name] FROM classes")]
        if self.updatedClassList == []:
            self.updatedClassList.append(None)
        
        self.updatedNameList = [Name[0] for Name in cursor.execute("SELECT [First Name] FROM students")]
        if self.updatedNameList == []:
            self.updatedNameList.append(None)

        self.updatedSurnameList = [Name[0] for Name in cursor.execute("SELECT [Surname] FROM students")]
        if self.updatedSurnameList == []:
            self.updatedSurnameList.append(None)

        self.firstNameLabel = tk.Label(self, text = 'First Name:', font = largeFont)
        self.firstNameLabel.grid(column = 1, row = 1, padx = (50,10), pady = (50,25), sticky = 'w')
        self.firstNameList = tk.OptionMenu(self, self.firstNameVar, *self.updatedNameList)
        self.firstNameList.config(font = mediumFont)
        self.firstNameList.grid(column = 2, row = 1, padx = (50,10), pady = (50,25), sticky = 'w')

        self.surnameLabel = tk.Label(self, text = 'Last Name:', font = largeFont)
        self.surnameLabel.grid(column = 1, row = 3, padx = (50,10), pady = 25, sticky = 'w')
        self.surnameList = tk.OptionMenu(self, self.surnameVar, *self.updatedSurnameList)
        self.surnameList.config(font = mediumFont)
        self.surnameList.grid(column = 2, row = 3, padx = (50,10), pady = 25, sticky = 'w')

        self.classLabel = tk.Label(self, text = 'Class:', font = largeFont)
        self.classLabel.grid(column = 1, row = 5, padx = (50,10), pady = 25, sticky = 'w')
        self.classList = tk.OptionMenu(self, self.classNameMenuLabel, *self.updatedClassList)
        self.classList.config(font = mediumFont)
        self.classList.grid(column = 2, row = 5, padx = (50,10), pady = 25, sticky = 'w')

        self.findStudentButton = tk.Button(self, text = 'Find Student', font = mediumFont, command = self.findStudent)
        self.findStudentButton.grid(column = 2, row = 7, pady = 25, sticky = 'w', padx = 50)

        self.backButton = tk.Button(self, text = 'Back', font = mediumFont, command = lambda: self.controller.showFrame(TeacherMenu))
        self.backButton.grid(column = 1, row = 7, pady = 25, sticky = 'w', padx = (50,25))

    def findStudent(self):
        firstName, surname, myClass = self.firstNameVar.get(), self.surnameVar.get(), self.classNameMenuLabel.get()
        
        try:
            cursor.execute('''SELECT Autumn1, Autumn2, Spring1, Spring2, Summer1, Summer2 FROM students
             WHERE [First Name] LIKE ? AND Surname LIKE ? AND Class LIKE ?''', (firstName, surname, myClass))
            results = list(cursor.fetchone()) # stores the first set of values returned by cursor
            terms = ['Autumn 1:', 'Autumn 2:', 'Spring 1:', 'Spring 2:', 'Summer 1:', 'Summer 2:']
            for i in range(6):
                termLabel_i = tk.Label(self, text = terms[i], font = smallFont)
                termLabel_i.grid(column = 1, row = 8 + i, padx = (50, 10), pady = 25, sticky = 'w')

                scoreLabel_i = tk.Label(self, text = results[i], font = smallFont)
                scoreLabel_i.grid(column = 2, row = 8 + i, padx = (50, 10), pady = 25, sticky = 'w')
            generateGraphButton = tk.Button(self, text = 'Generate Graph', font = mediumFont, command = lambda: self.addGraphPopUp(results))
            generateGraphButton.grid(column = 3, row = 1, padx = 50, pady = 50, sticky = 'w')
        except:
             pass
    
    def addGraphPopUp(self, results):
        popup = tk.Tk()
        popup.wm_title('Student Results Graph')
        f = Figure(figsize = (6,6), dpi = 100)
        a = f.add_subplot(111) # adds to 1 chart
        my_xticks = ['Autumn 1', 'Autumn 2', 'Spring 1', 'Spring 2', 'Summer 1', 'Summer 2']
        y = [results[0],results[1], results[2], results[3], results[4], results[5]]
        a.plot(my_xticks,y)

        canvas = FigureCanvasTkAgg(f, popup)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 7, row = 5)

        closeButton = tk.Button(popup, text = 'Close', command = popup.destroy)
        closeButton.grid(column = 1, row = 15)


app = backEnd() # equivilant of root = Tk (since backEnd() inherits from Tk)
app.state('zoomed') # makes window fullscreen
app.mainloop()

# create a students class. The class should hold a dictionary for each term and the number of times marks have been submitted.