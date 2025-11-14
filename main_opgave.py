from tkinter import *
from tkinter import messagebox
import mysql.connector

window = Tk()

window.geometry("950x800")

window.title("Vending Machine management")

#region Widgets
def createWidgets():
    txt_machineID = Entry(window, width=25)
    txt_machineID.place(x=155, y=35)
    machineID = Label(window, text="Enter vending machine ID")
    machineID.place(x=10, y=35)

    txt_Item = Entry(window, width=25)
    txt_Item.place(x=155, y=75)
    Item = Label(window, text="Enter item")
    Item.place(x=10, y=75)

    txt_itemAmount = Entry(window, width=25)
    txt_itemAmount.place(x=155, y=105)
    itemAmount = Label(window, text="Enter amount of item")
    itemAmount.place(x=10, y=105)

    txt_aThing = Entry(window, width=25)
    txt_aThing.place(x=155, y=135)
    aThing = Label(window, text="??????")
    aThing.place(x=10, y=135)

    lbl = Label(window, text="Vending Machine management", font="Areial")
    lbl.place(x=0, y=0)

    InsertButton = Button(window, text="Insert item", command=insertItem)
    InsertButton.place(x=15, y=165)

    GetButton = Button(window, text="Get ID", command=getValues)
    GetButton.place(x=90, y=165)

    DeleteButton = Button(window, text="Delete", command=deleteThings)
    DeleteButton.place(x=140, y=165)

    UpdateButton = Button(window, text="Update", command=updateValues)
    UpdateButton.place(x=195, y=165)

    Gettxt = Text(window, width=50)
    Gettxt.place(x=350, y=30)
#endregion

#region Insert Funtion
def insertItem():
    pass
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

    createWidgets()

    insertItem()

    updateValues()

    deleteThings()

    getValues()



    window.mainloop()
#endregion

if __name__ == "__main__":
    main()