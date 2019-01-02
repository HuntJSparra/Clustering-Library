#=======================================#
# Imports                               #
#=======================================#
# Python Imports
from copy import deepcopy
import csv
import os

# External Imports
from bokeh.io import show
from bokeh.io import output_file as bokeh_output_file
from bokeh.layouts import gridplot, row, column
from bokeh.palettes import Category20
from bokeh.plotting import figure

from sklearn.decomposition import PCA

# Module Imports
from src.parser import *
from src.mining import *

#=======================================#
# Globals & Constants                   #
#=======================================#

IRIS_TXT_PATH = os.path.join(os.getcwd(), 'Data', 'iris.txt')   # join() and getcwd() are used in order to support all OS
WINE_TXT_PATH = os.path.join(os.getcwd(), 'Data', 'wine.txt')
DRUG_CSV_PATH = os.path.join(os.getcwd(), 'Data', 'DrugConsumptionDataset.csv')

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
data = parse_drug_csv(DRUG_CSV_PATH)
class_removed_data = [row[:7] for row in data]

# Visualize Knee
bokeh_output_file(os.path.join(os.getcwd(), 'Graphs', 'knee_plots.html'))

# Data obtained from manually printing the results of runs of kmeans with different ks
knee_data = [[1, 0.0, 12836.058208647175, 0.0],
             [2, 0.7227260110762826, 11457.39422109651, 6.307943997820434e-05],
             [3, 1.218053261010091, 10756.594107778676, 0.00011323781940691159],
             [4, 1.4780378235960874, 10812.435509170442, 0.0001366979550853743],
             [5, 1.9710181052783824, 10360.843532598084, 0.0001902372233570571],
             [6, 2.264649563387941, 9861.0995396334, 0.00022965487309867805],
             [7, 2.784063078674442, 9770.548879669152, 0.0002849443887914632],
             [8, 3.332479008233955, 9851.243147776342, 0.0003382800483395006],
             [9, 5.858647316441963, 10838.184708633646, 0.0005405561423745613],
             [10, 5.785179029908228, 10422.696631222, 0.0005550558780132076],
             [11, 6.878385250656451, 10802.300253987054, 0.0006367519036621562],
             [12, 6.452174029884275, 8295.100557044972, 0.0007778295133992664],
             [13, 5.458982952516738, 7590.866507005598, 0.000719151489158537],
             [14, 38.2918002333837, 14082.452124117028, 0.002719114533171871],
             [15, 38.35582058897618, 12538.773810041126, 0.003058976991694404],
             [16, 38.78518709377855, 11905.940136187683, 0.0032576333032191514],
             [17, 34.71976504654846, 11493.406194834773, 0.003020842077447136],
             [18, 35.050562045954344, 11099.495822631043, 0.0031578517264260657],
             [19, 37.08238011226788, 9106.56401025597, 0.004072049575504555],
             [20, 35.76930224176117, 9014.389606145109, 0.003968022662053262],
             [21, 42.70716198567294, 9465.791520154935, 0.004511737015836359],
             [22, 43.268839015265115, 9479.919610205716, 0.004564262229469072],
             [23, 45.29646961822894, 8984.295030705898, 0.005041738885846672],
             [24, 124.06145648613916, 16836.302444297864, 0.007368687804022933],
             [25, 128.9656448708828, 17507.557980320373, 0.007366284036634266],
             [26, 127.0996781392646, 17891.979537659015, 0.007103723647332893],
             [27, 118.88705335853764, 15984.888917051767, 0.007437465094406488],
             [28, 115.46498888420585, 15438.03009445243, 0.007479256626510759],
             [29, 126.5513764596076, 16728.6947595072, 0.007564928303069568],
             [30, 125.22770872866242, 15904.437404025528, 0.007873759099266622]]

# Xs
knee_inter = [row[1] for row in knee_data]
knee_intra = [row[2] for row in knee_data]
knee_both = [row[3] for row in knee_data]

# Ys
knee_k = [row[0] for row in knee_data]

knee_inter_plot = figure(title="Interspread", plot_width=300, plot_height=300)
knee_inter_plot.xaxis.axis_label = "Interspread"
knee_inter_plot.yaxis.axis_label = "K"
knee_inter_plot.line(knee_inter, knee_k)

knee_intra_plot = figure(title="Intraspread", plot_width=300, plot_height=300)
knee_intra_plot.xaxis.axis_label = "Intraspread"
knee_intra_plot.yaxis.axis_label = "K"
knee_intra_plot.line(knee_intra, knee_k)

knee_both_plot = figure(title="Inter/Intra", plot_width=300, plot_height=300)
knee_both_plot.xaxis.axis_label = "Interspread/Interspread"
knee_both_plot.yaxis.axis_label = "K"
knee_both_plot.line(knee_both, knee_k)

