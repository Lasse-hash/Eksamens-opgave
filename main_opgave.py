from tkinter import *
from tkinter import messagebox
from dotenv import dotenv_values
import mysql.connector
from datetime import datetime

window = Tk()

window.geometry("350x150")

config = dotenv_values(r".env")

window.title("Vending Machine management")

window2 = Toplevel(window)
window2.geometry("940x800")
window2.withdraw()

window3 = Toplevel(window)
window3.geometry("940x800")
window3.withdraw()

window4 = Toplevel(window)
window4.geometry("940x800")
window4.withdraw()

machineStatus = ["FULL","HALF", "LOW", "EMPTY", "OFFLINE"]

options = ["NONE", "Refill machine", "Report issue", "Request maintenance"]

#region Widgets
def menuwidgets():
    placemachineButton = Button(window, text="Place a Vending Machine", command=showmenu3)
    placemachineButton.place(x=20, y=40)

    fillmachineButton = Button(window, text="Fill Vending Machine", command=showmenu2)
    fillmachineButton.place(x=190, y=40)

    KontaktmedarbejderButton = Button(window, text="Contact Employee", command=showmenu4)
    KontaktmedarbejderButton.place(x=120, y=80)

def menu2Widgets():
    txt_machineID = Entry(window2, width=25)
    txt_machineID.place(x=155, y=35)
    machineID = Label(window2, text="Enter vending machine ID")
    machineID.place(x=10, y=35)

    txt_Item = Entry(window2, width=25)
    txt_Item.place(x=155, y=75)
    Item = Label(window2, text="Enter item")
    Item.place(x=10, y=75)

    txt_itemAmount = Entry(window2, width=25)
    txt_itemAmount.place(x=155, y=105)
    itemAmount = Label(window2, text="Enter amount of item")
    itemAmount.place(x=10, y=105)

    txt_priceAmount = Entry(window2, width=25)
    txt_priceAmount.place(x=155, y=135)
    priceAmount = Label(window2, text="Enter price amount")
    priceAmount.place(x=10, y=135)

    lbl = Label(window2, text="Vending Machine management", font="Areial")
    lbl.place(x=0, y=0)

    InsertButton = Button(window2, text="Insert item", command=lambda: insertItem(txt_Item, txt_machineID, txt_itemAmount, txt_priceAmount))
    InsertButton.place(x=15, y=165)

    GetButton = Button(window2, text="Get ID", command=getValues)
    GetButton.place(x=90, y=165)

    DeleteButton = Button(window2, text="Delete", command=deleteThings)
    DeleteButton.place(x=140, y=165)

    UpdateButton = Button(window2, text="Update", command=lambda: updateValues(txt_machineID, None, None, txt_Item, txt_itemAmount))
    UpdateButton.place(x=195, y=165)

    MenuButton = Button(window2, text="Menu", command=showmenu)
    MenuButton.place(x=150, y=255)

    Gettxt = Text(window2, width=50)
    Gettxt.place(x=350, y=30)

def menu3Widgets():
    txt_machineID = Entry(window3, width=25)
    txt_machineID.place(x=155, y=35)
    machineID = Label(window3, text="Enter vending machine ID")
    machineID.place(x=10, y=35)

    txt_location = Entry(window3, width=25)
    txt_location.place(x=155, y=75)
    location = Label(window3, text="Enter City")
    location.place(x=10, y=75)

    machineStatusVar = StringVar(window3)
    machineStatusVar.set(machineStatus[0])
    machineStatusMenu = OptionMenu(window3, machineStatusVar, *machineStatus)
    machineStatusMenu.place(x=155, y=105)
    status = Label(window3, text="Enter the machine status")
    status.place(x=10, y=105)

    InsertButton = Button(window3, text="Insert Machine", command=lambda: insertMachine(txt_machineID, txt_location, machineStatusVar))
    InsertButton.place(x=25, y=145)

    GetButton = Button(window3, text="Get Machine", command=getValues)
    GetButton.place(x=25, y=185)

    DeleteButton = Button(
    window3, 
    text="Delete Machine", 
    command=lambda: delete_Vending(txt_machineID)
)

    DeleteButton.place(x=140, y=145)

    UpdateButton = Button(window3, text="Update Information", command=lambda: updateValues(txt_machineID, txt_location, machineStatusVar, None, None))
    UpdateButton.place(x=140, y=185)

    MenuButton = Button(window3, text="Menu", command=showmenu)
    MenuButton.place(x=150, y=250)

    Gettxt = Text(window3, width=50)
    Gettxt.place(x=350, y=30)

