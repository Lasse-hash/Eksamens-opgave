from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dotenv import dotenv_values
import mysql.connector

# Her laver vi hovedvinduet til programmet, så man kan se det på skærmen.
window = Tk()

# Sætter størrelsen på hovedvinduet, så det ikke fylder hele skærmen.
window.geometry("350x150")

# Variabel der holder styr på om der allerede bliver vist en messagebox popup.
messageboxstate = False

# Her læses databaseoplysninger fra en .env fil
config = dotenv_values(r".env")

# Giver vinduet en overskrift øverst
window.title("Vending Machine management")

# Her laver vi flere ekstra skjulte vinduer, som vi bruger til menuer osv
window2 = Toplevel(window)
window2.geometry("940x800")
window2.withdraw() # skjuler vinduet

window3 = Toplevel(window)
window3.geometry("940x800")
window3.withdraw()

window4 = Toplevel(window)
window4.geometry("940x800")
window4.withdraw()

# Laver tabeller ligesom Excel/regneark til de to menu-vinduer
tree = ttk.Treeview(window2, columns=("ID", "Machine ID", "Item Name", "Stock"), show="headings")
tree2 = ttk.Treeview(window3, columns=("ID", "Location", "Status"), show="headings")

# Dette er mulighederne for status på maskinerne
machineStatus = ["NONE", "FULL", "HALF", "LOW", "EMPTY", "OFFLINE"]

# Mulighederne hvis man skal sende besked til en medarbejder
options = ["NONE", "Refill machine", "Report issue", "Request maintenance"]

# Funktion der viser en besked i et popup-vindue. Så man kan give info til brugeren.
def Messageboxhandler(Messageboxheader, MessageboxText):
    global messageboxstate
    if messageboxstate == False:
        messageboxstate = True
        messagebox.showinfo(Messageboxheader, MessageboxText)
        messageboxstate = False

#region Widgets
# Menu-knapper der viser de forskellige sider i programmet når man trykker på dem
def menuwidgets():
    placemachineButton = Button(window, text="Place a Vending Machine", command=showmenu3)
    placemachineButton.place(x=20, y=40)

    fillmachineButton = Button(window, text="Fill Vending Machine", command=showmenu2)
    fillmachineButton.place(x=190, y=40)

    KontaktmedarbejderButton = Button(window, text="Contact Employee", command=showmenu4)
    KontaktmedarbejderButton.place(x=120, y=80)

# Her laver vi alle felter og knapper til menuen hvor man styrer varer i automaten
def menu2Widgets():
    # Kolonne-navne til tabellen så man kan se hvad hvad er
    tree.heading("ID", text="ID")
    tree.heading("Machine ID", text="Machine ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Stock", text="Stock")
    tree.column("ID", width=50, anchor="center")
    tree.column("Machine ID", width=80)
    tree.column("Item Name", width=200)
    tree.column("Stock", width=60)
    tree.place(x=350, y=30, width=400, height=200)

    # Tekstfelter og tekst til brugerens inputs (f.eks. maskin-ID, varenavn, antal)
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
    ItemID = Label(window2, text="item ID")
    ItemID.place(x=10, y=125)

    # En overskrift øverst
    lbl = Label(window2, text="Vending Machine management", font="Areial")
    lbl.place(x=0, y=0)

    # Knapper til at indsætte, hente, slette eller opdatere varer
    InsertButton = Button(window2, text="Insert item", command=lambda: insertItem(txt_Item, txt_machineID, txt_itemAmount))
    InsertButton.place(x=10, y=165)

    GetButton = Button(window2, text="Get ID", command=lambda: getitem(txt_ItemID, txt_machineID, txt_Item))
    GetButton.place(x=10, y=195)

    DeleteButton = Button(window2, text="Delete by item ID", command=lambda: deleteItem(txt_ItemID))
    DeleteButton.place(x=10, y=225)

    UpdateButton = Button(window2, text="Update", command=lambda: updateItems(txt_ItemID, txt_Item, txt_itemAmount))
    UpdateButton.place(x=10, y=255)

    MenuButton = Button(window2, text="Menu", command=showmenu)
    MenuButton.place(x=10, y=305)

