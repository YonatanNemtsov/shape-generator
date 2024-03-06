import math

def distance_point_point(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)


def distance_point_line_seg(point, line_start, line_end):
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return math.sqrt((x - x1)**2 + (y - y1)**2) 

    u = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
    
    if u < 0:  
        return distance_point_point(point, line_start)
    elif u > 1: 
        return distance_point_point(point, line_end)

    proj_x = x1 + u * dx
    proj_y = y1 + u * dy
    return math.sqrt((x - proj_x)**2 + (y - proj_y)**2)

def distance_point_circle(point, circle_center, radius):
    x, y = point
    cx, cy = circle_center
    distance_to_center = math.sqrt((x - cx)**2 + (y - cy)**2)
    distance_to_boundary = abs(distance_to_center - radius)
    return distance_to_boundary

def distance_point_polygon(point, polygon_vertices):
    min_edge_distance = float("inf")
    for i in range(len(polygon_vertices)):
        start = polygon_vertices[i]
        end = polygon_vertices[(i + 1) % len(polygon_vertices)]
        dist = distance_point_line_seg(point, start, end)
        min_edge_distance = min(min_edge_distance, dist)

    return min_edge_distance

def centroid(points):
    """Calculate the centroid of a polygon."""
    x_sum = sum(p[0] for p in points)
    y_sum = sum(p[1] for p in points)
    return x_sum / len(points), y_sum / len(points)

def angle_with_centroid(point, centroid):
    """Calculate the angle between the x-axis and the line formed by connecting the point to the centroid."""
    dx = point[0] - centroid[0]
    dy = point[1] - centroid[1]
    return math.atan2(dy, dx)


if __name__ == '__main__':
    print(distance_point_line_seg((0,0),(1,1),(1,-1)))
    print(distance_point_point((1,1),(0,0)))
    print(distance_point_circle((1,1),(0,0),1))
    print(distance_point_polygon(
        (0.5,0),[(0,1),(1,1),(2,2)]
    ))