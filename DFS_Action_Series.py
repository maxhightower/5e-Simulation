# Action Series Depth by First Search

import numpy as np

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, chebyshev_distance, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility
from DFS_World_States import world, world_grid_states

from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, bonus_subactions, object_action_subactions, object_free_subactions, subactions_req_allies, entity, subaction_dict


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

    return True

def rule_limited_move_speed(sequence, next_num, acting_entity):
    move_speed = acting_entity.speed
    move_points = {
                0: 1, 
                1: 2, 
                2: 3, 
                3: 4, 
                20: move_speed/2,
                23: 5,
                24: 6,
                }

    speed_spent = sum(move_points[move_type] for move_type in sequence if move_type in move_subactions)
    
    # if prone is taken, stand up hasn't been, multiply the costs of move_points by 2
    if 19 in sequence:
        # if between the last time 19 was called, there isn't a 20, false
        last_prone_index = len(sequence) - 1 - sequence[::-1].index(19)

        if 20 not in sequence[last_prone_index:]:
            if next_num in move_subactions:
                if speed_spent + (move_points[next_num]*2) > move_speed:
                    return False

    if next_num in move_subactions:
        if speed_spent + move_points[next_num] > move_speed:
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
    if next_num == 13 and 'shield' not in acting_entity.inventory or next_num == 13 and 'shield' not in acting_entity.equipped_armor:
        return False
    return True

def rule_concentration(sequence, next_num, acting_entity):
    if next_num == 14 and acting_entity.concentration == False:
        return False
    return True

def rule_actions_requiring_allies(sequence, next_num, acting_entity):
    if acting_entity.world.non_enemies == []:
        if next_num in subactions_req_allies:
            return False

    return True

def rule_off_hand_two_weapons_requirement(sequence, next_num, acting_entity):
    if next_num == 15 and len(acting_entity.weapon_equipped) < 2:
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
    if 20 in sequence and next_num == 20:
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
    if next_num == 31 and acting_entity.weapon_equipped == []:
        return False
    return True

def rule_equip_weapon(sequence, next_num, acting_entity):
    if next_num in [25,26] and acting_entity.weapon_equipped != []:
        return False
    return True

def rule_object_number_limitation(sequence, next_num, acting_entity):
    obj_act = [x for x in sequence if x in object_action_subactions]
    if next_num in object_action_subactions:
        if len(obj_act) > len(acting_entity.world.objects + acting_entity.inventory + acting_entity.weapon_equipped):
            return False
    return True


action_rules = [rule_only_one_action, 
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
         ]

