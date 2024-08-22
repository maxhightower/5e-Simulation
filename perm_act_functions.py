import numpy as np



def adjacent_locations(pos):
    adjacent_locations_list = []
    # for an 8 directional grid
    for i in range(-1,2):
        for j in range(-1,2):
            adjacent_locations_list.append([pos[0]+i,pos[1]+j])
    if pos in adjacent_locations_list:
        adjacent_locations_list.remove(pos)
    return adjacent_locations_list


def chebyshev_distance(pos1,pos2):
    return max(abs(pos1[0]-pos2[0]),abs(pos1[1]-pos2[1]))

def bresenham_line(start, end):
    """
    Implementation of Bresenham's line algorithm.
    
    :param start: Tuple of (x, y) for the starting point
    :param end: Tuple of (x, y) for the ending point
    :return: List of tuples representing all points on the line
    """
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    coordinates = []
    x, y = x1, y1

    while True:
        coordinates.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return coordinates


def calculate_full_path(entity_location, move_series_zip):
    """
    Calculate the full path using Bresenham's line algorithm for each segment.
    
    :param entity_location: Starting location of the entity
    :param move_series_zip: List of (action, location) tuples for movement actions
    :return: List of all coordinates in the path
    """
    # Create a list of all positions, starting with the entity's initial location
    all_positions = [entity_location] + [loc for _, loc in move_series_zip]
    
    # Use list comprehension to get Bresenham lines for each segment
    path_segments = [bresenham_line(start, end) 
                     for start, end in zip(all_positions, all_positions[1:])]
    
    # Flatten the list of segments and remove duplicates while preserving order
    full_path = []
    for segment in path_segments:
        full_path.extend(coord for coord in segment if coord not in full_path)
    
    return full_path


def check_opportunity_attacks(full_path, enemy_locations, disengage_action=8):
    """
    Check if the path prompts any opportunity attacks.
    
    :param full_path: List of coordinates in the path
    :param enemy_locations: List of enemy locations
    :param disengage_action: Action number for disengaging (default is 8)
    :return: Boolean indicating if an opportunity attack is prompted
    """
    # Assuming an opportunity attack is prompted if the path comes within 
    # 1 unit of an enemy location (adjust as needed for your game mechanics)
    for coord in full_path[1:]:  # Skip the starting position
        for enemy_loc in enemy_locations:
            if np.linalg.norm(np.array(coord) - np.array(enemy_loc)) <= 1:
                return True
    return False

def is_line_of_sight_clear(start, end, world):
    """
    Check if there's a clear line of sight between two points on the grid.
    
    :param start: Starting coordinates (x, y)
    :param end: Ending coordinates (x, y)
    :param world_grid: The game world grid
    :return: Boolean indicating if line of sight is clear
    """
    path = bresenham_line(start, end)
    
    for x, y in path[1:-1]:  # Exclude start and end points
        cell = world.grid2[x][y]
        
        # Check if cell is occupied or has terrain
        if cell[0] == 1 or cell[2] == 2:
            return False
        
        # Check if light is dark
        if cell[3] == 2:
            return False

        # Check for obscurement (you may want to adjust this logic based on your game rules)
        if cell[4] == 2:
            return False
        
        
        # You could add more complex checks here, e.g., for partial obscurement or light levels
    
    return True


def check_visibility(entity_location, enemy_locations, world_grid):
    """
    Check visibility of enemies from the entity's location.
    
    :param entity_location: Entity's coordinates (x, y)
    :param enemy_locations: List of enemy coordinates [(x, y), ...]
    :param world_grid: The game world grid
    :return: List of booleans indicating visibility of each enemy
    """
    list_of_visibilities = [is_line_of_sight_clear(entity_location, enemy_loc, world_grid) for enemy_loc in enemy_locations]

    return list_of_visibilities

