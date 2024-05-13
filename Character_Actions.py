import Dice_Rolls
import Establishing_Hierarchy
import Character_Functions
#import Effects
import operator
import random
import Armor_and_Weapons

# let's split the different options for builds for each class
# Artificer
  # Caster: Studded Leather, Ranged Simple Weapon, Melee Simple Weapon, Thieves Tools, Dungoneers Pack
  # Frontliner: Scale Mail, two Melee Simple Weapons, Thieves Tools, Dungoneers Pack

# Barbarian
# (a) a greataxe or (b) any martial melee weapon
# (a) two handaxes or (b) any simple weapon
# An explorer's pack, and four javelins
  # Classic: Greataxe, 2 Handaxes, Explorer's Pack, 4 Javelins
  # Polearm: Glaive, 2 Handaxes, Explorer's Pack, 4 Javelins

# Bard
#(a) a rapier, (b) a longsword, or (c) any simple weapon
#(a) a diplomat's pack or (b) an entertainer's pack
#(a) a lute or (b) any other musical instrument
#Leather armor, and a dagger
  # Caster:  Rapier, Lute, Entertainer's Pack, Leather Armor, Dagger
  # Frontliner: Longsword, Lute, Entertainer's Pack, Leather Armor, Dagger

# Cleric
#(a) a mace or (b) a warhammer (if proficient)
#(a) scale mail, (b) leather armor, or (c) chain mail (if proficient)
#(a) a light crossbow and 20 bolts or (b) any simple weapon
#(a) a priest's pack or (b) an explorer's pack
#A shield and a holy symbol
  # Caster: Mace, Scale Mail, Light Crossbow, Explorer's Pack
  # Frontliner: Warhammer, Chain Mail, Light Crossbow, Explorer's Pack

# Druid




def Choose_Inventory(Player_Character):
  Player_Character.First_Class.Inventory


##### Defining Saving Throws
def Check_Save_Proficiencies(Creature,Save):
  Ability_Score = Character_Functions.Saving_Throws.loc[Save]
  #if Creature.Effects      will handle this when I do the same for ability_checks
  if Save in Creature.Saving_Throws:
    line = str(Creature,'.',Ability_Score)
    Result = Dice_Rolls.Roll + Establishing_Hierarchy.abilityScoreToModifier(exec(line)) + Creature.Saving_Throws
  else:
    line = str(Creature,'.',Ability_Score)
    Result = Dice_Rolls.Roll + Establishing_Hierarchy.abilityScoreToModifier(exec(line))
  return Result


def Choose_Random_Weapon(Actor):
  weapons = Actor.Inventory['Weapons']
  # choose a random weapon from the list of weapons
  weapon_pick = random.choice(weapons)
  return weapon_pick

def Equip_Weapon(Actor,Weapon):
    Actor.Weapon_Equipped.append(Weapon)
    # this costs a action type I'm sure



def Choose_Best_Weapon(Actor):
  try:
    best_weapon = Actor.Inventory['Weapons'][0]
  except:
    best_weapon = Armor_and_Weapons.Dagger
    Actor.Inventory['Weapons'].append(Armor_and_Weapons.Dagger)
  #weapons = Actor.Inventory['Weapons']
  # remove weapons that are not proficient

  #for i in Actor.Inventory['Weapons']:
  #  if Dice_Rolls.Average_Roll(i.Dice_Num,i.Dice_Type) > Dice_Rolls.Average_Roll(best_weapon.Dice_Num,best_weapon.Dice_Type):
  #    # will need 
  #    best_weapon = i 
  return best_weapon
  # returns to change the Weapon Equipped if need be

def Attack_Action(Actor,Combat_Situation):
  Equip_Weapon(Actor,Choose_Best_Weapon(Actor))
  Weapon = Actor.Weapon_Equipped[0]
  Target = Dice_Rolls.Choose_Target_Offense(Actor,Combat_Situation)
  return Enact_Attack(Actor,Target,Weapon,Combat_Situation)