def menu4Widgets():
    txt_location = Entry(window4, width=25)
    txt_location.place(x=155, y=35) 
    location = Label(window4, text="Enter City")
    location.place(x=10, y=75)

    txt_machineID = Entry(window4, width=25)
    txt_machineID.place(x=155, y=75)
    machineID = Label(window4, text="Enter vending machine ID")
    machineID.place(x=10, y=35)

    variable = StringVar(window4)
    variable.set(options[0])
    optionsMenu = OptionMenu(window4, variable, *options)
    optionsMenu.place(x=155, y=105)
    optionLabel = Label(window4, text="Select an option")
    optionLabel.place(x=10, y=105)

    txt_employeeMessage = Entry(window4, width=25)
    txt_employeeMessage.place(x=155, y=145) 
    employeeMessage = Label(window4, text="Employee name")
    employeeMessage.place(x=10, y=145)  

    def sendReport():
        employee = txt_employeeMessage.get().strip()
        if not employee.replace(" ", "").isalpha():  
            messagebox.showerror("Input Error", "Employee name must contain only letters")
            return

        
        messagebox.showinfo(
            "Report sent",
            f"Your message '{variable.get()}' has been sent to {employee} at {txt_machineID.get()} for machine ID {txt_location.get()}"
        )

    InsertButton = Button(window4, text="Send Report", command=sendReport)
    InsertButton.place(x=15, y=185)

    MenuButton = Button(window4, text="Menu", command=showmenu)
    MenuButton.place(x=120, y=185)



def showmenu():
    window2.withdraw()
    window3.withdraw()
    window4.withdraw()
    window.deiconify()

def showmenu2():
    window.withdraw()
    window3.withdraw()
    window2.deiconify()

def showmenu3():
    window.withdraw()
    window2.withdraw()
    window3.deiconify()

def showmenu4():
    window.withdraw()
    window2.withdraw()
    window4.deiconify()
#endregion

#region Insert Funtion
def insertMachine(machineID, machineLocation, status):
    machineid = machineID.get()
    machinelocation = machineLocation.get()
    Status = status.get()
    if machinelocation == "" or machineid == "" or Status not in machineStatus:
        messagebox.showinfo("insert status", "all fields required")
    else: 
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObject = conn.cursor()
        cursorObject.execute("INSERT INTO vending_machines (location, status, last_refill) VALUES (%s, %s, %s)", (machinelocation, Status, timestamp))
        conn.commit()
        cursorObject.close()
        messagebox.showinfo("insert status", "inserted machine into database")
        conn.close()


def insertItem(itemID, machineID, amount, priceAmount):
    itemid = itemID.get().strip()
    machineid = machineID.get().strip()
    Amount = amount.get().strip()
    price = priceAmount.get().strip()

    
    if itemid == "" or machineid == "" or Amount == "" or price == "":
        messagebox.showerror("Insert Error", "All fields are required")
        return

    
    if not itemid.replace(" ", "").isalpha():
        messagebox.showerror("Insert Error", "Item name must contain only letters")
        return

   
    try:
        Amount = int(Amount)
    except ValueError:
        messagebox.showerror("Insert Error", "Amount must be a number")
        return

    
    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Insert Error", "Price must be a number")
        return

    
    messagebox.showinfo("Insert Status", f"Inserted {Amount} of {itemid} into machine {machineid} at price {price}")


#endregion

#region Get Funtion
def getValues():
    pass
#endregion

