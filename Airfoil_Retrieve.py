# Imported Functions
from bs4 import BeautifulSoup
import requests
import pandas as pd

# User Defined Functions
from Function_File import *

pd.set_option("display.max_rows", None, "display.max_columns", None)

# Enter your airfoils as strings        
chosen = ['fx76mp140', 'naca2421', 'e420', 's1223']
Reynolds = '1000000'
# chosen = ['fx76mp140']
# Base URL
Base_URL = 'http://airfoiltools.com'
# Retrieve airfoiltools html data
page = requests.get('http://airfoiltools.com/search/airfoils')
soup = BeautifulSoup(page.content, 'lxml')

# Retrieve all hyperlinks from html page, and then remove all that aren't for an airfoil
links_placehold =[]
for link in soup.find_all('a'):
    links_placehold.append(link.get('href'))
links = []
# String to select only airfoil links
approved = '/airfoil/details'
for airfoil in links_placehold:
    if approved in airfoil:
        links.append(airfoil)
airfoil_name = [] 
# Allows user to enter airfoil name with capitals and spaces
for choice in chosen:
    choice = choice.lower().replace(' ', '')
    for airfoil in links:
        if choice in airfoil.lower().replace(' ', ''):
            airfoil_name.append(airfoil)
# Allows user to double check that all the proper airfoils have been selected
# final_check = 'n'
# while final_check == 'n':
#     for i in range(len(airfoil_name)):
#         name = airfoil_name[i]
#         print(str(i) + ': ' + name[name.find('=') + len('='):name.rfind('-')])
#     check = input('Are there any airfoils to remove from the list? [y/n]\n')
#     if check == 'y':
#         remove = input('Please type the index of the airfoil you wsh to remove.\n')
#         airfoil_name.pop(int(remove))
#         print('The airfoil list is now: \n')
#         for i in range(len(airfoil_name)):
#             name = airfoil_name[i]
#             print(str(i) + ': ' + name[name.find('=') + len('='):name.rfind('-')])
#         final_check = input('Is this correct? [y/n]\n')
#     else:
#         break
            
 
# Retrieve data for each airfoil
for airfoil in airfoil_name:
    links2 = []
    polar = []
    selig = []
    lednicer = []
    URL = Base_URL + airfoil
    airfoil_page = requests.get(URL)
    soup2 = BeautifulSoup(airfoil_page.content, 'lxml')
    # Get all links on airfoil page
    for link in soup2.find_all('a'):
        links2.append(link.get('href'))
    for link in links2:
        # Retrieve Polar data
        if 'polar' and Reynolds in link and 'n5' not in link:
            polar.append(link)
        # Retrieve Lednicer file format
        if 'lednicerdatfile' in link:
            lednicer.append(link)
        # Retrieve Selig file format
        if 'seligdatfile' in link:
            selig.append(link)
    airfoil_name = airfoil.partition('=')[2]         
    # Save Selig .dat filetype
    selig_page = requests.get(Base_URL + selig[0])
    selig_data = selig_page.text
    save_file(airfoil_name, selig_data, 'selig')
    # Save Lednicer .dat filetype
    lednicer_page = requests.get(Base_URL + lednicer[0])
    lednicer_data = lednicer_page.text
    save_file(airfoil_name, lednicer_data, 'lednicer')

# Perform Calculations on each airfoil
#for file in text_files:
#    calc_camber(file)
    
        

# TODO Find lift and drag vs alpha data
# TODO Calculate camber line and plot airfoil -> Save as png
# TODO Thin airfoil theory and vortex panel solver
# TODO Plot lift and drag data -> Save as png