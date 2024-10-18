# DFS_Reward_Calculators
import numpy as np
import collections
from DFS_Universal_Rules import action_subactions, move_subactions, attack_subactions, free_subactions, subactions_req_objects, effect_subactions, effect_dictionary

from DFS_Entities import entity
from DFS_Functions import adjacent_locations, adjacent_locations_entities, chebyshev_distance, chebyshev_distance_entities, bresenham_line, calculate_full_path, calculate_full_path_entities, check_opportunity_attacks, is_line_of_sight_clear, check_visibility, move_speed_to_subactions, generate_pseudo_history, damage_calc1, damage_calc2, probability_hit_calc, expected_damage, calc_series_expected_damage



def check_rules_for_reward(any_one_series,ruleset,acting_entity):
    print(any_one_series)

    if len(any_one_series) in [0,1]:
        reward = 0
    else:
        reward = any_one_series[-1]

    for rule in ruleset:
        reward += rule(any_one_series, acting_entity)
    
    return reward


def calc_new_reward(any_series, acting_entity):
    # the input should be the combined series, not separate lists
    results = []
        


    # this function calculates the new reward values for the entire list of series
    if len(any_series[0]) == 1 or len(any_series[0]) == 0: # only one item means action
        ruleset = action_rules_reward

        for any_one_series in any_series:
            if any_one_series == []:
                new_reward = check_rules_for_reward(any_one_series, ruleset, acting_entity)
                same_series_new_reward = [any_one_series,new_reward]
                results.append(same_series_new_reward)
            else:
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

def rule_number_of_actions(any_one_series, acting_entity):
    if len(any_one_series) in [0,1]:
        for i in any_one_series:
            if i in acting_entity.subaction_catalog['action_subactions_reps']:
                return 1
    else:

    # need to access the action_subactions_text, action_subactions_reps from acting_entity.subaction_catalog
        for i in any_one_series[0]:
            if i in acting_entity.subaction_catalog['action_subactions_reps']:
                return 1
    return 0

def rule_number_of_free_actions(any_one_series, acting_entity):
    if len(any_one_series) in [0,1]:
        for i in any_one_series:
            if i in acting_entity.subaction_catalog['free_subactions_reps']:
                return 1
    else:


        # there are multiple lists within the free_subactions_reps list and only one per list can be taken
        # so its the number of lists that free actions are taken from
        free_subaction_lists = acting_entity.subaction_catalog['free_subactions_reps']
        # free_subaction_lists looks like [[4,25,27,29,31],[14]]
        for i in any_one_series[0]:
            for j in free_subaction_lists:
                if i in j:
                    return 1
    return 0
    


def rule_number_of_attacks(any_one_series, acting_entity):
    if len(any_one_series) in [0,1]:
        for i in any_one_series:
            if i in acting_entity.subaction_catalog['attack_subactions_reps']:
                return 1
    else:
        for i in any_one_series[0]:
            if i in acting_entity.subaction_catalog['attack_subactions_reps']:
                return 1
    
    return 0

def rule_prone(any_one_series, acting_entity):

    # need to find the index of 'prone' string from subaction_catalog['action_subactions_text']
    prone_index = acting_entity.subaction_catalog['move_subactions_text'].index('go prone')
    prone_value = acting_entity.subaction_catalog['move_subactions_reps'][prone_index]

    if len(any_one_series) in [0,1]:
        if prone_value in any_one_series:
            return -1
    else:
        if prone_value in any_one_series[0]:
            return -1

    return 0

def rule_prone_end(any_one_series, acting_entity):
    prone_index = acting_entity.subaction_catalog['move_subactions_text'].index('go prone')
    prone_value = acting_entity.subaction_catalog['move_subactions_reps'][prone_index]

    stand_index = acting_entity.subaction_catalog['move_subactions_text'].index('stand up')
    stand_value = acting_entity.subaction_catalog['move_subactions_reps'][stand_index]

    if len(any_one_series) in [0,1]:
        if prone_value in any_one_series:
            if stand_value not in any_one_series[any_one_series.index(prone_value):]:
                return -1
    else:

        if prone_value in any_one_series[0]:
            if stand_value not in any_one_series[any_one_series[0].index(prone_value):]:
                return -1
            
    return 0

def rule_action_series_length(any_one_series, acting_entity):
    if len(any_one_series) in [0,1]:
        act_series_len = len(any_one_series)
    else:
        act_series_len = len(any_one_series[0])
    
    if act_series_len >= 3:
        return 1
    if act_series_len <= 7:
        return 1
    if act_series_len > 10:
        return -1
    return 0

