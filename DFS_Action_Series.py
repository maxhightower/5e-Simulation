# Action Series Depth by First Search

import numpy as np
import multiprocessing
 

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, adjacent_locations_entities, chebyshev_distance, chebyshev_distance_entities, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility
from DFS_World_States import world, world_grid_states

from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, bonus_subactions, object_action_subactions, object_free_subactions, subactions_req_allies, entity, subaction_dict

from DFS_Entities import entity


class RuleBasedSequenceDFS:
    def __init__(self, min_length, max_length, start, end, rules, acting_entity):
        self.min_length = min_length
        self.max_length = max_length
        self.start = start
        self.end = end
        self.rules = rules
        self.sequences = []
        self.acting_entity = acting_entity

    def check_rules(self, sequence, next_num, acting_entity):
        # Apply all rules to the current sequence and next number
        return all(rule(sequence, next_num, acting_entity) for rule in self.rules)

    def dfs(self, current_sequence):
        # Check if the current sequence is within the desired length range
        if self.min_length <= len(current_sequence) <= self.max_length:
            self.sequences.append(current_sequence.copy())
        
        # Continue exploring if we haven't reached the maximum length
        if len(current_sequence) < self.max_length:
            for next_num in range(self.start, self.end + 1):
                if self.check_rules(current_sequence, next_num, self.acting_entity):
                    current_sequence.append(next_num)
                    self.dfs(current_sequence)
                    current_sequence.pop()  # Backtrack


    def generate_sequences(self):
        self.dfs([])
        return self.sequences


# rules
# - only one action
def rule_only_one_action(sequence, next_num, acting_entity):
    if next_num in action_subactions and sum(1 for seq in sequence if seq in action_subactions) == 1:
        return False
    return True

def rule_only_one_bonus_action(sequence, next_num, acting_entity):
    if next_num in bonus_subactions and sum(1 for seq in sequence if seq in bonus_subactions) == 1:
        return False
    return True

def rule_one_of_each_free_action(sequence, next_num, acting_entity):
    # free_subactions = [[4,25,27,29,31],[14]] # can do one of each list
    if next_num in free_subactions[0] and sum(1 for seq in sequence if seq in free_subactions[0]) == 1:
        return False
    if next_num in free_subactions[1] and sum(1 for seq in sequence if seq in free_subactions[1]) == 1:
        return False
    return True



def rule_no_redundant_moves(sequence, next_num, acting_entity):
    
    if len(sequence) > 0:
        if next_num == 0 and sequence[-1] == 0:
            return False
        if next_num == 1 and sequence[-1] == 1:
            return False
        if next_num == 2 and sequence[-1] == 2:
            return False
        if next_num == 3 and sequence[-1] == 3:
            return False
        
        if next_num == 0 and sequence[-1] == 1:
            return False
        if next_num == 1 and sequence[-1] == 0:
            return False
        
        if next_num == 1 and sequence[-1] == 2:
            return False
        if next_num == 2 and sequence[-1] == 1:
            return False
        
        if next_num == 0 and sequence[-1] == 2:
            return False
        if next_num == 2 and sequence[-1] == 0:
            return False
        
        if next_num == 0 and sequence[-1] == 3:
            return False
        if next_num == 3 and sequence[-1] == 0:
            return False
        
        if next_num == 0 and sequence[-1] == 23:
            return False
        if next_num == 23 and sequence[-1] == 0:
            return False
        
        if next_num == 2 and sequence[-1] == 3:
            return False
        if next_num == 3 and sequence[-1] == 2:
            return False
    
    #if len(sequence) == 0:
    #    return False

    #invalid_pairs = [
    #    (0, 0), (1, 1), (2, 2), (3, 3),
    #    (0, 1), (1, 0),
    #    (1, 2), (2, 1),
    #    (0, 2), (2, 0),
    #    (0, 3), (3, 0),
    #    (0, 23), (23, 0),
    #    (2, 3), (3, 2)
    #]

    #return any((next_num, sequence[-1]) == pair for pair in invalid_pairs)

    return True

