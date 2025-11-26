from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dotenv import dotenv_values
import mysql.connector

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

tree = ttk.Treeview(window2, columns=("ID", "Machine ID", "Item Name", "Stock"), show="headings")

tree2 = ttk.Treeview(window3, columns=("ID", "Location", "Status"), show="headings")

machineStatus = ["NONE", "FULL","HALF", "LOW", "EMPTY", "OFFLINE"]

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
    tree.heading("ID", text="ID")
    tree.heading("Machine ID", text="Machine ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Stock", text="Stock")
    tree.column("ID", width=50, anchor="center")
    tree.column("Machine ID", width=80)
    tree.column("Item Name", width=200)
    tree.column("Stock", width=60)
    tree.place(x=350, y=30, width=400, height=200)

    txt_machineID = Entry(window2, width=25)
    txt_machineID.place(x=155, y=35)
    machineID = Label(window2, text="Enter vending machine ID")
    machineID.place(x=10, y=35)

    txt_Item = Entry(window2, width=25)
    txt_Item.place(x=155, y=65)
    Item = Label(window2, text="Enter item")
    Item.place(x=10, y=65)

    txt_itemAmount = Entry(window2, width=25)
    txt_itemAmount.place(x=155, y=95)
    itemAmount = Label(window2, text="Enter amount of item")
    itemAmount.place(x=10, y=95)

    txt_ItemID = Entry(window2, width=25)
    txt_ItemID.place(x=155, y=125)
    ItemID = Label(window2, text="Enter item ID (for delete)")
    ItemID.place(x=10, y=125)


    lbl = Label(window2, text="Vending Machine management", font="Areial")
    lbl.place(x=0, y=0)

    InsertButton = Button(window2, text="Insert item", command=lambda: insertItem(txt_Item, txt_machineID, txt_itemAmount))
    InsertButton.place(x=10, y=165)

    GetButton = Button(window2, text="Get ID", command=lambda: getitem(txt_ItemID, txt_machineID, txt_Item))
    GetButton.place(x=10, y=195)

    DeleteButton = Button(window2, text="Delete by item ID", command=lambda: deleteItem(txt_ItemID))
    DeleteButton.place(x=10, y=225)

    UpdateButton = Button(window2, text="Update", command=lambda: updateValues(txt_machineID, None, None, txt_Item, txt_itemAmount))
    UpdateButton.place(x=10, y=255)

    MenuButton = Button(window2, text="Menu", command=showmenu)
    MenuButton.place(x=10, y=305)

def menu3Widgets():
    tree2.heading("ID", text="ID")
    tree2.heading("Location", text="Location")
    tree2.heading("Status", text="Status")
    tree2.column("ID", width=60, anchor="center")
    tree2.column("Location", width=150)
    tree2.column("Status", width=80)
    tree2.place(x=350, y=30, width=300, height=200)

    txt_machineID = Entry(window3, width=25)
    txt_machineID.place(x=80, y=35)
    machineID = Label(window3, text="Enter ID")
    machineID.place(x=10, y=35)

    txt_location = Entry(window3, width=25)
    txt_location.place(x=80, y=65)
    location = Label(window3, text="Enter City")
    location.place(x=10, y=65)
    
    machineStatusVar = StringVar(window3)
    machineStatusVar.set(machineStatus[0])
    machineStatusMenu = OptionMenu(window3, machineStatusVar, *machineStatus)
    machineStatusMenu.place(x=155, y=95)
    status = Label(window3, text="Enter the machine status")
    status.place(x=10, y=95)

    InsertButton = Button(window3, text="Insert Machine", command=lambda: insertMachine(txt_machineID, txt_location, machineStatusVar))
    InsertButton.place(x=10, y=135)

    GetButton = Button(window3, text="Get Machine", command=lambda: getValues(txt_machineID, txt_location, machineStatusVar))
    GetButton.place(x=10, y=165)

    DeleteButton = Button(
    window3, 
    text="Remove Machine", 
    command=lambda: delete_Vending(txt_machineID))

    DeleteButton.place(x=10, y=195)

    UpdateButton = Button(window3, text="Update Information", command=lambda: updateValues(txt_machineID, txt_location, machineStatusVar, None, None))
    UpdateButton.place(x=10, y=225)

    MenuButton = Button(window3, text="Menu", command=showmenu)
    MenuButton.place(x=10, y=275)   


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
    MenuButton.place(x=15, y=225)



