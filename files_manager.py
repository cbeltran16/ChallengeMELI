""" Delete the permissions of the public files """
import repository_manager as RepositoryManager
import google_drive_manager as driveManager

def process_files(files):
    """ Process the files"""
    RepositoryManager.insert_or_update_files(files)
    process_public_files(files)

def process_public_files(files):
    """ Delete the permissions of the public files """
    for file in files:
        if file['visibility'] == "Público":
           driveManager.delete_permissions(file['object'])