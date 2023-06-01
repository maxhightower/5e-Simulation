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

# Joey said to look into pygame
import pygame


 

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
print(len(Planes))


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
                print(space_name.Coordinates)

Generate_World(3,3,3)
