import numpy as np
import pandas as pd
import random
from random import randrange
import requests
import json
import sys
import time
import math
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

# I'm going to need to be able to store different environment information
# currently the environment is being represented by an array with an integer value per space
# I can instead use lists of ints to represent different environment conditions

# Cellular Automata???

class world:
    def __init__(self,Size):
        self.Size = Size
        self.Fig = None
        self.Grid = None
        self.Coin_Locations = []

    def Generate_Map(world):
        # generate a grid with the dimensions of world.Size
        grid = np.zeros([world.Size,world.Size])
        
        fig = plt.figure(figsize = [5,5])
        plt.xlim(0,world.Size)
        plt.ylim(0,world.Size)

        world.Grid = grid
        world.Fig = fig


    def Generate_Coins(world,number_of_coins):

        for coin in range(0,number_of_coins):
            coin_location_x = randrange(0,world.Size)
            coin_location_y = randrange(0,world.Size)

            coin_location = [coin_location_x,coin_location_y]
            world.Coin_Locations.append(coin_location)

        fig = world.Fig

        for coins in range(len(world.Coin_Locations)):
            world.Grid[world.Coin_Locations[coins][0],world.Coin_Locations[coins][1]] = 1
        
        plt.imshow(world.Grid, cmap='viridis', interpolation='nearest')
        plt.show()


environment_list_index_key = {
    0: "matter occupation", # 0 = empty, 1 = filled
    1: "matter type",       # 0 = air, 1 = water, 2 = fire, 3 = earth, 4 = plants, 5 = ice
    2: "on ground",         # 0 = no, 1 = yes
    3: "entity occupation", # 0 = unoccupied, 1 = occupied
    4: "terrain",           # 0 = normal, 1 = difficult, 2 = unpassable
    5: "light level",       # 0 = bright, 1 = dim, 2 = dark, 3 = magical darkness
    7: "obscurement",       # 0 = none, 1 = light, 2 = heavy
    8: "sound level",       # 0 = quiet, 1 = normal, 2 = loud
    9: "odor",              # 0 = none, 1 = light, 2 = heavy
    10: "piousness",         # 0 = normal, 1 = consecrated, 2 = desecrated
    11: "illusion",          # 0 = no, 1 = yes
    12: "wind",              # 0 = none, 1 = light, 2 = strong
    13: "temperature",       # 0 = extreme cold, 1 = normal, 2 = extreme heat
    14: "biome",             # 0 = none, 1 = arctic, 2 = coastal, 3 = desert, 4 = forest, 5 = grassland, 6 = hill, 7 = mountain, 8 = swamp, 9 = underdark, 10 = underwater, 11 = urban
    

    # on_fire boolean???
    # slippery
    # damaging terrain (spikes, lava)
    # pressure (air pressure, water pressure)
    # weather

    ####### redesign requirements:
    # need a way to have multiple entities within the same space
    # need a way to have multiple objects in the same space

}

# I'm going to need to make a fucking light tracing simulator for when fire is present it illuminates the areas
def Light_Rendering(world):
    locations = world.Grid
    rows, cols = locations.shape

    for location in locations:

        if location[1][2] == 2: # if there's fire in the space, change light level to bright
            location[6] = 0

def Sound_Rendering(world):
    pass

def Smell_Rendering(world):
    pass






 

# I need to go over the perception rules from 5e:
# Visibility, Perception, Distance, Sound...
    # "Characters can see up to 2 miles..."
    # "Rain cuts visibility down to 1 mile..."
    # "Fog cuts visibility down to 200ft..."
    # "Creatures can be more likely to hear one another before they see anything. If neither side is being stealthy, creatures automatically notice each other once they are within sight or hearing range of one another."
    # "When a character is trying to be quiet, they can typically only be heard 2d6 x 5ft (35ft) away, when they're at a normal noise level it's 2d6 x 10ft (70ft), and being really loud is 2d6 x 50ft (350ft)."

Noise_Level = {'Level': ['Quiet','Normal','Loud'],
               'Radius': [35,70,350]}       # may need to convert this into 7,16,70 if we go by spaces instead of ft

Temperatures = ['Extreme Cold','Normal','Extreme Heat']
Winds = ['None','Light','Strong']
Precipitations = ['None','Light','Heavy']
Condensations = ['None','Mist','Heavy Fog']