def showmenu():
    window2.withdraw()
    window3.withdraw()
    window4.withdraw()
    window.deiconify()

def showmenu2():
    window.withdraw()
    window3.withdraw()
    window4.withdraw()
    window2.deiconify()

def showmenu3():
    window.withdraw()
    window2.withdraw()
    window4.withdraw()
    window3.deiconify()

def showmenu4():
    window.withdraw()
    window2.withdraw()
    window4.withdraw()
    window4.deiconify()
#endregion

#region Insert Funtion
def insertMachine(machineID, machineLocation, status):
    machineid = machineID.get().strip()
    machinelocation = machineLocation.get().strip()
    Status = status.get().strip()
    if machinelocation == "" or machineid == "" or Status == machineStatus[5]:
        messagebox.showinfo("Insert Status", "location and status required")
    else: 
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObject = conn.cursor()
        cursorObject.execute("INSERT INTO vending_machines (location, status) VALUES (%s, %s)", (machinelocation, Status))
        conn.commit()
        cursorObject.close()
        messagebox.showinfo("insert status", "inserted machine into database")
        conn.close()


def insertItem(itemID, machineID, amount):
    itemid = itemID.get().strip()
    machineid = machineID.get().strip()
    Amount = amount.get().strip()
    if itemid == "" or machineid == "" or Amount == "":
        messagebox.showinfo("Insert Status", "All fields required")
    else:
        try:
            Amount = int(Amount)  # Make sure amount is a number
        except ValueError:
            return messagebox.showerror("Insert Error", "Amount must be a number")

    conn = mysql.connector.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"]
    )
    cursor = conn.cursor()

    # Insert item into the items table
    cursor.execute(
        "INSERT INTO items (item_name, quantity, vending_machine_id) VALUES (%s, %s, %s)",
        (itemid, Amount, machineid)
    )
    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Insert Status", f"Inserted {Amount} of {itemid} into machine {machineid}")

    
    if itemid == "" or machineid == "" or Amount == "":
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
#endregion

#region Get Funtion
def getValues(machineid, machinelocation, status):
    machineID = machineid.get()
    machineLocation = machinelocation.get()
    machinestatus = status.get()
    if machineID == "" and machineLocation == "" and machinestatus == machineStatus[5]:
        messagebox.showinfo("Update Status", "Failed: Must put machine id")
    else:
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObjeckt = conn.cursor()

        params = []
        condition = []

        if machineID.strip():
            condition.append("id=%s")
            params.append(machineID.strip())
        if machineLocation.strip():
            condition.append("location=%s")
            params.append(machineLocation.strip())
        if machinestatus.strip():
            condition.append("status=%s")
            params.append(machinestatus.strip())

        query = "SELECT * FROM vending_machines"
        if condition:
            query += " WHERE " + " AND ".join(condition)

        cursorObjeckt.execute(query, tuple(params))
        
        for item in tree2.get_children():
            tree2.delete(item)

        rows = cursorObjeckt.fetchall()
        
        
        for row in rows:
            tree2.insert("", "end", values=row)
        
        cursorObjeckt.close()
        conn.close()

