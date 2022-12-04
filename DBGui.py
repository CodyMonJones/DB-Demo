from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error

# Set the gui title and window
root = Tk()
root.title("Car Rental GUI")
root.geometry("400x400")

#Tabbed window for different options
tab_window = ttk.Notebook(root)

# Setting a tab frame for each CSV file for basic command testing
query_tab1 = ttk.Frame(tab_window)
query_tab2 = ttk.Frame(tab_window)
query_tab3 = ttk.Frame(tab_window)
query_tab4 = ttk.Frame(tab_window)

# Adding the tabs to the GUI window
tab_window.add(query_tab1, text='Query 1')
tab_window.add(query_tab2, text='Query 2')
tab_window.add(query_tab3, text='Query 3')
tab_window.add(query_tab4, text='Query 4')
tab_window.pack(expand= 1, fill="both")

def submit_vehicle():
    try:
        conn = sqlite3.connect("carRental.db")
    except Error as error:
        print(error)

    cur = conn.cursor()
    cur.execute("INSERT INTO VEHICLE VALUES (:vid, :description, :year, :type, :category)",
    {
        'vid': vid.get(),
        'description': description.get(),
        'year': year.get(),
        'type': carType.get(),
        'category': category.get()
    })


    conn.commit()
    conn.close()  

# Vehicle information to add to DB
#query 2 entry boxes and buttons
vid_label = Label(query_tab2, text = 'Vehicle ID: ')
vid_label.grid(row = 0, column  = 0)

vid = Entry(query_tab2, width = 30)
vid.grid(row = 0, column = 1, padx = 20)

description_label = Label(query_tab2, text = 'Description: ')
description_label.grid(row = 1, column  = 0)

description = Entry(query_tab2, width = 30)
description.grid(row = 1, column = 1)


year_label = Label(query_tab2, text = 'Year: ')
year_label.grid(row = 2, column = 0)

year = Entry(query_tab2, width = 30)
year.grid(row = 2, column = 1)


car_label = Label(query_tab2, text = 'Type: ')
car_label.grid(row = 3, column = 0)

carType = Entry(query_tab2, width = 30)
carType.grid(row = 3, column = 1)


category_label = Label(query_tab2, text = 'Category: ')
category_label.grid(row = 4, column = 0)

category = Entry(query_tab2, width = 30)
category.grid(row = 4, column = 1)

enterVehicle = Button(query_tab2, text = "Submit car", command = submit_vehicle)
enterVehicle.grid(row = 5, column = 0, columnspan = 2, padx = 10, pady = 10)      


def start_connection():
    #Setting the connection to the db file "carRental.db"
    #try except to indicate error has occured when connecting
    try:
        sqlite3.connect("carRental.db")
    except Error as error:
        print(error)


#Execute our window

start_connection()
root.mainloop()