# Blizzard

# Sandstorm

# 

# Weather consists of Temperature, Wind, and Precipitation plus...
# Extreme_Cold
# Extreme_Heat
# Strong_Wind
    # Sandstorm in Desert
# Heavy Precipitation
    # Lightly Obscured
# High_Altitude (10,000ft or higher so 2,000 spaces)



Weather_List = []
Visibility_Conditions = []
Environments_List = ['Arctic','Coastal','Desert','Forest','Grassland','Hill','Mountain','Swamp','Underdark','Underwater','Urban']


Planes = ['Material Plane','Ethereal Plane','Astral Plane','Feywild','Shadowfell','Avernus','Celestia',
          'Plane of Fire','Plane of Water','Plane of Air','Plane of Earth','Abyss','Beastlands','Limbo','Mechanus','Demiplane']
#print(len(Planes))


Environment = (range(0, 12),range(0, 12),range(-12, 12))
Environment[0][1]


# Coordinates
x = 2
y = 4
# Plotting
#plt.plot(x,y,'bo')
# Displaying grid
#plt.grid()
# Controlling axis
#plt.axis([-15, 15, -15, 15])
# Adding title
#plt.title('Single Point Plot')
# Displaying plot
#plt.show()


# Coordinates
x = [2, -4, 6, -8]
y = [4, 3, -8, 10]
# Plotting
#plt.plot(x,y,'bo')
# Displaying grid
#plt.grid()
# Controlling axis
#plt.axis([-15, 15, -15, 15])
# Adding title
#plt.title('Multiple Point Plot')
# Displaying plot
#plt.show()











#plt.plot(x,y,z,)
#fig = plt.figure()
#ax = plt.axes(projection='3d')
#plt.show()

#two doubles
#x coord
#y coord
#all movement is adjusting those variables by specific amounts
#position as a three tuple
#define movement or movement related actions as a three tuple
#movmenet would be defined as a three tuple that gets added to
#function that checks if the movemetn you propose is valid
#and if it is, add x,y,z 
#every space in the 3D environment is either empty or occupied 
#World or Encounter object for a game space where there would be functions that look at all creatures, size, and positions and defines a 3D vector space where every point is defined as occupied or unoccupied and dump that into a set and then you can do lookups into that set for if movement is valid
#you'll have a banishment mechanic where the caster gets banished and the new creature with the condition polymorphed which brings back the banished creature


# Each square needs the following disctinctions:
#  - Light Level: Bright, Dim, Dark
#  - Matter Level: Filled, Occupied, Unoccupied, Air, Water, Fire
#    Matter Type: 
#  - Obscurement: Light, Heavy
#  - Terrain: Normal, Difficult

Floor_Type = ['Grass','Stone','Gravel','Sand','Wood','Snow','Ice','']

Light_List = ['Bright','Dim','Dark']
Matter_Level_List = ['Filled','Occupied','Unoccupied','Air','Water','Ice','Fire']
Obscurement_List = ['None','Light','Heavy']
Terrain_List = ['Normal','Difficult','Unpassable']

class Space:
    def __init__(self,Coordinates,Light,Sound,Fill_Type,Substance,Obscurement,Terrain,Piousness,Manueverability):
        self.Coordinates = Coordinates # [x,y,z,d]
        self.Light = Light             # Bright, Dim, Dark
        self.Sound = Sound             # Quiet, Normal, Loud
        self.Fill_Type = Fill_Type     # Filled, Occupied, Unoccupied
        self.Substance = Substance     # Fire, Water, Earth, Plants, etc
        self.Obscurement = Obscurement # None, Light, Heavy
        self.Terrain = Terrain         # Normal, Difficult, Unpassable
        self.Piousness = Piousness     # Normal, Consecrated, Desecrated
        self.Manueverability = Manueverability  # Normal, Slippery, Check/Save Required



        # Frigid Water has rules
        # Slippery Ice
        # Thin Ice
        # Webs

def Generate_World(x,y,z):
    for i in range(0,x,1):
        for j in range(0,y,1):    
            for k in range(0,z,1):
                global space_name
                space_name = (str(i),'.',str(j),'.',str(k))
                space_name = Space([i,j,k],'Bright','Quiet','Unoccupied','Air','None','Normal','Normal','Normal')
                #print(space_name.Coordinates)

#Generate_World(3,3,3)
