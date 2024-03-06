from syntax import AtomicEntity, DescriptedEntity, Transformer, TransformedDescriptor
from shape_label_generation import generate_label
from PIL import Image, ImageDraw
import random
import math
from geometry_lib import distance_point_circle, distance_point_line_seg, distance_point_point, distance_point_polygon, centroid, angle_with_centroid

CIRCLE = 'circle'
TRIANGLE = 'triangle'
SQUARE = 'square'

INSIDE_OF = 'inside_of'
LEFT_OF = 'left_of'

def draw_picture(canvas, label, image_size=(64, 64), bounds=None):
    #print(bounds)
    # bounds: series of points representing a polygon. draw inside that polygon.
    if bounds is None:
        bounds = [(0, 0), (image_size[0] - 1, 0), (image_size[0] - 1, image_size[1] - 1), (0, image_size[1] - 1)]

    if isinstance(label, AtomicEntity):
        shape = generate_random_shape(label, bounds)
        draw_shape(canvas, shape)
    elif isinstance(label, DescriptedEntity):
        relation = label.descriptor.transformer
        obj1 = label.descriptor.object
        obj2 = label.entity

        if relation.name == INSIDE_OF:
            draw_inside_of(canvas, obj1, obj2, image_size, bounds)
        elif relation.name == LEFT_OF:
            draw_left_of(canvas, obj1, obj2, image_size, bounds)

def draw_shape(canvas, shape):
    draw = ImageDraw.Draw(canvas)
    draw.polygon(shape, outline=100, width=3)


def generate_random_shape(shape, bounds):
    if shape.name == CIRCLE:
        center = generate_random_point_inside_polygon_from_center(bounds, c = .15)
        max_radius = distance_point_polygon(center, bounds)  # Limiting radius to prevent overflow
        radius = random.uniform(max_radius*0.75, max_radius)
        return generate_circle(center, radius)
    elif shape.name == SQUARE:
        center = generate_random_point_inside_polygon_from_center(bounds, c = .15)
        max_side_length = 1.5 * distance_point_polygon(center, bounds)  # Limiting side length to prevent overflow
        side_length = int(random.uniform(max_side_length/2, max_side_length))
        half_side = side_length / 2
        return generate_square(center, half_side)
    elif shape.name == TRIANGLE:
        return generate_random_triangle(bounds)


def generate_random_point_inside_polygon(polygon, c = 0.75):
    min_x = min(polygon, key=lambda x: x[0])[0]
    max_x = max(polygon, key=lambda x: x[0])[0]
    min_y = min(polygon, key=lambda x: x[1])[1]
    max_y = max(polygon, key=lambda x: x[1])[1]
    while True:
        x = random.uniform((c*min_x + (1-c)*max_x), ((1-c)*min_x + c*max_x))
        y = random.uniform((c*min_y + (1-c)*max_y), ((1-c)*min_y + c*max_y))
        if is_point_inside_polygon((x, y), polygon):
            return x, y
        
def generate_random_point_inside_polygon_from_center(polygon, c = 0.75):
    center = centroid(polygon)
    max_length = distance_point_polygon(center, polygon)
    theta = random.random() * 2 * math.pi
    r = random.random() * max_length * c
    x = math.cos(theta) * r + center[0]
    y = math.sin(theta) * r + center[1]
    return (x,y)



def is_point_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def generate_circle(center, radius):
    points = []
    for theta in range(0, 360, 10):
        x = center[0] + int(radius * math.cos(math.radians(theta)))
        y = center[1] + int(radius * math.sin(math.radians(theta)))
        points.append((x, y))
    return points


def generate_square(center, half_side):
    cx, cy = center
    return [
        (cx - half_side, cy - half_side),
        (cx + half_side, cy - half_side),
        (cx + half_side, cy + half_side),
        (cx - half_side, cy + half_side)
    ]


def area_of_polygon(points):
    """Calculate the area of a polygon using the shoelace formula."""
    n = len(points)
    area = 0
    
    for i in range(n):
        j = (i + 1) % n
        #print("polygon area calc: ", points[i][0] * points[j][1] - points[j][0] * points[i][1])
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2

def angle_between_points(p1, p2, p3):
    """Calculate the angle between three points."""
    a = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    b = math.sqrt((p3[0] - p2[0]) ** 2 + (p3[1] - p2[1]) ** 2)
    c = math.sqrt((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2)
    return math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))

