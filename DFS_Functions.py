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
    





def check_rules_for_reward(any_one_series,ruleset,acting_entity):
    reward = any_one_series[-1]

    for rule in ruleset:
        reward += rule(any_one_series, acting_entity)
    
    return reward


def calc_new_reward(any_series, acting_entity):
    # the input should be the combined series, not separate lists
    results = []

    # this function calculates the new reward values for the entire list of series

    if len(any_series[0]) == 1 or len(any_series[0]) == 0: # only one item means action
        ruleset = action_rules

        for any_one_series in any_series:
            new_reward = check_rules_for_reward(any_one_series, ruleset, acting_entity)
            same_series_new_reward = [any_one_series[0], new_reward]
            results.append(same_series_new_reward)


    elif len(any_series[0]) == 3: # three items means action, location, and reward
        ruleset = action_location_reward_rules

        for any_one_series in any_series:
            new_reward = check_rules_for_reward(any_one_series, ruleset, acting_entity)
            same_series_new_reward = [any_one_series[0], any_one_series[1], new_reward]
            results.append(same_series_new_reward)

    elif len(any_series[0]) == 4: # four items means action, location, object, and reward
        ruleset = action_location_object_reward_rules

        for any_one_series in any_series:
            new_reward = check_rules_for_reward(any_one_series, ruleset, acting_entity)
            same_series_new_reward = [any_one_series[0], any_one_series[1], any_one_series[2], new_reward]
            results.append(same_series_new_reward)
            
    else:
        print('Invalid series length')

    return results
        

action_rules = [
    # for the number of actions taken, reward
    # for the number of free actions taken, reward
    # for the number of attacks made, reward
    # if the entity goes prone at all, punish
    # if the entity ends the turn while prone, punish
    # if the action series is between 3 and 6, reward else punish
    # if the action series is between 7 and 10, reward else punish
    # if the action series is greater than 10, punish
    # if 25 or 26 is in action_series, and 5 comes after it, reward (if the equip subaction is followed by the attack subaction, reward)
    # if the entity equips off hand and attacks with it, reward
    # if the entity picks up an item, and then equips it, reward
    # if the entity loses an item, slightly punish
    # for the number of attacks made, times the number of damage dealt, reward
    # if the entity unequips an item, and doesn't equip something else, punish
    # dropping items should be punished
    # if a subaction is taken, followed by disengage, followed by movement, reward
    # if shove-push is taken, followed by movement, reward
    # if mount subaction is taken twice, punish
    # if you mount and dismount in the same turn, punish

]

action_location_reward_rules = [
    # if the move path prompts an opportunity attack, punish
    # each opportunity attack that is while flanked is even more punished
    # each enemy that can see the entity causes the entity to be punished
    # slight punishment if the entity doesn't move
    # if the entity turns prone while adjacent to an enemy, punish
    # if an enemy can no longer move so that they would be adjacent to the entity, reward
    # if the entity ends their turn flanked, punish

]

action_location_object_reward_rules = [
    # if the entity picks up an item, and its a coin, reward
    # if the entity picks up an item, and its a weapon, reward
    # reward when the entity dons a shield, punish when the entity equips it
    # reward equal to the damage dealt when the entity attacks
    # if the damage dealt would reduce the target to 0 HP, reward
    # if an item is equipped and item.casting_focus is true, and cast subaction is taken after, reward
    # if an item is equipped and the item is a potion and then the drink potion subaction is taken, reward
    
    

]

action_location_object_entity_reward_rules = [
    # if mount lacks barding, punish

]


action_location_object_entity_spell_reward_rules = [
    # HP to allies that healed is rewarded
]






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












###### Reward Calculation Functions ######




