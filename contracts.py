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






# Load the list from the JSON file
with open('data_list.json', 'r') as file:
    data_list = json.load(file)

# Use the data_list
#print(data_list)

installing_files = []
count = 50
download_dir = "C:\\Users\\artur.sahakyan\\Desktop\\all_doc"



def install_files(driver):
    global count, installing_files
    
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
            install_files(driver)

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
    install_files(driver)
    installing_files.clear()
    time.sleep(1)
    search_box.clear()


for contract_id in data_list:
    count = 0
    get_contract(contract_id)
    print(f"count for {contract_id} is {count}")
    new_folder_name = f"C:\\Users\\artur.sahakyan\\Desktop\\specific_contract_doc\\{contract_id}"
    move_files_to_new_folder(download_dir, new_folder_name)


driver.refresh()

time.sleep(2)

# Close the browser
driver.quit()

# need to clean the search box then do other search