show(column(row(knee_inter_plot, knee_intra_plot), knee_both_plot))

# Show dendrogram
d_data = hca_visual(class_removed_data)

bokeh_output_file(os.path.join(os.getcwd(), 'Graphs', 'dendrogram.html'))

d_y = []
d_x = []

# y_tracker = {}

for count, row in enumerate(d_data):
    try:
        old_y0 = y_tracker[row[0]]
    except:
        old_y0 = 0

    try:
        old_y1 = y_tracker[row[1]]
    except:
        old_y1 = 0

    # d_y.append([old_y0, count+1])
    # d_y.append([old_y1, count+1])
    new_y = len(row[0].split(','))+len(row[1].split(','))-1
    d_y.append([len(row[0].split(','))-1, new_y])
    d_y.append([len(row[1].split(','))-1, new_y])

    # y_tracker[row[0]+','+row[1]] = count+1

    # Calculate where to put the point
    mid_point = sum_point(row[0]+','+row[1])
    d_x.append([sum_point(row[0]), mid_point])
    d_x.append([sum_point(row[1]), mid_point])

d_plot = figure(title="Dendrogram", plot_width=1000, plot_height=1000)
d_plot.yaxis.axis_label = "Cluster Size"
d_plot.multi_line(d_x, d_y)

show(d_plot)

# Get statistics
results = [] # To store results

for func in [kmeans, kmedoids, hca]:
    kmeans_data = func(class_removed_data, 13)
    results.append(kmeans_data)
    with open('Out_Files/'+func.__name__+'_data'+'.csv', 'w') as output_file:
        output_writer = csv.writer(output_file)
        for row in kmeans_data:
            output_writer.writerow(row)

    all_vals = {
                'Alcohol':   {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Amphet':    {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Amyl':      {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Benzos':    {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Caff':      {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Cannabis':  {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Choc':      {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Coke':      {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Crack':     {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Ecstasy':   {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Heroin':    {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Ketamine':  {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Legalh':    {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'LSD':       {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Meth':      {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Mushrooms': {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Nicotine':  {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'Semer':     {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},
                'VSA':       {'CL0':0,'CL1':0,'CL2':0,'CL3':0,'CL4':0,'CL5':0,'CL6':0,},}

    group_to_key = ['Group '+str(val)+':' for val in range(1,14)]
    group_size = [0 for val in range(1,14)]

    group_statistics = {}
    for key in group_to_key:
        group_statistics[key] = deepcopy(all_vals)

    point_to_key = ['Alcohol', 'Amphet', 'Amyl', 'Benzos', 'Caff', 'Cannabis', 'Choc', 'Coke', 'Crack', 'Ecstasy', 'Heroin', 'Ketamine', 'Legalh', 'LSD', 'Meth', 'Mushrooms', 'Nicotine', 'Semer', 'VSA']

    for point in kmeans_data:
        for original_point in data:
            if original_point[:7] == point[:-1]:
                class_data = original_point[7:]
                for val_count, val in enumerate(class_data):
                    group_statistics[group_to_key[int(point[-1])]][point_to_key[val_count]][class_data[val_count]] += 1
                group_size[int(point[-1])] += 1
                break

    for count, group in enumerate(group_statistics):
        for substance in group_statistics[group]:
            for classification in group_statistics[group][substance]:
                if group_size[count] == 0:
                    group_statistics[group][substance][classification] = -1
                else:
                    group_statistics[group][substance][classification] /= group_size[count]

    with open('Generated_Files/'+func.__name__+'_data_statistics.txt', 'w') as file:
        for group_key, group in group_statistics.items():
            file.write(group_key+'\n')
            for substance_key, classifications in group.items():
                out = '\t'+substance_key+':'+' '*(10-len(substance_key))
                for class_key, class_val in classifications.items():
                    out += '\t'+class_key+': '+"{0:.5f}".format(class_val)
                file.write(out+'\n')

    print('Finished ',func.__name__)

# Visualize Groups
bokeh_output_file(os.path.join(os.getcwd(), 'Graphs', 'clusters.html'))
figure_labels = ["K-Means", "K-Medoids", "HCA"]
figures = []
for count, result in enumerate(results):
    pca = PCA(n_components=2)
    data = [row[:-1] for row in result]
    pca.fit(data)
    pca = pca.transform(data)

    colormap = [Category20[13][int(row[-1])] for row in result]

    test_plot = figure(title=figure_labels[count], plot_width=300, plot_height=300)
    test_plot.xaxis.axis_label = "Principal Component 1"
    test_plot.yaxis.axis_label = "Principal Component 2"
    test_plot.circle(pca[:,0], pca[:,1], color=colormap)

    figures.append(test_plot)

show(gridplot(figures, ncols=2))