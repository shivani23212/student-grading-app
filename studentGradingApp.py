import tkinter as tk

largeFont = ("Verdana", 12)

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

        teacherButton = tk.Button(self, text = 'Teacher')
        teacherButton.grid(row = 0, column = 0, sticky = 'nesw')

        studentButton = tk.Button(self, text = 'Student')
        studentButton.grid(row = 0, column = 1, sticky = 'nesw')


app = backEnd() # equivilant of root = Tk (since backEnd() inherits from Tk)
app.state('zoomed') # makes window fullscreen
app.mainloop()