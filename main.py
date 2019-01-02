#=======================================#
# Imports                               #
#=======================================#
# Python Imports
import os

# External Imports
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row

# Module Imports
from src.parser import *
from src.mining import *

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
clustered_data = kmeans(data_without_species, 3)

# Output a pretty chart
p1_x = [point[-3] for point in clustered_data]
p1_y = [point[-2] for point in clustered_data]

# For coloring
colormap = ['green', 'blue', 'red']
p1_species = [colormap[int(point[-1])] for point in clustered_data]

p1 = figure(title = "K=3 Clustered Iris")
p1.xaxis.axis_label = 'Petal Length'
p1.yaxis.axis_label = 'Petal Width'

p1.circle(p1_x, p1_y, color=p1_species)

# Key
colormap = {'Iris-versicolor': 'green', 'Iris-virginica':'blue', 'Iris-setosa':'red'}
p2_species = [colormap[point[-1]] for point in data_without_labels]

p2 = figure(title = "Actual Iris")
p2.xaxis.axis_label = 'Petal Length'
p2.yaxis.axis_label = 'Petal Width'

p2.circle(p1_x, p1_y, color=p2_species)

p = row(p1, p2)

output_file("Out_Files/iris.html", title="Iris Example")

show(p)