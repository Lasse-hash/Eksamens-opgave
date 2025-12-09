import unittest
from unittest.mock import Mock, MagicMock, patch
import main_opgave

# Testklasse til at teste indsætningsfunktionerne i main_opgave
class TestInsertFunctions(unittest.TestCase):
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.Messageboxhandler')
    def test_InsertMachine_valid_data(self, mock_messagebox, mock_connect):
        # Opretter en "falsk" database forbindelse, så vi ikke bruger en rigtig database til testen
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Opretter mocks for felterne location og status og sætter dem til at returnere værdier
        mock_location = Mock()
        mock_location.get.return_value = "Copenhagen"
        mock_status = Mock()
        mock_status.get.return_value = "FULL"

        # Kalder insertMachine med gyldige data
        main_opgave.insertMachine(mock_location, mock_status)

        # Tjekker at SQL insert blev kaldt korrekt med forventede værdier
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO vending_machines (location, status) VALUES (%s, %s)",
            ("Copenhagen", "FULL")
        )
        mock_conn.commit.assert_called_once()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.Messageboxhandler')
    def test_InsertMachine_empty_location(self, mock_messagebox, mock_connect):
        # Tester at man får fejl, hvis location er tom
        mock_location = Mock()
        mock_location.get.return_value = ""
        mock_status = Mock()
        mock_status.get.return_value = "FULL"

        main_opgave.insertMachine(mock_location, mock_status)
        
        # Tjekker at fejlbesked blev vist
        mock_messagebox.assert_called_once_with("Insert Status", "Location required")
        # Tjekker at der IKKE blev lavet databaseforbindelse
        mock_connect.assert_not_called()
        
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Insert_valid_data(self, mock_messagebox, mock_connect):
        # Tester at korrekt data bliver indsættes i databasen for varer
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_itemID = Mock()
        mock_itemID.get.return_value = "Cola"
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "10"

        main_opgave.insertItem(mock_itemID, mock_machineID, mock_amount)

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO items (item_name, quantity, vending_machine_id) VALUES (%s, %s, %s)",
            ("Cola", 10, "1")
        )
        mock_conn.commit.assert_called_once()
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Insert_empty_fields(self, mock_messagebox, mock_connect):
        # Tester at der gives fejl hvis et felt er tomt ved insertItem
        mock_itemID = Mock()
        mock_itemID.get.return_value = ""
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "10"

        main_opgave.insertItem(mock_itemID, mock_machineID, mock_amount)
        
        # Skal vise fejlbesked til brugeren
        mock_messagebox.showinfo.assert_called_once_with("Insert Status", "All fields required")
        # Skal ikke prøve at forbinde til databasen
        mock_connect.assert_not_called()
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Insert_invalid_amount(self, mock_messagebox, mock_connect):
        # Tester at insertItem fejler hvis amount ikke er et tal
        mock_itemID = Mock()
        mock_itemID.get.return_value = "Cola"
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "abc"  # ugyldig

        main_opgave.insertItem(mock_itemID, mock_machineID, mock_amount)
        
        mock_messagebox.showinfo.assert_called_with("Insert Error", "Amount must be a number")
        mock_connect.assert_not_called()

