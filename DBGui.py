from tkinter import *
import sqlite3

# Set the gui title and window
root = Tk()
root.title("DB Gui")
root.geometry("400x400")

#Setting the connection to the db
conn = sqlite3.connect("")

#Cursor to grab the information we need and create our DB
cur = conn.cursor()
# cur.execute()
# cur.execute(''' ''')



#Execute our window
root.mainloop()