#=======================================#
# Imports                               #
#=======================================#
# Python Imports
import csv

# External Imports

# Iris Imports

#=======================================#
# Globals & Constants                   #
#=======================================#

__all__ = (
    'parse_iris_txt',
    'parse_drug_csv',
    'parse_wine_txt',
)

#=======================================#
# Public Methods                        #
#=======================================#

def parse_iris_txt(path: str):
    """
    Parses a the file on the given path. Only works for iris.txt
    with the format of sepal length, sepal width, petal length,
    petal width, and species
    Ex. row/line:
        '6.3,3.4,5.6,2.4,Iris-virginica'
    Args:
        path: path to file to load
    Returns:
        A 2d list with the first row being the labels and
        every other being an iris entry of the format
        [sepal length: str, sepal width: float, petal length: float, petal width: float, species: str]
    """
    iris_data = [['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width', 'Species']] # Initialize return data and add labels
    with open(path, 'r') as file:
        for line in file:
            line = line.replace('\n', '') # The end of the line is \n and will be reflected on the split if not removed
            row = line.split(',') # Split on comma to get
            # Convert strings to floats (excluding species at index 4)
            for count, value in enumerate(row):
                if count < 4:
                    row[count] = float(value)
            iris_data.append(row) # Add new entry to data

    return iris_data

def parse_drug_csv(path: str):
    drug_data = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            row = []
            for count, element in enumerate(line[6:]):
                if count < 7:
                    element = float(element)
                row.append(element)
            drug_data.append(row)
    return drug_data

def parse_wine_txt(path: str):
    wine_data = [['Alcohol', 'Malic Acid', 'Ash', 'Alcalinity of Ash', 'Magnesium', 'Magnesium', 'Total Phenols', 'Flavanoids', 'Nonflavanoid Phenols', 'Proanthocyanins', 'Color Intensity', 'Hue', 'OD280/OD315 of Diluted Wines', 'Proline']] # Initialize return data and add labels
    with open(path, 'r') as file:
        for line in file:
            line = line.replace('\n', '') # The end of the line is \n and will be reflected on the split if not removed
            row = line.split(',') # Split on comma to get
            # Convert strings to floats (excluding species at index 4)
            for count, value in enumerate(row):
                if count == 0:
                    row[count] = int(value)
                else:
                    row[count] = float(value)
            wine_data.append(row) # Add new entry to data

    return wine_data