def rule_equip_hand_followed_by_attack_with_hand(any_one_series, acting_entity):
    equip_main_hand_free_index_in_text = acting_entity.subaction_catalog['object_subactions_text'].index('object--free--self_equip_main_hand')
    equip_main_hand_free_index_rep = acting_entity.subaction_catalog['object_subactions_reps'][equip_main_hand_free_index_in_text]
    
    equip_main_hand_action_index_in_text = acting_entity.subaction_catalog['object_subactions_text'].index('object--action--self_equip_main_hand')
    equip_main_hand_action_index_rep = acting_entity.subaction_catalog['object_subactions_reps'][equip_main_hand_action_index_in_text]

    equip_off_hand_free_index_in_text = acting_entity.subaction_catalog['object_subactions_text'].index('object--free--self_equip_off_hand')
    equip_off_hand_free_index_rep = acting_entity.subaction_catalog['object_subactions_reps'][equip_off_hand_free_index_in_text]

    equip_off_hand_action_index_in_text = acting_entity.subaction_catalog['object_subactions_text'].index('object--action--self_equip_off_hand')
    equip_off_hand_action_index_rep = acting_entity.subaction_catalog['object_subactions_reps'][equip_off_hand_action_index_in_text]

    equip_both_hand_free_index_in_text = acting_entity.subaction_catalog['object_subactions_text'].index('object--free--self_equip_both_hands')
    equip_both_hand_free_index_rep = acting_entity.subaction_catalog['object_subactions_reps'][equip_both_hand_free_index_in_text]

    equip_both_hand_action_index_in_text = acting_entity.subaction_catalog['object_subactions_text'].index('object--action--self_equip_both_hands')
    equip_both_hand_action_index_rep = acting_entity.subaction_catalog['object_subactions_reps'][equip_both_hand_action_index_in_text]

    attack_main_hand_index_in_text = acting_entity.subaction_catalog['attack_subactions_text'].index('attack--weapon--main_hand')
    attack_main_hand_index_rep = acting_entity.subaction_catalog['attack_subactions_reps'][attack_main_hand_index_in_text]

    attack_off_hand_index_in_text = acting_entity.subaction_catalog['attack_subactions_text'].index('attack--weapon--off_hand')
    attack_off_hand_index_rep = acting_entity.subaction_catalog['attack_subactions_reps'][attack_off_hand_index_in_text]

    attack_both_hands_index_in_text = acting_entity.subaction_catalog['attack_subactions_text'].index('attack--weapon--both_hands')
    attack_both_hands_index_rep = acting_entity.subaction_catalog['attack_subactions_reps'][attack_both_hands_index_in_text]
    
    if len(any_one_series) in [0,1]:
        if equip_main_hand_free_index_rep in any_one_series:
            if attack_main_hand_index_in_text in any_one_series[any_one_series.index(equip_main_hand_free_index_rep):]:
                return 1
        if equip_main_hand_action_index_rep in any_one_series:
            if attack_main_hand_index_in_text in any_one_series[any_one_series.index(equip_main_hand_action_index_rep):]:
                return 1
            
        if equip_off_hand_free_index_rep in any_one_series:
            if attack_off_hand_index_in_text in any_one_series[any_one_series.index(equip_off_hand_free_index_rep):]:
                return 1
        if equip_off_hand_action_index_rep in any_one_series:
            if attack_off_hand_index_in_text in any_one_series[any_one_series.index(equip_off_hand_action_index_rep):]:
                return 1
            
        if equip_both_hand_free_index_rep in any_one_series:
            if attack_both_hands_index_in_text in any_one_series[any_one_series.index(equip_both_hand_free_index_rep):]:
                return 1
        if equip_both_hand_action_index_rep in any_one_series:
            if attack_both_hands_index_in_text in any_one_series[any_one_series.index(equip_both_hand_action_index_rep):]:
                return 1
            
    else:
        if equip_main_hand_free_index_rep in any_one_series[0]:
            if attack_main_hand_index_in_text in any_one_series[0][any_one_series[0].index(equip_main_hand_free_index_rep):]:
                return 1
        if equip_main_hand_action_index_rep in any_one_series[0]:
            if attack_main_hand_index_in_text in any_one_series[0][any_one_series[0].index(equip_main_hand_action_index_rep):]:
                return 1
            
        if equip_off_hand_free_index_rep in any_one_series[0]:
            if attack_off_hand_index_in_text in any_one_series[0][any_one_series[0].index(equip_off_hand_free_index_rep):]:
                return 1
        if equip_off_hand_action_index_rep in any_one_series[0]:
            if attack_off_hand_index_in_text in any_one_series[0][any_one_series[0].index(equip_off_hand_action_index_rep):]:
                return 1
            
        if equip_both_hand_free_index_rep in any_one_series[0]:
            if attack_both_hands_index_in_text in any_one_series[0][any_one_series[0].index(equip_both_hand_free_index_rep):]:
                return 1
        if equip_both_hand_action_index_rep in any_one_series[0]:
            if attack_both_hands_index_in_text in any_one_series[0][any_one_series[0].index(equip_both_hand_action_index_rep):]:
                return 1

    return 0


action_rules_reward = [
    # for the number of actions taken, reward
    rule_number_of_actions,
    # for the number of free actions taken, reward
    rule_number_of_free_actions,
    # for the number of attacks made, reward
    rule_number_of_attacks,
    # if the entity goes prone at all, punish
    rule_prone,
    # if the entity ends the turn while prone, punish
    rule_prone_end,
    # if the action series is between 3 and 6, reward else punish
    # if the action series is between 7 and 10, reward else punish
    # if the action series is greater than 10, punish
    rule_action_series_length,
    # if 25 (object free self equip main haind) or 26 (object action self equip main hand) is in action_series, and 5 (attack weapon main hand) comes after it, reward (if the equip subaction is followed by the attack subaction, reward)
    rule_equip_hand_followed_by_attack_with_hand,

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

                move_path = calculate_full_path_entities(acting_entity.location, move_act_loc)
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


            move_path = calculate_full_path_entities(acting_entity, [move_act_series,move_loc_series])
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

