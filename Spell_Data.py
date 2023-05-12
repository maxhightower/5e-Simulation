import pandas as pd
import math

Spells = pd.read_excel(r'C:\Users\maxhi\OneDrive\Desktop\TTRPGs\Python 5e Project Data (1).xlsx',sheet_name='Spells')
#print(Spells)

# Class Spell Lists

Artificer_Spell_List = Spells.loc[Spells.Artificer == "Artificer"]
Bard_Spell_List = Spells.loc[Spells.Bard == "Bard"]
Cleric_Spell_List = Spells.loc[Spells.Cleric == "Cleric"]
Druid_Spell_List = Spells.loc[Spells.Druid == "Druid"]
Paladin_Spell_List = Spells.loc[Spells.Paladin == "Paladin"]
Ranger_Spell_List = Spells.loc[Spells.Ranger == "Ranger"]
Sorcerer_Spell_List = Spells.loc[Spells.Sorcerer == "Sorcerer"]
Warlock_Spell_List = Spells.loc[Spells.Warlock == "Warlock"]
Wizard_Spell_List = Spells.loc[Spells.Wizard == "Wizard"]


# I can make things much easier on myself if I limit the spells I'm using to those that only deal damage

#First_Level_Spells = Spells.query("Level == 1")
#First_Level_Damage_Spells = First_Level_Spells.query("Damage_Heal_Effect == 'Damage'")
#print(First_Level_Damage_Spells)









# Area of Effect Spells
## Location is the Point of Origin
## What happens if the Point of Origin is a Creature???

def AOE_Spaces_Cylinder(Radius,Height):
    # A cylinder's point of origin is the center of a circle of a particular radius, as given in the spell description. The circle must either be on the ground or at the height of the spell effect. 
    # The energy in a cylinder expands in straight lines from the point of origin to the perimeter of the circle, forming the base of the cylinder. 
    # The spell's effect then shoots up from the base or down from the top, to a distance equal to the height of the cylinder.
    # A cylinder's point of origin is included in the cylinder's area of effect.
    One_Floor_Num_of_Spaces = Radius/5
    Total_Num_of_Spaces = One_Floor_Num_of_Spaces * (Height/5)
    return Total_Num_of_Spaces

def AOE_Spaces_Radius_Sphere(Radius):
    # You select a sphere's point of origin, and the sphere extends outward from that point. The sphere's size is expressed as a radius in feet that extends from the point.
    # A sphere's point of origin is included in the sphere's area of effect.
    Floor_Num_of_Spaces = Radius/5
    Total_Num_of_Spaces = Floor_Num_of_Spaces * (Radius/5)
    return Total_Num_of_Spaces

def AOE_Spaces_Cube(Radius):
    # You select a cube's point of origin, which lies anywhere on a face of the cubic effect. The cube's size is expressed as the length of each side.
    # A cube's point of origin is not included in the cube's area of effect, unless you decide otherwise.
    Floor_Num_of_Spaces = Radius/5
    Total_Num_of_Spaces = Floor_Num_of_Spaces * (Radius/5)
    return Total_Num_of_Spaces

def AOE_Spaces_Line(Length,Width):
    # A line extends from its point of origin in a straight path up to its length and covers an area defined by its width.
    # A line's point of origin is not included in the line's area of effect, unless you decide otherwise.
    Total_Num_of_Spaces = (Length/5) * (Width/5)
    return Total_Num_of_Spaces

def AOE_Spaces_Cone(Length):
    # A cone extends in a direction you choose from its point of origin. A cone's width at a given point along its length is equal to that point's distance from the point of origin. A cone's area of effect specifies its maximum length.
    # A cone's point of origin is not included in the cone's area of effect, unless you decide otherwise.
    Angle = 53.13
    Radius = Length * math.tan(Angle/2)
    #Num_of_Floors = (Radius*2)/5
    #First_Floor_Spaces = (Length * Radius)/5
    # Wait...if a circle is just a square, then a cone is just a pyramid...
    # and I can use the formula to find the area of that
    Total_Num_of_Spaces = ((int(Radius)*int(Radius))+int(Radius)*math.sqrt(((Radius/2)*(Radius/2))+(Length*Length)) + int(Radius)*math.sqrt(((Radius/2)*(Radius/2))+(Length*Length)))/5
    
    return Total_Num_of_Spaces


#print(AOE_Spaces_Cube(15))



######## Choosing the Best Spell for the Situation
## Application of Game Theory and Examination of Action Economy