#=======================================#
# Imports                               #
#=======================================#
# Python Imports
import math
import random

from typing import TypeVar

# External Imports
import numpy as np

# Iris Imports

#=======================================#
# Globals & Constants                   #
#=======================================#

RANDOM_SEED = 500

ListLike = TypeVar('ListLike', list, np.ndarray)

__all__ = (
    'kabsclust',
    'kmeans',
    'kmedoids',
    'hca',
    'hca_visual',
)

#=======================================#
# Public Methods                        #
#=======================================#

def kabsclust(data: list, groups: int, cluster):
    """
    Applies an abstracted clustering algorithm on data.
    KMeans Algorithm:
        1) Select k random points to be centers
        2) Group points to the centers
        3) Per group, set the center based on the passed function's criteria
        4) Repeat from (2) until a predetermined break
    Args:
        data: A 2d list with rows containing data points as
              numbers (either float or int)
        groups: K, or the number of groups the calculate in
                kmeans
    Returns:
        Returns the input data, but with a new row for group added at the beginning:
        [sepal length: str, sepal width: float, petal length: float, petal width: float, group: int]
    """
    _setup_random() # Set randomseed for consistency

    data = np.array(data) # Convert data from 2d list to 2d numpy array for easy calculation of data ranges

    # Generate centers
    centers=[]
    maximums = np.max(data, axis=0) # Find maximums for every column
    minimums = np.min(data, axis=0) # Find minimums for every column
    for num in range(0, groups): # For every group
        new_center = [] # Create a new center
        for count, value in enumerate(data[0]): # and for every column in data
            new_center.append(random.random()*(maximums[count]-minimums[count])+minimums[count]) # create a new coordinate for that center between the column's min and max
        centers.append(new_center)

    data = np.insert(data, len(data[0]), 0, axis=1) # Add column for groups

    # Begin loop of recalculating clusters and their centers
    remaining_passes = 12
    while (remaining_passes >= 0):
        remaining_passes -= 1
        data, centers = cluster(data, centers)

    return data.tolist() # Reconvert numpy array to list before returning

def kmeans(data: list, groups: int):
    """
    Applies the kmeans algorithm on data.
    KMeans Algorithm:
        1) Select k random points to be centers
        2) Group points to the centers
        3) Per group, set the center to be the mean center
           of the grouped points
        4) Repeat from (2) until a predetermined break
    Args:
        data: A 2d list with rows containing data points as
              numbers (either float or int)
        groups: K, or the number of groups the calculate in
                kmeans
    Returns:
        Returns the input data, but with a new row for group added at the beginning:
        [sepal length: str, sepal width: float, petal length: float, petal width: float, group: int]
    """
    def cluster(data: ListLike, centers: ListLike):
        # Group data by seeing which center the points are closest to
        for point in data:
            closest_center = -1
            closest_distance = float('inf') # Initialize closest values to be invalid (since _distance always returns a real number, it will be overwritten)
            for count, center in enumerate(centers): # For every center
                distance = _distance(point[:-1], center) # Calculate distance, removing the group column from point
                if distance < closest_distance: # If closer, then replace
                    closest_distance = distance
                    closest_center = count
            point[-1] = closest_center # Assign group (last index) to the closest

        # Calculate new centers
        new_centers = []
        for group in range(0, len(centers)): # For each group
            grouped_rows = data[data[:, -1] == group][:, :-1] # Get all the rows for that group, again removing the group column; see boolean indexing in Python for more info

            if len(grouped_rows) == 0: # If the center is "orphaned" (i.e. does not have any points that are closest to it)
                new_centers.append(centers[group]) # Keep the current center
            else:
                new_centers.append(_calculate_center(grouped_rows)) # Calculate the actual center for the data of that group

        return data, new_centers

    return kabsclust(data, groups, cluster) # Reconvert numpy array to list before returning

def kmedoids(data: list, groups: int):
    """
    Applies the kmedoids algorithm on data.
    KMeans Algorithm:
        1) Select k random points to be centers from the current data points
        2) Group points to the centers
        3) Per group, set the new center to be the point that minimizes
           the distance between all points
        4) Repeat from (2) until a predetermined break
    Args:
        data: A 2d list with the first row being labels and
              the remaining rows containing data points as
              numbers (either float or int)
        groups: K, or the number of groups the calculate in
                kmeans
    Returns:
        Returns the input data, but with a new row for group added at the beginning:
        [group: int, sepal length: str, sepal width: float, petal length: float, petal width: float, species: str]
    """
    def cluster(data: ListLike, centers: ListLike):
        # Group data by seeing which center the points are closest to
        for point in data:
            closest_center = -1
            closest_distance = float('inf') # Initialize closest values to be invalid (since _distance always returns a real number, it will be overwritten)
            for count, center in enumerate(centers): # For every center
                distance = _distance(point[:-1], center) # Calculate distance, removing the group column from point
                if distance < closest_distance: # If closer, then replace
                    closest_distance = distance
                    closest_center = count
            point[-1] = closest_center # Assign group (last index) to the closest

        # Calculate new centers
        new_centers = []
        for group in range(0, len(centers)): # For each group
            grouped_rows = data[data[:, -1] == group][:, :-1] # Get all the rows for that group, again removing the group column; see boolean indexing in Python for more info
            new_centers.append(_calculate_center_datapoint(grouped_rows)) # Calculate the actual center for the data of that group

        centers = new_centers

        return data, centers

    return kabsclust(data, groups, cluster) # Reconvert numpy array to list before returning

