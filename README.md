# Aero_Py
Aero_Py is a tool to aid in the process of selecting and validating an airfoil. The file works by first using BeautifulSoup to scrape [airfoiltools](airfoiltools.com) and fetch data about all the airfoils that the user has selected. It will then generate and save plots for the following. It will validate the lift and moment data using thin airfoil theory, and plot these curves alongside the fetched data. 
- Cl Vs Alpha
- Cd Vs Alpha
- Cm Vs Alpha
- Cl/CD Vs Alpha
- Cl Vs Cd
It will also calculate coordinates for the camber line. Then it will save text files of the camber line and of both the lednicer and selig format files for the airfoil coordinates. It will also save a csv file of the aerodynamic data fetched from [airfoiltools](airfoiltools.com), as well as that calculated. It will create a folder for each airfoil selected, as well as subfolders for the data and the plots that are saved. 
## How to use
The following steps are taken to use Aero_Py. 
1. Clone or download the files and place them in the desired directory.
2. Edit chosen to reflect the airfoils that you wish to analyze. 
3. Select the desired Reynolds number. The available Reynolds numbers can be found in the comment beside the Reynolds variable. 
4. If the user desires they can change the number of points the airfoil will be approximated by, as well as the step size for the numerical differentiation. However, this is not required. 
5. Follow the prompts to double check the airfoil. Take care to follow the prompts properly, as improper entering of data can cause the program to error. If the airfoil you have desired does not appear in the list, double check that the name is entered properly, and check how it appears on [airfoiltools](airfoiltools.com). 
6. Wait for the program to finish. Once the program is finished, all of the airfoil data will be found in the same directory as the python files. 
