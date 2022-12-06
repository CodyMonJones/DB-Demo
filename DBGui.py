from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
from datetime import datetime

# Set the gui title and window
root = Tk()
root.title("Car Rental GUI")
root.geometry("1000x1000")
workingDB = "carRental.db"


# Tabbed window for different options
tab_window = ttk.Notebook(root)


# Setting a tab frame for each CSV file for basic command testing
query_tab1 = ttk.Frame(tab_window)
query_tab2 = ttk.Frame(tab_window)
query_tab3 = ttk.Frame(tab_window)
query_tab4 = ttk.Frame(tab_window)
query_tab5 = ttk.Frame(tab_window)


# Adding the tabs to the GUI window
tab_window.add(query_tab1, text='Query 1')
tab_window.add(query_tab2, text='Query 2')
tab_window.add(query_tab3, text='Query 3')
tab_window.add(query_tab4, text='Query 4')
tab_window.add(query_tab5, text='Query 5')
tab_window.pack(expand=1, fill="both")


#Tree view for displaying customer data
tree_view1 = ttk.Treeview(query_tab1, selectmode='browse')
tree_view1.grid(row=5, column=1, padx=20, pady=20)
tree_view1["columns"] = ("1", "2", "3")
tree_view1["show"] = 'headings'
tree_view1.column("1", width=100, anchor='w')
tree_view1.column("2", width=100, anchor='w')
tree_view1.column("3", width=200, anchor='w')


#Treeview headings for customer
tree_view1.heading("1", text="Customer ID")
tree_view1.heading("2", text="Name")
tree_view1.heading("3", text="Phone Number")


#Tree view for displaying vehicle data
tree_view2 = ttk.Treeview(query_tab2, selectmode='browse')
tree_view2.grid(row=11, column=0, padx=20, pady=20)
tree_view2["columns"] = ("1", "2", "3", "4", "5")
tree_view2["show"] = 'headings'
tree_view2.column("1", width=200, anchor='w')
tree_view2.column("2", width=200, anchor='w')
tree_view2.column("3", width=100, anchor='w')
tree_view2.column("4", width=100, anchor='w')
tree_view2.column("5", width=100, anchor='w')


#treeview headings
tree_view2.heading("1", text="Vehicle ID")
tree_view2.heading("2", text="Description")
tree_view2.heading("3", text="Year")
tree_view2.heading("4", text="Type")
tree_view2.heading("5", text="Category")

#tree_view for showing available cars for Query 3
tree_view3 = ttk.Treeview(query_tab3, selectmode='browse')
tree_view3.grid(row=11, column=0, padx=5, pady=20)
tree_view3["columns"] = ("1", "2", "3", "4", "5")
tree_view3["show"] = 'headings'
tree_view3.column("1", width=200, anchor='w')
tree_view3.column("2", width=200, anchor='w')
tree_view3.column("3", width=100, anchor='w')
tree_view3.column("4", width=100, anchor='w')
tree_view3.column("5", width=100, anchor='w')

#treeview headings for showing available cars for Query 3 
tree_view3.heading("1", text="Vehicle ID")
tree_view3.heading("2", text="Description")
tree_view3.heading("3", text="Year")
tree_view3.heading("4", text="Weekly")
tree_view3.heading("5", text="Daily")

startDate = "XXXX-XX-XX"
endDate = "XXXX-XX-XX"
type_User_input = 0
category_User_input = 0
today = datetime.today().strftime('%Y-%m-%d')
total_amount = 0

format = '%Y-%m-%d'

def submit_rental_data():
    try:
        conn = sqlite3.connect(workingDB)
    except Error as error:
        print(error)

    cur = conn.cursor()
    rental_records = cur.execute("""
    SELECT DISTINCT VEHICLE.VehicleID AS VIN, Description, Year, Weekly, Daily
    FROM VEHICLE, RENTAL, RATE
    WHERE VEHICLE.VehicleID = RENTAL.VehicleID 
    AND VEHICLE.Type = :type 
    AND VEHICLE.Category = :cat 
    AND RATE.Type = VEHICLE.Type
    AND RATE.Category = VEHICLE.Category
    AND VEHICLE.VehicleID - 
        (SELECT VEHICLE.VehicleID 
        FROM VEHICLE, RENTAL 
        WHERE VEHICLE.VehicleID = RENTAL.VehicleID 
        AND VEHICLE.Type = :type AND VEHICLE.Category = :cat 
        AND ((StartDate >= :startD and StartDate <= :endD) 
            OR (ReturnDate <= :endD AND ReturnDate >= :startD) 
            OR (StartDate <= :startD AND ReturnDate >= :endD ))) 
    GROUP BY VEHICLE.VehicleID""",
    {
        'type'  : type_in.get(),
        'cat'   : cat_in.get(),
        'startD': startD.get(),
        'endD'  : endD.get()
    })
    startDate = startD.get()
    endDate = endD.get()
    type_User_input = type_in.get()
    category_User_input = cat_in.get()
    
    global car_count
    car_count = 0
    for vehicle in rental_records:
            tree_view3.insert("", index='end', iid=car_count, text=vehicle[0], values=(vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4])) 
            car_count += 1

    conn.commit()
    conn.close()