def generate_random_triangle(bounds):
    """Generate a random triangle inside the bounds."""
    min_area_percentage = 0.05
    min_angle_val = 25
    best_triangle = None

    for _ in range(1000):  # Adjust the number of iterations as needed
        triangle_points = []
        for _ in range(3):
            point = generate_random_point_inside_polygon(bounds, c = 0.2)
            triangle_points.append(point)

        # Calculate the area of the triangle
        #print('TRIANGLE AREA')
        #print(triangle_points)
        triangle_area = area_of_polygon(triangle_points)
        #print(triangle_area)
        # Calculate the smallest angle in the triangle
        angles = [angle_between_points(triangle_points[i], triangle_points[(i + 1) % 3], triangle_points[(i + 2) % 3])
                  for i in range(3)]
        min_angle = min(angles)
       

        # Calculate the area percentage
        #print('BOUNDS AREA')
        #print(bounds)
        bounds_area = area_of_polygon(bounds)
        area_percentage = triangle_area / bounds_area
        #print(min_angle, triangle_area, bounds_area, area_percentage)
        # Update the best triangle if it satisfies the conditions
        if min_angle > min_angle_val and area_percentage > min_area_percentage:
            min_area_percentage = area_percentage
            best_triangle = triangle_points

    return best_triangle

def draw_inside_of(canvas, obj1, obj2, image_size, bounds):
    #print(bounds)
    containing_shape = generate_random_shape(obj1, bounds)
    draw_shape(canvas, containing_shape)
    draw_picture(canvas, obj2, image_size, containing_shape)

def draw_left_of(canvas, obj1, obj2, image_size, bounds):
    # Split the polygon into left and right bounds based on the midpoint
    left_bounds, right_bounds = split_bounds(bounds)
    #print(10)
    draw_picture(canvas, obj1, image_size, left_bounds)
    draw_picture(canvas, obj2, image_size, right_bounds)





def split_bounds(bounds):
    # Find the bounding box of the polygon
    min_x = min(point[0] for point in bounds)
    max_x = max(point[0] for point in bounds)
    min_y = min(point[1] for point in bounds)
    max_y = max(point[1] for point in bounds)

    # Calculate the midpoint of the bounding box
    mid_x = (min_x + max_x) // 2

    # Find points of intersection with the line x = mid_x
    intersection_points = []
    for i in range(len(bounds)):
        x1, y1 = bounds[i]
        x2, y2 = bounds[(i + 1) % len(bounds)]

        # Check if line segment intersects with the line x = mid_x
        if (x1 <= mid_x <= x2) or (x2 <= mid_x <= x1):
            intersection_y = y1 + (mid_x - x1) * (y2 - y1) / (x2 - x1)
            intersection_points.append((mid_x, intersection_y))

    # Sort intersection points based on their y-coordinates
    intersection_points.sort(key=lambda point: point[1])

    # Split the bounds based on intersection points
    left_bounds = [(x, y) for x, y in bounds if x <= mid_x]
    right_bounds = [(x, y) for x, y in bounds if x >= mid_x]

    # Add intersection points to the left and right bounds
    for point in intersection_points:
        if point[0] <= mid_x:
            left_bounds.append(point)
        if point[0] >= mid_x:
            right_bounds.append(point)

    center_left = centroid(left_bounds)
    center_right = centroid(right_bounds)

    left_bounds = sorted(left_bounds, key=lambda point: angle_with_centroid(point, center_left))
    right_bounds = sorted(right_bounds, key=lambda point: angle_with_centroid(point, center_right))

    return left_bounds, right_bounds




if __name__ == '__main__':
    image_size = (1000,1000)  # For consistency
    
    def experiment1():
        for i in range(30):
            image = Image.new("RGB", image_size, (255, 255, 255))  # White background
            label = generate_label(max_depth=4, complexity=0.5)
            draw_picture(image, label, image_size)
            print(label.linear_rep())
            image.show()
    
    def experiment2():
        from shape_label_generation import triangle, square, circle, inside_of, left_of
        label = triangle

        image = Image.new("RGB", image_size, (255, 255, 255))  # White background
        draw_picture(image, label, image_size)
        print(label.linear_rep())
        image.show()
    

    experiment2()
    experiment1()
