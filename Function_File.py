import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np


def save_file(name, data, file_type):
    current_path = os.getcwd()

    # Create new folder
    new_folder = current_path + '/' + name
    data_folder = new_folder + '/data/'
    plot_folder = new_folder + '/plots/'
    if not os.path.exists(new_folder):
        os.makedirs(new_folder, exist_ok=True)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder, exist_ok=True)
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder, exist_ok=True)
    # Create save path for files
    output_file1 = os.path.join(data_folder, 'stripped_' + name + '_' + file_type + '.txt')
    output_file2 = os.path.join(data_folder, name + '_' + file_type + '.txt')
    airfoil_data = open(output_file1, 'w')
    airfoil_data.write(data.strip())
    airfoil_data.close()

    # Remove trailing and leading whitespace from each line
    with open(output_file1, 'r') as infile, open(output_file2, 'w') as outfile:
        for line in infile:
            outfile.write(line.strip() + '\n')
    os.remove(output_file1)
    return output_file2, new_folder, data_folder, plot_folder


def calc_camber(txt, num_points, name, folder):
    # Separate airfoil points data into top and bottom
    df = pd.read_csv(txt, sep='\s{1,}', header=None, skiprows=1, engine='python')
    df = df[[0, 1]]
    df.columns = list('XY')
    df_data = df.iloc[1:, :]
    df_data = df_data.astype(float)
    num1, decimal1 = str(df.at[0, 'X']).split('.')
    top_num = int(num1)
    num2, decimal2 = str(df.at[0, 'Y']).split('.')
    bottom_num = int(num2)
    df_top = df_data.head(top_num)
    df_bottom = df_data.tail(bottom_num)
    minimum = df_top['X'].min()
    maximum = df_top['X'].max()

    # Determine approximate camber line
    x_new = np.linspace(minimum, maximum, num=num_points, endpoint=True)
    top_new = interp1d(df_top['X'], df_top['Y'])
    bottom_new = interp1d(df_bottom['X'], df_bottom['Y'])
    camber = []
    for i in range(num_points):
        camber.append((top_new(x_new[i]) + bottom_new(x_new[i])) / 2)

    # Plot Airfoil
    plt.plot(df_top['X'], df_top['Y'], color='b', label='Airfoil')
    plt.plot(x_new, camber, color='r', label='Camber')
    plt.plot(df_bottom['X'], df_bottom['Y'], color='b')
    plt.ylim((-0.5, 0.5))
    plt.xlabel('x/c')
    plt.ylabel('y/c')
    plt.title(name[:-3])
    plt.legend(loc='best')
    plt.savefig(folder + '/' + name + '.png', bbox_inches='tight')
    plt.figure()
    # plt.show()
    return camber, top_new(x_new), bottom_new(x_new)