def add_rental():
    try:
        conn = sqlite3.connect(workingDB)
    except Error as error:
        print(error)
    
    cur = conn.cursor()
    weeklyDailyRates = cur.execute("""
        SELECT Daily, Weekly
        FROM RATE
        WHERE Type = :type
        AND Category = :cat""",
        {
            'type'  : type_in.get(),
            'cat'   : cat_in.get()
        })
    singleTuple = weeklyDailyRates.fetchall()[0]
    if(weekDaily_in.get() == "1"):
        total_amount = int(singleTuple[0]) * int(quant_in.get()) * int(numDayWeek_in.get())
    else:
        total_amount = int(singleTuple[1]) * int(quant_in.get()) * int(numDayWeek_in.get())

    tempNL = ""
    if (payNL.get() == '1'):
        tempNL = today
    else:
        tempNL = "NULL"

    
    rental_records = cur.execute("INSERT INTO RENTAL VALUES (:custID, :vin, :startD, :orderD, :rentType, :quant, :returnD, :amount, :nowLater, 0)",
    {
        'custID'    : custID.get(),
        'vin'       : vid_in.get(),
        'startD'    : startD.get(),
        'orderD'    : today,
        'rentType'  : weekDaily_in.get(),
        'quant'     : quant_in.get(),
        'returnD'   : endD.get(),
        'nowLater'  : tempNL,
        'amount'    : total_amount
    })

    conn.commit()
    conn.close()

#setting treeview columns
def submit_vehicle():
    try:
        conn = sqlite3.connect(workingDB)
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
    tree_view2.insert("", index='end', iid=vehicle_count, text="", values=(vid.get(), description.get(), year.get(), carType.get(), category.get()))
    #clears boxes once input is complete            
    vid.delete(0, END)
    description.delete(0, END)
    year.delete(0, END)
    carType.delete(0, END)
    category.delete(0, END)

    conn.commit()
    conn.close()


def add_customer():
    try:
        conn = sqlite3.connect(workingDB)
    except Error as error:
        print(error)

    cur = conn.cursor()
    cur.execute("INSERT INTO CUSTOMER(name, phone) VALUES (:name, :phone)",
    {   
        'name': customer_name.get(),
        'phone': customer_phone.get()
    })
    tree_view1.insert("", index='end', iid=customer_count, text="", values=(customer_count, customer_name.get(), customer_phone.get()))
    customer_name.delete(0, END)
    customer_phone.delete(0,END)

    conn.commit()
    conn.close()


def show_customer_data():
    try:
        conn = sqlite3.connect(workingDB)
    except Error as error:
        print(error)

    cur = conn.cursor()
    customer_records = cur.execute("SELECT * FROM CUSTOMER")

    global customer_count
    customer_count = 201
    for customer in customer_records:
        tree_view1.insert("", index='end', iid=customer_count, text=customer[0], values=(customer[0], customer[1], customer[2]))
        customer_count += 1

    conn.commit()
    conn.close()


def show_vehicle_data():
    try:
        conn = sqlite3.connect(workingDB)
    except Error as error:
        print(error)

    cur = conn.cursor()
    vehicle_records = cur.execute("SELECT * FROM VEHICLE")

    global vehicle_count
    vehicle_count = 0
    for vehicle in vehicle_records:
            tree_view2.insert("", index='end', iid=vehicle_count, text=vehicle[0], values=(vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4])) 
            vehicle_count += 1  

    conn.commit()
    conn.close()

#-----------------------------------------------------------------------------------------------------------------------
# Vehicle information to add to DB
# query 2 entry boxes and buttons
#-----------------------------------------------------------------------------------------------------------------------
vid_label = Label(query_tab2, text='Vehicle ID: ')
vid_label.grid(row=0, column=0, sticky=W)

vid = Entry(query_tab2, width=30)
vid.grid(row=1, column=0, sticky=W, pady=(0, 10))

description_label = Label(query_tab2, text='Description: ')
description_label.grid(row=2, column=0, sticky=W)

description = Entry(query_tab2, width=30)
description.grid(row=3, column=0, sticky=W, pady=(0, 10))


year_label = Label(query_tab2, text='Year: ')
year_label.grid(row=4, column=0, sticky=W)

year = Entry(query_tab2, width=30)
year.grid(row=5, column=0, sticky=W, pady=(0, 10))


car_label = Label(query_tab2, text='Type: ')
car_label.grid(row=6, column=0, sticky=W)

carType = Entry(query_tab2, width=30)
carType.grid(row=7, column=0, sticky=W, pady=(0, 10))


category_label = Label(query_tab2, text='Category: ')
category_label.grid(row=8, column=0, sticky=W)

category = Entry(query_tab2, width=30)
category.grid(row=9, column=0, sticky=W, pady=(0, 10))