def rule_limited_move_speed(sequence, next_num, acting_entity):
    move_speed = acting_entity.speed
    move_points = {
                0: 1, 
                1: 2, 
                2: 3, 
                3: 4, 
                19: 0,
                20: move_speed/2,
                23: 5,
                24: 6,
                54: move_speed/2,
                56: move_speed/2,
                }

    speed_spent = 0

    if 'prone' not in acting_entity.conditions:
        prone = 1
    else:
        prone = 2

    move_series = [x for x in sequence if x in move_subactions or x == 19 or x == 20]

    for i in move_series:
        if i == 19 and prone == False:
            prone = 2
        
        if i == 20 and prone == True:
            prone = 1

        speed_spent += move_points[i] * prone
    

    if next_num in move_subactions or next_num == 20:
        if move_points[next_num] + (speed_spent * prone) > move_speed:
            return False
        
    return True



def rule_one_of_each_free_action(sequence, next_num, acting_entity):
    # free_subactions = [[4,25,27,29,31],[14]] # can do one of each list
    if next_num in free_subactions[0] and sum(1 for seq in sequence if seq in free_subactions[0]) == 1:
        return False

    if next_num in free_subactions[1] and sum(1 for seq in sequence if seq in free_subactions[1]) == 1:
        return False

    return True


def rule_shield(sequence, next_num, acting_entity):
    # we need to check if it's possible to don a shield before allowing sequence that does so
    if next_num == 13:
    # first lets check if a shield actually exists to be donned
        # if there is not a shield in the inventory, then one must be picked up first
        if not any(item.type == 'shield' for item in acting_entity.inventory):
            # if there aren't any shields in the world, there isn't one to pick up
            if not any(item.type == 'shield' for item in acting_entity.world.objects):
                return False
            
            # if there are shields in the world, but none in the inventory, then the shield must be picked up first
            if not any(item in sequence for item in [4,7]):
                return False
    
    return True

def rule_concentration(sequence, next_num, acting_entity):
    if acting_entity.concentration == False and 11 not in sequence:
        if next_num == 14:
            return False

    return True

def rule_actions_requiring_allies(sequence, next_num, acting_entity):
    if acting_entity.world.non_enemies == []:
        if next_num in subactions_req_allies:
            return False
    return True

def rule_off_hand_two_weapons_requirement(sequence, next_num, acting_entity):
    list_of_subactions_that_equip_to_offhand = [37,38]
    # if one of the numbers in list_of_subactions_that_equip_to_offhand is in the sequence
    if not any(item in list_of_subactions_that_equip_to_offhand for item in sequence):
        if next_num == 15 and acting_entity.off_hand == []:
            return False

    return True

def rule_condition_rules(sequence, next_num, acting_entity):
    # escape grappled
    if next_num == 17 and 'grappled' not in acting_entity.conditions:
        return False
    # go prone
    if next_num == 19 and 'prone' in acting_entity.conditions:
        return False
    # stand up
    if next_num == 20 and 'grappled' in acting_entity.conditions:
        return False
    return True

def rule_standing_up_rules(sequence, next_num, acting_entity):
    # can't stand up twice
    if 'prone' not in acting_entity.conditions:
        prone = False
    else:
        prone = True
    
    for i in [x for x in sequence if x in [19,20]]:
        if i == 19:
            prone = True
        
        if i == 20:
            prone = False

    if prone == True and next_num == 19:
        return False
    
    if next_num == 20 and 19 not in sequence:
        return False
    return True

def rule_remove_redundant_prones(sequence, next_num, acting_entity):
    if len(sequence)>0:
        if next_num == 19 and sequence[-1] == 19:
            return False
        if 19 in sequence:
            # if between the last time 19 was called, there isn't a 20, false
            last_prone_index = len(sequence) - 1 - sequence[::-1].index(19)
            if 20 not in sequence[last_prone_index:] and next_num == 19:
                return False
    return True

def rule_remove_redundant_objects(sequence, next_num, acting_entity):
    if next_num in object_action_subactions:
        if any(item in object_action_subactions for item in sequence):
            return False

    if next_num in object_free_subactions:
        if any(item in object_free_subactions for item in sequence):
            return False
    return True

def rule_unequip_weapon(sequence, next_num, acting_entity):
    # eliminating extra series early
    # cannot unequip anything from hands if there's nothing in hands to start
    # AND there's not equip actions in the sequence
    if acting_entity.main_hand == [] and acting_entity.off_hand == []:
        # if any of the following numbers are in sequence: [25,26,37,38]
        if not any(num in sequence for num in {25,26,37,38}):
            if next_num in [31,32,40,41,42,43,44,45,46,47]: # if the next number would unequip from anywhere       
                return False
            
    return True