#region Update Funtion
def updateValues(machineid, machinelocation, status, machineitem, itemamount):
    machineID = machineid.get()
    if machineID == "":
        messagebox.showinfo("Update Status", "Failed: Must put machine id")
    else:
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObjekt = conn.cursor()

        
        if machinelocation is not None:
            machineLocation = machinelocation.get()
        else:
            machineItem = None
       
        if status is not None:
            machinestatus = status.get()
        else:
            machinestatus = None
        
        if machineitem is not None:
            machineItem = machineitem.get()
        else:
            machineItem = None

        if itemamount is not None:
            itemAmuont = itemamount.get()
        else:
            itemAmuont = None

        if not (machineLocation or machinestatus or machineItem or itemAmuont):
            messagebox.showinfo("Fetch status", "Need atleast one line filled")
            return

    if machinelocation or status:
        sets = []
        prams = []
        if machinelocation:
            sets.append("location=%s")
            prams.append(machineLocation)
        if status:
            sets.append("status=%s")
            prams.append(machinestatus)
        prams.append(machineID)
        cursorObjekt.execute(f"UPDATE vending_machines SET {', '.join(sets)} WHERE id=%s", tuple(prams))
        messagebox.showinfo("Update Status", "Updated items")

    if machineitem or itemamount is not None:
        sets = []
        prams = []
        if machineitem:
            sets.append("item_name=%s")
            prams.append(machineItem)
        if itemamount is not None:
            sets.append("quantity=%s")
            prams.append(itemAmuont)
        prams.append(machineID)  # assuming vending_machine_id = machineID
        cursorObjekt.execute(f"UPDATE items SET {', '.join(sets)} WHERE vending_machine_id=%s", tuple(prams))
        messagebox.showinfo("Update Status", "Updated items")

    conn.commit()
    conn.close()



        
#endregion

#region Delete Funtion
def delete_Vending(txt_machineID):
    machineID = txt_machineID.get().strip()
    if not machineID:
        return messagebox.showerror("Delete Error", "Please enter a machine ID")

    try:
        conn = mysql.connector.connect(
            host=config["DB_HOST"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            database=config["DB_NAME"]
        )
        cursor = conn.cursor()

        # Check if machine exists
        cursor.execute("SELECT id FROM vending_machines WHERE id=%s", (machineID,))
        if not cursor.fetchone():
            return messagebox.showerror("Delete Error", f"Machine {machineID} does not exist.")

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Delete machine {machineID}?"):
            return

        # Delete items and machine
        cursor.execute("DELETE FROM items WHERE vending_machine_id=%s", (machineID,))
        cursor.execute("DELETE FROM vending_machines WHERE id=%s", (machineID,))
        conn.commit()

        messagebox.showinfo("Delete Status", f"Vending machine {machineID} deleted successfully")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

def deleteItem(itemID):
    itemID = itemID.get().strip()
    if not itemID:
        return messagebox.showerror("Delete Error", "Please enter an item ID")
    
    try:
        conn = mysql.connector.connect(
            host=config["DB_HOST"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            database=config["DB_NAME"]
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM items WHERE id=%s", (itemID,))
        if not cursor.fetchone():
            return messagebox.showerror("Delete Error", f"Item {itemID} does not exist.")
        
        if not messagebox.askyesno("Confirm Delete", f"Delete item {itemID}?"):
            return
        
        cursor.execute("DELETE FROM items WHERE id=%s", (itemID,))
        conn.commit()

        messagebox.showinfo("Delete Status", f"Item {itemID} deleted successfully")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()   
         


def deleteThings():
    pass



#endregion

#region Main
def main():

    
    menu2Widgets()
    menu3Widgets()
    menu4Widgets()
    menuwidgets()

    window.mainloop()
#endregion

if __name__ == "__main__":
    
    conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"])
    cursor = conn.cursor()
    
    sql_file = r"vending_machine_database.sql"
    with open(sql_file, "r") as f:
        sql_commands = f.read()
    
    for command in sql_commands.split(";"):
        cmd = command.strip()
        if cmd:
            cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()

    main()
