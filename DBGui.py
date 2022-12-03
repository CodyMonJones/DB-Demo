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

def set_tabs():
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

def start_connection():
    #Setting the connection to the db file "carRental.db"
    #try except to indicate error has occured when connecting
    try:
        conn = sqlite3.connect("carRental.db")
    except Error as error:
        print(error)

    #Cursor to grab the information we need and create our DB
    cur = conn.cursor()


#Execute our window
set_tabs()
start_connection()
root.mainloop()
