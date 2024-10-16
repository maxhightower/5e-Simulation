import numpy as np
import collections
from DFS_Universal_Rules import action_subactions, move_subactions, attack_subactions, free_subactions, subactions_req_objects, effect_subactions, effect_dictionary

from DFS_Entities import entity



def adjacent_locations(pos):
    adjacent_locations_list = []
    # for an 8 directional grid
    for i in range(-1,2):
        for j in range(-1,2):
            adjacent_locations_list.append([pos[0]+i,pos[1]+j])
    if pos in adjacent_locations_list:
        adjacent_locations_list.remove(pos)
    return adjacent_locations_list

def adjacent_locations_entities(entity):
    # need to use a function that can handle the entity's location being a list
    # in order to handle different size creatures
    adjacent_locations_list = []

    #print(entity)
    #print(entity.location)

    for loc in entity.location:
        for i in range(-1,2):
            for j in range(-1,2):
                adjacent_locations_list.append([loc[0]+i,loc[1]+j])

    for loc in entity.location:
        if loc in adjacent_locations_list:
            adjacent_locations_list.remove(loc)

    return adjacent_locations_list



def chebyshev_distance(pos1,pos2):
    return max(abs(pos1[0]-pos2[0]),abs(pos1[1]-pos2[1]))

def chebyshev_distance_entities(entity1, pos2):
    # because the entity's location is stored as a list, due to a large entity taking up multiple spaces
    # the list of location's occupied needs to be checked for the closest space to the target
    # and from there to the target is the distance
    distances = [chebyshev_distance(x,pos2) for x in entity1.location]
    return min(distances)

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


def calculate_full_path(entity_location, actions_locations_series):
    # the input should look like the following:
    #       [ 
    #         [0, 8, 0, 37, 0, 15, 0],
    #         [ [1,1], [1,1], [1,1], [1,1], [1,1] ]
    #       ]

    #print('')

    action_series = actions_locations_series[0]
    location_series = actions_locations_series[1]

    move_act_series = [x for x in action_series if x in move_subactions]
    move_loc_series = [location_series[y] for y in range(len(location_series)) if action_series[y] in move_subactions]

    #print(f'move act series: {move_act_series}')
    #print(f'move loc series: {move_loc_series}')

    starting_location = entity_location
    all_main_positions = [starting_location] + [loc for loc in move_loc_series]
    #print(f'all main positions: {all_main_positions}')

    # need to go through each pair of locations and calculate the path between them
    full_path = []
    


    if len(move_loc_series) <= 1:
        return [starting_location] + move_loc_series
    
    else:

        for location_index in range(len(all_main_positions)):
            if (location_index + 1) > len(all_main_positions):
                break
            else:
                location_pair = [all_main_positions[location_index], all_main_positions[location_index+1]]

                #print(f'location pair: {location_pair}')
                # the calculated distance is the distance formula
                calculated_distance = np.linalg.norm(np.array(location_pair[0]) - np.array(location_pair[1]))
                #print(f'calculated distance: {calculated_distance}')
        
                # if the distance is greater than 1, then the path needs to be calculated
                if calculated_distance > 1:
                    path = bresenham_line(location_pair[0], location_pair[1])
                    full_path.extend(path)
                else:
                    full_path.append(location_pair[0])
                    full_path.append(location_pair[1])

            #print(f'full path: {full_path}')
        
            return full_path



    #"""
    #Calculate the full path using Bresenham's line algorithm for each segment.
    
    #:param entity_location: Starting location of the entity
    #:param move_series_zip: List of (action, location) tuples for movement actions
    #:return: List of all coordinates in the path
    #"""
    # Create a list of all positions, starting with the entity's initial location

    #print(f'move series zip: {move_series_zip}')
    #print(f'entity location: {entity_location}')

    #all_positions = [entity_location]
    #for loc in actions_locations_series[1]:
    #    all_positions.append(loc)
    
    #all_positions = [entity_location] + [loc for _, loc in move_series_zip]
    #print(f'all_positions: {all_positions}')

    # Use list comprehension to get Bresenham lines for each segment
    #path_segments = [bresenham_line(start, end) 
    #                 for start, end in zip(all_positions, all_positions[1:])]
    
    # Flatten the list of segments and remove duplicates while preserving order
    #full_path = []
    #for segment in path_segments:
    #    full_path.extend(coord for coord in segment if coord not in full_path)
    
    #return full_path

