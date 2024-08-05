import csv
import time
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog


def get_user_input():
    word = None
    folder = None

    # Function to handle click event on folder select button
    def select_folder():
        nonlocal folder
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_path.set(selected_folder)
            folder = selected_folder

    # Function to handle OK button click event
    def on_ok():
        nonlocal word, folder
        word = entry_word.get()
        folder = folder_path.get()

        if word == '' or word is None:
            # Word input field is empty, display an error message.
            error_label.config(text="The 'Searched word' field is mandatory.", fg="red")
        else:
            # The word entry field is filled, close the window.
            root.destroy()

    # Create a Tkinter window
    root = tk.Tk()
    root.geometry("350x200+0+0")
    root.title("Search on maps")

    # Input field for folder path
    label_folder = tk.Label(root, text="Select a storage folder:")
    label_folder.pack()
    folder_path = tk.StringVar()
    entry_folder = tk.Entry(root, textvariable=folder_path, width=30) 
    entry_folder.pack()
    select_button = tk.Button(root, text="Select a folder", command=select_folder)
    select_button.pack()

    # Spacing between fields
    spacer = tk.Label(root, text="")
    spacer.pack()

    # Word input field
    label_word = tk.Label(root, text="Please enter the search word :")
    label_word.pack()
    entry_word = tk.Entry(root, width=30)
    entry_word.pack()

    # Create a label to display error messages
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    # Bind the Enter key to the on_ok function
    entry_word.bind("<Return>", lambda event=None: on_ok())

    # Bouton OK
    ok_button = tk.Button(root, text="OK", command=on_ok)
    ok_button.pack()

    # Set folder selection field as the first active field
    entry_folder.focus_set()

    # Start the main UI loop
    root.mainloop()

    return word, folder


def create_file_csv(lien):
    try:
        # Create a CSV file to store the data.
        with open(lien_fichier_csv, 'w', newline='', encoding='utf-8') as csv_file:
            csvw_riter = csv.writer(csv_file, delimiter=';') 

            # Write the CSV file header.
            csvw_riter.writerow(['Name', 'Note', 'Address', 'Phone', 'website'])
        return True
    except FileNotFoundError:
        return False


def get_user_data():
    # Calling the function to get the word and folder values
    word, folder = get_user_input()
    word = word.strip()
    folder = folder.strip()
    if folder == '' or folder is None:
        csv_file_link = word.replace(' ', '_') + '_' + str(int(time.time())) + '.csv'
    else:
        csv_file_link = folder.replace('/', '\\') + "\\" + word.replace(' ', '_') + '_' + str(int(time.time())) + '.csv'
    word_searched = word.replace(' ', '+')
    return word_searched, csv_file_link


motRecherche, lien_fichier_csv = get_user_data()

# Create a CSV file to store the data.
while True:
    if create_file_csv(lien_fichier_csv):
        break
    else:
        motRecherche, lien_fichier_csv = get_user_data()

# Make sure you have installed the version of ChromeDriver compatible with your version of Chrome.
# You can download it here: https://sites.google.com/chromium.org/driver/
# Replace the path below with the path to the downloaded chromedriver.exe file.
chrome_driver_path = "chromedrivers\\chromedriver.exe"

# Create a Service object with the executable_path option.
chrome_service = ChromeService(executable_path=chrome_driver_path)

# Use the service to initialize the Chrome driver.
driver = webdriver.Chrome(service=chrome_service)

# Use the driver to navigate to Google Maps.
driver.get("https://www.google.com/search?q=" + motRecherche)

time.sleep(5)  # Wait a bit for the results to load.

try:
    # Click on "Other addresses" to give all the results (200: 20 per page).
    retoure_script = driver.execute_script(""" 
    var elements = document.querySelectorAll("a");
    // Cycle through the items to find the one with the text "Other addresses"
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].textContent === "Other addresses") {
        // Click on the element found,
        elements[i].click();
        return true;
        break; // Exit the loop once the element is found

        }
    }
    return false;
    """)
except:
    print("! Error :  Click on 'Other addresses'")
    input()

if retoure_script is False:
    print("! Error :  No address found")
    input()

time.sleep(5)  # Wait a bit for the page to load.

# XPath for list of results.
results_xpath = '//a[@class="vwVdIc wzN8Ac rllt__link a-no-hover-decoration"]'

# initialization of variables
anc_telephone = "xxxxxxxxxx"
t_s_p = 0  # time sleep +
premierNom = ''
num_page = 0
l_data = []

