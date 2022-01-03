import os
import pandas as pd


def save_file(name, data):
    current_path = os.getcwd()
    # Create new folder
    new_folder = current_path + '/' + name
    if not os.path.exists(new_folder):
        os.makedirs(new_folder, exist_ok=True)
    # Create save path for files
    output_file1 = os.path.join(new_folder, 'stripped_' + name + '.txt')
    output_file2 = os.path.join(new_folder, name + '.txt')
    airfoil_data = open(output_file1, 'w')
    airfoil_data.write(data.text.strip())
    airfoil_data.close()
    # Remove trailing and leading whitepsace from each line
    with open(output_file1, 'r') as infile, open(output_file2, 'w') as outfile:
        for line in infile:
            outfile.write(line.strip() + '\n')
    os.remove(output_file1)
    return output_file2


def calc_camber(txt):
    df = pd.read_csv(txt, sep='\s{1,}', header=None)
    df = df.iloc[1:, :]
    df = df.rename(columns={0:'X', 1:'Y'})
    df = df.drop(2, axis=1, errors='ignore')
    print(df)