enterVehicle = Button(query_tab2, text="Submit car", command=submit_vehicle)
enterVehicle.grid(row=10, column=0, columnspan=2, padx=100, pady=10, sticky=W)
#-----------------------------------------------------------------------------------------------------------------------
#Adding Customer Tab
#-----------------------------------------------------------------------------------------------------------------------
cust_name_label = Label(query_tab1, text='Name: ')
cust_name_label.grid(row=0, column=0, sticky=W)


customer_name = Entry(query_tab1, width=30)
customer_name.grid(row=1, column=0, pady=(0,10))
customer_name.insert(0, "J. Doe")

cust_phone_label = Label(query_tab1, text='Phone Number: ')
cust_phone_label.grid(row=2, column=0, sticky=W)

customer_phone = Entry(query_tab1, width=30)
customer_phone.grid(row=3, column=0, pady=(0,10))
customer_phone.insert(0, "(000) 000-0000")

enter_customer = Button(query_tab1, text="Add Customer", command=add_customer)
enter_customer.grid(row=4, column=0, columnspan=2, padx=100, pady=10, sticky=W)
#-----------------------------------------------------------------------------------------------------------------------
#Show available cars buttons/labels for Query 3
#-----------------------------------------------------------------------------------------------------------------------
Start_Date = Label(query_tab3, text='Start Date: ')
Start_Date.grid(row=0, column=0, sticky=W)

startD = Entry(query_tab3, width=30)
startD.grid(row=1, column=0, sticky=W, pady=(0, 10))
startD.insert(0, "YYYY-MM-DD")

End_Date = Label(query_tab3, text='End Date: ')
End_Date.grid(row=2, column=0, sticky=W)

endD = Entry(query_tab3, width=30)
endD.grid(row=3, column=0, sticky=W, pady=(0, 10))
endD.insert(0, "YYYY-MM-DD")

type_rental = Label(query_tab3, text='Type: ')
type_rental.grid(row=4, column=0, sticky=W)

type_in = Entry(query_tab3, width=30)
type_in.grid(row=5, column=0, sticky=W, pady=(0, 10))

Category_rental = Label(query_tab3, text='Category: ')
Category_rental.grid(row=6, column=0, sticky=W)

cat_in = Entry(query_tab3, width=30)
cat_in.grid(row=7, column=0, sticky=W, pady=(0, 10))

list_cars = Button(query_tab3, text="Show available cars", command=submit_rental_data)
list_cars.grid(row=8, column=0, columnspan=2, padx=100, pady=10, sticky=W)
#-----------------------------------------------------------------------------------------------------------------------
#Add rental buttons/labels for Query 3
#-----------------------------------------------------------------------------------------------------------------------
Vehicle_id = Label(query_tab3, text='Vehicle ID: ')
Vehicle_id.grid(row=12, column=0, sticky=W, pady=(0, 10))

vid_in = Entry(query_tab3, width=30)
vid_in.grid(row=13, column=0, sticky=W, pady=(0, 10))

Cust_ID = Label(query_tab3, text='Your Customer ID: ')
Cust_ID.grid(row=14, column=0, sticky=W, pady=(0, 10))

custID = Entry(query_tab3, width=30)
custID.grid(row=15, column=0, sticky=W, pady=(0, 10))

Pay_now_later = Label(query_tab3, text='Will you pay now or later? ')
Pay_now_later.grid(row=16, column=0, sticky=W, pady=(0, 10))

payNL = Entry(query_tab3, width=30)
payNL.grid(row=17, column=0, sticky=W, pady=(0, 10))
payNL.insert(0, "0 = Later : 1 = Now")

Quantity = Label(query_tab3, text='Number of Cars you want to rent: ')
Quantity.grid(row=18, column=0, sticky=W, pady=(0, 10))

quant_in = Entry(query_tab3, width=30)
quant_in.grid(row=19, column=0, sticky=W, pady=(0, 10))

WeeklyDaily = Label(query_tab3, text='Weekly or Daily rates: ')
WeeklyDaily.grid(row=20, column=0, sticky=W, pady=(0, 10))

weekDaily_in = Entry(query_tab3, width=30)
weekDaily_in.grid(row=21, column=0, sticky=W, pady=(0, 10))
weekDaily_in.insert(0, "1 = Daily, 7 = Weekly")

NumDaysOrWeeks = Label(query_tab3, text='Number of days or weeks')
NumDaysOrWeeks.grid(row=22, column=0, sticky=W, pady=(0, 10))

numDayWeek_in = Entry(query_tab3, width=30)
numDayWeek_in.grid(row=23, column=0, sticky=W, pady=(0, 10))

enterRental = Button(query_tab3, text="Submit Rental Request", command=add_rental)
enterRental.grid(row=24, column=0, columnspan=2, padx=100, pady=10, sticky=W)
#-----------------------------------------------------------------------------------------------------------------------
# Execute our window
show_customer_data()
show_vehicle_data()
submit_rental_data()
root.mainloop()
