import google_drive_manager as driveManager
import files_manager as filesManager
import repository_manager


if __name__ == "__main__":
    repository_manager.create_documents_table()
    filesManager.process_files(driveManager.search())

    