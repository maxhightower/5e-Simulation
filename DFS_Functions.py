import numpy as np
import collections
from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions



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

    #print(f'move series zip: {move_series_zip}')
    #print(f'entity location: {entity_location}')

    all_positions = [entity_location]
    for loc in move_series_zip[1]:
        all_positions.append(loc)
    
    #all_positions = [entity_location] + [loc for _, loc in move_series_zip]
    #print(f'all_positions: {all_positions}')

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


def precalc_reward(action_series, entity):
    reward_value = 0
    act_series_len = len(action_series)


    # if an item from action_subactions is in action_series:
    for i in [True for item in action_series if item in action_subactions]:
        reward_value += 1
    
    for i in [True for item in action_series if item in free_subactions]:
        reward_value += 1

    for i in [True for item in action_series if item in attack_subactions]:
        reward_value += 1


    #if entity.location in entity.world.enemy_adjacent_locations and 8 not in action_series and any(0 in action_series or 1 in action_series or 2 in action_series or 3 in action_series):
    #    reward_value -= 1
    
    if 19 in action_series:
        reward_value -= 1

    # if the entity ends the turn while prone
    if 19 in action_series:
        last_prone_index = len(action_series) - 1 - action_series[::-1].index(19)
        if 20 not in action_series[last_prone_index:]:
            reward_value -= 1

    # if the action series is between 3 and 6, reward else punish
    if act_series_len >= 3:
        reward_value += 1
    
    if act_series_len <= 7:
        reward_value += 1

    if act_series_len > 8:
        reward_value -= 1

    if 5 not in action_series:
        reward_value -= 1
    elif 6 not in action_series:
        reward_value -= 1
    elif 8 not in action_series:
        reward_value -= 1
    elif 9 not in action_series:
        reward_value -= 1
    else:
        pass

    
    # if 25 or 26 is in action_series, and 5 comes after it, reward
    if 25 in action_series:
        if 5 in action_series[action_series.index(25):]:
            reward_value += 1
    if 26 in action_series:
        if 5 in action_series[action_series.index(26):]:
            reward_value += 1
    
    
    # if 4 or 7 is in action_series, and 13, 25, or 26 comes after it, reward
    if 4 in action_series:
        if 13 in action_series[action_series.index(4):]:
            reward_value += 1
        if 25 in action_series[action_series.index(4):]:
            reward_value += 1
        if 26 in action_series[action_series.index(4):]:
            reward_value += 1
    if 7 in action_series:
        if 13 in action_series[action_series.index(7):]:
            reward_value += 1
        if 25 in action_series[action_series.index(7):]:
            reward_value += 1
        if 26 in action_series[action_series.index(7):]:
            reward_value += 1

    # for the number of attacks made, times the number of damage dealt, reward
    



    return reward_value

def precalc_reward_series(action_series_full_list, acting_entity):
    reward_series_full_list = [precalc_reward(i, acting_entity) for i in action_series_full_list]
    return reward_series_full_list






def analyze_reward_distribution(reward_series_full_list, action_series_full_list):
    total_count = len(reward_series_full_list)
    
    print(f'Total count: {total_count}')
    print(f'High: {max(reward_series_full_list)}')
    print(f'Low: {min(reward_series_full_list)}')
    print()

    # Count occurrences of each reward value
    reward_counts = collections.Counter(reward_series_full_list)
    
    # Calculate and print percentages for all reward values
    print("Reward Distribution:")
    for reward in sorted(reward_counts.keys()):
        count = reward_counts[reward]
        percentage = (count / total_count) * 100
        print(f'% of {reward}s: {percentage:.2f}%')
    print()

    print(f"Total Qualifiers: {len([x for x in reward_series_full_list if x >= 3])}")
    print()

    # Print individual rewards and actions
    #print("Individual Rewards and Actions:")
    #for i, (reward, action) in enumerate(zip(reward_series_full_list, action_series_full_list)):
    #    print(f'{i}: {reward} - {action}')

