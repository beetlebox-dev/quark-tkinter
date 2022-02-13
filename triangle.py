import math
import random
import xform


def rand_hex_color():
    hex_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    color = "#"
    for char in range(0, 6):
        color += str(random.choice(hex_chars))
    return color


def rand_hex_pure_hue():

    hex_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    rgb_components = ['FF', '00']
    rand_component = random.choice(hex_chars) + random.choice(hex_chars)
    rgb_components.append(rand_component)
    random.shuffle(rgb_components)

    hex_color = '#'
    for component in rgb_components:
        hex_color += component
    return hex_color


def rand_ngon_vertices(num_sides, upper_left_bound, lower_right_bound):
    """All points (__bound) are encoded as a list containing the x and y coordinate, i.e. [x, y].
    Returns list of vertices, with each vertex point as list."""
    vertices = []
    for vertex in range(0, num_sides):
        x = random.randint(upper_left_bound[0], lower_right_bound[0])
        y = random.randint(upper_left_bound[1], lower_right_bound[1])
        vertices.append([x, y])
    return vertices


class Triangle:

    def __init__(self, upper_left_bound, lower_right_bound, action, move_direction="rand", move_distance="rand",
                 revolution_amount="rand", stretch_axis="rand", num_sides=3, color="rand"):
        """All points (__bound) are encoded as a list containing the x and y coordinate, i.e. [x, y].
        Action can be "rotate", "stretch", or "blink".
        Optional variables (random by default): move_direction, move_distance, revolution_amount, stretch_axis.
        0 <= move_direction < 1, move_direction=0 is right, move_direction=0.25 is down.
        Move_distance is in pixels.
        If action="rotate", revolution_amount behavior each frame:
        a full rotation is 1 (clockwise) or -1 (counter-clockwise).
        If action="stretch", revolution_amount behavior each frame:
        no stretching is 1, half-width is 0.5, zero-width is 0, mirrored is -1, mirrored and double-width is -2.
        0 <= stretch_axis < 0.5.
        Y is stretch_axis=0, increasing stretch_axis rotates it counter-clockwise, X is stretch_axis=0.25.
        Num_sides is 3 by default."""
        self.upper_left_bound = upper_left_bound
        self.lower_right_bound = lower_right_bound
        self.init_vertices = rand_ngon_vertices(num_sides, upper_left_bound, lower_right_bound)
        self.action = action
        if move_direction == "rand":
            self.move_direction = random.uniform(0, 1)
        else:
            self.move_direction = move_direction
        if move_distance == "rand":
            self.move_distance = random.uniform(3, 10)
        else:
            self.move_distance = move_distance
        if revolution_amount == "rand":
            self.revolution_amount = random.uniform(0.08, 0.16) * random.choice([-1, 1])
        else:
            self.revolution_amount = revolution_amount
        if stretch_axis == "rand":
            self.stretch_axis = random.uniform(0, 0.5)
        else:
            self.stretch_axis = stretch_axis
        self.num_sides = num_sides
        if color == "rand":
            self.color = rand_hex_pure_hue()
        else:
            self.color = color

    def render(self, frame):
        if self.action == "rotate":
            actioned_vertices = \
                [xform.rotate_point(self.init_vertices[ngon_vertex], xform.centroid(self.init_vertices),
                                    self.revolution_amount * frame) for ngon_vertex in range(len(self.init_vertices))]
        elif self.action == "stretch":
            actioned_vertices = xform.stretch_points(self.init_vertices, self.stretch_axis,
                                                     math.cos(self.revolution_amount * 2 * math.pi * frame))
        else:  # "blink"
            actioned_vertices = rand_ngon_vertices(self.num_sides, self.upper_left_bound, self.lower_right_bound)
        moved_actioned_vertices = \
            [xform.move_point(actioned_vertices[ngon_vertex], self.move_direction, self.move_distance * frame)
             for ngon_vertex in range(len(actioned_vertices))]
        return moved_actioned_vertices