def calculate_full_path_entities(entity, actions_locations_series):
    full_path = []
    entity_locations = entity.location
    # the entity_locations is a list of the entity's location(s)

    if entity.size in ['tiny','small','medium']:
        # the width of the entity is 1
        # so the path will only be 1 wide
        
        move_series = entity.locations[0] + actions_locations_series[1]
        for i in range(len(move_series)):
            full_path.extend(bresenham_line(entity_locations[0], move_series[i]))


    else:
        # the path will need to be calculated for each location
        width = entity.width


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

    # need to change the qualifier to be the top 15% of rewards
    quality_threshold = np.percentile(reward_series_full_list, 99)

    print(f'Quality Threshold: {quality_threshold}')

    print(f"Total Qualifiers: {len([x for x in reward_series_full_list if x >= quality_threshold])}")
    print()

    # Print individual rewards and actions
    #print("Individual Rewards and Actions:")
    #for i, (reward, action) in enumerate(zip(reward_series_full_list, action_series_full_list)):
    #    print(f'{i}: {reward} - {action}')

# I want to create an analyze_reward_distribution function that could take in an action_reward_series, action_location_reward_series, action_location_object_reward_series, and so on
# and then output the distribution of rewards, the percentage of rewards that are above a certain threshold, and the percentage of rewards that are below a certain threshold

def analyze_reward_distribution_series(any_series, acting_entity, percentile):
    # the input should be the combined series, not separate lists

    if len(any_series[0]) == 2: # two items means action and reward
        reward_series_full_list = [x[1] for x in any_series]
        action_series_full_list = [x[0] for x in any_series]

    elif len(any_series[0]) == 3: # three items means action, location, and reward
        action_series_full_list = [x[0] for x in any_series]
        location_series_full_list = [x[1] for x in any_series]
        reward_series_full_list = [x[2] for x in any_series]

    elif len(any_series[0]) == 4: # four items means action, location, object, and reward
        action_series_full_list = [x[0] for x in any_series]
        location_series_full_list = [x[1] for x in any_series]
        object_series_full_list = [x[2] for x in any_series]
        reward_series_full_list = [x[3] for x in any_series]

    total_count = len(any_series)
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

    # need to change the qualifier to be the top 15% of rewards
    quality_threshold = np.percentile(reward_series_full_list, percentile)

    print(f'Quality Threshold ({percentile}): {quality_threshold}')

    print(f"Total Qualifiers: {len([x for x in reward_series_full_list if x >= quality_threshold])}")
    print()
 

 # Now what I want to do here is build a function that treats calculating the reward the same way rule checking is handled for DFS
 # in order for it to be more modular and flexible


# need a function to separate a move_speed into the appropriate number of subactions so that there can be no redundant or inefficient combinations
def move_speed_to_subactions(move_speed):
    labeled_move_speed_dictionary = {}
    move_speed_subaction_list = []

    # the move_speed should be a number
    if move_speed % 5 == 0:
        num_subactions = move_speed // 5
    else:
        num_subactions = move_speed // 5 + 1

    for i in range(num_subactions):
        labeled_move_speed_dictionary[i] = 5
        move_speed_subaction_list.append(5)

    if move_speed % 5 != 0:
        labeled_move_speed_dictionary[num_subactions - 1] = move_speed % 5
        move_speed_subaction_list[-1] = move_speed % 5

    # add the text to the value of the dictionary that says 'move x spaces'
    for key in labeled_move_speed_dictionary:
        labeled_move_speed_dictionary[key] = f'move {labeled_move_speed_dictionary[key]} spaces'

    # the output should be two things: labeled dictionary and list of subactions
    return labeled_move_speed_dictionary, move_speed_subaction_list 
    









