import unittest
from unittest.mock import MagicMock
from google_drive_manager import delete_permissions

class TestGoogleDriveManager(unittest.TestCase):
    def test_delete_permissions(self):
        # Create a mock file object
        file = MagicMock()
        file.GetPermissions.return_value = [
            {'role': 'owner', 'emailAddress': 'owner@example.com'},
            {'type': 'anyone', 'id': 'permission_id'}
        ]
        
        # Create a mock emailManager object
        emailManager = MagicMock()
        
        # Call the function under test
        delete_permissions(file)
        
        # Assert that the permission was deleted
        file.DeletePermission.assert_called_once_with('permission_id')
        
        # Assert that the email was sent to the owner
      
      

if __name__ == '__main__':
    unittest.main()