# Her laver vi input felter, labels og knapper til det vindue hvor man kan styre information om selve maskinerne
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

    # Dropdown menu hvor man kan vælge status på maskinen
    machineStatusVar = StringVar(window3)
    machineStatusVar.set(machineStatus[0])
    machineStatusMenu = OptionMenu(window3, machineStatusVar, *machineStatus)
    machineStatusMenu.place(x=155, y=95)
    status = Label(window3, text="Enter the machine status")
    status.place(x=10, y=95)

    # Knapper til at tilføje, opdatere og fjerne maskiner
    InsertButton = Button(window3, text="Insert Machine", command=lambda: insertMachine(txt_location, machineStatusVar))
    InsertButton.place(x=10, y=135)

    GetButton = Button(window3, text="Get Machine", command=lambda: getValues(txt_machineID, txt_location, machineStatusVar))
    GetButton.place(x=10, y=165)

    DeleteButton = Button(
        window3, 
        text="Remove Machine", 
        command=lambda: delete_Vending(txt_machineID))
    DeleteButton.place(x=10, y=195)

    UpdateButton = Button(window3, text="Update Information", command=lambda: updateMachine(txt_machineID, txt_location, machineStatusVar))
    UpdateButton.place(x=10, y=225)

    MenuButton = Button(window3, text="Menu", command=showmenu)
    MenuButton.place(x=10, y=275)   

# Her laver vi input felter og knap, hvis man vil skrive til en medarbejder (fx hvis der er fejl på maskinen)
def menu4Widgets():
    txt_location = Entry(window4, width=25)
    txt_location.place(x=155, y=35) 
    location = Label(window4, text="Enter City")
    location.place(x=10, y=75)

    txt_machineID = Entry(window4, width=25)
    txt_machineID.place(x=155, y=75)
    machineID = Label(window4, text="Enter vending machine ID")
    machineID.place(x=10, y=35)

    # Her er dropdown med muligheder for hvad man vil sige til medarbejderen
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

    InsertButton = Button(window4, text="Send Report", command=lambda: sendReport(txt_employeeMessage, variable, txt_machineID, txt_location))
    InsertButton.place(x=15, y=185)

    MenuButton = Button(window4, text="Menu", command=showmenu)
    MenuButton.place(x=15, y=225)

# Funktionerne under her bruges til at skifte mellem vinduer, så kun én af dem vises ad gangen.
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

# Funktion til at sende besked til medarbejderen, med tjek hvis man taster noget forkert ind
def sendReport(employeemessage, Variable, machineID, location):
    employee = employeemessage.get().strip()
    variable = Variable.get().strip()
    machineid = machineID.get().strip()
    Location = location.get().strip()
    if not employee.replace(" ", "").isalpha():  
        Messageboxhandler("Input Error", "Employee name must contain only letters")
        return
    Messageboxhandler(
        "Report sent",
        f"Your message '{variable}' has been sent to {employee} at {machineid} for machine ID {Location}"
    )

#region Insert Funtion
# Funktion til at lægge en ny maskine ind i databasen (med location og status)
def insertMachine(machineLocation, status):
    machinelocation = machineLocation.get().strip()
    Status = status.get().strip()
    if machinelocation == "":
        if Status == machineStatus[0]:
            Messageboxhandler("Insert Status", "Location and Status required")
            return
        else:
            Messageboxhandler("Insert Status", "Location required")
            return
    else: 
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObject = conn.cursor()
        cursorObject.execute("INSERT INTO vending_machines (location, status) VALUES (%s, %s)", (machinelocation, Status))
        conn.commit()
        cursorObject.close()   
        Messageboxhandler("insert status", "inserted machine into database")
        conn.close()

