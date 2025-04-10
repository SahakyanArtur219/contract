import os
import re

def sanitize_windows_filename(name):
    # Replace Windows-invalid characters with underscore
    return re.sub(r'[\\/*?:"<>|]', '_', name)


def rename_file(new_name_without_extension):
    # Folder where the file is located
    folder_path = "C:\\Users\\artur.sahakyan\\Desktop\\all_doc"
    
    
    # Step 1: Get the list of files in the folder
    files = os.listdir(folder_path)
    
    # Step 2: Check if there is exactly one file in the folder
    if len(files) == 1:
        old_file_name = files[0]  # Get the first (and only) file name
        old_file_path = os.path.join(folder_path, old_file_name)
        
        # Step 3: Extract the file name and extension from the original file path
        file_name, file_extension = os.path.splitext(old_file_name)
        
        # Step 4: Create the new file path by combining the folder path, new name, and original extension
        new_file_path = os.path.join(folder_path, new_name_without_extension + file_extension)
        
        # Step 5: Rename the file
        try:
            os.rename(old_file_path, new_file_path)
            print(f"File renamed successfully to: {new_name_without_extension}{file_extension}")
        except FileNotFoundError:
            print(f"The file at {old_file_path} was not found.")
        except PermissionError:
            print(f"Permission denied. Unable to rename the file.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("There is not exactly one file in the folder.")
        
