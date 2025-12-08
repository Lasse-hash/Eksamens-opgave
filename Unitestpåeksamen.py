import unittest
from unittest.mock import Mock, MagicMock, patch
import main_opgave


class TestInsertFunctions(unittest.TestCase):
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')    

    def test_Insert_valid_data(self, mock_messagebox, mock_connect):

        # Setup mock database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock Entry widgets for itemID, machineID, and amount
        mock_itemID = Mock()
        mock_itemID.get.return_value = "Cola"
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "10"

        # Call the function with correct parameters
        main_opgave.insertItem(mock_itemID, mock_machineID, mock_amount)

        # Verify that the database insert was called with correct parameters
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO items (item_name, quantity, vending_machine_id) VALUES (%s, %s, %s)",
            ("Cola", 10, "1")
        )
        mock_conn.commit.assert_called_once()
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Insert_empty_fields(self, mock_messagebox, mock_connect):
        # Mock Entry widgets med tomme felter
        mock_itemID = Mock()
        mock_itemID.get.return_value = ""
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "10"

        # Mock database så den ikke kaldes
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        # Kald funktionen med tomt itemID
        main_opgave.insertItem(mock_itemID, mock_machineID, mock_amount)
        
        # Verificer at fejlbesked blev vist
        mock_messagebox.showinfo.assert_called_once_with("Insert Status", "All fields required")
        # Verificer at database IKKE blev kaldt
        mock_connect.assert_not_called()
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Insert_invalid_amount(self, mock_messagebox, mock_connect):
        # Mock Entry widgets med ikke-numerisk amount
        mock_itemID = Mock()
        mock_itemID.get.return_value = "Cola"
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "abc"  # Ikke et tal

        # Mock database så den ikke kaldes
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        # Kald funktionen med ugyldig amount
        main_opgave.insertItem(mock_itemID, mock_machineID, mock_amount)
        
        # Verificer at fejlbesked blev vist
        mock_messagebox.showerror.assert_called_once_with("Insert Error", "Amount must be a number")
        # Verificer at database IKKE blev kaldt
        mock_connect.assert_not_called()

class TestUpdateFunctions(unittest.TestCase):

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')

    def test_Update_valid_data(self, mock_messagebox, mock_connect):


        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_itemID = Mock()
        mock_itemID.get.return_value = "1"
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_amount = Mock()
        mock_amount.get.return_value = "20"

        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        main_opgave.updateValues( mock_machineID, None, None, mock_itemID, mock_amount)

        mock_messagebox.showinfo.assert_called_with("Update Status", "Updated items")
        
        mock_conn.commit.assert_called_once()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Update_empty_machineID(self, mock_messagebox, mock_connect):
        # Mock Entry widget med tomt machineID
        mock_machineID = Mock()
        mock_machineID.get.return_value = ""

        # Kald funktionen med tomt machineID
        main_opgave.updateValues(mock_machineID, None, None, None, None)
        
        # Verificer at fejlbesked blev vist
        mock_messagebox.showinfo.assert_called_once_with("Update Status", "Failed: Must put machine id")
        # Verificer at database IKKE blev kaldt
        mock_connect.assert_not_called()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Update_invalid_machineID(self, mock_messagebox, mock_connect):
        # Mock Entry widget med ikke-numerisk machineID
        mock_machineID = Mock()
        mock_machineID.get.return_value = "abc"  # Ikke et tal
        mock_itemID = Mock()
        mock_itemID.get.return_value = "Cola"
        mock_amount = Mock()
        mock_amount.get.return_value = "10"

        # Kald funktionen med ugyldig machineID
        main_opgave.updateValues(mock_machineID, None, None, mock_itemID, mock_amount)
        
        # Verificer at fejlbesked blev vist
        mock_messagebox.showinfo.assert_called_once_with("Update Status", "Failed: ID must be a number")
        # Verificer at database IKKE blev kaldt
        mock_connect.assert_not_called()
    
    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    def test_Update_invalid_amount(self, mock_messagebox, mock_connect):
        # Mock Entry widgets med ikke-numerisk amount
        mock_machineID = Mock()
        mock_machineID.get.return_value = "1"
        mock_itemID = Mock()
        mock_itemID.get.return_value = "Cola"
        mock_amount = Mock()
        mock_amount.get.return_value = "abc"  # Ikke et tal

        # Kald funktionen med ugyldig amount
        main_opgave.updateValues(mock_machineID, None, None, mock_itemID, mock_amount)
        
        # Verificer at fejlbesked blev vist
        mock_messagebox.showinfo.assert_called_once_with("Update Status", "Failed: Item Amount must be a number")
        # Verificer at database IKKE blev kaldt
        mock_connect.assert_not_called()


class TestGetValuesFunctions(unittest.TestCase):

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    @patch('main_opgave.tree2')
    def test_getValues_empty_fields(self, mock_tree2, mock_messagebox, mock_connect):
        # Patch the global variable directly
        main_opgave.machineStatus = ['A', 'B', 'C', 'D', 'E', 'OFFLINE']
        
        machineid = Mock()
        machineid.get.return_value = ''
        machinelocation = Mock()
        machinelocation.get.return_value = ''
        status = Mock()
        status.get.return_value = 'OFFLINE'  # machineStatus[5]
        
        main_opgave.getValues(machineid, machinelocation, status)
        
        mock_messagebox.showinfo.assert_called_once_with("Update Status", "Failed: Must put machine id")
        mock_connect.assert_not_called()

    @patch('main_opgave.mysql.connector.connect')
    @patch('main_opgave.messagebox')
    @patch('main_opgave.tree2')
    def test_getValues_with_fields(self, mock_tree2, mock_messagebox, mock_connect):
        # Patch the global variable directly
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
        # Prepare mocks
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

    unittest.main()