def generate_pseudo_history(acting_entity,sequence, post_location_reward_list, object_subaction_index):
    potential_objects = []
    worldly_objects = acting_entity.world.objects

    action_series = post_location_reward_list[0]
    location_series = post_location_reward_list[1]
    object_series = [x for x in action_series if x in subactions_req_objects]

    #print(f'functions - pseudo; object_series: {object_series}')
    #print(f'functions - pseudo; object_subaction_index: {object_subaction_index}')
    #print(f'functions - pseudo; sequence: {sequence}')

    object_subaction = object_series[object_subaction_index]
    pseudo_inventory = acting_entity.inventory.copy()
    #pseudo_weapon_equipped = acting_entity.weapon_equipped.copy()
    pseudo_armor_equipped = acting_entity.equipped_armor.copy()
    pseudo_main_hand = acting_entity.main_hand.copy()
    pseudo_off_hand = acting_entity.off_hand.copy()
    pseudo_world = worldly_objects.copy()

    # now to go through the process that would happen if the sequence was followed
    for i in range(len(sequence)):
        temp_object = sequence[i]
        subaction = object_series[i]
        
        if subaction in [4,7]: # pickup
            if temp_object in pseudo_world:
                pseudo_world.remove(temp_object)
                pseudo_inventory.append(temp_object)
        

        if subaction in [31,32]: # unequip - main_hand
            if temp_object in pseudo_main_hand:
                pseudo_main_hand.remove(temp_object)
                pseudo_inventory.append(temp_object)

        if subaction in [40,41]: # unequip - off_hand
            if temp_object in pseudo_off_hand:
                pseudo_off_hand.remove(temp_object)
                pseudo_inventory.append(temp_object)

        if subaction in [25,26]: # equip - main_hand
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_main_hand.append(temp_object)
        
        if subaction in [37,38]: # equip - off_hand
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_off_hand.append(temp_object)


        if subaction in [13]: # don shield
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_armor_equipped.append(temp_object)
        
        if subaction in [39]: # doff shield
            if temp_object in pseudo_armor_equipped:
                pseudo_armor_equipped.remove(temp_object)
                pseudo_inventory.append(temp_object)

        
        if subaction in [29,30]: # drop object
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_world.append(temp_object)

        if subaction in [42,45]: # drop object - main_hand
            if temp_object in pseudo_main_hand:
                pseudo_main_hand.remove(temp_object)
                pseudo_world.append(temp_object)

        if subaction in [43,46]: # drop object - off_hand
            if temp_object in pseudo_off_hand:
                pseudo_off_hand.remove(temp_object)
                pseudo_world.append(temp_object)
        

        if subaction in [31,32]: # unequip - main_hand
            if temp_object in pseudo_main_hand:
                pseudo_main_hand.remove(temp_object)
                pseudo_inventory.append(temp_object)

        if subaction in [40,41]: # unequip - off_hand
            if temp_object in pseudo_off_hand:
                pseudo_off_hand.remove(temp_object)
                pseudo_inventory.append(temp_object)

        if subaction in [25,26]: # equip - main_hand
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_main_hand.append(temp_object)
        
        if subaction in [37,38]: # equip - off_hand
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_off_hand.append(temp_object)


        if subaction in [13]: # don shield
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_armor_equipped.append(temp_object)
        
        if subaction in [39]: # doff shield
            if temp_object in pseudo_armor_equipped:
                pseudo_armor_equipped.remove(temp_object)
                pseudo_inventory.append(temp_object)

        
        if subaction in [29,30]: # drop object
            if temp_object in pseudo_inventory:
                pseudo_inventory.remove(temp_object)
                pseudo_world.append(temp_object)

        if subaction in [42,45]: # drop object - main_hand
            if temp_object in pseudo_main_hand:
                pseudo_main_hand.remove(temp_object)
                pseudo_world.append(temp_object)

        if subaction in [43,46]: # drop object - off_hand
            if temp_object in pseudo_off_hand:
                pseudo_off_hand.remove(temp_object)
                pseudo_world.append(temp_object)
        
        if subaction in [44,47]: # drop object - both hands
            if temp_object in pseudo_main_hand:
                pseudo_main_hand.remove(temp_object)
            
            if temp_object in pseudo_off_hand:
                pseudo_off_hand.remove(temp_object)
        
            pseudo_world.append(temp_object)

    return pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world


def damage_calc1(subaction, acting_entity, main_hand, off_hand):
    damage = 0
    if subaction in attack_subactions:
        if subaction in [16,18]: # grapple and shove
            return 0    # these don't deal damage
        
        if subaction in subactions_req_objects:
            if subaction in [5,48]:
                if main_hand != [] and off_hand != []:
                    if subaction == 48 and main_hand[0] == off_hand[0] and main_hand[0].hands == 2:
                        damage = main_hand[0].damage + acting_entity.strength_mod

                if main_hand != []:
                    if main_hand[0].type != 'weapon':
                        damage = 1 + acting_entity.strength_mod
                    else:
                        if subaction == 5:
                            damage = main_hand[0].damage + acting_entity.strength_mod
                
            if off_hand != []:
                if subaction == 15:
                    if off_hand[0].type != 'weapon':
                        damage = 1
                    else:
                        damage = off_hand[0].damage


        elif subaction == 36: # unarmed strike
            damage = max(acting_entity.strength_mod, 1)

    else:
        #print('not an attack subaction')
        pass

    return damage
    # need to identify the entity, the weapon, and the target
    # eventually the input needs to be changed to the the act_loc_obj_rew

    

