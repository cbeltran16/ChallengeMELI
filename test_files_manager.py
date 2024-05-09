import pytest
from unittest.mock import MagicMock
import files_manager

def test_process_files():
    files = [{'name': 'file1', 'visibility': 'Público', 'object': 'file1_object'}, {'name': 'file2', 'visibility': 'Privado', 'object': 'file2_object'}]
    RepositoryManager = MagicMock()
    files_manager.RepositoryManager.insert_or_update_files = RepositoryManager
    driveManager = MagicMock()
    files_manager.driveManager.delete_permissions = driveManager

    files_manager.process_files(files)

    RepositoryManager.assert_called_once_with(files)

def test_process_public_files():
    files = [{'name': 'file1', 'visibility': 'Público', 'object': 'file1_object'}, {'name': 'file2', 'visibility': 'Privado', 'object': 'file2_object'}]
    drive_manager = MagicMock()
    files_manager.driveManager.delete_permissions = drive_manager

    files_manager.process_public_files(files)

    drive_manager.assert_called_once_with('file1_object')

if __name__ == '__main__':
    pytest.main()