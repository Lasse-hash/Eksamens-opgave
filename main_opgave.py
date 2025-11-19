from tkinter import *
from tkinter import messagebox
import mysql.connector

window = Tk()

window.geometry("350x150")

window.title("Vending Machine management")

window2 = Toplevel(window)
window2.geometry("940x800")
window2.withdraw()

window3 = Toplevel(window)
window3.geometry("940x800")
window3.withdraw()

machineStatus = ["OK", "LOW", "EMPTY", "OFFLINE"]


#region Widgets
def menuwidgets():
    placemachineButton = Button(window, text="Place a Vending Machine", command=showmenu3)
    placemachineButton.place(x=20, y=40)

    fillmachineButton = Button(window, text="Fill Vending Machine", command=showmenu2)
    fillmachineButton.place(x=190, y=40)


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

    #txt_aThing = Entry(window2, width=25)
    #txt_aThing.place(x=155, y=135)
    #aThing = Label(window2, text="??????")
    #aThing.place(x=10, y=135)

    lbl = Label(window2, text="Vending Machine management", font="Areial")
    lbl.place(x=0, y=0)

    InsertButton = Button(window2, text="Insert item", command=lambda: insertItem(txt_Item, txt_machineID, txt_itemAmount))
    InsertButton.place(x=15, y=165)

    GetButton = Button(window2, text="Get ID", command=getValues)
    GetButton.place(x=90, y=165)

    DeleteButton = Button(window2, text="Delete", command=deleteThings)
    DeleteButton.place(x=140, y=165)

    UpdateButton = Button(window2, text="Update", command=updateValues)
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
    location = Label(window3, text="Enter location")
    location.place(x=10, y=75)

    txt_status = Entry(window3, width=25)
    txt_status.place(x=155, y=105)
    status = Label(window3, text="Enter the machine status")
    status.place(x=10, y=105)

    InsertButton = Button(window3, text="Insert Machine", command=lambda: insertMachine(txt_machineID, txt_location, txt_status))
    InsertButton.place(x=25, y=145)

    GetButton = Button(window3, text="Get Machine", command=getValues)
    GetButton.place(x=25, y=185)

    DeleteButton = Button(window3, text="Delete Machine", command=deleteThings)
    DeleteButton.place(x=140, y=145)

    UpdateButton = Button(window3, text="Update Information", command=updateValues)
    UpdateButton.place(x=140, y=185)

    MenuButton = Button(window3, text="Menu", command=showmenu)
    MenuButton.place(x=150, y=250)

    Gettxt = Text(window3, width=50)
    Gettxt.place(x=350, y=30)


def showmenu():
    window2.withdraw()
    window3.withdraw()
    window.deiconify()

def showmenu2():
    window.withdraw()
    window3.withdraw()
    window2.deiconify()

def showmenu3():
    window.withdraw()
    window2.withdraw()
    window3.deiconify()
#endregion

#region Insert Funtion
def insertMachine(machineID, machineLocation, status):
    machineid = machineID.get()
    machinelocation = machineLocation.get()
    Status = status.get()
    if machinelocation == "" or machineid == "" or Status not in machineStatus:
        messagebox.showinfo("insert status", "all fields required")
    else: messagebox.showinfo("Insert Status", f"Inserted {machineid} in {machinelocation} with status: {Status}")

def insertItem(itemID, machineID, amount):
    itemid = itemID.get()
    machineid = machineID.get()
    Amount = amount.get()
    if itemid == "" or machineid == "" or Amount == "":
        messagebox.showinfo("insert status", "all fields required")
    else: messagebox.showinfo("Insert Status", f"Inserted {Amount} of {itemid} into machine {machineid}")
#endregion

#region Get Funtion
def getValues():
    pass
#endregion

#region Update Funtion
def updateValues():
    pass
#endregion

#region Delete Funtion
def deleteThings():
    pass
#endregion

#region Main
def main():

    
    menu2Widgets()
    menu3Widgets()
    menuwidgets()

    window.mainloop()
#endregion

if __name__ == "__main__":
    main()
