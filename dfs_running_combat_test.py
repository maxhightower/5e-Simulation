# DFS_Running_Combat Test Version
from DFS_World_States import world, world_grid_states, Weapon
from DFS_Universal_Rules import entity, theoretical_turn_length, subaction_dict, target_distance_scores
from DFS_Action_Series import RuleBasedSequenceDFS, action_rules 
from DFS_Location_Series import RuleBasedLocationSequenceDFS2, location_rules
from DFS_Functions import precalc_reward_series, analyze_reward_distribution, post_loc_series_reward_calc, post_obj_reward_series_calc, post_obj_reward_series_calc2
from DFS_Object_Series import RuleBasedObjectSequenceDFS1, object_rules




stage = world(11)
stage.generate_map()
actor = entity(stage)
stage.add_enemy((1,1))
stage.add_enemy((-2,0))
stage.add_enemy((0,3))
#stage.add_enemy((2,2))
#stage.add_enemy((-3,-3))
#stage.add_enemy((1,-1))
stage.add_coin((3,0))
stage.add_coin((-1,-1))
stage.add_coin((1,1))

stage.add_item_to_inventory(actor, Weapon('dagger', 'weapon', 1, 1, 0))

stage.add_weapon_dagger((-2,-1))
stage.add_weapon_dagger((-1,-2))
stage.add_weapon_greataxe((2,0))


action_sequence_generator = RuleBasedSequenceDFS(min_length=0,max_length=theoretical_turn_length, start=0, end=len(subaction_dict), rules=action_rules, acting_entity=actor)
action_series_full_list = action_sequence_generator.generate_sequences()
print(action_series_full_list)


reward_series_full_list = precalc_reward_series(action_series_full_list, actor)
print(reward_series_full_list)


analyze_reward_distribution(reward_series_full_list, action_series_full_list)


location_series_generator = RuleBasedLocationSequenceDFS2(action_series_list=action_series_full_list,
                                                             reward_series_list=reward_series_full_list,
                                                             location_rules=location_rules,
                                                             acting_entity=actor,
                                                             target_distance_scores=target_distance_scores)
location_series_full_list = location_series_generator.generate_sequences()


post_location_reward_list = post_loc_series_reward_calc(action_series_full_list, location_series_full_list, reward_series_full_list, actor)
print(len(post_location_reward_list))
print(post_location_reward_list)

# Object Series
object_series_generator = RuleBasedObjectSequenceDFS1(post_location_reward_list = post_location_reward_list, 
                                                     target_distance_scores = target_distance_scores,
                                                     object_rules = object_rules, 
                                                     acting_entity = actor)
object_series_full_list = object_series_generator.generate_object_sequences()
print(len(object_series_full_list))
print(object_series_full_list)