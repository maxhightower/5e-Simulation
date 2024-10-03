import numpy as np
import collections
from DFS_Universal_Rules import action_subactions, move_subactions, attack_subactions, free_subactions, subactions_req_objects, effect_subactions, effect_dictionary



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

    print(f"Total Qualifiers: {len([x for x in reward_series_full_list if x >= 6])}")
    print()

    # Print individual rewards and actions
    #print("Individual Rewards and Actions:")
    #for i, (reward, action) in enumerate(zip(reward_series_full_list, action_series_full_list)):
    #    print(f'{i}: {reward} - {action}')

def generate_pseudo_history(acting_entity,sequence, post_location_reward_list, object_subaction_index):
    potential_objects = []
    worldly_objects = acting_entity.world.objects

    action_series = post_location_reward_list[0]
    location_series = post_location_reward_list[1]
    object_series = [x for x in action_series if x in subactions_req_objects]
    print(f'object series: {object_series}')
    print(f'object subaction index: {object_subaction_index}')
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
                if subaction == 48 and main_hand[0] == off_hand[0] and main_hand[0].hands == 2:
                    damage = main_hand[0].damage + acting_entity.strength_mod
                
                if subaction == 5:
                    damage = main_hand[0].damage + acting_entity.strength_mod
                
            if subaction == 15:
                damage = main_hand[0].damage


        elif subaction == 36: # unarmed strike
            damage = max(acting_entity.strength_mod, 1)

    else:
        #print('not an attack subaction')
        pass

    return damage
    # need to identify the entity, the weapon, and the target
    # eventually the input needs to be changed to the the act_loc_obj_rew

def damage_calc2(act_loc_obj_rew, acting_entity):
    action_series = act_loc_obj_rew[0]
    location_series = act_loc_obj_rew[1]
    object_series = act_loc_obj_rew[2]
    reward = act_loc_obj_rew[3]

    attack_and_effect_series = [x for x in action_series if x in attack_subactions or x in effect_subactions]
    attack_series = [x for x in action_series if x in attack_subactions]

    pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity, object_series, act_loc_obj_rew, len(object_series))

    # I'm going to need to calculate the damage for each damage dealing subaction within the action_series
    damage_series = []

    for subaction in attack_series:
        subaction_damage = 0
        # first find the order of attacks, then identify the effects used that are associated with the attack
        relevant_effects = attack_and_effect_series[attack_series.index(subaction):]
        
        for i in relevant_effects:
            if effect_dictionary[i].type == 'damage_bonus':
                subaction_damage += effect_dictionary[i].effect

        
        # this is currently setup to assign a single effect to only the next attack, not all attacks
        # perhaps there should be sub_effects and turn_effects,
        # sub_effects are only applied to the next attack, while turn_effects are applied to all attacks of a certain type in the turn
        # turn_effects are complicated enough to require representation in a list (or even a class???) 

        # or perhaps all effects need more details... such as duration, application circumstances, etc...





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
    if 25 in action_series:
        if 5 in action_series[action_series.index(25):]:
            reward_value += 1
    if 26 in action_series:
        if 5 in action_series[action_series.index(26):]:
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
        reward_value -= 0.5
    if 30 in action_series:
        reward_value -= 0.5
    if 42 in action_series:
        reward_value -= 0.5
    if 43 in action_series:
        reward_value -= 0.5
    if 44 in action_series:
        reward_value -= 0.5
    if 45 in action_series:
        reward_value -= 0.5
    if 46 in action_series:
        reward_value -= 0.5
    if 47 in action_series:
        reward_value -= 0.5

    # if the entity unequips an item, and doesn't equip something later, punish
    # equip: 25, 26, 37, 38, 13
    # unequip: 31, 32, 40, 41, 39

    #if 25 in action_series:
    #    if 31 not in action_series[action_series.index(25):]:


    # new rewards to add
    # perhaps dropping items should be discouraged
    if 29 in action_series or 30 in action_series:
        reward_value -= 1
    




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
                
                
                # punishing for each enemy that can see the entity
                if move_path != []:   
                    vis_count = len(check_visibility(move_path[-1], acting_entity.world.enemy_locations, acting_entity.world))
                    post_loc_reward -= vis_count/2


                # punishing slightly if the entity doesn't move
                if move_path == []:
                    post_loc_reward -= 0.5


                # if the object action targets entity's location, but inventory is empty...
                
                # if they end their turn prone while adjacent to an enemy 
                if 19 in action_series:
                    if len(move_path) > 1:
                        if 20 not in action_series[:-action_series.index(19)] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                           post_loc_reward -= 1
                        # need to add a check for if the enemy in enemy_adjacent_locations is currently visible, otherwise it shouldn't be taken into account by the acting entity
                
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
    #print(action_series_full_list)


    for i in range(len(action_series_full_list)):
        action_series = action_series_full_list[i]
        location_series = location_series_full_list[i]
        reward = reward_series_full_list[i]
        object_series_list = object_series_full_list[i]
    
        print(f'action series: {action_series}')
        print(f'location series: {location_series}')
        print(f'object series list: {object_series_list}')


        if object_series_list != []:
            for obj_series in object_series_list:
                post_obj_reward = reward

                # if the object action targets entity's location, but inventory is empty...
                
                # if they end their turn prone while adjacent to an enemy
                if 19 in action_series and 20 not in action_series[:-action_series.index(19)] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                    post_obj_reward -= 1
                
                # if the path is in a circle...
                # if the 
                
                # if the pickup action was taken, and the object was a coin, reward
                if 4 in action_series or 7 in action_series:
                    # the object associated with the subaction
                    obj = obj_series[action_series.index(4) or action_series.index(7)]
                    if obj.Type == 'coin':
                        post_obj_reward += 1


                new_act_loc_rew_series = (action_series, location_series, obj_series, post_obj_reward)
                post_object_list.append(new_act_loc_rew_series)



    return_set = (action_series, location_series, object_series_list, post_obj_reward)
    post_object_list = sorted(return_set, key=lambda x: x[2],reverse=True)
    return post_object_list



