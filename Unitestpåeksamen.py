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

        

        mock_conn.commit.assert_called_once()


class TestDeleteFunctions(unittest.TestCase):
    
    @patch("main_opgave.messagebox.showerror")
    def test_empty_id(self, mock_showerror):
        mock_machineID = Mock()
        mock_machineID.get.return_value = ""  # empty input

        main_opgave.delete_Vending(mock_machineID)

        mock_showerror.assert_called_once_with("Delete Error", "Please enter a machine ID")


    @patch("main_opgave.messagebox.showerror")
    @patch("main_opgave.mysql.connector.connect")
    def test_machine_not_exist(self, mock_connect, mock_showerror):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # simulate missing machine

        mock_machineID = Mock()
        mock_machineID.get.return_value = "999"

        main_opgave.delete_Vending(mock_machineID)

        mock_cursor.execute.assert_called_once_with(
            "SELECT id FROM vending_machines WHERE id=%s", ("999",)
        )
        mock_showerror.assert_called_once_with("Delete Error", "Machine 999 does not exist.")
        mock_conn.commit.assert_not_called()  # DB not touched
        


    @patch("main_opgave.messagebox.askyesno", return_value=False)
    @patch("main_opgave.mysql.connector.connect")
    @patch("main_opgave.messagebox.showerror")
    def test_user_cancels(self, mock_showerror, mock_connect, mock_askyesno):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (123,)  # machine exists

        mock_machineID = Mock()
        mock_machineID.get.return_value = "123"

        main_opgave.delete_Vending(mock_machineID)

        # Only the SELECT query should have run
        self.assertEqual(mock_cursor.execute.call_count, 1)
        mock_cursor.execute.assert_called_with(
            "SELECT id FROM vending_machines WHERE id=%s", ("123",)
        )

        # Confirm deletion was asked
        mock_askyesno.assert_called_once_with("Confirm Delete", "Delete machine 123?")

        # No commit should have happened
        mock_conn.commit.assert_not_called()

        # No error message
        mock_showerror.assert_not_called()


    @patch("main_opgave.messagebox.askyesno", return_value=True)
    @patch("main_opgave.messagebox.showinfo")
    @patch("main_opgave.mysql.connector.connect")
    def test_successful_delete(self, mock_connect, mock_showinfo, mock_askyesno):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (123,)  # machine exists

        mock_machineID = Mock()
        mock_machineID.get.return_value = "123"

        main_opgave.delete_Vending(mock_machineID)

        # Confirm deletion called
        mock_askyesno.assert_called_once_with("Confirm Delete", "Delete machine 123?")
        # Check delete queries
        self.assertEqual(mock_cursor.execute.call_count, 3)
        mock_conn.commit.assert_called_once()
        mock_showinfo.assert_called_once_with("Delete Status", "Vending machine 123 deleted successfully")




if __name__ == '__main__':

    unittest.main()


