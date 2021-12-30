from bs4 import BeautifulSoup
import requests
import re

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
# Enter your airfoils as strings        
chosen = ['fx76mp140', 'naca2421', 'e420']
airfoil_name = [] 
# Allows user to enter airfoil name with capitals and spaces
for choice in chosen:
    choice = choice.lower().replace(' ', '')
    for airfoil in links:
        if choice in airfoil.lower().replace(' ', ''):
            airfoil_name.append(airfoil)
# Retrieve data for each airfoil
for airfoil in airfoil_name:
    URL = Base_URL + airfoil
    airfoil_page = requests.get(URL)
    soup2 = BeautifulSoup(airfoil_page.content, 'lxml')
    # Find XFOIL data for Re = 1 million for airfoil
    airfoil_links = []
    dat_link = []
    dat = soup2.find('td', class_='cell2')
    airfoil_data = open(airfoil.partition('=')[2] + ".txt", "w")
    n = airfoil_data.write(dat.text.strip())
    airfoil_data.close()
    print(dat.text)
        

        # Save .dat link
        # Link for airfoil data found at line 383