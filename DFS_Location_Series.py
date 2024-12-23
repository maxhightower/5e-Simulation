# Location Series Depth by First Search

import numpy as np

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, adjacent_locations_entities, chebyshev_distance, chebyshev_distance_entities, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility
from DFS_World_States import world, world_grid_states

import DFS_Action_Series

from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, subactions_req_targets, object_subactions, entity, target_distance_scores
from DFS_Entities import entity

# this one handles location series
class RuleBasedLocationSequenceDFS2:
    def __init__(self, action_series_list, reward_series_list, target_distance_scores, location_rules, acting_entity):
        self.action_series_list = action_series_list
        self.reward_series_list = reward_series_list
        self.target_distance_scores = target_distance_scores
        self.location_rules = location_rules
        self.acting_entity = acting_entity

        self.location_series_list = []
        
        self.sequences = []
        


    # I think what I want to have happen is that self.sequences will be filled per action_series 
    # then appended to location_series_list 
    # then reset and used for the next action_series

    def get_potential_locations(self, sub_index, tar_act_series, current_sequence, acting_entity, grid_locations):
        # identify the distance the subaction allows
        #print('')
        #print('--entered potential locations--')
        subaction = tar_act_series[sub_index]
        distance_allowable = target_distance_scores[subaction]

        # identify the entity's location at that given subaction
        entity_loc_series = [current_sequence[loc_index] for loc_index in range(len(current_sequence)) if tar_act_series[loc_index] in move_subactions]
        
        #print(f'Entity_loc_series: {entity_loc_series}')
        if len(entity_loc_series) < 1:
            entity_location = acting_entity.location
        else:
            entity_location = entity_loc_series[-1]


        # identify which locations/spaces can be accessed within that distance
        locations_accessible = []
        for loc in grid_locations:
            #if chebyshev_distance(entity_location, loc) <= distance_allowable:
            #    locations_accessible.append(loc)

            if chebyshev_distance_entities(acting_entity, loc) <= distance_allowable:
                locations_accessible.append(loc)


        #print(f'locations accessible {locations_accessible}')
        #print(f'entity is at {entity_location}; allowable distance for action {subaction} is {distance_allowable}; locations accessible are {locations_accessible}')

        #print(f'Locations accessible: {locations_accessible}')
        #print(' ')
        return locations_accessible


    def check_rules(self, sequence, next_loc, acting_entity, action_series):
        return all(location_rule(sequence, next_loc, acting_entity, action_series) for location_rule in self.location_rules)


    def dfs(self, action_series, current_sequence, grid_locations):
        tar_act_series = [i for i in action_series if i in subactions_req_targets]
        required_sequence_length = len(tar_act_series)
        
        if len(current_sequence) == required_sequence_length:
            #print(f'finishing if current sequence: {current_sequence}')
            return [current_sequence.copy()]  # Return a list containing the completed sequence
        
        all_sequences = []
        sub_index = len(current_sequence)  # This ensures we're looking at the correct subaction
        
        locations_accessible = self.get_potential_locations(
            sub_index=sub_index,
            tar_act_series=tar_act_series,
            current_sequence=current_sequence,
            acting_entity=self.acting_entity,
            grid_locations=grid_locations
        )

        for next_loc in locations_accessible:
            if self.check_rules(current_sequence, next_loc, self.acting_entity, tar_act_series):
                current_sequence.append(next_loc)
                all_sequences.extend(self.dfs(action_series, current_sequence, grid_locations))
                current_sequence.pop()
        
        #print(f'sequences being returned from dfs to results 1 {all_sequences[:20]}')
        return all_sequences

    def generate_sequences(self):
        grid_locations = [
            [x - 5, y - 5]
            for x in range(len(self.acting_entity.world.grid))
            for y in range(len(self.acting_entity.world.grid[x]))
        ]
        quality_threshold = np.percentile(self.reward_series_list, 99) 
        print(f'Quality threshold: {quality_threshold}')

        for action_series_index, action_series in enumerate(self.action_series_list):

            if self.reward_series_list[action_series_index] >= quality_threshold:
                #print('')
                #print('---------------------')
                #print(f'{action_series}: {self.reward_series_list[action_series_index]}')
                
                sequences = self.dfs(
                    action_series=action_series,
                    current_sequence=[],
                    grid_locations=grid_locations
                )
                
                self.location_series_list.append(sequences)
            
            else: 
                self.location_series_list.append([])
        
        #print(f'Finished generate sequences: {self.location_series_list}')
        return self.location_series_list




