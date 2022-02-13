import math


def centroid(list_of_points):
    """All points are encoded as a list containing the x and y coordinate, i.e. [x, y].
    Returns centroid point as list."""
    num_points = len(list_of_points)
    x_sum = 0
    y_sum = 0
    for point in list_of_points:
        x_sum += point[0]
        y_sum += point[1]
    x_centroid = x_sum / num_points
    y_centroid = y_sum / num_points
    return [x_centroid, y_centroid]


def move_point(point, direction, distance):
    """All points are encoded as a list containing the x and y coordinate, i.e. [x, y].
    0 <= direction < 1, right is direction=0, down is direction=0.25.
    Distance is in pixels.
    Returns moved point as list."""
    theta = direction * math.pi * 2
    x_point = point[0]
    y_point = point[1]
    x_moved_point = distance * math.cos(theta) + x_point
    y_moved_point = distance * math.sin(theta) + y_point
    return [round(x_moved_point), round(y_moved_point)]


def rotate_point(point, pivot, rotation_amount):
    """All points (point, pivot) are encoded as a list containing the x and y coordinate, i.e. [x, y].
    Full rotations are 1 (clockwise) or -1 (counter-clockwise).
    Returns rotated point as list."""
    x_point = point[0]
    y_point = point[1]
    x_pivot = pivot[0]
    y_pivot = pivot[1]
    radians = rotation_amount * math.pi * 2
    x_rotated_point = (x_point - x_pivot) * math.cos(radians) - (y_point - y_pivot) * math.sin(radians) + x_pivot
    y_rotated_point = (x_point - x_pivot) * math.sin(radians) + (y_point - y_pivot) * math.cos(radians) + y_pivot
    return [round(x_rotated_point), round(y_rotated_point)]


def stretch_points(list_of_points, axis, stretch_amount):
    """All points are encoded as a list containing the x and y coordinate, i.e. [x, y].
    0 <= axis < 0.5. Y is axis=0, top-left quadrant to bottom-right quadrant is axis=0.125, X is axis=0.25.
    Stretch_amount: no change is 1, half-width is 0.5, zero-width is 0, mirrored is -1, mirrored and double-width is -2.
    Returns list of stretched points, with each point as list."""
    points_centroid = centroid(list_of_points)
    moved_points = [[point[0] - points_centroid[0], point[1] - points_centroid[1]] for point in list_of_points]
    rotated_points = [rotate_point(point, [0, 0], axis) for point in moved_points]
    stretched_points = [[point[0] * stretch_amount, point[1]] for point in rotated_points]
    unrotated_points = [rotate_point(point, [0, 0], -axis) for point in stretched_points]
    unmoved_points = [[point[0] + points_centroid[0], point[1] + points_centroid[1]] for point in unrotated_points]
    int_unmoved_points = [[round(point[0]), round(point[1])] for point in unmoved_points]
    return int_unmoved_points
