from tkinter import *
from tkinter import ttk
import sqlite3

# Set the gui title and window

root = Tk()
root.title("Car Rental GUI")
root.geometry("400x400")

#Tabbed window for different options
tab_window = ttk.Notebook(root)

def set_tabs():
    # Setting a tab frame for each CSV file for basic command testing
    customer_tab = ttk.Frame(tab_window)
    rate_tab     = ttk.Frame(tab_window)
    rental_tab   = ttk.Frame(tab_window)
    vehicle_tab  = ttk.Frame(tab_window)    

    # Adding the tabs to the GUI window
    tab_window.add(customer_tab, text='Customers')
    tab_window.add(rate_tab,     text='Rates')
    tab_window.add(rental_tab,   text='Rentals')
    tab_window.add(vehicle_tab,  text='Vehicles')
    tab_window.pack(expand= 1, fill="both")

    #setting the tabs
    ttk.Label(customer_tab, text = "customer tab").grid(column = 0, row = 0, padx = 30, pady = 30)
    ttk.Label(rate_tab, text = "rate tab").grid(column = 0, row = 0, padx = 30, pady = 30)
    ttk.Label(rental_tab, text = "rental tab").grid(column = 0, row = 0, padx = 30, pady = 30)
    ttk.Label(vehicle_tab, text = "vehicle tab").grid(column = 0, row = 0, padx = 30, pady = 30)


def start_connection():
    #Setting the connection to the db file "carRental.db"
    conn = sqlite3.connect("carRental.db")

    #Cursor to grab the information we need and create our DB
    cur = conn.cursor()


#Execute our window
set_tabs()
start_connection()
root.mainloop()