# Funktion til at ligge en vare ind i databasen for en maskine
def insertItem(itemID, machineID, amount):
    itemid = itemID.get().strip()
    machineid = machineID.get().strip()
    Amount = amount.get().strip()
    if itemid == "" or machineid == "" or Amount == "":
        Messageboxhandler("Insert Status", "All fields required")
        return  # Hvis nogen felter mangler, stoppes funktionen
    else:
        try:
            Amount = int(Amount)  # Sikrer at amount faktisk er et tal
        except ValueError:
            Messageboxhandler("Insert Error", "Amount must be a number")
            return
    conn = mysql.connector.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"]
    )
    cursor = conn.cursor()
    # Her indsætter vi varen i tabellen
    cursor.execute(
        "INSERT INTO items (item_name, quantity, vending_machine_id) VALUES (%s, %s, %s)",
        (itemid, Amount, machineid)
    )
    conn.commit()
    cursor.close()
    conn.close()
    Messageboxhandler("Insert Status", f"Inserted {Amount} of {itemid} into machine {machineid}")
    
    # Gamle ekstra tjek (måske lidt mærkelige, men beholdt som originalen ønskede)
    if itemid == "" or machineid == "" or Amount == "":    
        Messageboxhandler("Insert Error", "All fields are required")
        return

    if not itemid.replace(" ", "").isalpha():    
        Messageboxhandler("Insert Error", "Item name must contain only letters")
        return

    try:
        Amount = int(Amount)
    except ValueError:
        Messageboxhandler("Insert Error", "Amount must be a number")
        return
#endregion

#region Get Funtion
# Funktion til at finde maskiner i databasen ud fra brugerens input
def getValues(machineid, machinelocation, status):
    machineID = machineid.get()
    machineLocation = machinelocation.get()
    machinestatus = status.get()
    if machineID == "" and machineLocation == "" and machinestatus == machineStatus[5]:
        Messageboxhandler("Update Status", "Failed: Must put machine id")
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
        if machinestatus.strip() != machineStatus[0]:
            condition.append("status=%s")
            params.append(machinestatus.strip())

        query = "SELECT * FROM vending_machines"
        if condition:
            query += " WHERE " + " AND ".join(condition)

        cursorObjeckt.execute(query, tuple(params))
        
        # Tømmer tabellen inden vi viser nye data
        for item in tree2.get_children():
            tree2.delete(item)

        rows = cursorObjeckt.fetchall()
        for row in rows:
            tree2.insert("", "end", values=row)

        cursorObjeckt.close()
        conn.close()

# Funktion til at finde varer i databasen med ID eller navn
def getitem(itemID, machineID, itemName):
    itemid = itemID.get()
    machineid = machineID.get()
    itemname = itemName.get()

    if itemid == "" and machineid == "" and itemname == "":
        Messageboxhandler("Get Status", "Atleast one field required to get values")
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

        # Først tømmer vi listen i tabellen
        for item in tree.get_children():
            tree.delete(item)

        rows = cursorObjeckt.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

        cursorObjeckt.close()
        conn.close()
#endregion

#region Update Funtion
# Funktion til at opdatere (rette) info om en maskine
def updateMachine(machineid, machinelocation, status):
    machineID = machineid.get()
    if machineID == "":
        Messageboxhandler("Update Status", "Failed: Must put machine id")
    else:
        try:
            machineidTry = machineid.get()
            machineidTry = int(machineidTry)
        except ValueError:
            Messageboxhandler("Update Status", "Failed: ID must be a number")
            return

        machineLocation = machinelocation.get() if machinelocation else ""
        machinestatus = status.get() if status else machineStatus[0]

        if not (machineLocation or machinestatus):
            Messageboxhandler("Fetch status", "Need atleast one field filled.")
            return
        
        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObjekt = conn.cursor()

        allowed_columns = {
            "status": "status=%s",
            "location": "location=%s"
        }

        if machinelocation or status:
            sets = []
            prams = []
            if machineLocation != "":
                sets.append(allowed_columns["location"])
                prams.append(machineLocation)
            if machinestatus != machineStatus[0]:
                sets.append(allowed_columns["status"])
                prams.append(machinestatus)

            if sets:
                prams.append(machineID)
                query = "UPDATE vending_machines SET " + ", ".join(sets) + " WHERE id=%s" # nosec
                cursorObjekt.execute(query, tuple(prams))
                Messageboxhandler("Update Status", "Updated items")

        conn.commit()
        cursorObjekt.close()
        conn.close()

