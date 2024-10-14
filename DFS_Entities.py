# DFS_Entities
import numpy as np
from DFS_Universal_Rules import subaction_dict, size_options, size_space_orientation



subaction_dict_monster = {}
move_cost_dict_mosnter = {}


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
    def __init__(self,type, world, size, *args):
        self.type = type                # player character, monster, npc
        self.world = world
        self.location = None           # need to change this to a list so that it can handle large+ entity sizes
        

        # kwargs[0] represents the template for if they are a monster
        if self.type == 'monster':
            self.template = args[0]
            self.subaction_dict = subaction_dict_monster
            self.move_cost_dict = move_cost_dict_mosnter

            orientation = args[1]
            size_layouts = size_space_orientation[size]
            if len(size_layouts) > 1:
                spaces_orientation = orientation
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
        self.size = 'medium'
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





    def add_subaction(self, subaction):
        self.subactions.append(subaction)
        # this will need more work later...

    def add_spell(self, spell):
        self.spells.append(spell)


    def create_entity(self, type):
        if type == 'player character':
            pass

        elif type == 'monster':
            pass




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

