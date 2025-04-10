from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyautogui
import json
import os
import shutil
import re
import os
from rename_file_file  import rename_file


'''
def rename_file(file_name):
    

    # Specify the folder path and the current file name
    folder_path = download_dir  # Replace with your folder path
    
    files = os.listdir(folder_path)

    # Check if there is exactly one file in the folder
    if len(files) == 1:
        old_file_name = files[0]  # Get the first (and only) file name
        new_file_name = file_name  # Replace with the new desired file name
    
        # Create full paths for old and new file names
        old_file_path = os.path.join(folder_path, old_file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
    
        # Rename the file
        os.rename(old_file_path, new_file_path)
    
        print(f"File renamed from '{old_file_name}' to '{new_file_name}'")
    else:
        print("There is not exactly one file in the folder.")
'''






def sanitize_windows_filename(name):
    # Replace Windows-invalid characters with underscore
    return re.sub(r'[\\/*?:"<>|]', '_', name)


def move_files_to_new_folder(source_folder, new_folder_name):
    # Step 1: Create the new folder (if it doesn't already exist)
    new_folder = os.path.join(source_folder, new_folder_name)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print(f"Created new folder: {new_folder}")
    else:
        print(f"Folder already exists: {new_folder}")
    
    # Step 2: Move all files from the source folder to the new folder
    files = os.listdir(source_folder)  # List all files in the source folder
    
    for file in files:
        # Get the full path of the file
        file_path = os.path.join(source_folder, file)
        
        # Only move files, not directories
        if os.path.isfile(file_path):
            try:
                # Move the file to the new folder
                shutil.move(file_path, os.path.join(new_folder, file))
                print(f"Moved {file} to {new_folder}")
            except Exception as e:
                print(f"Error moving file {file}: {e}")



with open('grouped_data.json', 'r', encoding='utf-8') as file:
    data_list = json.load(file)

# Use the data_list
#print(data_list)

installing_files = []
count = 50
download_dir = "C:\\Users\\artur.sahakyan\\Desktop\\all_doc"
new_folder_name_path = " "


def install_files(driver, file_name):
    global count, installing_files, new_folder_name_path
    
    try:
        button_scanMenu1 = driver.find_element(By.ID, "scanMenu1")
        print("Button with ID 'scanMenu1' found, returning early.")
        return  # If button exists, return early without doing anything else
    except:
        pass


    button = driver.find_element(By.ID, "scanMenu0")
    button.click()
    time.sleep(3)
    download_links = driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu li a")



    for link in download_links:
        link_text = link.text
        if (link_text.endswith('.pdf') or link_text.endswith('.PDF')) and (link_text not in installing_files): 
            print(f"Clicking on file: {link_text}") 
            link.click()
            installing_files.append(link_text)
            count = count + 1
            file_name = sanitize_windows_filename(file_name)
            rename_file(file_name)
            move_files_to_new_folder(download_dir, new_folder_name_path)

            install_files(driver, file_name)

# Set up Chrome options to connect to the remote debugging port
chrome_options = Options()


chrome_prefs = {
    "download.default_directory": download_dir,  # Set the custom download directory
    "download.prompt_for_download": False,  # Prevent the download prompt
    "download.directory_upgrade": True,  # Allow Chrome to change the directory
    "safebrowsing.enabled": True  # Enable safe browsing (optional)
}
chrome_options.add_experimental_option("prefs", chrome_prefs)


chrome_options.add_argument("--remote-debugging-port=9222")  # Connect to Chrome on port 9222

# Optionally, you can disable the automation warning
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Connect to the running Chrome instance on port 9222
driver = webdriver.Chrome(options=chrome_options)

# Go to a website (if not already opened)
driver.get("https://armeps.am/ppcm/public/contracts")


button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "hide-filters"))
)
button.click()

search_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[ng-model='filter.number']"))
)



def get_contract(cont_id):
    global installing_files
    print(f"searching id is {cont_id}")
    search_box.send_keys(cont_id)

    pyautogui.press('enter')

    time.sleep(1)
    pyautogui.press('enter')
    
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)
    install_files(driver, cont_id)
    installing_files.clear()
    time.sleep(1)
    search_box.clear()


'''

for contract_id in data_list:
    
    count = 0
    get_contract(contract_id)
    print(f"count for {contract_id} is {count}")
    

    updated_folder_name = sanitize_windows_filename(contract_id)

    new_folder_name = f"C:\\Users\\artur.sahakyan\\Desktop\\specific_contract_doc\\{updated_folder_name}"
    move_files_to_new_folder(download_dir, new_folder_name)

''' 



# Iterate over each key-value pair in the JSON data
for organization, contract_codes in data_list.items():
    

    print(f"Organization: {organization}")
    print("Contract Codes:")
    
    updated_folder_name = sanitize_windows_filename(organization)
    new_folder_name_path = f"C:\\Users\\artur.sahakyan\\Desktop\\specific_contract_doc\\{updated_folder_name}"



    # Iterate over the list of contract codes for the current organization
    for code in contract_codes:

        get_contract(code)
        
        print(f"- {code}")
    print("-" * 30)  # Print a separator line between organizations






driver.refresh()

time.sleep(2)

# Close the browser
driver.quit()

# need to clean the search box then do other search