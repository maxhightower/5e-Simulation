import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from collections import defaultdict
#import networkx as nx
from DFS_Functions import adjacent_locations, chebyshev_distance, bresenham_line, calculate_full_path, check_opportunity_attacks, is_line_of_sight_clear, check_visibility

from DFS_Entities import entity
from DFS_Universal_Rules import size_options, size_space_orientation


world_grid_states = {
    0: 'is_occupied',
    1: 'is_ground',
    2: 'terrain',   # 0 = normal, 1 = difficult, 2 = unpassable
    3: 'light',     # 0 = bright, 1 = dim, 2 = dark, 3 = magical darkness
    4: 'obscure',   # 0 = none, 1 = light, 2 = heavy
    5: 'entities',
    6: 'objects',
}

class enemy:
    def __init__(self,world):
        self.world = world
        self.is_spawned = False

        self.caster = False
        self.concentrating = False

        self.attack_limit = 1

        self.hp = 2
        self.ac = 10
        self.conditions = []

        self.reaction_used = False

        if self.is_spawned == False:
            self.location = [0,0]
            
        elif self.is_spawned == True:
            x_loc = world.grid[np.where(world.grid[:,0] == max(world.grid))]
            print('x: ',x_loc)
            y_loc = world.grid[np.where(world.grid[0,:] == max(world.grid))]
            print('y: ',y_loc)
            self.location = [x_loc,y_loc]



# This class represents a directed graph using
# adjacency list representation
class graph:

    # Constructor
    def __init__(self):

        # Default dictionary to store graph
        self.graph = defaultdict(list)
#        self.grid_vis = nx.Graph()
     
    def add_edge(self, u, v):
        self.graph[u].append(v)
#        self.grid_vis.add_edge(u, v)  # Add edge to the NetworkX graph as well




    # A function used by DFS
    def dfs_util(self, v, visited):
 
        # Mark the current node as visited and print it
        visited.add(v)
        print(v, end=' ')
 
        # Recur for all the vertices adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.dfs_util(neighbour, visited)


    # The function to do DFS traversal. It uses recursive DFSUtil()
    def dfs(self, v):
 
        # Create a set to store visited vertices
        visited = set()
 
        # Call the recursive helper function to print DFS traversal
        self.dfs_util(v, visited)

class Object:
    def __init__(self, name, type, flammable, casting_focus):
        self.name = name
        self.type = type
        self.flammable = flammable
        self.casting_focus = casting_focus

# create subclass Coin that inherits from Object
class Coin(Object):
    def __init__(self, name, type):
        super().__init__(name, type, flammable=False, casting_focus=False)
        self.type = 'treasure'

class Weapon(Object):
    def __init__(self, name, type, damage, weight, hands):
        super().__init__(name, type, flammable=False, casting_focus=False)
        self.type = 'weapon'
        self.damage = damage
        self.weight = weight
        self.hands = 0 # 0 is one-handed, 1 is two-handed, and 2 is versatile

class Shield(Object):
    def __init__(self, name, type, hands):
        super().__init__(name, type, flammable=False, casting_focus=False)
        self.type = 'shield'
        self.hands = 0

class Potion(Object):
    def __init__(self, name, type, hands):
        super().__init__(name, type, flammable=False, casting_focus=False)
        self.type = 'potion'
        self.hands = 0

class Wand(Object):
    def __init__(self, name, type, hands):
        super().__init__(name, type, flammable=False, casting_focus=True)
        self.name = 'wand'
        self.type = 'other'
        self.hands = 0