def rule_equip_weapon(sequence, next_num, acting_entity):
    if next_num in [25,26] and acting_entity.weapon_equipped != []:
        return False
    return True

def rule_object_number_limitation(sequence, next_num, acting_entity):
    # only object actions
    obj_act = [x for x in sequence if x in object_action_subactions]

    if next_num in object_action_subactions:
        # there can't be more object actions than there are objects in the world...
        if len(obj_act) > len(acting_entity.world.objects + acting_entity.inventory + acting_entity.weapon_equipped):
            return False
    return True

    # how should I actually limit object actions?

def rule_mount_subaction_range(sequence, next_num, acting_entity):
    # if there are no creatures within 1 space of the acting_entity, then the mount subactions are invalid
    # **** must take into account that the entity could move to a space where a mount could be mounted****

    # so at the very least, if it's the first subaction, then it's valid
    if next_num == 54 and len(sequence) == 0:
        for loc in adjacent_locations(acting_entity.location):
            if not any(entity.location == loc for entity in acting_entity.world.entities):
                return False
        
    #print(acting_entity)
    #print(acting_entity.location)
    # if there are no move_subactions in the sequence, then the mount subactions are invalid
    if next_num == 54 and not any(x in sequence for x in move_subactions):
        for loc in adjacent_locations_entities(acting_entity):
            if not any(entity.location == loc for entity in acting_entity.world.entities):
                return False

    return True

def rule_mount_once_per_turn(sequence, next_num, acting_entity):
    # if there's already a mount subaction in the sequence, then the next mount subaction is invalid
    if next_num == 54 and 54 in sequence:
        return False
    return True


# how should action series take a controlled mount into account?
# it should append the mount's subactions to the acting_entity's subactions
# 




action_rules_permit = [rule_only_one_action, 
         rule_only_one_bonus_action, 
         rule_no_redundant_moves,
         rule_limited_move_speed,
         rule_one_of_each_free_action,
         rule_shield,
         rule_concentration,
         rule_actions_requiring_allies,
         rule_off_hand_two_weapons_requirement,
         rule_condition_rules,
         rule_standing_up_rules,
         rule_remove_redundant_prones,
         rule_remove_redundant_objects,
         rule_unequip_weapon,
         rule_equip_weapon,
         rule_object_number_limitation,
         #rule_mount_subaction_range,
         rule_mount_once_per_turn,
         
]

action_rules_sources = ['standard'] * len(action_rules_permit)


controlled_mount_subactions = {
    '0': 'Dash',
    '1': 'Disengage',
    '2': 'Dodge',
    # and then it also gets its move speed subactions
}

mount_subaction_rules = [

]

mount_subaction_rules_sources = ['controlled_mount'] * len(mount_subaction_rules)


'''
class ParallelizedRuleBasedSequenceDFS:
    def __init__(self, min_length, max_length, start, end, rules, acting_entity):
        self.min_length = min_length
        self.max_length = max_length
        self.start = start
        self.end = end
        self.rules = rules
        self.acting_entity = acting_entity

    def check_rules(self, sequence, next_num):
        return all(rule(sequence, next_num, self.acting_entity) for rule in self.rules)

    def dfs(self, current_sequence, results):
        if self.min_length <= len(current_sequence) <= self.max_length:
            results.append(current_sequence.copy())
        
        if len(current_sequence) < self.max_length:
            for next_num in range(self.start, self.end + 1):
                if self.check_rules(current_sequence, next_num):
                    current_sequence.append(next_num)
                    self.dfs(current_sequence, results)
                    current_sequence.pop()

    def parallel_dfs(self, initial_sequence):
        manager = multiprocessing.Manager()
        results = manager.list()
        self.dfs(initial_sequence, results)
        return list(results)

    def generate_sequences(self):
        num_cores = multiprocessing.cpu_count()
        initial_sequences = [[i] for i in range(self.start, min(self.end + 1, self.start + num_cores))]
        
        with multiprocessing.Pool(processes=num_cores) as pool:
            partial_results = pool.map(self.parallel_dfs, initial_sequences)
        
        return [seq for sublist in partial_results for seq in sublist]
'''

