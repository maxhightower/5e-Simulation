# Object Series

import numpy as np

import DFS_Functions
import DFS_World_States
from DFS_Functions import adjacent_locations, chebyshev_distance, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility, generate_pseudo_history
from DFS_World_States import world, world_grid_states

import DFS_Action_Series

from DFS_Universal_Rules import action_subactions, move_subactions, action_subactions, attack_subactions, free_subactions, subactions_req_targets, object_subactions, target_distance_scores, subactions_req_objects


# what needs to happen in this DFS
# given an action_series and location_series, 
# where there are subactions that interact with an object, 
# we need to create a series that represents each object available to interact with


# Discussion: Does Object Series need a similar output to Location Series?
# location series required an output comprising of a list of many potential locations for one action series
# this was because with multiple types of move subactions, there could be multiple potential locations
# and then iteratively more possible locations based on previous decisions.
# The question to answer is, are there new object series that can come from previous object choices?
# Yes, there are possible sequences where an entity picks up an object then equips it, 
# so new possibilities are possible based on previous decisions within the same object_series 

# What gets stored in the object_series_list?
# Is it class instances of objects?

# How should the DFS and Potential_Objects functions work?
# the DFS function works by appending object class instances to a list based on the rules
# within the DFS function, the Potential_Objects function is called to get a list of objects that can be interacted with
# the Potential_Objects function should return a list of class instances
# the Potential_Objects function should be given 
#       - the current object sequence, 
#       - the post_reward_location_list,
#       - the acting_entity,
#       - the 

# BUT if the DFS is to iterate through a list of objects, 

# there needs to be a Worldly list of objects (aka a list of objects that exist in the world)
# which is different from the list of objects that can be interacted with in a given action series (aka potential_objects)





