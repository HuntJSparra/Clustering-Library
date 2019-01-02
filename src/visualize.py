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