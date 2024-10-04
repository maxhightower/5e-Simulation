# DFS Universal Rules
import numpy as np

# should each entity have a custom version of the data below
# and then what's below is the default for player characters???
# according to the rules, monsters aren't limited by the same system that player characters are



subaction_dict = {
    '0': 'Move_One',                # needs a target
    '1': 'Move_Two',
    '2': 'Move_Three',
    '3': 'Move_Four',
    '4': 'Object (Free) Ground Pickup',      # needs a target
    '5': 'Attack (Weapon) (Main_Hand)',              # needs a target
    '6': 'Dodge',
    '7': 'Object (Action) Ground Pickup',              # needs a target
    '8': 'Disengage',
    '9': 'Hide',
    '10': 'Help (Attack)',
    '11': 'Cast',                                       # sometimes Cast needs a target, object, or is a bonus action...
    '12': 'Dash',
    '13': 'Don Shield',
    '14': 'End Concentration',
    '15': 'Attack (Weapon) (Off_Hand)',
    '16': 'Grapple',
    '17': 'Escape Grapple',
    '18': 'Shove',
    '19': 'Go Prone',
    '20': 'Stand Up',
    '21': 'Stabilize Creature',
    '22': 'Wake Creature',
    '23': 'Move_Five',
    '24': 'Move_Six',
    '25': 'Object (Free) Self Equip Main_Hand',
    '26': 'Object (Action) Self Equip Main_Hand',
    '27': 'Object (Free) Environment',
    '28': 'Object (Action) Environment',
    '29': 'Object (Free) Ground Drop Inventory',
    '30': 'Object (Action) Ground Drop Inventory',
    '31': 'Object (Free) Self Unequip (Main_Hand)',
    '32': 'Object (Action) Self Unequip (Main_Hand)',
    '33': 'Drink Potion',
    '34': 'Activate Magic Item',
    '35': 'Help (Skill Check)',
    '36': 'Attack (Unnarmed Strike)',
    '37': 'Object (Free) Self Equip Off_Hand',
    '38': 'Object (Action) Self Equip Off_Hand',
    '39': 'Doff Shield',
    '40': 'Object (Free) Self Unequip (Off_Hand)',
    '41': 'Object (Action) Self Unequip (Off_Hand)',
    '42': 'Object (Free) Ground Drop Main_Hand',
    '43': 'Object (Free) Ground Drop Off_Hand',
    '44': 'Object (Free) Ground Drop Both_Hands',
    '45': 'Object (Action) Ground Drop Main_Hand',
    '46': 'Object (Action) Ground Drop Off_Hand',
    '47': 'Object (Action) Ground Drop Both_Hands',
    '48': 'Attack (Weapon) (Both_Hands)',
    '49': 'Object (Free) Self Equip Both_Hands',
    '50': 'Object (Action) Self Equip Both_Hands',
    '51': 'Object (Free) Self Unequip (Both_Hands)',
    #'52': 'Object (Action) Self Unequip (Both_Hands)',


}


# does picking up an item automatically equip it?
# no it goes straight to inventory


move_subactions = [0,1,2,3,23,24]
    # jump
    # crawl
    # squeeze

action_subactions = [5,6,7,8,9,10,11,12,13,16,17,18,21,22,26,28,30,32,33,34,35,36,38,39,41,45,46,47,48,50,52]
attack_subactions = [5,16,18,36,48]
free_subactions = [[4,25,27,29,31,37,40,42,43,44],[14]] # can do one of each list
bonus_subactions = [15]
object_subactions = [4,7,25,26,27,28,29,30,31,32,37,38,40,41,42,43,44,45,46,47,49,50,51,52]
object_action_subactions = [7,26,28,30,32,38,41,45,46,47,50,52]
object_free_subactions = [4,25,27,29,31,37,40,42,43,44,49,51]

subactions_req_targets = [0,1,2,3,4,5,7,10,15,23,24,27,28,29,30,35,36,48]
# subactions_req_targets = move_subactions + object_subactions + attack_subactions

subactions_req_allies = [10,21,22,35]
subactions_req_objects = [4,5,7,13,15,25,26,29,30,31,32,33,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
subactions_req_entity = [5,10,15,16,18,21,22,35,36,48]

# conjoined subactions are where when you do one subaction, you can do another subaction without cost
conjoined_subactions = []

circumstance_subactions = [] # these are subactions that impose ADV or DisADV
effect_subactions = [] # these are subactions that provide bonsues or penalties
sub_effects = []
turn_effects = []

effect_dictionary = {} # this will assign the effect_subaction_number to the effect_class

class effect:
    def __init__(self, name, type, duration, target, effect):
        self.name = name
        self.type = type
        self.duration = duration
        self.target = target
        self.effect = effect



theoretical_turn_length = len(free_subactions) + 6 + 1 + 1

class entity:
    def __init__(self,world):
        self.world = world
        self.is_spawned = False

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

        self.spells = {}

        if self.is_spawned == False:
            self.location = [0,0]
            
        elif self.is_spawned == True:
            x_loc = world.grid[np.where(world.grid[:,0] == max(world.grid))]
            print('x: ',x_loc)
            y_loc = world.grid[np.where(world.grid[0,:] == max(world.grid))]
            print('y: ',y_loc)
            self.location = [x_loc,y_loc]

        self.speed = 6
        self.coins = 0

        self.shield_proficient = False # because shield is considered medium armor, the default should be false

        self.hands = 2
        self.main_hand = []
        self.off_hand = []

        self.strength_mod = 1

        # want to implement entity size
        # self.size = 'medium'
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


        # will need to have a add_entity() in order to add a key: value pair to circumstances per enemy in world


target_distance_scores = { # the distance from which a location can be per subaction
            0: 1,
            1: 2, 
            2: 3,
            3: 4,
            5: 1,
            4: 1,
            7: 1,
            10: 1,
            15: 1,
            23: 5,
            24: 6,
            27: 1,
            28: 1,
            29: 1,
            30: 1,
            31: 1,
            32: 1,
            35: 1,
            36: 1,
            48: 1,
        }

def add_optional_rule_action_options():
    pass
    # add the following subactions to subaction_dict
    # - climb onto bigger creature
    # - disarm
    # - healing surge
    # - overrun
    # - shove aside
    # - tumble

    # additionally will need to add the target_distance_scores for each of these subactions
    # - climb onto bigger creature = 1
    # - disarm = 1 (melee range)
    # - healing surge = self
    # - overrun = 1
    # - shove aside = 1
    # - tumble = 1