class RuleBasedObjectSequenceDFS:
    def __init__(self, post_location_reward_list, target_distance_scores, object_rules, acting_entity):
        self.post_location_reward_list = post_location_reward_list
        self.target_distance_scores = target_distance_scores
        self.object_rules = object_rules
        self.acting_entity = acting_entity

        self.object_series_list = []
        self.sequences = []





    def get_potential_objects(self, 
                              sequence, 
                              acting_entity, 
                              post_location_reward_list, 
                                      # filled via subaction_index aka the length of the sequence
                                                            # meaning 
                              ):
        # the goal of this function is to return a list of objects, 
        # out of the objects in the world, 
        # that can be interacted with based on the current sequence
    
        ###  ------  Setting Up Constants  ------  ###
        object_subaction_index = len(sequence)
        potential_objects = []
        worldly_objects = acting_entity.world.objects


        action_series = post_location_reward_list[0]
        location_series = post_location_reward_list[1]
        object_series = [x for x in action_series if x in subactions_req_objects]

        #print(f'object series: {object_series}')
        #print(f'object subaction index: {object_subaction_index}') 
        
        object_subaction = object_series[object_subaction_index]


        pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity,sequence, post_location_reward_list, object_subaction_index)


        #action = action_series[object_subaction_index]
        if location_series != []:
            location = location_series[-1]
            
        # Ground Pickup
        if object_subaction in [4,7]:
            for object in acting_entity.world.grid2[location[0]][location[1]][6]:
                potential_objects.append(object)
        

        #next_action = post_location_reward_list[0][object_subaction_index]

        # action_index = len(sequence) # this presumes the last in the line is what we're looking at
        #   instead we'll create object_subaction_index





        ###  ------  Adjusting for Sequence History  ------  ###

        # because the object series is generated iteratively/recursively,
        # an object may be newly usable/unusable based on the previous subaction and object choices

        # every act_loc_obj sequence will begin the same, with the constants
        # 


        ###  Situationally Adjusting Potential Objects  ###                         This seems more like rule based filtration
        # information that is known at any point in the object_series generation
        # the full action_series is always known
        # the full location_series is always known

        # for each object subaction, in order, 
        #for action_index in range(len(obj_act)):

            # if an object has been picked up, it can be used by later subactions
        #    if obj_act[action_index] in [4,7]:
        #        potential_objects.append(sequence[action_index])

            # if an object has been dropped, it can be picked up, unless 4 or 7 is 
        #    if obj_act[action_index] in [29,30]:
        #        if sequence[action_index] in acting_entity.inventory:
        #            potential_objects.remove(sequence[action_index])



        # Pulling from Inventory
        if object_subaction in [13,25,26,29,30,33,37,38]:
            for object in pseudo_inventory:
                potential_objects.append(object)

        # Pulling from Main Hand
        if object_subaction in [5,31,32,42,45]:
            for object in pseudo_main_hand:
                potential_objects.append(object)

        # Pulling from Off Hand
        if object_subaction in [15,39,40,41,43,46]:
            for object in pseudo_off_hand:
                potential_objects.append(object)

        # Pulling from Either
        if object_subaction in [44,47]:
            for object in pseudo_main_hand + pseudo_off_hand:
                potential_objects.append(object)

        return potential_objects
    
    def check_rules(self, sequence, next_object, acting_entity, post_location_reward_list):
        return all([rule(sequence, next_object, acting_entity, post_location_reward_list) for rule in self.object_rules])

    
    def dfs(self, current_sequence, next_object, acting_entity, act_loc_rew, available_objects, post_location_reward_list):


        action_series = act_loc_rew[0]
        tar_act_series = [i for i in action_series if i in subactions_req_targets]
        obj_act_series = [i for i in action_series if i in subactions_req_objects]
        required_sequence_length = len(obj_act_series)
        
        #all_sequences = []
        subaction_index = len(current_sequence)

        # the desired outcome
        if len(current_sequence) == len([x for x in act_loc_rew[0] if x in subactions_req_objects]):
            if self.check_rules(current_sequence, next_object, acting_entity, act_loc_rew):
                return current_sequence.copy()
        
        # the contingency for if less objects are available
        #if len(current_sequence) == len(available_objects) and len(available_objects) < len([x for x in act_loc_rew[0] if x in subactions_req_objects]):
        #    if self.check_rules(current_sequence, next_object, acting_entity, act_loc_rew):
        #        return current_sequence.copy()
        
        # there needs to be a minimum number of objects then for scenario generation, however through class features that may not be a problem

        potential_objects = self.get_potential_objects(current_sequence, 
                                                       acting_entity, 
                                                       act_loc_rew)
        
        #print(f'number of potential objects: {len(potential_objects)}')

        for next_object in potential_objects:
            if self.check_rules(current_sequence, next_object, self.acting_entity, act_loc_rew):
                current_sequence.append(next_object)
                self.object_series_list.append(self.dfs(current_sequence, next_object, acting_entity, act_loc_rew, potential_objects, post_location_reward_list))
                current_sequence.pop()
        
        return self.object_series_list
    
    def generate_object_sequences(self):
        post_location_reward_list = self.post_location_reward_list

        # in order to generate the object series, what is the order of operations that must be followed?
        # for post_location_reward_list 
        #   for subaction in action_series
        #    if subaction is an object subaction
        #      get potential objects
        #      for each potential object
        #        if object passes all rules
        #          add object to sequence
        #          dfs(sequence, acting_entity, post_location_reward_list)
        #          pop object from sequence
        # return object_series_list
        # lets do that

        act_loc_obj_rew = []
        
        worldly_objects = self.acting_entity.world.objects
        
        reward_series_list = [i[2] for i in post_location_reward_list]

        act_loc_rew_pass_count = 0
        quality_threshold = np.percentile(reward_series_list, 90)

        #print(f'Post Location Reward List: {post_location_reward_list}')

        for act_loc_rew in post_location_reward_list:
            action_series, location_series, reward = act_loc_rew
            #print(f'act_loc_rew: {act_loc_rew}') # ([25, 5, 0], [[1, 1], [1, 1]], 5.5)
    # need to change the qualifier to be the top 15% of rewards

            if int(act_loc_rew[2]) >= quality_threshold:
                act_loc_rew_pass_count += 1



                for subaction_index in range(len(act_loc_rew[0])):
                    

                    subaction = act_loc_rew[0][subaction_index]
                    if subaction in subactions_req_objects:
                        

                        potential_objects = self.get_potential_objects([], self.acting_entity, act_loc_rew)
                        
                        for next_object in potential_objects:
                            
                            sequences = self.dfs([], next_object, self.acting_entity, act_loc_rew, potential_objects, post_location_reward_list)

                            #print(f'sequences: {sequences}')
                            self.object_series_list.append(sequences)

            
            # how to un-nest the object_series_list
            



            #else:
                 #self.object_series_list.append([])

                result = [action_series, location_series, self.object_series_list, reward]
            #act_loc_obj_rew.append(result)
            
                if result not in act_loc_obj_rew:
                    act_loc_obj_rew.append(result)
                self.object_series_list = []

        print(f'act_loc_obj_rew pass count: {act_loc_rew_pass_count}')
        return act_loc_obj_rew

        #return self.object_series_list


# this one handles location series
class RuleBasedLocationSequenceDFS3:
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
            if chebyshev_distance(entity_location, loc) <= distance_allowable:
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
        
        print(f'objects needed: {required_sequence_length}')

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
                all_sequences.append(self.dfs(action_series, current_sequence, grid_locations))
                current_sequence.pop()
        
        #print(f'sequences being returned from dfs to results 1 {all_sequences[:20]}')
        return all_sequences

    def generate_sequences(self):
        grid_locations = [
            [x - 5, y - 5]
            for x in range(len(self.acting_entity.world.grid))
            for y in range(len(self.acting_entity.world.grid[x]))
        ]

        for action_series_index, action_series in enumerate(self.action_series_list):
                # need to change the qualifier to be the top 15% of rewards

            quality_threshold = np.percentile(self.reward_series_list, 85)

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




