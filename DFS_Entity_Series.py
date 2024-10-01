# DFS_Entity_Series.py

import numpy as np

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, chebyshev_distance, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility
from DFS_World_States import world, world_grid_states

import DFS_Action_Series

from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, subactions_req_targets, object_subactions, target_distance_scores, subactions_req_objects


# basically go through the action_location_object series, and if the action requries an entity, 
# and there are multiple entities in the location associated,
# then create a branch for each entity that can be targeted by the action
