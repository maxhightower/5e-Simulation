#import Establishing_Hierarchy
from random import randrange
import Dice_Rolls

Simple_Weapons = ['Club','Dagger','Greatclub','Handaxe','Javelin','Light Hammer','Mace','Quarterstaff','Sickle','Spear']
Martial_Weapons = ['Battleaxe','Flail','Glaive','Greataxe','Greatsword','Halberd','Lance','Longsword','Maul','Morningstar','Pike','Rapier','Scimitar','Shortsword','Trident','War Pick','Warhammer','Whip','Hand Crossbow','Heavy Crossbow','Longbow']
Martial_Melee_Weapons = ['Battleaxe','Flail','Glaive','Greataxe','Greatsword','Halberd','Lance','Longsword','Maul','Morningstar','Pike','Rapier','Scimitar','Shortsword','Trident','War Pick','Warhammer','Whip']

class Armor:
  def __init__(self,Type,Base_AC,Add_Dex,Dex_Limit,AC_Bonus,Magical_Bonus):
    self.Type = Type    # Heavy, Medium, Light, Shield
    self.Base_AC = Base_AC
    self.Add_Dex = Add_Dex
    self.Dex_Limit = Dex_Limit
    self.AC_Bonus = AC_Bonus        # This one is for shield
    self.Magical_Bonus = Magical_Bonus  # This one is for +1,+2,+3 armors

Unarmored = Armor('None',10, True, False,False,False)
Padded = Armor('Light',11,True,False,False,False)
Leather = Armor('Light',11,True,False,False,False)
Studded_Leather = Armor('Light',12,True,False,False,False)
Hide_Armor = Armor('Medium',12,True,2,False,False)
Chain_Shirt = Armor('Medium',13,True,True,False,False)
Scale_Mail = Armor('Medium',14,True,True,False,False)
Breastplate = Armor('Medium',14,True,True,False,False)
Half_Plate = Armor('Medium',15,True,True,False,False)
Ring_Mail = Armor('Heavy',14,False,False,False,False)
Chain_Mail = Armor('Heavy',16,False,False,False,False)
Splint = Armor('Heavy',17,False,False,False,False)
Plate = Armor('Heavy',18,False,False,False,False)
Shield = Armor('Shield',False,False,False,2,False)

Donning_Doffing_Armor = {
  'Light Armor': ['1_Minute','1_Minute'],
  'Medium Armor': ['5_Minutes','1_Minute'],
  'Heavy Armor': ['10_Minutes','5_Minutes'],
  'Shield': ['1_Action','1_Action']}


def Don_Armor(Armor,Player_Character):
  Player_Character.Armor_Equipped.append(Armor)

def Doff_Armor(Armor,Player_Character):
  Player_Character.Armor_Equipped


def Calc_Average_Damage(Dice_Type,Dice_Num):
  return Dice_Rolls.Average_Roll(Dice_Num,Dice_Type,0,0)

class Weapon:
  def __init__(self,Name,Type,Category,Dice_Type,Dice_Num,Damage_Type,Heavy,Light,Two_Handed,Versatile,Versatile_Dice,Finesse,Thrown,Range,Reload,Ammunition):
    self.Name = Name
    self.Type = Type            # Simple or Martial
    self.Category = Category    # Melee or Ranged
    self.Dice_Type = Dice_Type
    self.Dice_Num = Dice_Num
    self.Damage_Type = Damage_Type
    self.Reach = 5
    self.Heavy = Heavy
    self.Light = Light
    self.Two_Handed = Two_Handed
    self.Versatile = Versatile
    self.Versatile_Dice = Versatile_Dice
    self.Finesse = Finesse
    self.Thrown = Thrown
    self.Range = Range
    self.Reload = Reload
    self.Ammunition = Ammunition
    self.Special = False

    self.Average_Damage = Calc_Average_Damage(Dice_Type,Dice_Num)

    # place holder for if I create a script that checks str,dex,int, or cha based on weapon or based on character


def Roll_Weapon_Damage(Weapon):
  x = randrange(Weapon.Dice_Num,Weapon.Dice_Num * Weapon.Dmg_Dice) #statistically this makes 2d6 and 1d12 the same when they're not but I'll change that later
  return x


# Starter Weapons