class RuleBasedSequenceDFS2:
    def __init__(self, acting_entity):
        self.acting_entity = acting_entity
        self.min_length = 1
        self.max_length = len(acting_entity.subaction_catalog['free_subaction_groups']) + acting_entity.speed + 1 + 1
        self.start = 0
        self.end = len(acting_entity.subactions)
        self.rules = acting_entity.dfs_rules['action_rules']['permit']
        self.sequences = []

    def check_rules(self, sequence, next_num, acting_entity):
        # Apply all rules to the current sequence and next number
        return all(rule(sequence, next_num, acting_entity) for rule in self.rules)

    def dfs(self, current_sequence):
        # Check if the current sequence is within the desired length range
        if self.min_length <= len(current_sequence) <= self.max_length:
            self.sequences.append(current_sequence.copy())
            #print(current_sequence)
        
        # Continue exploring if we haven't reached the maximum length
        if len(current_sequence) < self.max_length:
            for next_num in range(self.start, self.end + 1):
                if self.check_rules(current_sequence, next_num, self.acting_entity):
                    current_sequence.append(next_num)
                    self.dfs(current_sequence)
                    current_sequence.pop()  # Backtrack


    def generate_sequences(self):
        #print(self.rules)
        self.dfs([])
        return self.sequences
    

# now to redefine the action rules...
def rule_only_one_action2(sequence, next_num, acting_entity):
    if next_num in acting_entity.subaction_catalog['action_subactions_reps'] and sum(1 for seq in sequence if seq in acting_entity.subaction_catalog['action_subactions_reps']) == 1:
        return False
    return True

def rule_only_one_bonus_action2(sequence, next_num, acting_entity):
    if next_num in acting_entity.subaction_catalog['bonus_subactions_reps'] and sum(1 for seq in sequence if seq in acting_entity.subaction_catalog['bonus_subactions_reps']) == 1:
        return False
    return True

def rule_no_redundant_moves2(sequence, next_num, acting_entity):
    # this is to prevent sequential subactions that have an equivalent representative
    # for example, move one space, then move one space again
    # or move one space, then move two spaces

    if len(sequence) > 0:
        if next_num == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move one space']) and sequence[-1] == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move one space']):
            return False
        if next_num == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move two spaces']) and sequence[-1] == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move one space']):
            return False
        if next_num == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move one space']) and sequence[-1] == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move two spaces']):
            return False
        if next_num == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move two spaces']) and sequence[-1] == acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['move two spaces']):
            return False
    return True


def rule_limited_move_speed2(sequence, next_num, acting_entity):
    move_speed = acting_entity.speed
    move_points = acting_entity.subaction_catalog['move_points']
    speed_spent = 0

    if 'prone' not in acting_entity.conditions:
        prone = 1
    else:
        prone = 2

    move_series = [x for x in sequence if x in acting_entity.subaction_catalog['move_subactions_reps']]

    prone_rep = acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['go prone'])
    stand_rep = acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['stand up'])


    for i in move_series:
        if i == prone_rep and prone == 1:
            prone = 2
        
        if i == stand_rep and prone == 2:
            prone = 1

        speed_spent += move_points[i] * prone

    if next_num in acting_entity.subaction_catalog['move_subactions_reps']:
        if move_points[next_num] + (speed_spent * prone) > move_speed:
            return False
        
    return True

def rule_one_of_each_free_action2(sequence, next_num, acting_entity):
    # free_subactions = [[4,25,27,29,31],[14]] # can do one of each list
    pass

def rule_shield_actions_need_shields2(sequence, next_num, acting_entity):
    pass

def rule_concentration2(sequence, next_num, acting_entity):
    # by using 
    end_concentration_index = acting_entity.subaction_catalog['free_subactions_text'].index('end_concentration')
    end_concentration_rep = acting_entity.subaction_catalog['free_subactions_reps'][end_concentration_index]

    casting_index = acting_entity.subaction_catalog['action_subactions_text'].index('cast')
    casting_rep = acting_entity.subaction_catalog['action_subactions_reps'][casting_index]


    # acting_entity.subaction_catalog['free_subaction_groups']

    if acting_entity.concentration == False and casting_rep not in sequence:
        if next_num == end_concentration_rep:
            return False
    return True