# Funktion til at rette varer i databasen (fx hvis man har skrevet forkert)
def updateItems(itemid, machineitem, itemamount):  
    itemID = itemid.get()
    if itemID == "":
        Messageboxhandler("Fetch status", "Need to put item ID to update the item.")
        return
    else:
        try:
            itemidTry = itemid.get()
            itemidTry = int(itemidTry)
        except ValueError:
            Messageboxhandler("Update Status", "Failed: ID must be a number")
            return
        if itemamount:
            try:
                itemamountTry = itemamount.get()
                itemamountTry = int(itemamountTry)
            except ValueError:
                Messageboxhandler("Update Status", "Failed: Item Amount must be a number")
                return

        machineItem = machineitem.get() if machineitem else ""
        itemAmount = itemamount.get() if itemamount else ""

        if not (machineItem or itemAmount):
            Messageboxhandler("Fetch status", "Need atleast one field filled.")
            return

        allowed_columns = {
            "item_name": "item_name=%s",
            "quantity": "quantity=%s",
        }

        conn = mysql.connector.connect(host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"], database=config["DB_NAME"])
        cursorObjekt = conn.cursor()

        if machineitem or itemamount:
            sets = []
            prams = []
            if machineItem != "":
                sets.append(allowed_columns["item_name"])
                prams.append(machineItem)
            if itemAmount != "":
                sets.append(allowed_columns["quantity"])
                prams.append(itemAmount)

            if sets:
                prams.append(itemID)
                query = "UPDATE items SET " + ", ".join(sets) + " WHERE id=%s" # nosec

            cursorObjekt.execute(query, tuple(prams))
            Messageboxhandler("Update Status", "Updated items")

    conn.commit()
    cursor.close()
    conn.close()
#endregion

#region Delete Funtion
# Funktion til at slette en maskine fra databasen (og alle dens varer)
def delete_Vending(txt_machineID):
    machineID = txt_machineID.get().strip()
    if not machineID:
        Messageboxhandler("Delete Error", "Please enter a machine ID")
        return 
    try:
        conn = mysql.connector.connect(
            host=config["DB_HOST"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            database=config["DB_NAME"]
        )
        cursor = conn.cursor()

        # Tjekker først om maskinen findes
        cursor.execute("SELECT id FROM vending_machines WHERE id=%s", (machineID,))
        if not cursor.fetchone():
            return Messageboxhandler("Delete Error", f"Machine {machineID} does not exist.")

        # Pop up hvor bruger skal bekræfte at de vil slette
        if not messagebox.askyesno("Confirm Delete", f"Delete machine {machineID}?"):
            return

        # Først slet alle varer fra maskinen, så selve maskinen
        cursor.execute("DELETE FROM items WHERE vending_machine_id=%s", (machineID,))
        cursor.execute("DELETE FROM vending_machines WHERE id=%s", (machineID,))
        conn.commit()

        Messageboxhandler("Delete Status", f"Vending machine {machineID} deleted successfully")

    except mysql.connector.Error as err:
        Messageboxhandler("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Funktion til at slette en enkelt vare ud fra dens ID
def deleteItem(itemIDField):
    item_id = itemIDField.get().strip()
    if not item_id:
        return Messageboxhandler("Delete Error", "Please enter an item ID")
    try:
        item_id = int(item_id)
    except ValueError:
        return Messageboxhandler("Delete Error", "Item ID must be a number")
    try:
        conn = mysql.connector.connect(
            host=config["DB_HOST"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            database=config["DB_NAME"]
        )
        cursor = conn.cursor()

        # Henter navn og maskine på varen før vi sletter, så vi kan vise en besked
        cursor.execute("SELECT item_name, vending_machine_id FROM items WHERE id=%s", (item_id,))
        result = cursor.fetchone()
        if not result:
            return Messageboxhandler("Delete Error", f"Item with ID {item_id} does not exist.")
        item_name, machine_id = result

        if not messagebox.askyesno("Confirm Delete", f"Delete '{item_name}' (ID: {item_id}) from machine {machine_id}?"):
            return

        # Sletter varen
        cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
        conn.commit()

        Messageboxhandler("Delete Status", f"Item '{item_name}' (ID: {item_id}) deleted successfully")
        # Nulstiller feltet så der står tomt bagefter
        itemIDField.delete(0, END)

    except mysql.connector.Error as err:
        Messageboxhandler("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()   
#endregion

#region Main
# Det her er hovedfunktionen, hvor vi sørger for at alle vinduer og knapper bliver lavet og programmet starter op med .mainloop()
def main():
    menu2Widgets()
    menu3Widgets()
    menu4Widgets()
    menuwidgets()
    window.mainloop()
#endregion

# Her starter vi alt det vigtige hvis vi kører filen direkte (fx sørger for at databasen findes og laver database-tabellerne)
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