Club = Weapon('Club',"Simple","Martial",4,1,"Bludgeoning",False,True,False,False,False,False,False,False,False,False)
Dagger = Weapon('Dagger',"Simple","Martial",4,1,"Piercing",False,True,False,False,False,True,True,'20/60',False,False)
Greatclub = Weapon('Greatclub',"Simple","Martial",8,1,"Bludgeoning",5,False,False,True,False,False,False,False,False,False)
Handaxe = Weapon('Handaxe',"Simple","Martial",6,1,"Slashing",False,True,False,False,False,False,True,'20/60',False,False)
Javelin = Weapon('Javelin',"Simple","Martial",6,1,"Piercing",False,False,False,False,False,False,True,'30/120',False,False)
Light_Hammer = Weapon('Light_Hammer',"Simple","Martial",4,1,"Bludgeoning",False,True,False,False,False,False,True,'20/60',False,False)
Mace = Weapon('Mace',"Simple","Martial",6,1,"Bludgeoning",False,False,False,False,False,False,False,False,False,False)
Quarter_Staff = Weapon('Quarter_Staff',"Simple","Martial",6,1,"Bludgeoning",False,False,False,True,10,False,False,False,False,False)
Sickle = Weapon('Sickle',"Simple","Martial",4,1,"Slashing",False,True,False,False,False,False,False,False,False,False)
Spear = Weapon('Spear',"Simple","Martial",6,1,"Piercing",False,False,False,True,8,True,True,'20/60',False,False)
Light_Crossbow = Weapon('Light_Crossbow',"Simple","Ranged",8,1,"Piercing",False,False,False,False,False,False,False,'80/320',False,True)
Dart = Weapon('Dart',"Simple","Martial",4,1,"Piercing",False,False,False,False,False,True,True,'20/60',False,False)
Shortbow = Weapon('Shortbow',"Simple","Ranged",6,1,"Piercing",False,False,True,False,False,False,False,'80/320',False,False)
Sling = Weapon('Sling',"Simple","Ranged",4,1,"Bludgeoning",False,False,False,False,False,False,False,'30/120',False,True)
Battleaxe = Weapon('Battleaxe',"Martial","Martial",8,1,"Slashing",False,False,False,True,10,False,False,False,False,False)
Flail = Weapon('Flail',"Martial","Martial",8,1,"Bludgeoning",False,False,False,False,False,False,False,False,False,False)
#Glaive = Weapon("Martial","Martial",10,1,"Slashing",10,True,False,True,False,False,False,False,False,False,False,False,True)
Greataxe = Weapon('Greataxe',"Martial","Martial",12,1,"Slashing",True,False,True,False,False,False,False,False,False,False)
Greatsword = Weapon('Greatsword',"Martial","Martial",6,2,"Slashing",True,False,True,False,False,False,False,False,False,False)
#Halberd = Weapon("Martial","Martial",10,1,"Slashing",10,True,False,True,False,False,False,False,False,False,False,False,True)
#Lance = Weapon("Martial","Martial",12,1,"Piercing",10,False,False,False,False,False,False,False,False,False,False,True,True)
Longsword = Weapon('Longsword',"Martial","Martial",8,1,"Slashing",False,False,False,True,10,True,False,False,False,False)
Maul = Weapon('Maul',"Martial","Martial",2,6,"Bludgeoning",True,False,True,False,False,False,False,False,False,False)
Morningstar = Weapon('Morningstar',"Martial","Martial",8,1,"Piercing",False,False,False,False,False,False,False,False,False,False)
#Pike = Weapon("Martial","Martial",10,1,"Piercing",10,True,False,True,False,False,False,False,False,False,False,False,True)
Rapier = Weapon('Rapier',"Martial","Martial",8,1,"Piercing",False,False,False,False,False,True,False,False,False,False)
Scimitar = Weapon('Scimitar',"Martial","Martial",6,1,"Slashing",False,True,False,False,False,True,False,False,False,False)
Shortsword = Weapon('Shortsword',"Martial","Martial",6,1,"Piercing",False,True,False,False,False,True,False,False,False,False)
Trident = Weapon('Trident',"Martial","Martial",6,1,"Piercing",False,False,False,True,8,False,True,'20/60',False,False)
War_Pick = Weapon('War_Pick',"Martial","Martial",8,1,"Piercing",False,False,False,False,False,False,False,False,False,False)
Warhammer = Weapon('Warhammer',"Martial","Martial",8,1,"Bludgeoning",False,False,False,True,10,True,False,False,False,False)
#Whip = Weapon("Martial","Martial",4,1,"Slashing",10,False,False,False,False,False,True,False,False,False,False,False,True)
Blowgun = Weapon('Blowgun',"Martial","Ranged",1,1,"Piercing",False,False,False,False,False,False,False,'25/100',False,True)
Hand_Crossbow = Weapon('Hand_Crossbow',"Martial","Ranged",6,1,"Piercing",5,False,True,False,False,False,False,False,'30/120',False)
Heavy_Crossbow = Weapon('Heavy_Crossbow',"Martial","Ranged",10,1,"Piercing",5,True,False,True,False,False,False,False,'100/400',False)
Longbow = Weapon('Longbow',"Martial","Ranged",8,1,"Piercing",5,False,False,True,False,False,False,False,'150/600',False)
#Net = Weapon("Martial","Martial",0,1,False,5,False,False,False,False,False,False,True,'5/15',False,False,True,True)

Spiked_Club = Weapon('Spiked_Club',"Simple","Martial",8,1,"Bludgeoning",False,True,False,True,10,False,False,False,False,False)


def Equip_Weapon(Creature,Weapon):
  Creature,




def Suit_Up(Player_Character):      # I want this function to say, okay here's what armor the player character currently has
                                    # Let's check what's in the player character's inventory under armor, 
                                    # compare that with the armor proficiencies the character has
                                    # and if there's an armor that provides a better benefit, put it on
  Player_Character.Inventory

  Player_Character.Armor_Equipped
  Player_Character.Armor_Profs
  
  Player_Character.Weapons_Equipped
  Player_Character.Weapon_Profs



