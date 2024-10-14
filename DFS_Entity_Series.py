# DFS_Entity_Series.py

import numpy as np

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, chebyshev_distance, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility
from DFS_World_States import world, world_grid_states


from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, subactions_req_targets, object_subactions, target_distance_scores, subactions_req_objects, subactions_req_entity

from DFS_Entities import entity

# basically go through the action_location_object series, and if the action requries an entity, 
# and there are multiple entities in the location associated,
# then create a branch for each entity that can be targeted by the action

class RuleBasedEntitySequenceDFS:
    def __init__(self, action_location_object_reward_series_full_list, target_distance_scores, entity_rules, acting_entity):
        self.action_location_object_reward_series_full_list = action_location_object_reward_series_full_list
        self.target_distance_scores = target_distance_scores
        self.entity_rules = entity_rules
        self.acting_entity = acting_entity
        
        self.entity_series_list = []
    
    def get_potential_entities(self, sequence, acting_entity, act_loc_obj_rew):
        potential_entities = []

        
        action_series = act_loc_obj_rew[0]
        location_series = act_loc_obj_rew[1]
        object_series = act_loc_obj_rew[2]
        reward = act_loc_obj_rew[3]


        entity_subaction_index = len(sequence)
        
        # ent_act_series is a list of actions that require an entity to be targeted
        ent_act_series = [i for i in action_series if i in subactions_req_entity]


        # ent_loc_series is the list of locations those actions are already targeting
        ent_loc_series = [location_series[i] for i in range(len(location_series)) if action_series[i] in subactions_req_entity]

        # the entities that are targetable, 
        # need to identify the location being targeted by the action

        # the number of entities in the sequence 
        # represents the item in ent_act_series that is being enacted
        # and the item in ent_loc_series that is being targeted

        if ent_loc_series != []:

            try:

                targeted_location = ent_loc_series[-1]
                # now to find the entities that are in the targeted location
                for entity in acting_entity.world.enemies:
                    if entity.location == targeted_location:
                        potential_entities.append(entity)

            except:
                targeted_location = ent_loc_series[0]




            potential_entities = list(set(potential_entities))

        return potential_entities

    def check_entity_rules(self, sequence, next_entity, acting_entity, act_loc_obj_rew):
        return all([entity_rule(sequence, next_entity, acting_entity, act_loc_obj_rew) for entity_rule in self.entity_rules])
    
    def dfs(self, current_sequence, next_entity, acting_entity, act_loc_obj_rew):

        action_series = act_loc_obj_rew[0]
        location = act_loc_obj_rew[1]
        object = act_loc_obj_rew[2]
        reward = act_loc_obj_rew[3]



        if len(current_sequence) == len(self.action_location_object_reward_series_full_list):
            return [current_sequence]
        
        potential_entities = self.get_potential_entities(current_sequence, acting_entity, act_loc_obj_rew)

        if len(potential_entities) == 0:
            return [current_sequence]
        
        for next_entity in potential_entities:
            if self.check_entity_rules(current_sequence, next_entity, acting_entity, act_loc_obj_rew):
                current_sequence.append(next_entity)
                self.entity_series_list.append(self.dfs(current_sequence, next_entity, acting_entity, act_loc_obj_rew, potential_entities, action_location_object_reward_series_full_list))
                current_sequence.pop()
        
        return self.entity_series_list
        
    def generate_entity_sequences(self):
        act_loc_obj_ent_rew_series_full_list = []


        action_location_object_reward_series_full_list = self.action_location_object_reward_series_full_list
        act_loc_obj_ent_rew = []
        reward_series_list = [i[3] for i in action_location_object_reward_series_full_list]

        quality_threshold = np.percentile(reward_series_list, 99)

        for act_loc_obj_rew in action_location_object_reward_series_full_list:
            action_series, location_series, object_series, reward_series = act_loc_obj_rew

            if reward_series >= quality_threshold and len([x for x in action_series if x in subactions_req_entity]) > 0:
                potential_entities = self.get_potential_entities([], self.acting_entity, act_loc_obj_rew)

                for next_entity in potential_entities:
                    sequences = self.dfs([], next_entity, self.acting_entity, act_loc_obj_rew, potential_entities)

                    if sequences not in self.entity_series_list:
                        self.entity_series_list.append(sequences)
            
            ent_act = [i for i in action_series if i in subactions_req_entity]
            entity_series_set = [tuple(i) for i in self.entity_series_list]

            for i in entity_series_set:
                if len(i) == len(ent_act):
                    results = [action_series, location_series, object_series, i, reward_series]

                    if results not in act_loc_obj_ent_rew_series_full_list:
                        act_loc_obj_ent_rew_series_full_list.append(results)
            
            self.entity_series_list = []
        
        return results


def rule_mount_target_must_be_willing(sequence, next_entity, acting_entity, act_loc_obj_rew):
    if next_entity in acting_entity.world.enemies:
        return False

    return True

# Help (Attack)
# Help (Skill Check)
# Stabilize Creature
# Wake Creature



entity_rules = [
    rule_mount_target_must_be_willing,

]