# Testklasse til opdateringsfunktioner
class TestUpdateFunctions(unittest.TestCase):

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.Messageboxhandler')
    def test_UpdateMachine_valid_data(self, mock_messagebox, mock_connect):
        # Tester at updateMachine kan køre med gyldige data og faktisk laver update i databasen
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_location = Mock()
        mock_location.get.return_value = "Copenhagen"
        mock_status = Mock()
        mock_status.get.return_value = "FULL"

        main_opgave.updateMachine(mock_machineID, mock_location, mock_status)

        mock_connect.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.Messageboxhandler')
    def test_UpdateMachine_empty_machineID(self, mock_messagebox, mock_connect):
        # Tester at der gives fejl hvis machineID er tomt ved updateMachine
        mock_machineID = Mock()
        mock_machineID.get.return_value = ""

        main_opgave.updateMachine(mock_machineID, None, None)
        
        mock_messagebox.assert_called_once_with("Update Status", "Failed: Must put machine id")
        mock_connect.assert_not_called()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.Messageboxhandler')
    def test_UpdateMachine_invalid_machineID(self, mock_messagebox, mock_connect):
        # Tester at der gives fejl hvis ID ikke er et tal
        mock_machineID = Mock()
        mock_machineID.get.return_value = "abc"
        mock_location = Mock()
        mock_location.get.return_value = "Copenhagen"
        mock_status = Mock()
        mock_status.get.return_value = "FULL"

        main_opgave.updateMachine(mock_machineID, mock_location, mock_status)
        
        mock_messagebox.assert_called_once_with("Update Status", "Failed: ID must be a number")
        mock_connect.assert_not_called()
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.Messageboxhandler')
    def test_UpdateItems_empty_itemID(self, mock_messagebox, mock_connect):
        # Tester at der gives fejl hvis itemID mangler
        mock_itemID = Mock()
        mock_itemID.get.return_value = ""

        main_opgave.updateItems(mock_itemID, None, None)
        
        mock_messagebox.assert_called_once_with("Fetch status", "Need to put item ID to update the item.")
        mock_connect.assert_not_called()

# Testklasse til slettefunktioner
class TestDeleteFunctions(unittest.TestCase):
    
    @patch("main_opgave.Messageboxhandler")
    def test_empty_id(self, mock_messagebox):
        # Tester at der gives fejl hvis machineID mangler når man vil slette
        mock_machineID = Mock()
        mock_machineID.get.return_value = ""

        main_opgave.delete_Vending(mock_machineID)

        mock_messagebox.assert_called_once_with("Delete Error", "Please enter a machine ID")

    @patch("main_opgave.Messageboxhandler")
    @patch("main_opgave.mysql.connector.connect")
    def test_machine_not_exist(self, mock_connect, mock_messagebox):
        # Tester at fejl vises hvis maskinen ikke findes i databasen
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # simulerer at maskinen ikke findes

        mock_machineID = Mock()
        mock_machineID.get.return_value = "999"

        main_opgave.delete_Vending(mock_machineID)

        mock_cursor.execute.assert_called_once_with(
            "SELECT id FROM vending_machines WHERE id=%s", ("999",)
        )
        mock_messagebox.assert_called_with("Delete Error", "Machine 999 does not exist.")
        mock_conn.commit.assert_not_called()

    @patch("main_opgave.messagebox.askyesno", return_value=False)
    @patch("main_opgave.mysql.connector.connect")
    @patch("main_opgave.Messageboxhandler")
    def test_user_cancels(self, mock_messagebox, mock_connect, mock_askyesno):
        # Tester at der ikke slettes noget hvis brugeren klikker "nej" på popup
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (123,)  # maskinen findes

        mock_machineID = Mock()
        mock_machineID.get.return_value = "123"

        main_opgave.delete_Vending(mock_machineID)

        # Kun SELECT skal køres når man trykker nej
        self.assertEqual(mock_cursor.execute.call_count, 1)
        mock_cursor.execute.assert_called_with(
            "SELECT id FROM vending_machines WHERE id=%s", ("123",)
        )

        mock_askyesno.assert_called_once_with("Confirm Delete", "Delete machine 123?")
        mock_conn.commit.assert_not_called()
        mock_messagebox.assert_not_called()

    @patch("main_opgave.messagebox.askyesno", return_value=True)
    @patch("main_opgave.Messageboxhandler")
    @patch("main_opgave.mysql.connector.connect")
    def test_successful_delete(self, mock_connect, mock_messagebox, mock_askyesno):
        # Tester at man faktisk sletter når man klikker "ja"
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (123,)

        mock_machineID = Mock()
        mock_machineID.get.return_value = "123"

        main_opgave.delete_Vending(mock_machineID)

        # Popup spørger om bekræftelse
        mock_askyesno.assert_called_once_with("Confirm Delete", "Delete machine 123?")
        # Der køres tre SQL queries: SELECT og to DELETE
        self.assertEqual(mock_cursor.execute.call_count, 3)
        mock_conn.commit.assert_called_once()
        mock_messagebox.assert_called_with("Delete Status", "Vending machine 123 deleted successfully")

