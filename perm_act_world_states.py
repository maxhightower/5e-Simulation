import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np


world_grid_states = {
    0: 'is_occupied',
    1: 'is_ground',
    2: 'terrain',   # 0 = normal, 1 = difficult, 2 = unpassable
    3: 'light',     # 0 = bright, 1 = dim, 2 = dark, 3 = magical darkness
    4: 'obscure',   # 0 = none, 1 = light, 2 = heavy
    5: 'entities',
    6: 'objects',
}


class world:
    def __init__(self,size):
        self.size = size
        self.fig = None
        self.grid = None
        self.coin_locations = []
        self.enemy_locations = []
        
    def generate_map(world):
        grid = np.zeros([world.size,world.size])
    
        grid2 = []
        for x in range(world.size):
            grid2.append([])
            for y in range(world.size):
                grid2[x].append([0,0,0,0,0,[],[]])                    
                grid2[x][y][1] = 1                     

        fig = plt.figure(figsize = [5,5])
        plt.xlim(0,world.size)
        plt.ylim(0,world.size)

        world.grid = grid
        world.grid2 = grid2
        world.fig = fig


    def add_enemy(world,location):
        # add an enemy to the grid at the specified location
        world.grid[location[0],location[1]] = 2
        world.enemy_locations.append(location)

    def add_coin(world,location):
        world.grid[location[0],location[1]] = 1
        world.coin_locations.append(location)