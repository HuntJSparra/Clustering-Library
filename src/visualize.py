#=======================================#
# Imports                               #
#=======================================#
# Python Imports
from bokeh.plotting import figure, show, output_file

# External Imports

# Iris Imports

#=======================================#
# Globals & Constants                   #
#=======================================#

__all__ = (
    'visualize_2d',
    'visualize_hca',
)

#=======================================#
# Public Methods                        #
#=======================================#

def visualize_2d(x, y, color, title='', x_axis_label='', y_axis_label=''):
    p = figure(title=title)
    p.xaxis.axis_label = x_axis_label
    p.yaxis.axis_label = y_axis_label

    p.circle(x, y, color=color)

    return p

def visualize_hca(hca_out, title=''):
    p = figure(title=title)

    for merged_clusters in hca_out:
        c1_center = sum(merged_clusters[0])/len(merged_clusters[0])
        c2_center = sum(merged_clusters[1])/len(merged_clusters[1])
        new_size = len(merged_clusters[0])+len(merged_clusters[1])
        xs = [c1_center, c1_center, c2_center, c2_center]
        ys = [len(merged_clusters[0])-1, len(merged_clusters[0])+len(merged_clusters[1])-1, len(merged_clusters[0])+len(merged_clusters[1])-1, len(merged_clusters[1])-1]
        p.line(xs, ys)

    return p