while True:  # 'while True' 1
    # Open the results list on the currently visible page.
    results = driver.find_elements(By.XPATH, results_xpath)
    len_results = results.__len__()
    num_page += 1
    print(f'Page {num_page} :')

    # Browse the results and collect the data.
    for i in range(len_results):
        print(f"  {i + 1}")
        while True:  # 'while True' 2
            result = results[i]

            # # #  Click on the element with index i, then extract the data
            try:
                # Click the element using JavaScript to avoid click errors.
                driver.execute_script("arguments[0].scrollIntoView();", result)
                driver.execute_script("arguments[0].click();", result)
                time.sleep(3 + t_s_p)  # Wait a little more for the page to load.
            except:
                if t_s_p == 0:
                    print(f"\t! Error  :  Click on the element {i + 1}", end=" ")
                else:
                    print(".", end=" ")
                time.sleep(3)
                t_s_p += 1
                if t_s_p <= 20:
                    continue  # 'while True' 2
                else:
                    break  # 'while True' 2
            if t_s_p > 0:
                t_s_p = 0
                print()

            # # #  Extract name
            try:
                nom = driver.execute_script(
                    """ return document.querySelector('h2[data-dtype="d3ifr"]').textContent.replace(';', ','); """)
            except:
                try:
                    nom = driver.execute_script(
                        """ return arguments[0].querySelector('span').textContent.replace(';', ','); """, result)
                except:
                    if t_s_p == 0:
                        print("\t! Error  : there is no 'name'", end=' ')
                    else:
                        print(".", end=" ")
                    time.sleep(3)
                    t_s_p += 1
                    if t_s_p <= 20:
                        continue  # 'while True' 2
                    else:
                        nom = ''
                        print("\t! Error  :  there is no 'name'")
            if t_s_p > 0:
                t_s_p = 0
                print()
            if i == 0:
                premierNom = nom
            if nom != '':
                print("\tTéléphone : ", nom)

            # # #  Extract the phone
            try:
                telephone = driver.execute_script(
                    """ return document.querySelector('span[aria-label*="Appeler"]').textContent; """)
                if telephone == anc_telephone:
                    if t_s_p == 0:
                        print("\t! Error  : 'telephone' repeats", end=' ')
                    else:
                        print(".", end=" ")
                    time.sleep(3)
                    t_s_p += 1
                    if t_s_p <= 20:
                        continue  # 'while True' 2
                    else:
                        if nom == l_data[0]:
                            break  # 'while True' 2
                        else:
                            pass
                else:
                    anc_telephone = telephone
            except:
                telephone = ''
                print("\t! Error  : there is no telephone'")
            if t_s_p > 0:
                t_s_p = 0
                print()
            if telephone != '':
                print("\tTéléphone : ", telephone)

            # # #  Extract note
            try:
                note = driver.execute_script(""" return document.querySelector('div[class="CJQ04"]').textContent; """)
                print("\tNote : ", note)
            except:
                note = ''
                print("\t! Error  :  there is no 'note'")

            # # #  Extract address
            try:
                adresse = driver.execute_script(
                    """ return document.querySelector('span[class="LrzXr"]').textContent.replace(';', ','); """)
                print("\tAdresse : ", adresse)
            except:
                adresse = ''
                print("\t! Error  :  there is no \"address\"")

            # # #  Extract website
            try:
                siteWeb = driver.execute_script(
                    """ return document.querySelector('a[class="mI8Pwc"]').getAttribute("href"); """)
                print("\tSiteWeb : ", siteWeb)
            except:
                siteWeb = ''
                print("\t! Error  : there is no website")

            # # #  Write the data to the CSV file.
            l_data = [nom, note, adresse, telephone, siteWeb]
            with open(lien_fichier_csv, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(l_data)

            # End of element extraction
            break  # 'while True' 2

    for i in range(60):
        # # #  Click "Next" to give the next 20 results.
        try:
            driver.execute_script('document.getElementById("pnnext").click();')
        except:
            if t_s_p == 0:
                print("! Error  :  Cliquer sur 'Suivant'", end=' ')
                t_s_p = 1  # Wait a little more for the page to load.
            else:
                print(".", end=" ")
            time.sleep(5)
            continue  # for i in range(200):
        t_s_p = 0
        time.sleep(5)  # Wait a bit for the page to load.

        # # # check if the following list is displayed
        try:
            nom = driver.execute_script(
                """ return document.querySelector('a[role="link"]').querySelector('span').textContent.replace(';', ','); 
                """)
            if premierNom != nom:
                t_s_p = 0
                break  # for i in range(200):
            else:
                if t_s_p == 0:
                    print("! Error  :  Click on 'Next' (stays on the old list)", end=' ')
                    t_s_p = 1  ## Wait a little more for the page to load.
                else:
                    print(".", end=" ")
                time.sleep(5)
                continue  # for i in range(200):
        except:
            if t_s_p == 0:
                print("! Error  :  empty page", end=' ')
            else:
                print(".", end=" ")
            t_s_p = 1
            time.sleep(5)
            continue  # for i in range(200):
        t_s_p = 0

    # if it gets to page 11 then no other results.
    if num_page >= 10:
        print("\n$$$$$ Fin $$$$$")
        break  # 'while True' 1

    if t_s_p == 1:
        print("\nProblem displaying Next list")
        input()
        break  # 'while True' 1

time.sleep(3)
# Close the browser when finished.
driver.quit()

input()
