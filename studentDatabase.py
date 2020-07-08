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
                PRIMARY KEY ([First Name], Surname),
                FOREIGN KEY (Class) REFERENCES classes([Class Name])
                )''')
# add 
conn.commit()
conn.close()