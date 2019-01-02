#=======================================#
# Imports                               #
#=======================================#
# Python Imports
import os

# External Imports
from bokeh.plotting import show, output_file
from bokeh.layouts import row

# Module Imports
from src.parser import *
from src.mining import *
from src.visualize import *

#=======================================#
# Globals & Constants                   #
#=======================================#

IRIS_TXT_PATH = os.path.join(os.getcwd(), 'Data', 'iris.txt')   # join() and getcwd() are used in order to support all OS
WINE_TXT_PATH = os.path.join(os.getcwd(), 'Data', 'wine.txt')

#=======================================#
# Public Methods                        #
#=======================================#

def sum_point(point: str):
    total = 0
    length = 0
    for index_str in point.split(','):
        total += int(index_str)
        length += 1
    return total/length

#=======================================#
# Code                                  #
#=======================================#
# Load data
data = parse_iris_txt(IRIS_TXT_PATH)
data_without_labels = data[1:]
data_without_species = [point[:-1] for point in data_without_labels]

# Cluster the data
kmeans_data = kmeans(data_without_species, 3)
kmedoids_data = kmedoids(data_without_species, 3)

# Output a pretty chart
x = [point[-3] for point in kmeans_data]
y = [point[-2] for point in kmeans_data]

colormap = ['green', 'blue', 'red']
kmeans_species = [colormap[int(point[-1])] for point in kmeans_data]
p_kmeans = visualize_2d(x, y, kmeans_species, title='kmeans', y_axis_label="Petal Width")

colormap = ['green', 'blue', 'red']
kmedoids_species = [colormap[int(point[-1])] for point in kmedoids_data]
p_kmedoids = visualize_2d(x, y, kmedoids_species, title='kmedoids', x_axis_label="Petal Length")

colormap = {'Iris-versicolor': 'green', 'Iris-virginica':'blue', 'Iris-setosa':'red'}
key_species = [colormap[point[-1]] for point in data_without_labels]
p_key = visualize_2d(x, y, key_species, title='key')

p = row(p_kmeans, p_kmedoids, p_key)

output_file('Out_Files/iris.html', title='Iris Example')

show(p)