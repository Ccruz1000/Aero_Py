# Imported Functions
from bs4 import BeautifulSoup
import requests

# User Defined Functions
from Function_File import *


# Enter your airfoils as strings        
chosen = ['fx76mp140', 'naca2421', 'e420', 's1223']
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
final_check = 'n'
while final_check == 'n':
    for i in range(len(airfoil_name)):
        name = airfoil_name[i]
        print(str(i) + ': ' + name[name.find('=') + len('='):name.rfind('-')])
    check = input('Are there any airfoils to remove from the list? [y/n]\n')
    if check == 'y':
        remove = input('Please type the index of the airfoil you wsh to remove.\n')
        airfoil_name.pop(int(remove))
        print('The airfoil list is now: \n')
        for i in range(len(airfoil_name)):
            name = airfoil_name[i]
            print(str(i) + ': ' + name[name.find('=') + len('='):name.rfind('-')])
        final_check = input('Is this correct? [y/n]\n')
    else:
        break
            
            
text_files = [] 
# Retrieve data for each airfoil
for airfoil in airfoil_name:
    URL = Base_URL + airfoil
    airfoil_page = requests.get(URL)
    soup2 = BeautifulSoup(airfoil_page.content, 'lxml')
    # Save .dat data file to text file
    dat = soup2.find('td', class_='cell4')
    print(dat.prettify())
 #   airfoil_data = airfoil.partition('=')[2]
    # Create folder for each airfoil
 #   name = save_file(airfoil_data, dat)
 #   text_files.append(name)

# Perform Calculations on each airfoil
#for file in text_files:
#    calc_camber(file)
    
        

# TODO Find lift and drag vs alpha data
# TODO Calculate camber line and plot airfoil -> Save as png
# TODO Thin airfoil theory and vortex panel solver
# TODO Plot lift and drag data -> Save as png