def rule_location_spacing_rule(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    move_points = {
            0: 1, 
            1: 2, 
            2: 3, 
            3: 4, 
            20: acting_entity.speed/2,
            23: 5,
            24: 6,
            54: acting_entity.speed/2,
            56: acting_entity.speed/2,
            }


    #act_loc_zip = zip(tar_act_req,sequence)
    #for i in range(len(tar_act_req)):
    # if next_loc is further away from the previous location than the action allows, false
    #if chebyshev_distancenext_loc...move_points[tar_act_req[len(sequence)+1]]
    # is this one even needed because of the locations_includable???
    return True

def rule_no_unaddressed_location_series(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    if len(sequence) + 1 < len(tar_act_req):
        print('no unaddressed locations')
        return False
    return True

def rule_no_excess_locations(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    if len(sequence) + 1 > len(tar_act_req):
        print('no excess locations')
        return False
    return True

def rule_no_repeating_locations(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    for act_index in range(len(sequence)):
        loc = sequence[act_index]
        act = sequence[act_index]

        if act in move_subactions and next_loc == loc:
            #print('no repeating move locations')
            return False

    return True


def rule_attacks_target_enemies(sequence, next_loc, acting_entity, action_series):

    # if tar_act_req[action_index] == 5:
    #    print(f'sequence {sequence}')
    #    print(f'action_index for next_loc ({next_loc}): {action_index}; action: {tar_act_req[action_index]}')
    #    print(f'tar_act_req: {tar_act_req}')

    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if tar_act_req[loc_index] in move_subactions]
        #print(f'Entity_loc_series: {entity_loc_series}')
    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location
    else:
        entity_location = entity_loc_series[-1]
    action_index = len(sequence)

    #print(acting_entity.world.enemy_locations)
    #print(next_loc)
    if tar_act_req[action_index] in attack_subactions:
        if next_loc not in acting_entity.world.enemy_locations:
            #print('attack does not target enemies')
            #print('false')
            return False
    
    #print('passed the enemy test')
    return True


def rule_objects_target_objects(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if tar_act_req[loc_index] in move_subactions]
        #print(f'Entity_loc_series: {entity_loc_series}')
    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location
    else:
        entity_location = entity_loc_series[-1]
    action_index = len(sequence)

    #print(f'item locations: {acting_entity.world.coin_locations}')
    print(action_series)
    print(action_index)
    print(tar_act_req)
    print(tar_act_req[action_index])

    if tar_act_req[action_index] in attack_subactions:
        if next_loc not in acting_entity.world.coin_locations or next_loc == entity_location:
            #print('object does not target object')
            return False
        
    
    return True

def rule_hide_in_low_light(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    action_index = len(sequence)
    if tar_act_req[action_index] == 9:
        x, y = next_loc
        if acting_entity.world.grid[x][y][3] not in [2,3]:
            #print('cannot hide in bright light')
            return False
    return True

# what about large creatures hiding in low light?



def rule_move_space_efficiency(sequence, next_loc, acting_entity, action_series):
    pass
    # essentially, the move should be efficient and not going in a circle
    # efficient movement should be calculated via vectors??? or geometry???

def rule_move_speed_efficiency(sequence, next_loc, acting_entity, action_series):
    move_points = {
        0: 1, 
        1: 2, 
        2: 3, 
        3: 4, 
        20: acting_entity.speed/2,
        23: 5,
        24: 6,
        54: acting_entity.speed/2,
        56: acting_entity.speed/2,
        }
    # essentially, the move shouldn't use more speed than available via difficult terrain
    # will need to calculate the sum of the move speed spent according to each loc used on a move_subaction
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    total_move_speed_spent = 0
    
    difficult_terrain = False
    for loc_index in range(len(sequence)):

        if tar_act_req[loc_index] in move_subactions:
            # causes of difficult terrain
            # - enemy creature

            if acting_entity.world.grid[sequence[loc_index]][0] == 1:
                difficult_terrain = True
            
            if acting_entity.world.grid[sequence[loc_index]][2] == 1:
                difficult_terrain = True
            
            if difficult_terrain == True:
                total_move_speed_spent += move_points[tar_act_req[loc_index]] * 2

            elif difficult_terrain == False:
                total_move_speed_spent += move_points[tar_act_req[loc_index]]
                
    if total_move_speed_spent >= acting_entity.speed:
        return False
    
    if acting_entity.world.grid[next_loc][0] == 1 or acting_entity.world.grid[sequence[loc_index]][2] == 1:
        difficult_terrain = True

    move_speed_required_for_next_action = move_points[tar_act_req[len(sequence)]]

    if difficult_terrain == True:
       move_speed_required_for_next_action = move_points[tar_act_req[len(sequence)]] * 2


    if tar_act_req[len(sequence)] in move_subactions and total_move_speed_spent + move_speed_required_for_next_action > acting_entity.speed:
        return False
    
    return True

# what about large creatures? if a single space is difficult terrain, is the whole space difficult terrain?


def rule_enemy_attempt_2(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    action_index = len(sequence)
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if tar_act_req[loc_index] in move_subactions]
    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location
    else:
        entity_location = entity_loc_series[-1]
    
    if len(acting_entity.world.grid2[next_loc[0]][next_loc[1]][5]) == 0:
        return False
    
    return True

def rule_object_attempt_2(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    action_index = len(sequence)
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if tar_act_req[loc_index] in move_subactions]
    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location
    else:
        entity_location = entity_loc_series[-1]
    
    subaction = tar_act_req[action_index]
    if subaction in [4,7]:
        if acting_entity.world.grid2[next_loc[0]][next_loc[1]][6] == []:
            return False
    elif subaction in [25,26]:
        if acting_entity.inventory == [] and acting_entity.weapon_equipped == []:
            return False

    return True

def rule_mount_must_have_entity(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    action_index = len(sequence)
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if tar_act_req[loc_index] in move_subactions]
    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location
    else:
        entity_location = entity_loc_series[-1]
    
    action = tar_act_req[action_index]
    if action == 54:
       if acting_entity.world.grid2[next_loc[0]][next_loc[1]][5] == []:
            return False
    
    return True

def rule_mount_must_be_size_larger(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    action_index = len(sequence)
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if tar_act_req[loc_index] in move_subactions]
    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location
    else:
        entity_location = entity_loc_series[-1]
    
    action = tar_act_req[action_index]

    sizes = ['tiny','small','medium','large','huge','gargantuan']

    if len(acting_entity.world.grid2[next_loc[0]][next_loc[1]][5]) == 1:
        if action == 54:
            mount_size = acting_entity.world.grid2[next_loc[0]][next_loc[1]][5][0].size
            entity_size = acting_entity.size
            mount_size_index = sizes.index(mount_size)
            entity_size_index = sizes.index(entity_size)
            if mount_size_index <= entity_size_index:
                return False

    return True


location_rules = [
    #rule_location_spacing_rule,
    #rule_no_excess_locations,
    rule_no_repeating_locations,
    #rule_no_unaddressed_location_series,
    #rule_attacks_target_enemies,
    #rule_objects_target_objects,
    rule_hide_in_low_light,
    #rule_move_space_efficiency,
    #rule_move_speed_efficiency,
    rule_enemy_attempt_2,
    rule_object_attempt_2,
    rule_mount_must_have_entity,
    rule_mount_must_be_size_larger,
]

location_rules_sources = ['standard'] * len(location_rules)


class RuleBasedLocationSequenceDFS3:
    def __init__(self, acting_entity, action_reward_series_full_list):
        self.acting_entity = acting_entity
        self.action_reward_series_full_list = action_reward_series_full_list
        self.target_distance_scores = acting_entity.target_distance_scores
        self.location_rules_permit = acting_entity.dfs_rules['location_rules']['permit']


        self.location_series_list = []
        
        self.sequences = []
        


    # I think what I want to have happen is that self.sequences will be filled per action_series 
    # then appended to location_series_list 
    # then reset and used for the next action_series

    def get_potential_locations(self, sub_index, tar_act_series, current_sequence, grid_locations):
        # identify the distance the subaction allows
        #print('')
        #print('--entered potential locations--')
        subaction = tar_act_series[sub_index]
        distance_allowable = target_distance_scores[subaction]

        # identify the entity's location at that given subaction
        entity_loc_series = [current_sequence[loc_index] for loc_index in range(len(current_sequence)) if tar_act_series[loc_index] in move_subactions]
        
        #print(f'Entity_loc_series: {entity_loc_series}')
        if len(entity_loc_series) < 1:
            entity_location = self.acting_entity.location
        else:
            entity_location = entity_loc_series[-1]


        # identify which locations/spaces can be accessed within that distance
        locations_accessible = []
        for loc in grid_locations:
            #if chebyshev_distance(entity_location, loc) <= distance_allowable:
            #    locations_accessible.append(loc)

            if chebyshev_distance_entities(self.acting_entity, loc) <= distance_allowable:
                locations_accessible.append(loc)


        #print(f'locations accessible {locations_accessible}')
        #print(f'entity is at {entity_location}; allowable distance for action {subaction} is {distance_allowable}; locations accessible are {locations_accessible}')

        #print(f'Locations accessible: {locations_accessible}')
        #print(' ')
        return locations_accessible


    def check_rules(self, sequence, next_loc, action_reward_series):
        return all(location_rule(sequence, next_loc, self.acting_entity, action_reward_series[0]) for location_rule in self.location_rules_permit)



    def dfs(self, action_reward_series, current_sequence, grid_locations):
        #print(f'start of dfs: {action_reward_series}')
        if len(action_reward_series) == 0:
            return action_reward_series
        
        else:

            tar_act_series = [i for i in action_reward_series if i in subactions_req_targets]
            required_sequence_length = len(tar_act_series)
            
            if len(current_sequence) == required_sequence_length:
                #print(f'finishing if current sequence: {current_sequence}')
                return [current_sequence.copy()]  # Return a list containing the completed sequence
            
            all_sequences = []
            sub_index = len(current_sequence)  # This ensures we're looking at the correct subaction
            
            locations_accessible = self.get_potential_locations(
                sub_index=sub_index,
                tar_act_series=tar_act_series,
                current_sequence=current_sequence,
                grid_locations=grid_locations
            )

            for next_loc in locations_accessible:
                if self.check_rules(current_sequence, next_loc, tar_act_series):
                    current_sequence.append(next_loc)
                    all_sequences.extend(self.dfs(action_reward_series, current_sequence, grid_locations))
                    current_sequence.pop()
            
        #print(f'sequences being returned from dfs to results 1 {all_sequences[:20]}')
        return all_sequences

    def generate_sequences(self):
        action_location_reward_series_list = []

        grid_locations = [
            [x - 5, y - 5]
            for x in range(len(self.acting_entity.world.grid))
            for y in range(len(self.acting_entity.world.grid[x]))
        ]
        quality_threshold = np.percentile([x[1] for x in self.action_reward_series_full_list], 99) 
        print(f'Quality threshold: {quality_threshold}')

        for action_reward_series in self.action_reward_series_full_list:
            #print(f'for loop in generate_sequences: {action_reward_series}')

            action_series = action_reward_series[0]
            reward = action_reward_series[1]
            #print(f"Reward: {reward}")
            if reward >= quality_threshold:
                #print('')
                #print('---------------------')
                #print(f'{action_series}: {self.reward_series_list[action_series_index]}')
                
                sequences = self.dfs(
                    action_reward_series=action_reward_series,
                    current_sequence=[],
                    grid_locations=grid_locations
                )

                self.location_series_list.append(sequences)
            
        for action_index in range(len(self.action_reward_series_full_list)):
            action_series = self.action_reward_series_full_list[action_index][0]
            reward = self.action_reward_series_full_list[action_index][1]
            sequences = self.location_series_list[action_index]

            if len(sequences) > 0:
                for sequence in sequences:
                    action_location_reward_series_list.append([action_series, sequences, reward])
                    print(f'{action_series}, {reward}, {sequence}')
            #else: 
            #    self.location_series_list.append([])

        
        #print(f'Finished generate sequences: {self.location_series_list}')
        return action_location_reward_series_list

def rule_move_subactions_targetable_distance(sequence, next_loc, acting_entity, action_series):
    move_points = acting_entity.subaction_catalog['move_cost_dict']
    target_distance_scores = acting_entity.subaction_catalog['target_distance_scores']

    tar_act_req = [x for x in action_series if x in acting_entity.subaction_catalog['subactions_req_targets']]

    # if the location targeted is further away than the action allows, false

    # first determine where the entity currently is located (this may have changed depending on the sequence)
    entity_loc_series = [sequence[loc_index] for loc_index in range(len(sequence)) if action_series[loc_index] in acting_entity.subaction_catalog['move_subactions']]

    if len(entity_loc_series) < 1:
        entity_location = acting_entity.location[0]
    else:
        entity_location = entity_loc_series[-1]

    # then determine the distance the action allows
    distance_allowable = target_distance_scores[action_series[len(sequence)]]

    # then determine the distance between the entity and the target location
    distance_to_target = chebyshev_distance_entities(acting_entity, next_loc)

    if distance_to_target > distance_allowable:
        return False
    
    return True



def rule_no_unaddressed_location_series(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    if len(sequence) + 1 < len(tar_act_req):
        return False
    return True

def rule_no_excess_locations(sequence, next_loc, acting_entity, action_series):
    tar_act_req = [x for x in action_series if x in subactions_req_targets]
    if len(sequence) + 1 > len(tar_act_req):
        return False
    return True



location_rules_permit = [
    rule_move_subactions_targetable_distance,
    rule_no_unaddressed_location_series,
]