def getitem(itemID, machineID, itemName):
    itemid = itemID.get()
    machineid = machineID.get()
    itemname = itemName.get()

    if itemid == "" and machineid == "" and itemname == "":
        messagebox.showinfo("Get Status", "Atleast one field required to get values")
    else:
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObjeckt = conn.cursor()

        params = []
        conditions = []

        if itemid.strip():
            conditions.append("id=%s")
            params.append(itemid.strip())
        if machineid.strip():
            conditions.append("vending_machine_id=%s")
            params.append(machineid.strip())
        if itemname.strip():
            conditions.append("item_name=%s")
            params.append(itemname.strip())
        
        query = "SELECT * FROM items"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursorObjeckt.execute(query, tuple(params))

        for item in tree.get_children():
            tree.delete(item)

        rows = cursorObjeckt.fetchall()
        
        for row in rows:
            tree.insert("", "end", values=row)
        
        cursorObjeckt.close()
        conn.close()


#endregion

#region Update Funtion
def updateValues(machineid, machinelocation, status, machineitem, itemamount):
    machineID = machineid.get()
    if machineID == "":
        messagebox.showinfo("Update Status", "Failed: Must put machine id")
    else:
        try:
            machineidTry = machineid.get()
            machineidTry = int(machineidTry)
            
        except ValueError:
            messagebox.showinfo("Update Status", "Failed: ID must be a number")
            return
        try:
            itemamountTry = itemamount.get()
            itemamountTry = int(itemamountTry)
        except ValueError:
            messagebox.showinfo("Update Status", "Failed: Item Amount must be a number")
            return
        
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObjekt = conn.cursor()

        allowed_columns = {
            "item_name": "item_name=%s",
            "quantity": "quantity=%s",
            "status": "status=%s",
            "location": "location=%s"
        }
        
        machineLocation = machinelocation.get() if machinelocation else None
        machinestatus = status.get() if status else None
        machineItem = machineitem.get() if machineitem else None
        itemAmount = itemamount.get() if itemamount else None

        if not (machineLocation or machinestatus or machineItem or itemAmount):
            messagebox.showinfo("Fetch status", "Need atleast one line filled")
            return

        if machinelocation or status:
            sets = []
            prams = []
            if machinelocation:
                sets.append(allowed_columns["location"])
                prams.append(machineLocation)
            if status:
                sets.append(allowed_columns["status"])
                prams.append(machinestatus)

            prams.append(machineID)
            query = "UPDATE vending_machines SET " + ", ".join(sets) + " WHERE vending_machines_id=%s"

            cursorObjekt.execute(query, tuple(prams))
            messagebox.showinfo("Update Status", "Updated items")

        if machineitem or itemamount is not None:
            sets = []
            prams = []
            if machineitem:
                sets.append(allowed_columns["item_name"])
                prams.append(machineItem)
            if itemamount is not None:
                sets.append(allowed_columns["quantity"])
                prams.append(itemAmount)

            prams.append(machineID)

            query = "UPDATE items SET " + ", ".join(sets) + " WHERE vending_machines_id=%s"

            cursorObjekt.execute(query, tuple(prams))
            messagebox.showinfo("Update Status", "Updated items")

        conn.commit()
        cursor.close()
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

def deleteItem(itemIDField):
    item_id = itemIDField.get().strip()
    
    if not item_id:
        return messagebox.showerror("Delete Error", "Please enter an item ID")
    
    try:
        item_id = int(item_id)
    except ValueError:
        return messagebox.showerror("Delete Error", "Item ID must be a number")
    
    try:
        conn = mysql.connector.connect(
            host=config["DB_HOST"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            database=config["DB_NAME"]
        )
        cursor = conn.cursor()

        # Hent item info før sletning
        cursor.execute("SELECT item_name, vending_machine_id FROM items WHERE id=%s", (item_id,))
        result = cursor.fetchone()
        
        if not result:
            return messagebox.showerror("Delete Error", f"Item with ID {item_id} does not exist.")
        
        item_name, machine_id = result
        
        if not messagebox.askyesno("Confirm Delete", f"Delete '{item_name}' (ID: {item_id}) from machine {machine_id}?"):
            return
        
        # Slet den specifikke item baseret på ID
        cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
        conn.commit()

        messagebox.showinfo("Delete Status", f"Item '{item_name}' (ID: {item_id}) deleted successfully")
        
        # Ryd feltet
        itemIDField.delete(0, END)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()   
        

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
