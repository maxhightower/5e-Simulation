# DFS_Entities
import numpy as np
from DFS_Universal_Rules import subaction_dict, size_options, size_space_orientation, target_distance_scores



subaction_dict_monster = {}
move_cost_dict_mosnter = {}
target_distance_scores_monster = {}


# need a function that breaks the move_speed a monster is capable of into a number of subactions that aren't redundant
# so 30 movement speed would be 6 subactions of 5 feet each

# what are *args and **kwargs?
# *args is used to pass a non-keyworded, variable-length argument list
# **kwargs is used to pass a keyworded, variable-length argument list

# give me an example of how to use args and kwargs
# def test_var_args(f_arg, *argv):
#     print("first normal arg:", f_arg)
#     for arg in argv:
#         print("another arg through *argv:", arg)

# test_var_args('yasoob','python','eggs','test')


class entity:
    def __init__(self,type, world, location, size, *args):
        self.type = type                # player character, monster, npc
        self.world = world
        self.location = location           # need to change this to a list so that it can handle large+ entity sizes
        
        # perhaps subactions should be stored as a list...so that appending is easier
        # and then a seperate list can be used to store the sources of each subaction...

        self.subactions = []
        self.subaction_catalog = {
            'move_subactions_text': [],        # name/text of the subaction that will be called by series_to_text function
            'move_subactions_sources': [],     # source of the subaction
            'move_subactions_reps': [],        # the current number representing the subactions in the list
            
            # should the appropriate rules be stored in the subaction_catalog as well?
            # the benefits of this would be that the rules would be entity specific
            # any outliers could be stored in the entity object itself...


            'action_subactions_text': [],
            'action_subactions_sources': [],
            'action_subactions_reps': [],

            'bonus_subactions_text': [],
            'bonus_subactions_sources': [],
            'bonus_subactions_reps': [],

            'free_subactions_text': [],
            'free_subactions_sources': [],
            'free_subactions_reps': [],

            'attack_subactions_text': [],
            'attack_subactions_sources': [],
            'attack_subactions_reps': [],

            'object_subactions_text': [],
            'object_subactions_sources': [],
            'object_subactions_reps': [],
            
            'effect_subactions_text': [],
            'effect_subactions_sources': [],
            'effect_subactions_reps': [],

            # because the above sections should define all subactions
            # the below sections don't need to store text or source and can just use the
            # reps within the lists

            'object_action_subactions': [],
            'object_free_subactions': [],
            'subactions_req_targets': [],
            'subactions_req_allies': [],
            'subactions_req_objects': [],
            'subactions_req_entity': [],
            'subactions_req_location': [],
            
            'conjoined_subactions': [],

            'sub_effects': [],
            'turn_effects': [],
            'cast_subactions': [],

            'target_distance_scores': {}, 
            'move_cost_dict': {},

        }

        self.dfs_rules = {
            'action_rules': [],
            'location_rules': [],
            'object_rules': [],
            'entity_rules': [],
            'spell_rules': [],
        }

        #self.reward_rules = {}   # just a concept for now... 

        #self.effect_dictionary = {}

        # kwargs[0] represents the template for if they are a monster
        if self.type == 'monster':
            self.template = args[0] 
                # input templates such as: ['name', 'sourcebook','year']

            self.subaction_dict = subaction_dict_monster
            self.move_cost_dict = move_cost_dict_mosnter
            self.target_distance_scores = target_distance_scores_monster

            self.orientation = args[1]
            size_layouts = size_space_orientation[size]
            if len(size_layouts) > 1:
                spaces_orientation = self.orientation
            else:
                spaces_orientation = size_layouts[0]
            
            # use string manipulation to identify the length and heigth by splitting by 'x'
            length = int(spaces_orientation.split('x')[0])
            height = int(spaces_orientation.split('x')[1])

            self.size = size
            self.space_orientation = spaces_orientation
            self.length = length
            self.height = height

            self.is_mountable = args[2]
            self.speed = args[3]

        else:
            # elif self.type == 'player character':
            self.template = None

            self.subaction_dict = subaction_dict
            self.subaction_sources = []
            self.target_distance_scores = target_distance_scores


            self.size = size
            self.space_orientation = size_space_orientation[size]
            self.length = 1
            self.height = 1

            self.is_mountable = False
            self.speed = 6

            self.move_cost_dict = {
                0: 1, 
                1: 2, 
                2: 3, 
                3: 4, 
                20: self.speed/2,
                23: 5,
                24: 6,
                54: self.speed/2,
                }

        # self.template will be used to pull the relevant information from the monster manual



        self.caster = False
        self.concentrating = False
        self.concentration = False

        self.attack_limit = 1


        self.weapon_equipped = []
        self.equipped_armor = []
        self.inventory = []

        self.ac = 10
        self.hp = 1
        self.conditions = []

        self.circumstances = {}

        self.spells = []
        self.spell_slots = [] # with the index being the spell level


        self.coins = 0

        self.shield_proficient = False # because shield is considered medium armor, the default should be false

        self.hands = 2
        self.main_hand = []
        self.off_hand = []

        self.strength_mod = 1

        # want to implement entity size
        #self.size = 'medium'
        # self.space_orientation = '1x1'
            # medium options: '1x1'
            # large options: '2x2', '1x4'
            # huge options: '3x3', '2x4', '1x9'
            # gargantuan options: '4x4', '3x6', '2x8', '1x16'
        # what will be required to implement size?
        # 1. how to represent the same entity is occupying multiple spaces in the world_grid
        # 2. world.enemy_locations
        # 3. world.enemy_locations_adjacent
        # 4. rules for spawning enemies and entities
        # 5. entities two sizes smaller than an entity can move through that entity's space unimpeded
        # 6. entities two sizes larger than an entity can move through that entity's space unimpeded
        # 7. otherwise it's considered difficult terrain
        # 8. entities can't end their turn in the same space as another entity



        

        # need a way to track allies, enemies, neutral, and uncertain entities
        self.allies = []
        self.enemies = []
        self.neutral = []
        self.uncertain = []

        # how should this be implemented?

        self.is_mounted = False
        self.is_ridden = False


    def subactions_based_on_move_speed(self):
        move_speed = self.speed 

        move_speed_subaction_reps = []
        move_speed_subaction_text = []

        # move speed for player character is usually 30 feet, or 6 spaces
        # so there needs to be 6 subactions
        # move speed for a monster is usually 30 feet, but could be 40 or 50
        # additionally certain effects can increase or decrease the move speed
        # the self.speed is already divided by 5 so that it's in spaces, not feet

        # based on the self.subactions list, the reps for the move subactions will be determined

        if len(self.subactions) == 0:
            for i in range(move_speed):
                move_speed_subaction_reps.append(i)
                move_speed_subaction_text.append('move ' + str(i+1) + ' space')

            move_speed_subaction_sources = [['basic rules','speed']] * len(move_speed_subaction_reps) # include the dependent attribute

            self.subaction_catalog['move_subactions_reps'] = move_speed_subaction_reps
            self.subaction_catalog['move_subactions_text'] = move_speed_subaction_text
            self.subaction_catalog['move_subactions_sources'] = move_speed_subaction_sources

            self.subaction_catalog['subactions_req_location'] = [i for i in self.subaction_catalog['move_subactions_reps']]

            # now to add to move_cost_dict
            for i in range(move_speed):
                self.subaction_catalog['move_cost_dict'][i] = i+1

            # now add to self.subactions
            self.subactions += move_speed_subaction_reps

            # and finally need to fill in target_distance_scores for each subaction
            for i in range(move_speed):
                self.subaction_catalog['target_distance_scores'][i] = i+1

    def subactions_post_move_speed(self):
        # the idea here is to then add all of the non-move speed dependent move subactions
        # such as go prone, stand up, mount, dismount

        go_prone = len(self.subactions)
        self.subaction_catalog['move_subactions_text'].append('go prone')
        self.subaction_catalog['move_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['move_subactions_reps'].append(go_prone)
        self.subaction_catalog['move_cost_dict'][go_prone] = 0
        self.subactions.append(go_prone)

        stand_up = len(self.subactions)
        self.subaction_catalog['move_subactions_text'].append('stand up')
        self.subaction_catalog['move_subactions_sources'].append(['basic rules','speed'])
        self.subaction_catalog['move_subactions_reps'].append(stand_up)
        self.subaction_catalog['move_cost_dict'][stand_up] = self.speed/2
        self.subactions.append(stand_up)

        mount = len(self.subactions)
        self.subaction_catalog['move_subactions_text'].append('mount')
        self.subaction_catalog['move_subactions_sources'].append(['basic rules','speed'])
        self.subaction_catalog['move_subactions_reps'].append(mount)
        self.subaction_catalog['subactions_req_location'].append(mount)
        self.subaction_catalog['subactions_req_entity'].append(mount)
        self.subaction_catalog['move_cost_dict'][mount] = self.speed/2
        self.subactions.append(mount)
        self.subaction_catalog['target_distance_scores'][mount] = 1

        dismount = len(self.subactions)
        self.subaction_catalog['move_subactions_text'].append('dismount')
        self.subaction_catalog['move_subactions_sources'].append(['basic rules','speed'])
        self.subaction_catalog['move_subactions_reps'].append(dismount)
        self.subaction_catalog['subactions_req_location'].append(dismount)
        self.subaction_catalog['move_cost_dict'][dismount] = self.speed/2
        self.subactions.append(dismount)
        self.subaction_catalog['target_distance_scores'][dismount] = 1

    def subactions_universal(self):
        # dodge, disengage, hide, search, 

        dodge = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('dodge')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(dodge)
        self.subactions.append(dodge)
        

        disengage = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('disengage')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(disengage)
        self.subactions.append(disengage)

        hide = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('hide')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(hide)
        self.subactions.append(hide)

        search = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('search')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(search)
        self.subactions.append(search)
        # will need to determine how the search action works in this system later...

    def subactions_object_interactions(self):
        # Object (Free) Ground Pickup
        object_free_ground_pickup = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--ground_pickup')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_ground_pickup)
        self.subaction_catalog['object_free_subactions'].append(object_free_ground_pickup)
        self.subaction_catalog['subactions_req_targets'].append(object_free_ground_pickup)
        self.subaction_catalog['subactions_req_location'].append(object_free_ground_pickup)
        self.subaction_catalog['subactions_req_objects'].append(object_free_ground_pickup)
        self.subactions.append(object_free_ground_pickup)
        self.subaction_catalog['target_distance_scores'][object_free_ground_pickup] = 1
        
        self.subaction_catalog['free_subactions_text'].append('object--free--ground_pickup')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_ground_pickup)


        # Object (Action) Ground Pickup
        object_action_ground_pickup = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--ground_pickup')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_ground_pickup)
        self.subaction_catalog['object_action_subactions'].append(object_action_ground_pickup)
        self.subaction_catalog['subactions_req_targets'].append(object_action_ground_pickup)
        self.subaction_catalog['subactions_req_location'].append(object_action_ground_pickup)
        self.subaction_catalog['subactions_req_objects'].append(object_action_ground_pickup)
        self.subactions.append(object_action_ground_pickup)
        self.subaction_catalog['target_distance_scores'][object_action_ground_pickup] = 1
        self.subaction_catalog['action_subactions_text'].append('object--action--ground_pickup')
        self.subaction_catalog['action_subactions_sources'].append(object_action_ground_pickup)
        self.subaction_catalog['action_subactions_reps'].append(object_action_ground_pickup)


        # Object (Free) Ground Drop from Inventory
        object_free_ground_drop_from_inventory = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--ground_drop_from_inventory')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_ground_drop_from_inventory)
        self.subaction_catalog['object_free_subactions'].append(object_free_ground_drop_from_inventory)
        self.subaction_catalog['subactions_req_targets'].append(object_free_ground_drop_from_inventory)
        self.subaction_catalog['subactions_req_location'].append(object_free_ground_drop_from_inventory)
        self.subaction_catalog['subactions_req_objects'].append(object_free_ground_drop_from_inventory)
        self.subactions.append(object_free_ground_drop_from_inventory)
        self.subaction_catalog['target_distance_scores'][object_free_ground_drop_from_inventory] = 1

        # Object (Action) Ground Drop from Inventory
        object_action_ground_drop_from_inventory = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--ground_drop_from_inventory')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_ground_drop_from_inventory)
        self.subaction_catalog['object_action_subactions'].append(object_action_ground_drop_from_inventory)
        self.subaction_catalog['subactions_req_targets'].append(object_action_ground_drop_from_inventory)
        self.subaction_catalog['subactions_req_location'].append(object_action_ground_drop_from_inventory)
        self.subaction_catalog['subactions_req_objects'].append(object_action_ground_drop_from_inventory)
        self.subactions.append(object_action_ground_drop_from_inventory)
        self.subaction_catalog['target_distance_scores'][object_action_ground_drop_from_inventory] = 1
        self.subaction_catalog['action_subactions_text'].append('object--action--ground_drop_from_inventory')
        self.subaction_catalog['action_subactions_sources'].append(object_action_ground_drop_from_inventory)
        self.subaction_catalog['action_subactions_reps'].append(object_action_ground_drop_from_inventory)



        # Object (Free) Ground Drop Main Hand
        object_free_ground_drop_main_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--ground_drop_main_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_ground_drop_main_hand)
        self.subaction_catalog['object_free_subactions'].append(object_free_ground_drop_main_hand)
        self.subaction_catalog['subactions_req_targets'].append(object_free_ground_drop_main_hand)
        self.subaction_catalog['subactions_req_location'].append(object_free_ground_drop_main_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_free_ground_drop_main_hand)
        self.subactions.append(object_free_ground_drop_main_hand)
        self.subaction_catalog['target_distance_scores'][object_free_ground_drop_main_hand] = 1
        
        self.subaction_catalog['free_subactions_text'].append('object--free--ground_drop_main_hand')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_ground_drop_main_hand)

        # Object (Free) Ground Drop Off Hand
        object_free_ground_drop_off_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--ground_drop_off_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_ground_drop_off_hand)
        self.subaction_catalog['object_free_subactions'].append(object_free_ground_drop_off_hand)
        self.subaction_catalog['subactions_req_targets'].append(object_free_ground_drop_off_hand)
        self.subaction_catalog['subactions_req_location'].append(object_free_ground_drop_off_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_free_ground_drop_off_hand)
        self.subactions.append(object_free_ground_drop_off_hand)
        self.subaction_catalog['target_distance_scores'][object_free_ground_drop_off_hand] = 1
        
        self.subaction_catalog['free_subactions_text'].append('object--free--ground_drop_off_hand')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_ground_drop_off_hand)

        # Object (Free) Ground Drop Both Hands
        object_free_ground_drop_both_hands = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--ground_drop_both_hands')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_ground_drop_both_hands)
        self.subaction_catalog['object_free_subactions'].append(object_free_ground_drop_both_hands)
        self.subaction_catalog['subactions_req_targets'].append(object_free_ground_drop_both_hands)
        self.subaction_catalog['subactions_req_location'].append(object_free_ground_drop_both_hands)
        self.subaction_catalog['subactions_req_objects'].append(object_free_ground_drop_both_hands)
        self.subactions.append(object_free_ground_drop_both_hands)
        self.subaction_catalog['target_distance_scores'][object_free_ground_drop_both_hands] = 1
        
        self.subaction_catalog['free_subactions_text'].append('object--free--ground_drop_both_hands')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_ground_drop_both_hands)

        # Object (Action) Ground Drop Main Hand
        object_action_ground_drop_main_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--ground_drop_main_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_ground_drop_main_hand)
        self.subaction_catalog['object_action_subactions'].append(object_action_ground_drop_main_hand)
        self.subaction_catalog['subactions_req_targets'].append(object_action_ground_drop_main_hand)
        self.subaction_catalog['subactions_req_location'].append(object_action_ground_drop_main_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_action_ground_drop_main_hand)
        self.subactions.append(object_action_ground_drop_main_hand)
        self.subaction_catalog['target_distance_scores'][object_action_ground_drop_main_hand] = 1
        self.subaction_catalog['action_subactions_text'].append('object--action--ground_drop_main_hand')
        self.subaction_catalog['action_subactions_sources'].append(object_action_ground_drop_main_hand)
        self.subaction_catalog['action_subactions_reps'].append(object_action_ground_drop_main_hand)

        # Object (Action) Ground Drop Off Hand
        object_action_ground_drop_off_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--ground_drop_off_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_ground_drop_off_hand)
        self.subaction_catalog['object_action_subactions'].append(object_action_ground_drop_off_hand)
        self.subaction_catalog['subactions_req_targets'].append(object_action_ground_drop_off_hand)
        self.subaction_catalog['subactions_req_location'].append(object_action_ground_drop_off_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_action_ground_drop_off_hand)
        self.subactions.append(object_action_ground_drop_off_hand)
        self.subaction_catalog['target_distance_scores'][object_action_ground_drop_off_hand] = 1
        self.subaction_catalog['action_subactions_text'].append('object--action--ground_drop_off_hand')
        self.subaction_catalog['action_subactions_sources'].append(object_action_ground_drop_off_hand)
        self.subaction_catalog['action_subactions_reps'].append(object_action_ground_drop_off_hand)
        
        # Object (Action) Ground Drop Both Hands
        object_action_ground_drop_both_hands = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--ground_drop_both_hands')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_ground_drop_both_hands)
        self.subaction_catalog['object_action_subactions'].append(object_action_ground_drop_both_hands)
        self.subaction_catalog['subactions_req_targets'].append(object_action_ground_drop_both_hands)
        self.subaction_catalog['subactions_req_location'].append(object_action_ground_drop_both_hands)
        self.subaction_catalog['subactions_req_objects'].append(object_action_ground_drop_both_hands)
        self.subactions.append(object_action_ground_drop_both_hands)
        self.subaction_catalog['target_distance_scores'][object_action_ground_drop_both_hands] = 1
        self.subaction_catalog['action_subactions_text'].append('object--action--ground_drop_both_hands')
        self.subaction_catalog['action_subactions_sources'].append(object_action_ground_drop_both_hands)
        self.subaction_catalog['action_subactions_reps'].append(object_action_ground_drop_both_hands)




        # Object (Free) Environment
        # Object (Action) Environment




        # Object (Free) Self Equip Main Hand
        object_free_self_equip_main_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--self_equip_main_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_self_equip_main_hand)
        self.subaction_catalog['object_free_subactions'].append(object_free_self_equip_main_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_free_self_equip_main_hand)
        self.subactions.append(object_free_self_equip_main_hand)
        self.subaction_catalog['free_subactions_text'].append('object--free--self_equip_main_hand')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_self_equip_main_hand)


        # Object (Free) Self Equip Off Hand
        object_free_self_equip_off_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--self_equip_off_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_self_equip_off_hand)
        self.subaction_catalog['object_free_subactions'].append(object_free_self_equip_off_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_free_self_equip_off_hand)
        self.subactions.append(object_free_self_equip_off_hand)
        self.subaction_catalog['free_subactions_text'].append('object--free--self_equip_off_hand')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_self_equip_off_hand)


        # Object (Free) Self Equip Both Hands
        object_free_self_equip_both_hands = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--self_equip_both_hands')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_self_equip_both_hands)
        
        self.subaction_catalog['object_free_subactions'].append(object_free_self_equip_both_hands)
        
        self.subaction_catalog['subactions_req_objects'].append(object_free_self_equip_both_hands)
        
        self.subactions.append(object_free_self_equip_both_hands)
        self.subaction_catalog['free_subactions_text'].append('object--free--self_equip_both_hands')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_self_equip_both_hands)




        # Object (Action) Self Equip Main Hand
        object_action_self_equip_main_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--self_equip_main_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_self_equip_main_hand)
        
        self.subaction_catalog['object_action_subactions'].append(object_action_self_equip_main_hand)
        
        self.subaction_catalog['action_subactions_text'].append('object--action--self_equip_main_hand')
        self.subaction_catalog['action_subactions_sources'].append(object_action_self_equip_main_hand)
        self.subaction_catalog['action_subactions_reps'].append(object_action_self_equip_main_hand)
        
        self.subaction_catalog['subactions_req_objects'].append(object_action_self_equip_main_hand)
        
        self.subactions.append(object_action_self_equip_main_hand)

        # Object (Action) Self Equip Off Hand
        object_action_self_equip_off_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--self_equip_off_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_self_equip_off_hand)
        
        self.subaction_catalog['object_action_subactions'].append(object_action_self_equip_off_hand)
        
        self.subaction_catalog['action_subactions_text'].append('object--action--self_equip_off_hand')
        self.subaction_catalog['action_subactions_sources'].append(object_action_self_equip_off_hand)
        self.subaction_catalog['action_subactions_reps'].append(object_action_self_equip_off_hand)

        self.subaction_catalog['subactions_req_objects'].append(object_action_self_equip_off_hand)
        
        self.subactions.append(object_action_self_equip_off_hand)

        # Object (Action) Self Equip Both Hands
        object_action_self_equip_both_hands = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--self_equip_both_hands')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_self_equip_both_hands)
        
        self.subaction_catalog['object_action_subactions'].append(object_action_self_equip_both_hands)
        
        self.subaction_catalog['action_subactions_text'].append('object--action--self_equip_both_hands')
        self.subaction_catalog['action_subactions_sources'].append(object_action_self_equip_both_hands)
        self.subaction_catalog['action_subactions_reps'].append(object_action_self_equip_both_hands)

        self.subaction_catalog['subactions_req_objects'].append(object_action_self_equip_both_hands)
        
        self.subactions.append(object_action_self_equip_both_hands)




        # Object (Free) Self Unequip Main Hand
        object_free_self_unequip_main_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--self_unequip_main_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_self_unequip_main_hand)
        self.subaction_catalog['object_free_subactions'].append(object_free_self_unequip_main_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_free_self_unequip_main_hand)
        self.subactions.append(object_free_self_unequip_main_hand)
        self.subaction_catalog['free_subactions_text'].append('object--free--self_unequip_main_hand')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_self_unequip_main_hand)


        # Object (Free) Self Unequip Off Hand
        object_free_self_unequip_off_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--self_unequip_off_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_self_unequip_off_hand)
        self.subaction_catalog['object_free_subactions'].append(object_free_self_unequip_off_hand)
        self.subaction_catalog['subactions_req_objects'].append(object_free_self_unequip_off_hand)
        self.subactions.append(object_free_self_unequip_off_hand)
        self.subaction_catalog['free_subactions_text'].append('object--free--self_unequip_off_hand')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_self_unequip_off_hand)

        
        # Object (Free) Self Unequip Both Hands
        object_free_self_unequip_both_hands = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--free--self_unequip_both_hands')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_free_self_unequip_both_hands)
        
        self.subaction_catalog['object_free_subactions'].append(object_free_self_unequip_both_hands)

        self.subaction_catalog['subactions_req_objects'].append(object_free_self_unequip_both_hands)
        
        self.subactions.append(object_free_self_unequip_both_hands)
        self.subaction_catalog['free_subactions_text'].append('object--free--self_unequip_both_hands')
        self.subaction_catalog['free_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['free_subactions_reps'].append(object_free_self_unequip_both_hands)



        # Object (Action) Self Unequip Main Hand
        object_action_self_unequip_main_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--self_unequip_main_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_self_unequip_main_hand)
        
        self.subaction_catalog['object_action_subactions'].append(object_action_self_unequip_main_hand)
        
        self.subaction_catalog['action_subactions_text'].append('object--action--self_unequip_main_hand')
        self.subaction_catalog['action_subactions_sources'].append(object_action_self_unequip_main_hand)
        self.subaction_catalog['action_subactions_reps'].append(object_action_self_unequip_main_hand)

        self.subaction_catalog['subactions_req_objects'].append(object_action_self_unequip_main_hand)
        
        self.subactions.append(object_action_self_unequip_main_hand)

        # Object (Action) Self Unequip Off Hand
        object_action_self_unequip_off_hand = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--self_unequip_off_hand')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_self_unequip_off_hand)
        
        self.subaction_catalog['object_action_subactions'].append(object_action_self_unequip_off_hand)
        
        self.subaction_catalog['action_subactions_text'].append('object--action--self_unequip_off_hand')
        self.subaction_catalog['action_subactions_sources'].append(object_action_self_unequip_off_hand)
        self.subaction_catalog['action_subactions_reps'].append(object_action_self_unequip_off_hand)

        self.subaction_catalog['subactions_req_objects'].append(object_action_self_unequip_off_hand)
        
        self.subactions.append(object_action_self_unequip_off_hand)

        # Object (Action) Self Unequip Both Hands
        object_action_self_unequip_both_hands = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('object--action--self_unequip_both_hands')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['object_subactions_reps'].append(object_action_self_unequip_both_hands)
        
        self.subaction_catalog['object_action_subactions'].append(object_action_self_unequip_both_hands)
        
        self.subaction_catalog['action_subactions_text'].append('object--action--self_unequip_both_hands')
        self.subaction_catalog['action_subactions_sources'].append(object_action_self_unequip_both_hands)        
        self.subaction_catalog['action_subactions_reps'].append(object_action_self_unequip_both_hands)

        self.subaction_catalog['subactions_req_objects'].append(object_action_self_unequip_both_hands)
        
        self.subactions.append(object_action_self_unequip_both_hands)




        # Don Shield
        don_shield = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('don_shield')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(don_shield)
        self.subaction_catalog['object_action_subactions'].append(don_shield)
        self.subaction_catalog['action_subactions_text'].append('don_shield')
        self.subaction_catalog['action_subactions_reps'].append(don_shield)
        self.subaction_catalog['subactions_req_objects'].append(don_shield)
        self.subactions.append(don_shield)

        # Doff Shield
        doff_shield = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('doff_shield')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(doff_shield)
        self.subaction_catalog['object_action_subactions'].append(doff_shield)
        self.subaction_catalog['action_subactions_text'].append('doff_shield')
        self.subaction_catalog['action_subactions_reps'].append(doff_shield)
        self.subaction_catalog['subactions_req_objects'].append(doff_shield)
        self.subactions.append(doff_shield)

        # Drink Potion
        drink_potion = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('drink_potion')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(drink_potion)
        self.subaction_catalog['object_action_subactions'].append(drink_potion)
        self.subaction_catalog['action_subactions_reps'].append(drink_potion)
        self.subaction_catalog['subactions_req_objects'].append(drink_potion)
        self.subactions.append(drink_potion)
        

        # Feed Potion
        feed_potion = len(self.subactions)
        self.subaction_catalog['object_subactions_text'].append('feed_potion')
        self.subaction_catalog['object_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['object_subactions_reps'].append(feed_potion)
        self.subaction_catalog['object_action_subactions'].append(feed_potion)
        self.subaction_catalog['subactions_req_targets'].append(feed_potion)
        self.subaction_catalog['subactions_req_location'].append(feed_potion)
        self.subaction_catalog['subactions_req_objects'].append(feed_potion)
        self.subaction_catalog['subactions_req_entity'].append(feed_potion)
        self.subactions.append(feed_potion)
        self.subaction_catalog['target_distance_scores'][feed_potion] = 1
        self.subaction_catalog['action_subactions_text'].append('feed_potion')
        self.subaction_catalog['action_subactions_reps'].append(feed_potion)
        self.subaction_catalog['action_subactions_sources'].append(feed_potion)

    def subactions_attack(self):
        # attack (action) with weapon in main hand
        attack_main_hand = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('attack--weapon--main_hand')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['attack_subactions_reps'].append(attack_main_hand)
        self.subaction_catalog['subactions_req_objects'].append(attack_main_hand)
        self.subaction_catalog['subactions_req_targets'].append(attack_main_hand)
        self.subaction_catalog['subactions_req_location'].append(attack_main_hand)
        self.subaction_catalog['subactions_req_entity'].append(attack_main_hand)
        self.subactions.append(attack_main_hand)
        self.subaction_catalog['target_distance_scores'][attack_main_hand] = 1
        self.subaction_catalog['action_subactions_text'].append('attack--weapon--main_hand')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['action_subactions_reps'].append(attack_main_hand)


        # attack (bonus action) with weapon in off hand
        attack_off_hand = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('attack--weapon--off_hand')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['attack_subactions_reps'].append(attack_off_hand)
        self.subaction_catalog['subactions_req_objects'].append(attack_off_hand)
        self.subaction_catalog['subactions_req_targets'].append(attack_off_hand)
        self.subaction_catalog['subactions_req_location'].append(attack_off_hand)
        self.subaction_catalog['subactions_req_entity'].append(attack_off_hand)
        self.subactions.append(attack_off_hand)
        self.subaction_catalog['target_distance_scores'][attack_off_hand] = 1
        self.subaction_catalog['bonus_subactions_text'].append('attack--weapon--off_hand')
        self.subaction_catalog['bonus_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['bonus_subactions_reps'].append(attack_off_hand)

        # attack (action) with weapon in both hands
        attack_both_hands = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('attack--weapon--both_hands')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['attack_subactions_reps'].append(attack_both_hands)
        self.subaction_catalog['subactions_req_objects'].append(attack_both_hands)
        self.subaction_catalog['subactions_req_targets'].append(attack_both_hands)
        self.subaction_catalog['subactions_req_location'].append(attack_both_hands)
        self.subaction_catalog['subactions_req_entity'].append(attack_both_hands)
        self.subactions.append(attack_both_hands)
        self.subaction_catalog['target_distance_scores'][attack_both_hands] = 1
        self.subaction_catalog['action_subactions_text'].append('attack--weapon--both_hands')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['action_subactions_reps'].append(attack_both_hands)

        # grapple (action) with main hand
        grapple_main_hand = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('grapple--main_hand')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['attack_subactions_reps'].append(grapple_main_hand)
        self.subaction_catalog['subactions_req_objects'].append(grapple_main_hand)
        self.subaction_catalog['subactions_req_targets'].append(grapple_main_hand)
        self.subaction_catalog['subactions_req_location'].append(grapple_main_hand)
        self.subaction_catalog['subactions_req_entity'].append(grapple_main_hand)
        self.subactions.append(grapple_main_hand)
        self.subaction_catalog['target_distance_scores'][grapple_main_hand] = 1
        self.subaction_catalog['action_subactions_text'].append('grapple--main_hand')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['action_subactions_reps'].append(grapple_main_hand)


        # grapple (action) with off hand
        grapple_off_hand = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('grapple--off_hand')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['attack_subactions_reps'].append(grapple_off_hand)
        self.subaction_catalog['subactions_req_objects'].append(grapple_off_hand)
        self.subaction_catalog['subactions_req_targets'].append(grapple_off_hand)
        self.subaction_catalog['subactions_req_location'].append(grapple_off_hand)
        self.subaction_catalog['subactions_req_entity'].append(grapple_off_hand)
        self.subactions.append(grapple_off_hand)
        self.subaction_catalog['target_distance_scores'][grapple_off_hand] = 1
        self.subaction_catalog['action_subactions_text'].append('grapple--off_hand')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules','hands'])
        self.subaction_catalog['action_subactions_reps'].append(grapple_off_hand)


        # unarmed strike (action)
        unarmed_strike = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('unarmed_strike')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['attack_subactions_reps'].append(unarmed_strike)
        self.subaction_catalog['subactions_req_targets'].append(unarmed_strike)
        self.subaction_catalog['subactions_req_location'].append(unarmed_strike)
        self.subaction_catalog['subactions_req_entity'].append(unarmed_strike)
        self.subactions.append(unarmed_strike)
        self.subaction_catalog['target_distance_scores'][unarmed_strike] = 1
        self.subaction_catalog['action_subactions_text'].append('unarmed_strike')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(unarmed_strike)


        # shove - push
        shove_push = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('shove--push')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['attack_subactions_reps'].append(shove_push)
        self.subaction_catalog['subactions_req_targets'].append(shove_push)
        self.subaction_catalog['subactions_req_location'].append(shove_push)
        self.subaction_catalog['subactions_req_entity'].append(shove_push)
        self.subactions.append(shove_push)
        self.subaction_catalog['target_distance_scores'][shove_push] = 1
        self.subaction_catalog['action_subactions_text'].append('shove--push')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(shove_push)

        # shove - prone
        shove_prone = len(self.subactions)
        self.subaction_catalog['attack_subactions_text'].append('shove--prone')
        self.subaction_catalog['attack_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['attack_subactions_reps'].append(shove_prone)
        self.subaction_catalog['subactions_req_targets'].append(shove_prone)
        self.subaction_catalog['subactions_req_location'].append(shove_prone)
        self.subaction_catalog['subactions_req_entity'].append(shove_prone)
        self.subactions.append(shove_prone)
        self.subaction_catalog['target_distance_scores'][shove_prone] = 1
        self.subaction_catalog['action_subactions_text'].append('shove--prone')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(shove_prone)

    def subactions_teamwork(self):
        # help (attack)
        help_attack = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('help--attack')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(help_attack)
        self.subaction_catalog['subactions_req_targets'].append(help_attack)
        self.subaction_catalog['subactions_req_location'].append(help_attack)
        self.subaction_catalog['subactions_req_entity'].append(help_attack)
        self.subaction_catalog['subactions_req_allies'].append(help_attack)
        self.subactions.append(help_attack)
        self.subaction_catalog['target_distance_scores'][help_attack] = 1


        # help (skill)
        help_skill = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('help--skill')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(help_skill)
        self.subaction_catalog['subactions_req_targets'].append(help_skill)
        self.subaction_catalog['subactions_req_location'].append(help_skill)
        self.subaction_catalog['subactions_req_entity'].append(help_skill)
        self.subaction_catalog['subactions_req_allies'].append(help_skill)
        self.subactions.append(help_skill)
        self.subaction_catalog['target_distance_scores'][help_skill] = 1


        # wake
        wake = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('wake')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(wake)
        self.subaction_catalog['subactions_req_targets'].append(wake)
        self.subaction_catalog['subactions_req_location'].append(wake)
        self.subaction_catalog['subactions_req_entity'].append(wake)
        self.subactions.append(wake)
        self.subaction_catalog['target_distance_scores'][wake] = 1

        # stabilize
        stabilize = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('stabilize')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(stabilize)
        self.subaction_catalog['subactions_req_targets'].append(stabilize)
        self.subaction_catalog['subactions_req_location'].append(stabilize)
        self.subaction_catalog['subactions_req_entity'].append(stabilize)
        self.subactions.append(stabilize)
        self.subaction_catalog['target_distance_scores'][stabilize] = 1

    def subactions_casting(self):
        # cast
        cast = len(self.subactions)
        self.subaction_catalog['action_subactions_text'].append('cast')
        self.subaction_catalog['action_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['action_subactions_reps'].append(cast)
        self.subaction_catalog['subactions_req_targets'].append(cast)
        self.subaction_catalog['subactions_req_location'].append(cast)
        self.subaction_catalog['subactions_req_entity'].append(cast)
        self.subaction_catalog['subactions_req_objects'].append(cast)
#        self.subaction_catalog['subactions_req_spells'].append(cast)

        self.subactions.append(cast)

        # end concentration
        end_concentration = len(self.subactions)
        self.subaction_catalog['free_subactions_text'].append(['end_concentration'])
        self.subaction_catalog['free_subactions_sources'].append(['basic rules'])
        self.subaction_catalog['free_subactions_reps'].append([end_concentration])
        self.subactions.append(end_concentration)


    def add_rules_for_dfs(self, rules, target):
        self.dfs_rules[target] = rules


    def update_subactions(self):
        pass

        # to run when an attribute that a subaction is dependent on
        # such as move speed requiring a recalculation of move subactions

    def add_spell(self, spell):
        self.spells.append(spell)


    def add_subaction(self, subaction):
        self.subactions.append(subaction)
        # this will need more work later...

    def add_spell(self, spell):
        self.spells.append(spell)

        # concepts for implementation
        # 1. seperate spell subaction list for if the cast action is taken
        #       self.spell_subactions.append(len(spell_subactions))
        #       self.spell_class_object_ids_to_subactions[spell] = len(spell_subactions)
        #       self.spell_subactions_sources.append(self.source)

        # 2. spell subactions also go in the subaction_dict
        #       self.subaction_dict[len(spell_subactions)] = spell.name
        #       self.subaction_dict_sources[len(spell_subactions)] = self.source


        # if the spell is an action, bonus action, or reaction
        # append it to the relevant list


    def create_entity(self, type):
        if type == 'player character':
            pass

        elif type == 'monster':
            pass

    def print_subactions_and_catalog(self):
        print(self.subactions)
        print()
        for key in self.subaction_catalog:
            print(key, self.subaction_catalog[key])


#class enemy:
#    def __init__(self,world):
#        self.world = world
#        self.is_spawned = False

#        self.caster = False
#        self.concentrating = False

#        self.attack_limit = 1

#        self.hp = 2
#        self.ac = 10
#        self.conditions = []

#        self.reaction_used = False

#        if self.is_spawned == False:
#            self.location = [0,0]
            
#        elif self.is_spawned == True:
#            x_loc = world.grid[np.where(world.grid[:,0] == max(world.grid))]
#            print('x: ',x_loc)
#            y_loc = world.grid[np.where(world.grid[0,:] == max(world.grid))]
#            print('y: ',y_loc)
#            self.location = [x_loc,y_loc]