def post_obj_reward_series_calc2(act_loc_obj_rew_series, acting_entity):
    #print(action_series_full_list)

    post_object_list = []

    for i in range(len(act_loc_obj_rew_series)):
        print('')
        #print(act_loc_obj_rew_series[i])

        action_series = act_loc_obj_rew_series[i][0]
        location_series = act_loc_obj_rew_series[i][1]
        reward = act_loc_obj_rew_series[i][3]
        object_series_list = act_loc_obj_rew_series[i][2]
    
        print(f'action series: {action_series}')
        print(f'location series: {location_series}')
        print(f'object series list: {object_series_list}')
        print(f'reward: {reward}')

        # actions that are only move_actions
        move_act_series = [x for x in action_series if x in move_subactions]
        print(f'move act series: {move_act_series}')

        # locations that are only move_actions
        move_loc_series = [location_series[y] for y in range(len(location_series)) if action_series[y] in move_subactions]
        print(f'move loc series: {move_loc_series}')



        if move_loc_series != []:

            # move_act_loc needs to be a representation of each move_subaction being used (pulled from the action_series) and each location that it's moving to (pulled from the location_series)
            move_act_loc = ([x for x in action_series if x in move_subactions],[location_series[y] for y in range(len(location_series)) if move_act_series[y] in move_subactions])
            print(f'move action location series: {move_act_loc}')


            move_path = calculate_full_path(acting_entity.location, move_act_loc)
            print(f'move path: {move_path}')


        if object_series_list != []:
            for obj_series in object_series_list:
                post_obj_reward = reward

                # if the object action targets entity's location, but inventory is empty...
                
                # if they end their turn prone while adjacent to an enemy
                if 19 in action_series and 20 not in action_series[:-action_series.index(19)]:
                    if move_path != [] and move_path[-1] in acting_entity.world.enemy_adjacent_locations:
                        post_obj_reward -= 1
                
                # if the path is in a circle...
                # if the 
                
                # if the pickup action was taken, and the object was a coin, reward
                if obj_series != []:
                    #if any([4 in action_series, 7 in action_series]):
                        # the object associated with the subaction
                    #    obj = obj_series[action_series.index(4) or action_series.index(7)]
                    #    if obj.Type == 'coin':
                    #        post_obj_reward += 1
                    if 4 in action_series:
                        print(f'here 4: {obj_series[action_series.index(4)]}')
                        if obj_series[action_series.index(4)].name == 'coin':
                            post_obj_reward += 1
                    if 7 in action_series:
                        print(f'here 7: {obj_series[action_series.index(7)]}')
                        if obj_series[action_series.index(7)].name == 'coin':
                            post_obj_reward += 1


                # the potential damage, without taking the target into account
                damage_calc()


                # the risk based on the number of enemies that can be seen

                # the AC of an entity throughout the turn, such as donning armor or using a shield

                # 

                new_act_loc_rew_series = (action_series, location_series, obj_series, post_obj_reward)
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

