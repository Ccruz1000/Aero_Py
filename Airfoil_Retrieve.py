# Imported Functions
from bs4 import BeautifulSoup
import requests
import pandas as pd

# User Defined Functions
from Function_File import *
from Thin_Airfoil import thin_airfoil

chosen = ['fx76mp140', 'e420', 's1223', 'naca2421', 'naca0012']  # Enter your airfoils as strings
Reynolds = '1000000'  # Select Reynolds number ('50000', '100000', '200000', '500000', '1000000')
num_points = 150  # Select how many points to approximate airfoil with
h = 0.001  # Select step size for numerical differentiation
# Base URL
Base_URL = 'http://airfoiltools.com'
# Retrieve airfoiltools html data
page = requests.get('http://airfoiltools.com/search/airfoils')
soup = BeautifulSoup(page.content, features='html.parser')

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
airfoil_name = remove_airfoil(airfoil_name)

# Retrieve data for each airfoil
for airfoil in airfoil_name:
    # Initiate arrays
    links2 = []
    links3 = []
    polar = []
    selig = []
    lednicer = []
    URL = Base_URL + airfoil
    airfoil_page = requests.get(URL)
    soup2 = BeautifulSoup(airfoil_page.content, features='html.parser')
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
    airfoil_name = airfoil_name[:-3]
    # Save Selig .dat filetype
    selig_page = requests.get(Base_URL + selig[0])
    selig_data = selig_page.text
    save_file(airfoil_name, selig_data, 'selig')
    # Save Lednicer .dat filetype
    lednicer_page = requests.get(Base_URL + lednicer[0])
    lednicer_data = lednicer_page.text
    file, new_folder, data_folder, plot_folder = save_file(airfoil_name, lednicer_data, 'lednicer')
    x_coord, camber, top, bottom = calc_camber(file, num_points, airfoil_name, plot_folder)
    # Save camber line
    camber_line = pd.DataFrame({'X' : x_coord, 'Y': camber})
    np.savetxt(data_folder + '/' + airfoil_name + '_camber_line.txt', camber_line.values, fmt='%f')
    # Save Polar file
    polar_page = requests.get(Base_URL + polar[0])
    soup3 = BeautifulSoup(polar_page.content, features='html.parser')
    for link in soup3.find_all('a'):
        links3.append(link.get('href'))
    for link in links3:
        if 'csv' in link:
            csv = Base_URL + link
    df = pd.read_csv(csv, skiprows=10)
    df.to_csv(data_folder + '/' + airfoil_name + '_XFOIL_Data' + '.csv', index=False, encoding='utf-8-sig')
    # Initiate Plotting Arrays
    calc_cl = []
    calc_cm = []
    # Calculate lift and moment coefficient
    for alpha in df['Alpha']:
        cl, cm = thin_airfoil(alpha, camber, x_coord, h)
        calc_cl.append(cl)
        calc_cm.append(cm)

    # Create plots to compare with calculated data
    # Lift plot
    plt.plot(df['Alpha'], calc_cl, color='r', label='Thin Airfoil CL')
    plt.plot(df['Alpha'], df['Cl'], color='b', label='XFoil CL')
    plt.legend(loc='best')
    plt.xlabel('Alpha (Deg)')
    plt.ylabel('CL')
    plt.title('Lift Curve')
    plt.savefig(plot_folder + '/' + airfoil_name + '_Lift_Curve.png', bbox_inches='tight')
    plt.close('all')
    # plt.show()
    # Moment plot
    plt.plot(df['Alpha'], calc_cm, color='r', label='Thin Airfoil CM')
    plt.plot(df['Alpha'], df['Cl'], color='b', label='XFoil CM')
    plt.legend(loc='best')
    plt.xlabel('Alpha (Deg)')
    plt.ylabel('CM')
    plt.title('Moment Curve')
    plt.savefig(plot_folder + '/' + airfoil_name + '_Moment_Curve.png', bbox_inches='tight')
    plt.close('all')
    # plt.show()
    # Drag Polar
    plt.plot(df['Cd'], df['Cl'], color='b')
    plt.xlabel('CD')
    plt.ylabel('CL')
    plt.title('Drag Polar')
    plt.savefig(plot_folder + '/' + airfoil_name + '_Drag_Polar.png', bbox_inches='tight')
    plt.close('all')
    # plt.show()
    # Drag plot
    plt.plot(df['Cl'], df['Cd'], color='b')
    plt.xlabel('Alpha (Deg)')
    plt.ylabel('CD')
    plt.title('Drag Curve')
    plt.savefig(plot_folder + '/' + airfoil_name + '_Drag_Curve.png', bbox_inches='tight')
    plt.close('all')
    # plt.show()
    # L/D Ratio plot
    plt.plot(df['Alpha'], df['Cl']/df['Cd'], color='b')
    plt.xlabel('Alpha (Deg)')
    plt.ylabel('CL/CD')
    plt.title('Lift to Drag Curve')
    plt.savefig(plot_folder + '/' + airfoil_name + '_Lift_to_Drag.png', bbox_inches='tight')
    plt.close('all')
    # plt.show()


# TODO create vortex panel solver, and plot vortex panel data