def Enact_Attack(Actor,Target,Weapon,Combat_Situation):
  Attack_Modifier = Establishing_Hierarchy.Attack_Score(Actor) + Actor.Prof_Bonus
  Armor_Class = Target.AC

  if Actor.Circumstances['Attack Rolls'] == 'Advantage':
    Roll = Dice_Rolls.d20_Advantage()

  elif Actor.Circumstances['Attack Rolls'] == 'Disadvantage':
    Roll = Dice_Rolls.d20_Disadvantage()

  else:
    Roll = Dice_Rolls.d20()

  Establishing_Hierarchy.Current_Attack_Roll = Roll + Attack_Modifier


  #for i in Actor.Effects['Self_Attacking']['Rolling'][Weapon.Type]:
    # check if any effects can be added


  x = Dice_Rolls.Roll(Actor,Weapon.Dice_Num,Weapon.Dice_Type) + Establishing_Hierarchy.Attack_Score(Actor)
  y = Attack_Modifier


  if Weapon.Damage_Type == 'Bludgeoning' or Weapon.Damage_Type == 'Piercing' or Weapon.Damage_Type == 'Slashing':
    x = x + Actor.Effects['Self_Dealing_Damage']['Bludgeoning'][0].Bonus
  
  #for i in Actor.Effects['Self_Dealing_Damage'][Weapon.Dmg_Type]:
  #  x = x + Actor.Effects['Self_Dealing_Damage'][Weapon.Dmg_Type][i]
  
  if Establishing_Hierarchy.Current_Attack_Roll > Armor_Class:
    if Roll in Actor.Crit:
      damage = (x * 2) + y
    
      if str(Weapon.Dmg_Type.lower(),'res') in Target.WRI:
        damage = damage/2
      elif str(Weapon.Dmg_Type.lower(),'immue') in Target.WRI:
        damage = 0
      else: pass


    else:
      damage = x + y
      if str(Weapon.Damage_Type.lower()+'res') in Target.WRI:
        damage = damage/2
      elif str(Weapon.Damage_Type.lower()+'immue') in Target.WRI:
        damage = 0
      else: pass

  elif Establishing_Hierarchy.Current_Attack_Roll == Armor_Class:
    damage = (x + y)/2
    if str(Weapon.Damage_Type.lower()+'res') in Target.WRI:
      damage = damage/2
    elif str(Weapon.Damage_Type.lower()+'immue') in Target.WRI:
        damage = 0
    else: pass
  else:
      #print('Miss')
      damage = 0
  
   # it's going to return the information needed to update the combat log
  return 'Action','Attack','Offense',Target, damage





# Actions
# Move
def Move(Creature,Distance,Direction):
  First_Location = Creature.Location
  if Direction == 'x':
    Current_Location = Creature.Location    # (x, y, z)
    New_Location = Current_Location + (Distance,0)
    #elif Direction == 'y':
    #  Current_Location = Creature.Location   # (x, y, z)
    #  New_Location = Current_Location + (0,Distance)
  else:
    Current_Location = Creature.Location    # (x, y, z)
    New_Location = Current_Location + (0,Distance)
  return New_Location


#Hide
def Fastest_Speed(Creature):
  Distance_Travelable = max(Creature.Speed.iteritems(), key=operator.itemgetter(1))[0]      # I don't know if this will return the actual speed or the speed type
  return Distance_Travelable

def Possible_Movement(Creature):
  if Fastest_Speed(Creature) == 'Flying':
    Creature.Location                 # I am going to need to go back and define the location of a player_character later
  elif Fastest_Speed(Creature) == 'Burrowing':
    pass
  elif Fastest_Speed(Creature) == 'Flyhover':
    pass
  else:
    pass