def post_loc_series_reward_calc(all_action_series, all_location_series, all_reward_series, acting_entity):
    act_loc_rew_zip = list(zip(all_action_series, all_location_series, all_reward_series))
    
    #print(act_loc_rew_zip)
    post_reward_list = []
    
    for i in range(len(act_loc_rew_zip)):

        action_series = act_loc_rew_zip[i][0]
        locs_for_act = act_loc_rew_zip[i][1]
        pre_reward = act_loc_rew_zip[i][2]

        if locs_for_act != []:
            #print()
            

            #new_reward_list = [pre_reward for x in locs_for_act]

            #print(act_loc_rew_zip[i][0])
            
            for loc_series in locs_for_act:
                post_loc_reward = pre_reward

                act_loc_rew_series = (action_series, loc_series, pre_reward)
                #print(f'act loc rew series: {act_loc_rew_series}')

                # act loc rew series: ([0, 4, 6], [[-1, -1], [-2, -2]], 0.25)
                move_act_loc = ([x for x in action_series if x in move_subactions],[loc_series[y] for y in range(len(loc_series)) if action_series[y] in move_subactions])
                #print(f'move act loc: {move_act_loc}')

                move_path = calculate_full_path(acting_entity.location, move_act_loc)
                #print(f'move path: {move_path}')

                if check_opportunity_attacks(move_path, acting_entity.world.enemy_locations):
                    post_loc_reward -= 1
                
                #print(move_path)
                if move_path != []:   
                    vis_count = len(check_visibility(move_path[-1], acting_entity.world.enemy_locations, acting_entity.world))
                    post_loc_reward -= vis_count


                if move_path == []:
                    post_loc_reward -= 0.5


                # if the object action targets entity's location, but inventory is empty...
                
                # if they end their turn prone while adjacent to an enemy
                if 19 in action_series and 20 not in action_series[:-action_series.index(19)] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                    post_loc_reward -= 1
                
                # if the path is in a circle...
                # if the 
                

                new_act_loc_rew_series = (action_series, loc_series, post_loc_reward)
                post_reward_list.append(new_act_loc_rew_series)            

    post_reward_list = sorted(post_reward_list, key=lambda x: x[2],reverse=True)
    return post_reward_list

            #only_move_act = [x for x in all_action_series if x in move_subactions]
            #only_move_loc = [x for x in all_location_series if all_action_series]

            #for loc_series_index in range(len(locs_for_act)):
            #    post_calc_reward = 0

                #entity_path_traveled = []
            #    move_series_zip = [(act,loc) for act, loc, rew in act_loc_rew_zip if act in move_subactions]
            #    print(move_series_zip)
            
                #move_path = calculate_full_path(acting_entity.location, list(zip()))


            #    new_reward_list[loc_series_index] += post_calc_reward

            #reward_series_full_list[i] = new_reward_list




    # if they end their turn prone adjacent to an enemy creature, punish
    # if their movement leaves a space adjacent to an enemy creature and the disengage action isn't taken, punish

    # if the Attack action was made unarmed, +1
    # if the Attack action was made with a light weapon, +2
    # if the Attack action was made with a heavy weapon, +3

    # if the Pickup action was made, a weapon was picked up, and then the Equip action was made, +1
    # if the Equip action was made, and then the Attack action was made, +1

    # if the Pickup action was made, a shield was picked up, and the Don action was made, +1

    # if the Pickup subaction was made, a potion was picked up, and then the Consume Potion subaction was made, +1

def post_obj_reward_series_calc(action_series_full_list, location_series_full_list, reward_series_full_list, object_series_full_list, acting_entity):
    
    for i in action_series_full_list:
        action_series = action_series_full_list[i]
        location_series = location_series_full_list[i]
        reward = reward_series_full_list[i]
        object_series_list = object_series_full_list[i]
    
        if object_series_list != []:
            for obj_series in object_series_list:
                post_obj_reward = reward

                # if the object action targets entity's location, but inventory is empty...
                
                # if they end their turn prone while adjacent to an enemy
                if 19 in action_series and 20 not in action_series[:-action_series.index(19)] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                    post_reward -= 1
                
                # if the path is in a circle...
                # if the 
                

                new_act_loc_rew_series = (action_series, location_series, obj_series, post_obj_reward)
                post_reward_list.append(new_act_loc_rew_series)



    return_set = (action_series, location_series, object_series_list, post_obj_reward)
    post_object_list = sorted(return_set, key=lambda x: x[2],reverse=True)
    return post_object_list


def process_combat_zip(combat_zip):
    action_series = combat_zip[0]
    location_series = combat_zip[1]

    #tar_act_series = [x for x in action_series if x in ]