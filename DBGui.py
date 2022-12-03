from tkinter import *
from tkinter import ttk
import sqlite3

# Set the gui title and window
root = Tk()
root.title("DB Gui")
root.geometry("400x400")

#Tabbed window for different options
tab_window = ttk.Notebook(root)

# Setting a tab frame for each CSV file for basic command testing
customer_tab = ttk.Frame(tab_window)
rate_tab     = ttk.Frame(tab_window)
rental_tab   = ttk.Frame(tab_window)
vehicle_tab  = ttk.Frame(tab_window)

# Adding the tabs to the GUI window
ttk.Label(customer_tab, Text='Customers')
ttk.Label(rate_tab,     Text='Rates')
ttk.Label(rental_tab,   Text='Rentals')
ttk.Label(vehicle_tab,  Text='Vehicles')

#Setting the connection to the db
conn = sqlite3.connect("")

#Cursor to grab the information we need and create our DB
cur = conn.cursor()
# cur.execute()
# cur.execute(''' ''')



#Execute our window
root.mainloop()