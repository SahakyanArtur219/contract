import os

def create_desktop_ini(folder_path, custom_name):
    # Path to the desktop.ini file
    ini_path = os.path.join(folder_path, 'desktop.ini')
    
    # Content for the desktop.ini file
    ini_content = f"""
    [.ShellClassInfo]
    LocalizedResourceName={custom_name}
    """
    
    # Write the content to the desktop.ini file
    with open(ini_path, 'w') as ini_file:
        ini_file.write(ini_content.strip())
    
    # Set the file attributes to hidden and system
    os.system(f'attrib +h +s "{ini_path}"')

# Example usage
folder_path = r'C:\Users\artur.sahakyan\Desktop\specific_contract_doc'
custom_name = 'Your\\Custom/Naaaame'
create_desktop_ini(folder_path, custom_name)
