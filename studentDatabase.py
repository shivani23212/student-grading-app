import sqlite3

conn = sqlite3.connect('school.db') # connects to a database
                                    # (creates db if doesnt exist)
cursor = conn.cursor() # object that allows us to edit db
#--------------------------------------------------------------------
cursor.execute('DROP TABLE classes')
cursor.execute('DROP TABLE students')
cursor.execute('''CREATE TABLE IF NOT EXISTS classes
                ([Class Name] TEXT NOT NULL PRIMARY KEY,
                [Year Group] TEXT NOT NULL,
                [Max Size] INTEGER NOT NULL)''') # ignore 2nd and 3rd column

conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS students(
                [First Name] TEXT NOT NULL,
                Surname TEXT NOT NULL,
                Class TEXT NOT NULL,
                Autumn1 REAL,
                Autumn2 REAL,
                Spring1 REAL,
                Spring2 REAL,
                Summer1 REAL,
                Summer2 REAL,
                PRIMARY KEY ([First Name], Surname),
                FOREIGN KEY (Class) REFERENCES classes([Class Name])
                )''')
# add table for test results : first name, last name, autm1, autm2, spr1, spr2, sum1, sum2
# composite primary key: first and last name (also foreign key) -- or should i add this to the students table? 
conn.commit()
conn.close()