def precalc_reward(action_series, entity):
    reward_value = 0
    act_series_len = len(action_series)


    # if an item from action_subactions is in action_series:
    for i in [True for item in action_series if item in action_subactions]:
        reward_value += 1
    
    # the list of freeactions are now a list of lists
    for i in free_subactions:
        for j in i:
            if j in action_series:
                reward_value += 1
        
    for i in [True for item in action_series if item in attack_subactions]:
        reward_value += 1


    #if entity.location in entity.world.enemy_adjacent_locations and 8 not in action_series and any(0 in action_series or 1 in action_series or 2 in action_series or 3 in action_series):
    #    reward_value -= 1
    
    # if the entity goes prone at all
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

    if act_series_len > 10:
        reward_value -= 1

    #if 5 not in action_series:
    #    reward_value -= 1
    #elif 6 not in action_series:
    #    reward_value -= 1
    #elif 8 not in action_series:
    #    reward_value -= 1
    #elif 9 not in action_series:
    #    reward_value -= 1
    #elif 36 not in action_series:
    #    reward_value -= 1
    #else:
    #    pass

    
    # if 25 or 26 is in action_series, and 5 comes after it, reward
    # aka if the equip subaction is followed by the attack subaction, reward
    if 25 in action_series:
        if 5 in action_series[action_series.index(25):]:
            reward_value += 1
    if 26 in action_series:
        if 5 in action_series[action_series.index(26):]:
            reward_value += 1
    
    # if the entity equips off hand and attacks with it, reward 
    if 37 in action_series:
        if 15 in action_series[action_series.index(37):]:
            reward_value += 1
    if 38 in action_series:
        if 15 in action_series[action_series.index(38):]:
            reward_value += 1


    
    # if the entity picks up an item, and then equips it, reward
    if 4 in action_series:
        if 13 in action_series[action_series.index(4):]:
            reward_value += 1
        if 25 in action_series[action_series.index(4):]:
            reward_value += 1
        if 26 in action_series[action_series.index(4):]:
            reward_value += 1
        if 37 in action_series[action_series.index(4):]:
            reward_value += 1
        if 38 in action_series[action_series.index(4):]:
            reward_value += 1

    if 7 in action_series:
        if 13 in action_series[action_series.index(7):]:
            reward_value += 1
        if 25 in action_series[action_series.index(7):]:
            reward_value += 1
        if 26 in action_series[action_series.index(7):]:
            reward_value += 1
        if 37 in action_series[action_series.index(7):]:
            reward_value += 1
        if 38 in action_series[action_series.index(7):]:
            reward_value += 1

    # for the number of attacks made, times the number of damage dealt, reward
    
    # if the entity loses an item, slightly punish
    # 29, 30, 42, 43, 44, 45, 46, 47
    if 29 in action_series:
        reward_value -= 1
    if 30 in action_series:
        reward_value -= 1
    if 42 in action_series:
        reward_value -= 1
    if 43 in action_series:
        reward_value -= 1
    if 44 in action_series:
        reward_value -= 1
    if 45 in action_series:
        reward_value -= 1
    if 46 in action_series:
        reward_value -= 1
    if 47 in action_series:
        reward_value -= 1

    # if the entity unequips an item, and doesn't equip something later, punish
    # equip: 25, 26, 37, 38, 13
    # unequip: 31, 32, 40, 41, 39

    #if 25 in action_series:
    #    if 31 not in action_series[action_series.index(25):]:


    # new rewards to add
    # perhaps dropping items should be discouraged
    if 29 in action_series or 30 in action_series:
        reward_value -= 1
    

    # if a subaction is taken, and then disengage is taken, and then movement is taken, reward
    for i in range(len(action_series)):
        if action_series[i] in move_subactions:
            if 8 in action_series[:i]:
                if any(x in action_series[:action_series.index(8)] for x in move_subactions):
                    reward_value += 1


    # if shove - push is taken, and then movement is taken, reward
    if 53 in action_series:
        if any(x in action_series for x in move_subactions):
            reward_value += 1
    




    return reward_value

def precalc_reward_series(action_series_full_list, acting_entity):
    reward_series_full_list = [precalc_reward(i, acting_entity) for i in action_series_full_list]
    return reward_series_full_list







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
                
                # each opportunity attack while flanked is even worse, additional punishment if that's the case

                
                # punishing for each enemy that can see the entity
                if move_path != []:   
                    vis_count = len(check_visibility(move_path[-1], acting_entity.world.enemy_locations, acting_entity.world))
                    post_loc_reward -= 1


                # punishing slightly if the entity doesn't move
                if move_path == []:
                    post_loc_reward -= 1


                # if the object action targets entity's location, but inventory is empty...
                
                # if they end their turn prone while adjacent to an enemy 
                if 19 in action_series:
                    if len(move_path) > 1:
                        if 20 not in action_series[:-action_series.index(19)] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                           post_loc_reward -= 1
                        # need to add a check for if the enemy in enemy_adjacent_locations is currently visible, otherwise it shouldn't be taken into account by the acting entity
                
                # if the path is in a circle...
                # if the 


                # need to reward the entity for how hard it would be for an enemy to hit them
                # this includes the move speed needed to reach them, including difficult terrain


                # if the entity is flanked by enemies, punish
                # if two or more enemies are in spaces adjacent to the entity,
                


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