class TestGetValuesFunctions(unittest.TestCase):

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    @patch('main_opgave.tree2')
    def test_getValues_empty_fields(self, mock_tree2, mock_messagebox, mock_connect):
        # Tester at man får fejl hvis alle felter er tomme (og status er OFFLINE)
        main_opgave.machineStatus = ['A', 'B', 'C', 'D', 'E', 'OFFLINE']
        
        machineid = Mock()
        machineid.get.return_value = ''
        machinelocation = Mock()
        machinelocation.get.return_value = ''
        status = Mock()
        status.get.return_value = 'OFFLINE'
        
        main_opgave.getValues(machineid, machinelocation, status)
        
        mock_messagebox.showinfo.assert_called_once_with("Update Status", "Failed: Must put machine id")
        mock_connect.assert_not_called()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    @patch('main_opgave.tree2')
    def test_getValues_with_fields(self, mock_tree2, mock_messagebox, mock_connect):
        # Tester at værdier bliver hentet korrekt fra databasen og tabellen viser nyt indhold
        main_opgave.machineStatus = ['A', 'B', 'C', 'D', 'E', 'OFFLINE']
        main_opgave.config = {"DB_HOST": "h", "DB_USER": "u", "DB_PASSWORD": "p", "DB_NAME": "db"}

        machineid = Mock()
        machineid.get.return_value = '42'
        machinelocation = Mock()
        machinelocation.get.return_value = 'Viborg'
        status = Mock()
        status.get.return_value = 'ACTIVE'

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(42, "Viborg", "ACTIVE")]

        mock_tree2.get_children.return_value = [1, 2]

        main_opgave.getValues(machineid, machinelocation, status)

        mock_messagebox.showinfo.assert_not_called()
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_tree2.delete.assert_any_call(1)
        mock_tree2.delete.assert_any_call(2)
        mock_tree2.insert.assert_called_once_with("", "end", values=(42, "Viborg", "ACTIVE"))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

class TestGetItemFunctions(unittest.TestCase):

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    @patch('main_opgave.tree')
    def test_getitem_empty_fields(self, mock_tree, mock_messagebox, mock_connect):
        # Tester at fejlbesked vises når alle felter er tomme
        itemID = Mock()
        itemID.get.return_value = ''
        machineID = Mock()
        machineID.get.return_value = ''
        itemName = Mock()
        itemName.get.return_value = ''

        main_opgave.getitem(itemID, machineID, itemName)

        mock_messagebox.showinfo.assert_called_once_with("Get Status", "Atleast one field required to get values")
        mock_connect.assert_not_called()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    @patch('main_opgave.tree')
    def test_getitem_with_fields(self, mock_tree, mock_messagebox, mock_connect):
        # Tester at varer bliver hentet og tabellen opdateret
        main_opgave.config = {"DB_HOST": "h", "DB_USER": "u", "DB_PASSWORD": "p", "DB_NAME": "db"}

        itemID = Mock()
        itemID.get.return_value = '13'
        machineID = Mock()
        machineID.get.return_value = '77'
        itemName = Mock()
        itemName.get.return_value = 'Pepsi'

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(13, 77, "Pepsi")]

        mock_tree.get_children.return_value = [9]

        main_opgave.getitem(itemID, machineID, itemName)

        mock_messagebox.showinfo.assert_not_called()
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_tree.delete.assert_any_call(9)
        mock_tree.insert.assert_called_once_with("", "end", values=(13, 77, "Pepsi"))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    # Kører alle unittests når filen bliver kørt direkte
    unittest.main()