# rules: you can't interact equip an object if you're already equipped with an object
# you can't pick up an object already picked up

# how should the order of operations work?
# should it take two object actions to take an item off the ground, hold it, and then put it in inventory?
# or should it go straight to inventory if object action is taken and equipping something is what takes...

def rule_equip_status(sequence, next_object, acting_entity, i):
    # need to go through the sequence and see where each object ends up in the sequence
    action_series = i[0]
    location_series = i[1]
    
    obj_act = [x for x in action_series if x in subactions_req_objects]
    # obj_loc needs to be the relevant locations of the actions in obj_act
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    equip_sequence = []

    return True

# rule about handing things to creatures only requiring the DELIVERER to use a subaction, not the recipient

# You can only equip weapons not other object types
def rule_only_equip_weapons(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    #print(f'sequence: {sequence}')
    #print(f'action series: {action_series}')
    action = action_series[len(sequence)]

    if action == 25 or action == 26:
        if next_object.type != 'weapon':
            return False
    
    return True

def rule_attack_with_weapons(sequence, next_object, acting_entity, i):
    print(f'i: {i}')
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    print(f'sequence: {sequence}')
    print(f'action_series: {action_series}')
    
    number = len(sequence)
    action = action_series[number]

    if action == 5:
        if next_object.type != 'weapon':
            return False
    
    return True


# if by the time you take the cast action, you are wearing armor that you aren't proficient in, you cannot cast
    # A shield counts as armor, and is an object
    # however, because of the wording of page 201, it seems implied that the caster simply couldn't start to cast, 
    # i.e. they can't choose the cast action, rather than the spell failing
    # so should this rule be in the object series or the action series?
        # it has to be in the object series, because the state of wearing can change, however this may need to be revisited later

    # the way to do this currently: if the entity is taking the cast action, armor that the entity is not proficient in cannot be equipped beforehand

def rule_spellcasting_with_shield(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    number = len(sequence)
    action = action_series[number]

    pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity, sequence, i, len(sequence))


    if acting_entity.shield_proficient == False:
        # don or doff shield is action 13
        # if the cast action (action 11) is taken
        if 11 in action_series:
            # a shield cannot be equipped before the cast action
            # you can be holding a shield and not donning it

            # if shield is in acting_entity.equipped_armor and 13 is not before 11, return False
            if 'shield' in pseudo_off_hand:
                if 13 not in [action_series[i] for i in range(len(action_series)) if i < action_series.index(11)]:
                    return False
            
            # shield is not in acting_entity.equipped_armor and 13 is before 11, return False
            if 'shield' not in pseudo_off_hand:
                if 13 in [action_series[i] for i in range(len(action_series)) if i < action_series.index(11)]:
                    return False
                
    if acting_entity.shield_proficient == False:
        # and 11 is before where 13 is in the action_series
        if action == 13 and 11 in [action_series[i] for i in range(len(action_series)) if i < number]:
            if next_object.type == 'shield':
                return False
            
    return True


# how should what the entity is holding be represented?
# - equipped_weapon?
# - hands?

# what is impacted by what the entity is holding?
# - armor class, via if the entity is holding a shield
# - damage, via the difference between a one-handed, two-handed, or versatile weapon
# - damage, via main-hand vs off-hand and the two-weapon fighting style
# - spellcasting, via somatic and material components
        # "if a spell requires a somatic component, the caster must have free use of at least one hand to perform these gestures"
        # "A spellcaster must have a hand free to access a spell's material components—or to hold a spellcasting focus—
        #   but it can be the same hand that he or she uses to perform somatic components."

# the logical solution for this is to represent this by having each hand be a separate property that can store an object
# this way, the entity can have a shield in one hand and a weapon in the other, or one weapon in both
    # if equipping an item would...
        # should there be unique subactions for adding or removing items per hand???
        # should there be a hand series??? because some creatures have more than two hands...

# what if picking something up defaults to main hand, uses off hand if main hand is full, and then...
# should it be restricted if hands are full???

# can only have one item in each hand at a time
def rule_limit_hand_capacity(sequence, next_object, acting_entity, i):

    main_hand_status = acting_entity.main_hand
    off_hand_status = acting_entity.off_hand

    # determine using sequence what the current main_hand_status and off_hand_status would be



    if len(acting_entity.main_hand) > 1:
        return False
    
    if len(acting_entity.off_hand) > 1:
        return False

    return True


# will eventually need a rule about attacking with a two-handed weapon when it only exists in one of your hands
def rule_one_handed_attack_with_two_handed_weapon(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]

    if action in attack_subactions:
        if next_object.type == 'weapon':
            if all([next_object.hands == 1, acting_entity.main_hand == [next_object], acting_entity.off_hand == [next_object]]):
                return False

    return True

def rule_only_drink_potions(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]

    if action == 33:
        if next_object.type != 'potion':
            return False
    return True

def rule_only_don_doff_shields(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]

    if action in [13,39]:
        if next_object.type != 'shield':
            return False
    return True

# can't drop off hand when shield is equipped, because the 13 subaction is required
def rule_cannot_drop_offhand_while_donning_shield(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]

    pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity, sequence, i, len(sequence))

    # [40,41,43,46]
    if action in [40,41,43,46] and pseudo_off_hand[0].type == 'shield':
        return False
    
    return True
        