class world:
    def __init__(self,size):
        self.size = size
        self.fig = None
        self.grid = None

        self.grid_graph = graph()

        self.coin_locations = []
        self.enemy_locations = []
        self.enemies = []
        self.enemy_adjacent_locations = []
        self.non_enemies = []
        self.objects = []

        self.entity_locations = []
        self.entities = []
        # I'll be using the index of world.objects to represent objects within object_series 
        
    def generate_map(world):
        grid = np.zeros([world.size,world.size])
    
        grid2 = []
        for x in range(world.size):
            grid2.append([])
            for y in range(world.size):
                grid2[x].append([0,0,0,0,0,[],[]])                    
                grid2[x][y][1] = 1                     

        #fig = plt.figure(figsize = [5,5])
        #plt.xlim(0,world.size)
        #plt.ylim(0,world.size)

        world.grid = grid
        world.grid2 = grid2
        #world.fig = fig

        # now to generate grid_graph for depth first search
        for i in range(world.size):
            for j in range(world.size):
                current = i * world.size + j
                # Add edge to right neighbor
                if j < world.size - 1:
                    world.grid_graph.add_edge(current, current + 1)
                # Add edge to bottom neighbor
                if i < world.size - 1:
                    world.grid_graph.add_edge(current, current + world.size)



    def add_enemy(world,location):
        # add an enemy to the grid at the specified location
        enemy_count = len(world.enemy_locations)
        enemy_id = f'enemy_{enemy_count+1}'
        enemy_id = enemy(world)
        enemy_id.location = location


        world.grid[location[0],location[1]] = 2
        world.grid2[location[0]][location[1]][5].append(enemy_id)
        world.enemy_locations.append(location)
        world.enemies.append(enemy_id)
        world.enemy_adjacent_locations.append(adjacent_locations(enemy_id.location))

    
    def add_entity(self,set_location,name):
        # the way that adding an entity to the program will work is as follows:
        #   actor = entity('player character',stage,'medium')
        #   stage.add_entity([0,0],actor)
        # so first the entity is created, then it is added to the stage

        #print('add entity')
        #print(f'name: {name}')
        #print(f'location: {name.location}')
        #print(f'set location: {set_location}')

        set_location = [set_location[0]-5,set_location[1]-5]

        sizes = [1,2,3,4,5]

        if name.type == 'player character':
            size = 'medium'
            #name = entity(type,self,size)
            
            name.location = [set_location]
            #print('add entity')
            #print(f'new location: {name.location}')
            # this will be where character creation is handled



            # place character in world
            self.grid[set_location[0],set_location[1]] = 2
            self.grid2[set_location[0]][set_location[1]][5].append(name)
            self.entity_locations.append(set_location)

        elif name.type == 'monster':
            #name = entity(type,self,size)

            # we assume the location given is the top left of the monster
            # given the size_options and size_space_orientation, we can determine the full space occupied by the monster
            spaces_orientation = name.orientation


            size_layouts = size_space_orientation[size_options[size_options.index(name.size)]]


            # I'm going to be ignoring size_layouts for now and simply using squares
            if name.size in ['tiny','small','medium']:
                temp_length = 1
                temp_height = 1
            elif name.size in ['large']:
                temp_length = 2
                temp_height = 2
            elif name.size in ['huge']:
                temp_length = 3
                temp_height = 3
            elif name.size in ['gargantuan']:
                temp_length = 4
                temp_height = 4
            elif name.size in ['colossal']:
                temp_length = 5
                temp_height = 5
            

            #if len(size_layouts) > 1:
            #    print(orientation)
            #    spaces_orientation = size_layouts[orientation]
            #else:
            #    print(orientation)
            #    spaces_orientation = size_layouts[0]
            
            # use string manipulation to identify the length and heigth by splitting by 'x'
            name.length = int(spaces_orientation.split('x')[0])
            name.height = int(spaces_orientation.split('x')[1])

            name.locations_occupying = []

            for i in range(name.length): 
                for j in range(name.height):
                    name.locations_occupying.append([set_location[0]+i,set_location[1]+j])
                    name.location = [set_location[0],set_location[1]]
                
            for loc in name.locations_occupying:
                self.grid[loc[0],loc[1]] = 2
                self.grid2[loc[0]][loc[1]][5].append(name)
                self.entity_locations.append(loc)

        # will need a check to see if the location is already occupied by another entity
        # if so, it will be shunted to the nearest open space
        # and a message will be printed about the new location

        self.entities.append(name)

            

        #print(name.location)











    def add_coin(world,location):
        # create instance of Coin class
        coin = Coin(name='coin', type='treasure')

        world.grid[location[0],location[1]] = 1
        world.grid2[location[0]][location[1]][6].append(coin)
        world.coin_locations.append(location)
        world.objects.append(coin)

    def add_weapon_dagger(world,location):
        dagger = Weapon(name='dagger', type='weapon', damage=1, weight=1, hands=0)

        world.grid[location[0],location[1]] = 1
        world.grid2[location[0]][location[1]][6].append(dagger)
        world.objects.append(dagger)

    def add_weapon_greataxe(world,location):
        greataxe = Weapon(name='greataxe', type='weapon', damage=2, weight=2, hands=1)

        world.grid[location[0],location[1]] = 1
        world.grid2[location[0]][location[1]][6].append(greataxe)
        world.objects.append(greataxe)

    def add_shield(world,location):
        shield = Shield(name='shield', type='shield')
        
        world.grid[location[0],location[1]] = 1
        world.grid2[location[0]][location[1]][6].append(shield)
        world.objects.append(shield)

    def add_item_to_inventory(world,entity,item):
        entity.inventory.append(item)
        world.objects.append(item)



    def show_map(world):
        # first I'll need to create a new list of lists to store just the entity data
        # the map goes from -5 to 5 so the world.size is 11

        # now plot
        plt.figure(figsize = [10,10])
        plt.imshow(world.grid, cmap='viridis', interpolation='nearest') 
        # show all x and y ticks
        # subtract 5 from the x and y ticks to get the correct location

        plt.xticks(np.arange(0,world.size,1),np.arange(-5,6,1))
        plt.yticks(np.arange(0,world.size,1),np.arange(-5,6,1))

        # add a grid
        plt.grid(color='black',linewidth=0.5,alpha=0.5)

        plt.gca().invert_yaxis()

        # add a text label for each cell where if the cell is occupied, it will display the entity name
        for i in range(world.size):
            for j in range(world.size):
                if len(world.grid2[i][j][5]) > 0:
                    plt.text(j,i,world.grid2[i][j][5][0].name,ha='center',va='center',color='black')
                elif len(world.grid2[i][j][6]) > 0:
                    plt.text(j,i,world.grid2[i][j][6][0].name,ha='center',va='center',color='black')                    

        # need to add a check for if monsters of bigger sizes to combine the text
        # need to add a check for if multiple entities are in the same cell
        # need to add a check for if multiple objects are in the same cell
        # need to add a check for if an entity and an object are in the same cell

        plt.show()

        # I'll do on using 3d voxels later...




