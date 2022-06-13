import sqlite3 as sl

def del_db():
   con = sl.connect('Data.db')
   cur= con.cursor()

   #Creating tables
   with open('docs\schema.sql') as f:
      con.executescript(f.read())

if __name__ == "__main__":
   del_db()