def damage_calc2(action_location_object_series, acting_entity):
    action_series = action_location_object_series[0]
    location_series = action_location_object_series[1]
    object_series = action_location_object_series[2]
    #reward = act_loc_obj_rew[3]

    attack_and_effect_series = [x for x in action_series if x in attack_subactions or x in effect_subactions]
    attack_series = [x for x in action_series if x in attack_subactions]

    #pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity, object_series, act_loc_obj_rew, len(object_series))

    # I'm going to need to calculate the damage for each damage dealing subaction within the action_series
    damage_series = []

    for subaction_index in range(len(attack_series)):
        subaction_damage = 0
        # first find the order of attacks, then identify the effects used that are associated with the attack
        relevant_effects = attack_and_effect_series[attack_series.index(attack_series[subaction_index]):]
        
        for i in relevant_effects:
            if i in effect_subactions:
                if effect_dictionary[i].type == 'damage_bonus':
                    subaction_damage += effect_dictionary[i].effect

        object_sequence = [object_series[x] for x in range(len(object_series)) if action_series[x] in attack_subactions]

        pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity, object_sequence, action_location_object_series, subaction_index)

        subaction_damage += damage_calc1(attack_series[subaction_index], acting_entity, pseudo_main_hand, pseudo_off_hand)

        damage_series.append(subaction_damage)

        # this is currently setup to assign a single effect to only the next attack, not all attacks
        # perhaps there should be sub_effects and turn_effects,
        # sub_effects are only applied to the next attack, while turn_effects are applied to all attacks of a certain type in the turn
        # turn_effects are complicated enough to require representation in a list (or even a class???) 

        # or perhaps all effects need more details... such as duration, application circumstances, etc...

    return damage_series

def probability_hit_calc(action_location_object_series, acting_entity, target_entity):
    action_series = action_location_object_series[0]
    location_series = action_location_object_series[1]
    object_series = action_location_object_series[2]
    #reward = act_loc_obj_rew[3]

    # the subaction should dictate which type of attack check is being made
    # and thus the type of bonuses which are allowed (spellcasting, strength, dexterity, etc.)



    armor_class = target_entity.ac

    circumstances = []
    # need to go through acting_entity's conditions and circumstances

    #if sum([1 for x in circumstances if x == 'ADV']) > 0 and sum([1 for x in circumstances if x == 'DIS']) > 0:
        
    # attack bonus
    attack_bonus = acting_entity.strength_mod + acting_entity.proficiency_bonus

    # always hits on a 20

    bonuses = []
    for i in action_series:
        if i in effect_subactions:
            if effect_dictionary[i].type == 'attack_bonus':
                bonuses.append(effect_dictionary[i].effect)
    
    attack_bonus += sum(bonuses)

    # the probability of hitting is the probability of rolling a number that is greater than or equal to the target's armor class
    # the probability of rolling a number between 1 and 20 is 1/20

    probability = (21 - (armor_class - attack_bonus))/20


    return probability

def expected_damage(action_location_object_series, acting_entity, target_entity):
    # this is the expected damage for a single attack
    # taking into account:
    # - effects, circumstances, and conditions
    # - the probability of hitting
    # - resistances and vulnerabilities

    # chance of normal damage
    # chance of critical damage
    # chance of missing

    # the damage will need to be separated by a list of damage types



    expected_damage_results = []


def calc_series_expected_damage(action_location_object_series, acting_entity, target_entity):
    pass




def process_turn(act_loc_obj_rew, acting_entity):
    # move actions 
    # object actions
    # dealing damage
    action_series = act_loc_obj_rew[0]
    location_series = act_loc_obj_rew[1]
    object_series = act_loc_obj_rew[2]
    reward = act_loc_obj_rew[3]

    # should this go subaction by subaction to check for reactions?

    for subaction in action_series:
        # this goes subaction by subaction
        check_reactions(subaction, acting_entity)
        # this is where the observer pattern will come in

        # global list/dictionary of observers??? that gets checked each time a subaction is made as a shortcut
        # the following elements are relevant and need to be represented: 
        # - the entity that can react
        # - the reacting subaction
        # - the subaction which triggers the reacting subaction
        # - the situation which is required for the reacting subaction (proximity, line of sight, etc.)
        # - the reward value required for the reacting subaction to be triggered (risk the reacting entity takes in reacting)
        # - the reward value that the reacting entity gets for reacting


def check_reactions(subaction, acting_entity):
    pass

    # process turn will go subaction by subaction to check for reactions, 
    # so this function will be given the entity acting and the subaction
    # it will need to check each entity in the world to see if they have a subaction that follows the rules in order to react
    # then it will need to calculate if the reward value is high enough to react or not


    # this will need a 