#    def visualize(self, dfs_path=None):
#        pos = {i: (i % self.size, self.size - 1 - i // self.size) for i in range(self.size * self.size)}
#        plt.figure(figsize=(10, 10))
#        
        # Calculate the offset to center the coordinates
#        offset = (self.size - 1) // 2
        
        # Create a mapping of node indices to centered (x,y) coordinates
#        pos = {i: ((i % self.size) - offset, offset - (i // self.size)) for i in range(self.size * self.size)}


#        nx.draw(self.grid_graph.grid_vis, pos, with_labels=False, node_shape='s',node_color='lightgrey', node_size=4500, font_size=8, font_weight='bold')
        

        
        # Draw node labels (centered coordinates)
#        labels = {node: f"({x},{y})" for node, (x, y) in pos.items()}
#        nx.draw_networkx_labels(self.grid_graph.grid_vis, pos, labels, font_size=8)
        
#        if dfs_path:
#            path_edges = list(zip(dfs_path, dfs_path[1:]))
#            nx.draw_networkx_edges(self.grid_graph.grid_vis, pos, edgelist=path_edges, edge_color='r', width=2)
        
#        plt.axis('off')
#        plt.tight_layout()
#        plt.show()



# how to handle random combat scenario generation...
# perhaps I can limit it to pre-established 5e encounters?
# phandelver, dragon of icespire peak, etc.

# or I could completely randomize it...