def post_obj_reward_series_calc2(act_loc_obj_rew_series, acting_entity):
    #print(action_series_full_list)

    post_object_list = []

    for i in range(len(act_loc_obj_rew_series)):
        #print('')
        #print(act_loc_obj_rew_series[i])

        action_series = act_loc_obj_rew_series[i][0]
        location_series = act_loc_obj_rew_series[i][1]
        object_series = act_loc_obj_rew_series[i][2]
        reward = act_loc_obj_rew_series[i][3]
    
        #print(f'action series: {action_series}')
        #print(f'location series: {location_series}')
        #print(f'object series list: {object_series_list}')
        #print(f'reward: {reward}')

        # actions that are only move_actions
        move_act_series = [x for x in action_series if x in move_subactions]
        #print(f'move act series: {move_act_series}')

        # locations that are only move_actions
        move_loc_series = [location_series[y] for y in range(len(location_series)) if action_series[y] in move_subactions]
        #print(f'move loc series: {move_loc_series}')



        if move_loc_series != []:

            # move_act_loc needs to be a representation of each move_subaction being used (pulled from the action_series) and each location that it's moving to (pulled from the location_series)
            #move_act_loc = ([x for x in action_series if x in move_subactions],[location_series[y] for y in range(len(location_series)) if move_act_series[y] in move_subactions])
            #print(f'move action location series: {move_act_loc}')


            move_path = calculate_full_path(acting_entity.location, [move_act_series,move_loc_series])
            #print(f'move path: {move_path}')


        if object_series != []:
            post_obj_reward = reward

            # if the object action targets entity's location, but inventory is empty...
            
            # if they end their turn prone while adjacent to an enemy
            if 19 in action_series and 20 not in action_series[:-action_series.index(19)]:
                if move_path != [] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                    post_obj_reward -= 1
            
            # if the path is in a circle...
            # if the 
            
            # if the pickup action was taken, and the object was a coin, reward
                #if any([4 in action_series, 7 in action_series]):
                    # the object associated with the subaction
                #    obj = obj_series[action_series.index(4) or action_series.index(7)]
                #    if obj.Type == 'coin':
                #        post_obj_reward += 1
            if 4 in action_series:
                #print(f'here 4: {object_series[action_series.index(4)]}')
                if object_series[action_series.index(4)].name == 'coin':
                    post_obj_reward += 1
            if 7 in action_series:
                #print(f'here 7: {object_series[action_series.index(7)]}')
                if object_series[action_series.index(7)].name == 'coin':
                    post_obj_reward += 1


            # the potential damage, without taking the target into account
            damage_series = damage_calc2([action_series, location_series, object_series],acting_entity)
            #print(f'damage series: {damage_series}')
            post_obj_reward += sum(damage_series)
            

            # the risk based on the number of enemies that can be seen

            # the AC of an entity throughout the turn, such as donning armor or using a shield

            # if the damage dealt would reduce the target to 0 hp, reward


            # reward when you don shield, small penalty when you equip it
            # if the action is 13 and object is shield, reward
            if 13 in action_series:
                if object_series[action_series.index(13)].type == 'shield':
                    post_obj_reward += 1
                
            if 13 in action_series:
                if object_series[action_series.index(13)].type == 'shield':
                    if acting_entity.shield_proficiency == False:
                        post_obj_reward -= 1

            # if the action is in [25,26,37,38] and the object is a shield, penalize
            #if any(x in action_series for x in [25,26,37,38]):
            #    if obj_series[action_series.index(25) or action_series.index(26) or action_series.index(37) or action_series.index(38)].type == 'shield':
            #        post_obj_reward -= 1

            #print(f'action series: {action_series}')
            #print(f'object series: {object_series}')
            obj_act_series = [x for x in action_series if x in subactions_req_objects]
            #print(f'obj act series: {obj_act_series}')

            # rewrite the above using four if statements instead of the [or] statement
            if 25 in action_series:
                if object_series[obj_act_series.index(25)].type == 'shield':
                    post_obj_reward -= 1
            if 26 in action_series:
                if object_series[obj_act_series.index(26)].type == 'shield':
                    post_obj_reward -= 1
            if 37 in action_series:
                #print(action_series.index(37))
                if object_series[obj_act_series.index(37)].type == 'shield':
                    post_obj_reward -= 1
            if 38 in action_series:
                if object_series[obj_act_series.index(38)].type == 'shield':
                    post_obj_reward -= 1




            # if an item is equipped and then unequipped and then equipped again, punish

            # if an item is picked up and then dropped, punish

            # if an item is picked up and then equipped and then unequipped and then dropped, punish

            # if an item is equipped and item.casting_focus == True, and the cast action (14) is taken, reward
            #if any(x in action_series for x in [25,26,37,38]):
            #    if obj_series[action_series.index(25) or action_series.index(26) or action_series.index(37) or action_series.index(38)].casting_focus == True:
            #        if 14 in [x for x in action_series if x in action_series[action_series.index(25) or action_series.index(26) or action_series.index(37) or action_series.index(38):]]:
            #            post_obj_reward += 1

            # rewrite the above using four if statements instead of the [or] statement
            if 25 in action_series:
                if object_series[obj_act_series.index(25)].casting_focus == True:
                    if 14 in action_series[action_series.index(25):]:
                        post_obj_reward += 1
            if 26 in action_series:
                if object_series[obj_act_series.index(26)].casting_focus == True:
                    if 14 in action_series[action_series.index(26):]:
                        post_obj_reward += 1
            if 37 in action_series:
                if object_series[obj_act_series.index(37)].casting_focus == True:
                    if 14 in action_series[action_series.index(37):]:
                        post_obj_reward += 1
            if 38 in action_series:
                if object_series[obj_act_series.index(38)].casting_focus == True:
                    if 14 in action_series[action_series.index(38):]:
                        post_obj_reward += 1
            

            # if an item is equipped and it is a potion and then drink potion (33) is taken, reward
            #if any(x in action_series for x in [25,26,37,38]):
            #    if object_series[obj_act_series.index(25) or obj_act_series.index(26) or obj_act_series.index(37) or obj_act_series.index(38)].type == 'potion':
            #        if 33 in [x for x in action_series if x in action_series[action_series.index(25) or action_series.index(26) or action_series.index(37) or action_series.index(38):]]:
            #            post_obj_reward += 1

            # rewrite the above using four if statements instead of the [or] statement

            if 25 in action_series:
                if object_series[obj_act_series.index(25)].type == 'potion':
                    if 33 in action_series[action_series.index(25):]:
                        post_obj_reward += 1
            if 26 in action_series:
                if object_series[obj_act_series.index(26)].type == 'potion':
                    if 33 in action_series[action_series.index(26):]:
                        post_obj_reward += 1
            if 37 in action_series:
                if object_series[obj_act_series.index(37)].type == 'potion':
                    if 33 in action_series[action_series.index(37):]:
                        post_obj_reward += 1
            if 38 in action_series:
                if object_series[obj_act_series.index(38)].type == 'potion':
                    if 33 in action_series[action_series.index(38):]:
                        post_obj_reward += 1


            # for each instance of DisADV an enemy would have against the entity, reward

            # for each instance of ADV the entity would have against an enemy, reward

            # for each instance of ADV an enemy would have against the entity, punish

            # for each instance of DisADV the entity would have against an enemy, punish


            new_act_loc_rew_series = (action_series, location_series, object_series, post_obj_reward)
            post_object_list.append(new_act_loc_rew_series)
        else:
            # if statement if any item in action_series in object_subactiions
            post_obj_reward = reward
            if any(item in action_series for item in subactions_req_objects):
                post_obj_reward -= 10

            act_loc_obj_rew_item = (action_series, location_series, [], post_obj_reward)
            post_object_list.append(act_loc_obj_rew_item)

    #return_set = (action_series, location_series, object_series_list, post_obj_reward)
    post_object_list = sorted(post_object_list, key=lambda x: x[3],reverse=True)
    return post_object_list