def Check_Cover(Creature,Target,World):
  if 'Dash' in Creature.Bonus_Actions:
    Distance = Fastest_Speed(Creature) * 2
  else:
    Distance = Fastest_Speed(Creature)




  Locations_Available = []
  
  Creature.Speed # check the furthest distance that a creature could get to

def Hide_Action(Creature,Location,World):
  # does the creature have half cover?
  # if not does the creature have an ability that allows him to hide anyway

  # Things to check for:
    # Feats: Skulker, 
    # Effects: 
    # Features: Shadow Stealth, Mask of the Wild, Indescernable Nature?
  # these things are needed to determine what can actually hide the creature



  Dice_Rolls.Ability_Check(Creature,'Stealth','Dexterity')

# Dodge
def Dodge_Action(Creature):
  pass


#Dash
def Dash_Action(Creature):
  # take the number of different speeds 
  # range 1 through length
  # get a random number of that
  # pick a direction
  # double the movement
  # impact the x,y,z coordinates
  Fastest_Speed(Creature)





#Disengage
def Disengage_Action(Creature):
  pass


#Help
#Help_Attack_Buff = Effects.Buff_Circumstance_Effect('Attack Roll','Creature','Instantaneous','Attack Roll','Advantage: ')     # the duration may need to be changed for in combat
#Help_Check_Buff = Effects.Buff_Circumstance_Effect('Ability Check','Creature','Instantaneous','Ability Check','Advantage: ')

#def Help_Action(Creature,Target):   # i forget whether the target was supposed to be the task/attack or the creature being helped
  # help action grants advantage on an attack roll or ability check
#  Effects.Apply_Buff_Circumstance_Effect


#Search
def Search_Action(Creature):
  if 'Blinded' in Creature.Conditions: # since the search action can be taken (technically) with different senses, I'll need to elaborate a lot further than previously expected
    pass
  else:
    Dice_Rolls.Ability_Check(Creature,'Perception','Wisdom')


#Improvise
# I'm not even sure if this is possible? perhaps as an interact with environment option


#Ready an Action
def Ready_Action(Creature,Trigger):
  len(Creature.Actions)
  # randomly choose one of the actions
  # choose a target if needed probably from enemies and allies
  # choose a trigger for the reaction



#Activate an Item
# I need a creature.equipment thing for this...

def Activate_Magic_Item(Creature,Item):
  Creature.Inventory

# Use an Object

# Make an ability check

# Influence Action
Influence_Goals = ['Pacify']
Social_Check_Demeaners = ['Hostile','Neutral','Friendly']
Means_of_Influence = ['Persuasion','Deception','Intimidation','Performance']

def Find_Best_Skill_Prof(Creature,Available_Skills):
  List_of_Bonuses = {
    'Skills': [],
    'Bonuses': []
  }
  for i in Available_Skills:
    Creature.Skill_Profs

  Best_Skill_Bonus = 1
  return Best_Skill_Bonus
  # what about the rule that using an instrument/tool gives advantage on the check if proficient with the item...

Character_Functions.Ability_Checks    # this is where the skills are assigned their ability score


def Influence_Action(Creature):
  # choose random Influence Goals
  # choose a target
  # contested ability check
  Influence_Goals

  Dice_Rolls.Ability_Check(Creature,'Persuasion','Charisma')


# Search

def Search_Action(Creature):
  Area_of_Search = Creature.Location      # Need to return the whole number locations that fall inside the area of a cone


# Investigate an Illusion
def Investigate_Illusion_Action(Creature):
  Area_of_Investigation = Creature.Location
  Dice_Rolls.Ability_Check(Creature,'Investigation')


# Options from Pathfinder:
  # Escape
  # Seek (cone)

def Escape_Action(Creature):
  Find_Best_Skill_Prof(Creature,['Athletics','Acrobatics'])



def None_Action():
  pass


#def Two_Weapon_Fighting_Attack_Bonus_Action(Attacker,Defender,Weapon):
#  Weapon_Attack(Attacker,Defender,Weapon)

def Cast_Action(Target,Spell):
  pass