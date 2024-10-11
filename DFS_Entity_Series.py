# DFS_Entity_Series.py

import numpy as np

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, chebyshev_distance, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility
from DFS_World_States import world, world_grid_states

import DFS_Action_Series

from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, subactions_req_targets, object_subactions, target_distance_scores, subactions_req_objects, subactions_req_entity


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
            worldly_entities = acting_entity.world.entities

            entity_subaction_index = len(sequence)
            
            action_series = act_loc_obj_rew[0]
            location_series = act_loc_obj_rew[1]
            object_series = act_loc_obj_rew[2]
            reward = act_loc_obj_rew[3]

            ent_act_series = [i for i in action_series if i in subactions_req_entity]

            try:
                entity_subaction = ent_act_series[entity_subaction_index]
            except:
                print(f'entity_subaction_index: {entity_subaction_index}')
                print(f'ent_act_series: {ent_act_series}')
                print(f'sequence: {sequence}')
                print(f'acting_entity: {acting_entity}')
                print(f'act_loc_obj_rew: {act_loc_obj_rew}')

                entity_subaction = ent_act_series[entity_subaction_index]

            if location_series != []:
                location = location_series[entity_subaction_index]


            subaction_reach = target_distance_scores[entity_subaction]
            
            # I want to find each entity within the space that is being targeted
            for entity_location in acting_entity.world.enemy_locations:
                pass


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
            
        def generate_entity_sequences(self):
            action_location_object_reward_series_full_list = self.action_location_object_reward_series_full_list
            act_loc_obj_ent_rew = []
            reward_series_list = [i[3] for i in action_location_object_reward_series_full_list]

            quality_threshold = np.percentile(reward_series_list, 99)

            for act_loc_obj_rew in action_location_object_reward_series_full_list:
                action_series, location_series, object_series, reward_series = act_loc_obj_rew

                if reward_series >= quality_threshold and len([x for x in action_series if x in subactions_req_entity]) > 0:
                    
                    for next_entity in potential_entities:
                        sequences = self.dfs([], next_entity, self.acting_entity, act_loc_obj_rew, potential_entities)

                        if sequences not in self.entity_series_list:
                            self.entity_series_list.append(sequences)
