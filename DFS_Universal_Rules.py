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
    '5': 'Attack (Weapon)',              # needs a target
    '6': 'Dodge',
    '7': 'Object (Action) Ground Pickup',              # needs a target
    '8': 'Disengage',
    '9': 'Hide',
    '10': 'Help (Attack)',
    '11': 'Cast',                                       # sometimes Cast needs a target, object, or is a bonus action...
    '12': 'Dash',
    '13': 'Don or Doff Shield',
    '14': 'End Concentration',
    '15': 'Off Hand Weapon Attack',
    '16': 'Grapple',
    '17': 'Escape Grapple',
    '18': 'Shove',
    '19': 'Go Prone',
    '20': 'Stand Up',
    '21': 'Stabilize Creature',
    '22': 'Wake Creature',
    '23': 'Move_Five',
    '24': 'Move_Six',
    '25': 'Object (Free) Self Equip',
    '26': 'Object (Action) Self Equip',
    '27': 'Object (Free) Environment',
    '28': 'Object (Action) Environment',
    '29': 'Object (Free) Ground Drop',
    '30': 'Object (Action) Ground Drop',
    '31': 'Object (Free) Self Unequip',
    '32': 'Object (Action) Self Unequip',
    '33': 'Drink Potion',
    '34': 'Activate Magic Item',
    '35': 'Help (Skill Check)',
    #'36': 'Attack (Unnarmed Strike)',

}


# does picking up an item automatically equip it?
# 


move_subactions = [0,1,2,3,23,24]
    # jump
    # crawl
    # squeeze

action_subactions = [5,6,7,8,9,10,11,12,13,16,17,18,21,22,26,28,30,32,33,34,35,36]
attack_subactions = [5,16,18,36]
free_subactions = [[4,25,27,29,31],[14]] # can do one of each list
bonus_subactions = [15]
object_subactions = [4,7,25,26,27,28,29,30,31,32,]
object_action_subactions = [7,26,28,30,32]
object_free_subactions = [4,25,27,29,31]

subactions_req_targets = [0,1,2,3,4,5,7,10,15,23,24,27,28,29,30,35,36]
# subactions_req_targets = move_subactions + object_subactions + attack_subactions

subactions_req_allies = [10,21,22,35]
subactions_req_objects = [4,5,7,13,15,25,26,29,30,31,32,33,34]

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