def rule_cannot_both_hand_equip_one_handed_weapon(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]

    pseudo_inventory, pseudo_main_hand, pseudo_off_hand, pseudo_armor_equipped, pseudo_world = generate_pseudo_history(acting_entity, sequence, i, len(sequence))

    # [49,50]
    if action in [49,50]:
        if next_object.type == 'weapon' and next_object.hands in [0,1]:
            return False
    
    return True


# need a rule that states you can't equip the same object to both off hand and main hand seperately

# need a rule that states shields don't go to main hand, only off hand


# need a rule removing redundant object actions
def rule_no_redundant_equipping_unequipping_dropping(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]
    previous_action = action_series[len(sequence)-2]

    # equipping
    # if an object is equipped to main hand, and the current action is equipping to off hand
    if any([25 in action_series, 26 in action_series]) and action in [37,38]:
        # unless any unequip or drop actions happen in between the two
        if 25 in action_series and 37 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(25) and i < action_series.index(37)]
        
        if 25 in action_series and 38 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(25) and i < action_series.index(38)]

        if 26 in action_series and 37 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(26) and i < action_series.index(37)]
        
        if 26 in action_series and 38 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(26) and i < action_series.index(38)]
        
        if any([31,32,40,41,42,43]) in in_between_sequence:
            return True
        
        else:
            # if the object is the same between the two actions, return False
            if acting_entity.main_hand[0] == acting_entity.off_hand[0]:
                return False
    

    # unequipping
    if any([31 in action_series, 32 in action_series]) and action in [40,41]:
        # unless any unequip or drop actions happen in between the two
        if 31 in action_series and 40 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(25) and i < action_series.index(37)]
        
        if 32 in action_series and 40 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(25) and i < action_series.index(38)]

        if 31 in action_series and 41 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(26) and i < action_series.index(37)]
        
        if 32 in action_series and 41 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(26) and i < action_series.index(38)]
        
        if any([25,26,37,38,42,43]) in in_between_sequence:
            return True
        
        else:
            # if the object is the same between the two actions, return False
            if acting_entity.main_hand[0] == acting_entity.off_hand[0]:
                return False
    


    # dropping
    if any([37 in action_series, 38 in action_series]) and action in [49,50]:
        # unless any unequip or drop actions happen in between the two
        if 37 in action_series and 49 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(25) and i < action_series.index(37)]
        
        if 37 in action_series and 50 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(25) and i < action_series.index(38)]

        if 38 in action_series and 49 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(26) and i < action_series.index(37)]
        
        if 38 in action_series and 50 in action_series:
            in_between_sequence = [action_series[i] for i in range(len(action_series)) if i > action_series.index(26) and i < action_series.index(38)]
        
        if any([25,26,31,32,40,41]) in in_between_sequence:
            return True
        
        else:
            # if the object is the same between the two actions, return False
            if acting_entity.main_hand[0] == acting_entity.off_hand[0]:
                return False

    return True


def rule_one_free_hand_to_grapple(sequence, next_object, acting_entity, i):
    action_series = i[0]
    location_series = i[1]

    obj_act = [x for x in action_series if x in subactions_req_objects]
    obj_loc = [location_series[i] for i in range(len(location_series)) if action_series[i] in obj_act]

    action = action_series[len(sequence)-1]






object_rules = [
    rule_equip_status,
    #rule_only_equip_weapons,
    rule_attack_with_weapons,
    rule_spellcasting_with_shield,
    rule_limit_hand_capacity,
    rule_one_handed_attack_with_two_handed_weapon,
    rule_only_drink_potions,
    rule_only_don_doff_shields,
    rule_cannot_drop_offhand_while_donning_shield,
    rule_cannot_both_hand_equip_one_handed_weapon,
    rule_no_redundant_equipping_unequipping_dropping,




]