import sqlite3

conn = sqlite3.connect('school.db') # connects to a database
                                    # (creates db if doesnt exist)
cursor = conn.cursor() # object that allows us to edit db
#--------------------------------------------------------------------
cursor.execute('''CREATE TABLE IF NOT EXISTS classes
                (Name TEXT NOT NULL PRIMARY KEY,
                [Year Group] TEXT NOT NULL,
                [Max Size] INTEGER NOT NULL)''') # [] allows names with spaces

conn.commit()

conn.close()