def hca(data: list, groups: int):
    # Generate Matrix
    distance_matrix = {}
    for row, datapoint in enumerate(data):
        distance_matrix[str(row)] = {}
        for other_row, other_datapoint in enumerate(data):
            if row == other_row:
                continue
            distance_matrix[str(row)][str(other_row)] = _distance(datapoint, other_datapoint)

    while len(distance_matrix) > groups:
        # Get closest pair
        point_A = '-1'
        point_B = '-1'
        closest_distance = float('inf')
        for key_A, distance_dict in distance_matrix.items():
            for key_B, distance in distance_dict.items():
                if distance < closest_distance:
                    point_A = key_A
                    point_B = key_B
                    closest_distance = distance

        # Cluster the two and update the matrix
        # Replace distance_matrix[point_A] and distance_matrix[point_B] with distance_matrix[point_A+','+point_B]
        new_key = point_A+','+point_B
        distance_matrix[new_key] = {}
        for key in distance_matrix[point_A]:
            if key == point_A or key == point_B:
                continue
            distance_matrix[new_key][key] = (distance_matrix[point_A][key]+distance_matrix[point_B][key])/2

        # Delete old information
        for key in distance_matrix[point_A]:
            if key == point_A or key == point_B:
                continue
            del distance_matrix[key][point_A]
            del distance_matrix[key][point_B]
            distance_matrix[key][new_key] = distance_matrix[new_key][key]
        del distance_matrix[point_A]
        del distance_matrix[point_B]

    data = np.array(data)
    data = np.insert(data, len(data[0]), 0, axis=1) # Add column for groups
    for group, key in enumerate(distance_matrix):
        # Turn key back into group
        for index in key.split(','):
            data[int(index)][-1] = group

    return data.tolist()

def hca_visual(data: list):
    # Generate Matrix
    distance_matrix = {}
    for row, datapoint in enumerate(data):
        distance_matrix[str(row)] = {}
        for other_row, other_datapoint in enumerate(data):
            if row == other_row:
                continue
            distance_matrix[str(row)][str(other_row)] = _distance(datapoint, other_datapoint)

    merge_order = []

    while len(distance_matrix) > 1:
        # Get closest pair
        point_A = '-1'
        point_B = '-1'
        closest_distance = float('inf')
        for key_A, distance_dict in distance_matrix.items():
            for key_B, distance in distance_dict.items():
                if distance < closest_distance:
                    point_A = key_A
                    point_B = key_B
                    closest_distance = distance

        # Cluster the two and update the matrix
        # Replace distance_matrix[point_A] and distance_matrix[point_B] with distance_matrix[point_A+','+point_B]
        new_key = point_A+','+point_B
        distance_matrix[new_key] = {}
        for key in distance_matrix[point_A]:
            if key == point_A or key == point_B:
                continue
            distance_matrix[new_key][key] = (distance_matrix[point_A][key]+distance_matrix[point_B][key])/2

        # Add to merge_order
        merge_order.append([point_A, point_B])

        # Delete old information
        for key in distance_matrix[point_A]:
            if key == point_A or key == point_B:
                continue
            del distance_matrix[key][point_A]
            del distance_matrix[key][point_B]
            distance_matrix[key][new_key] = distance_matrix[new_key][key]
        del distance_matrix[point_A]
        del distance_matrix[point_B]

    return merge_order

#=======================================#
# Internal Methods                      #
#=======================================#

def _setup_random():
    """
    Sets the randomseed for all functions to use.
    RANDOM_SEED can be modified above.
    Returns:
        None
    """
    random.seed(RANDOM_SEED)

def _distance(point1: ListLike, point2: ListLike):
    """
    Gets the euclidean distance between 2 points
    Args:
        point1: A list of numbers
        point2: A list of numbers
    Returns:
        Float
    """
    assert(len(point1) == len(point2)) # Ensure the points have the same dimensionality; if not, there is an error in the program

    distance = 0
    for val1, val2 in zip(point1, point2): # For every axis
        delta = val2-val1 # Get the distance between the two points on that axis
        distance += delta*delta # Square and add to distance
    return math.sqrt(distance) # Return the square root as according to the Euclidean formula

def _calculate_center(points: ListLike):
    """
    Get the center between points of an arbitrary dimension
    Args:
        points: A list of points
    Returns:
        The center represented as a list of floats
    """
    center = []
    for dimension in range(0, len(points[0])): # For every dimension/axis
        center_point_on_axis = 0
        for point in points:
            center_point_on_axis += point[dimension] # Get the sum value of all points on that axis
        center_point_on_axis /= len(points) # Get the mean from said sum
        center.append(center_point_on_axis) # That will be the mean for that axis
    return center

def _calculate_center_datapoint(points: ListLike):
    """
    From a list of points of an arbitary dimension, selects
    the point that minimizes distance between all points in
    the list
    Args:
        points: A list of points
    Returns:
        The point represented as a list of floats
    """

    def sum_distance(point: ListLike):
        """
        Returns the sum of the distance between the point and every other point
        in points
        """
        distance_sum = 0
        # Calculating the distance between the point and itself does not affect the sum and has a negligible affect on performance
        for other_point in points:
            distance_sum += _distance(point, other_point)

        return distance_sum

    best_point = points[0]
    best_sum_distance = sum_distance(best_point)

    for new_point in points[1:]: # For every other point
        new_sum_distance = sum_distance(new_point) # Calculate the distance
        if new_sum_distance < best_sum_distance: # If the distance is less, set it to be the new best point
            best_point = new_point
            best_sum_distance = new_sum_distance

    return best_point