def rule_actions_requiring_allies2(sequence, next_num, acting_entity):
    if next_num in acting_entity.subaction_catalog['subactions_req_allies']:
        if acting_entity.allies == []:
            return False
    return True

def rule_off_hand_two_weapons_requirement2(sequence, next_num, acting_entity):
    pass

def rule_condition_rules2(sequence, next_num, acting_entity):
    # escape grappled
    escape_grapple_index = acting_entity.subaction_catalog['action_subactions_text'].index('escape_grapple')
    escape_grapple_rep = acting_entity.subaction_catalog['action_subactions_reps'][escape_grapple_index]

    # if you're not grappled, you can't escape the grapple
    if next_num == escape_grapple_rep and 'grappled' not in acting_entity.conditions:
        return False

    # perhaps this type of rule should be handled during a more advanced stage
    # because a pseudo-history may need to be generated...
    # however, if you start the round grappled, and escape the grapple, 
    # you theoretically shouldn't become grappled again in the same round,
    # at least more times than not

    # go prone
    go_prone_index = acting_entity.subaction_catalog['move_subactions_text'].index('go prone')
    go_prone_rep = acting_entity.subaction_catalog['move_subactions_reps'][go_prone_index]

    move_series = [x for x in sequence if x in acting_entity.subaction_catalog['move_subactions_reps']]

    prone_rep = acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['go prone'])
    stand_rep = acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['stand up'])

    # if you're prone, you can't go prone again
    for i in move_series:
        if i == prone_rep and prone == 1:
            prone = 2
        
        if i == stand_rep and prone == 2:
            prone = 1

    if next_num == go_prone_rep and prone == 2:
        return False

    
    # stand up
    # if you're grappled, you can't stand up
    # and if you're not prone, you can't stand up
    stand_up_index = acting_entity.subaction_catalog['move_subactions_text'].index('stand up')
    stand_up_rep = acting_entity.subaction_catalog['move_subactions_reps'][stand_up_index]

    if next_num == stand_up_rep and 'grappled' in acting_entity.conditions:
        return False
    
    if next_num == stand_up_rep and prone == 1:
        return False

    return True



def rule_remove_redundant_prones2(sequence, next_num, acting_entity):
    prone_index = acting_entity.subaction_catalog['move_subactions_text'].index('go prone')
    prone_rep = acting_entity.subaction_catalog['move_subactions_reps'][prone_index]
    
    if len(sequence)>0:
        if next_num == prone_rep and sequence[-1] == prone_rep:
            return False
        if prone_rep in sequence:
            # if between the last time 19 was called, there isn't a 20, false
            last_prone_index = len(sequence) - 1 - sequence[::-1].index(prone_rep)
            stand_index = acting_entity.subaction_catalog['move_subactions_reps'].index(acting_entity.subaction_catalog['move_subactions_text']['stand up'])
            if stand_index not in sequence[last_prone_index:] and next_num == prone_rep:
                return False
    return True

def rule_remove_redundant_objects2(sequence, next_num, acting_entity):
    pass

def rule_mount_once_per_turn2(sequence, next_num, acting_entity):
    mount_index = acting_entity.subaction_catalog['free_subactions_text'].index('mount')
    mount_rep = acting_entity.subaction_catalog['free_subactions_reps'][mount_index]

    if mount_rep in sequence and mount_rep == next_num:
        return False
    
    return True

def rule_no_spells_known(sequence, next_num, acting_entity):
    # if there are no spells known, then the cast spell subactions are invalid
    cast_index = acting_entity.subaction_catalog['action_subactions_text'].index('cast')
    cast_rep = acting_entity.subaction_catalog['action_subactions_reps'][cast_index]

    if cast_rep == next_num and acting_entity.spells_known == []:
        return False
    return True

action_rules_permit2 = [
    rule_only_one_action2,
    rule_only_one_bonus_action2,
    rule_no_redundant_moves2,
    rule_limited_move_speed2,
    #rule_one_of_each_free_action2,
    #rule_shield_actions_need_shields2,
    rule_concentration2,
    rule_actions_requiring_allies2,
    rule_remove_redundant_prones2,
    #rule_remove_redundant_objects2,
    rule_mount_once_per_turn2,
    rule_condition_rules2,

]