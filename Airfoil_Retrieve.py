from bs4 import BeautifulSoup
import requests

# Retrieve airfoiltools html data
page = requests.get('http://airfoiltools.com/search/airfoils')
soup = BeautifulSoup(page.content, 'html.parser')

# Retrieve all hyperlinks from html page, and then remove all that aren't for an airfoil
links_hold =[]
for link in soup.find_all('a'):
    links_hold.append(link.get('href'))
links = []
# String to select only airfoil links
approved = '/airfoil/details'
for airfoil in links_hold:
    if approved in airfoil:
        links.append(airfoil)
print(links[1255])
chosen = input('Input your airfoil:\n')
chosen = chosen.lower().replace(' ', '')
print(chosen)
airfoil_name = []
for airfoil in links:
    if chosen in airfoil.lower():
        airfoil_name.append(airfoil)

print(airfoil_name)