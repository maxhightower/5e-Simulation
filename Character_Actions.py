import Dice_Rolls
import Establishing_Hierarchy
import Character_Functions
#import Effects
import operator


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




# Attack Roll
def Weapon_Attack(Attacker,Defender,Weapon):
  Attack_Modifier = Establishing_Hierarchy.Attack_Score(Attacker) + Attacker.Prof_Bonus
  Armor_Class = Defender.AC
  #print('Target AC:',Armor_Class)

  if Attacker.Circumstances['Attack Rolls'] == 'Advantage':
    #print('Advantage')
    Roll = Dice_Rolls.d20_Advantage()
    #print(Roll)

  elif Attacker.Circumstances['Attack Rolls'] == 'Disadvantage':
    #print('Disadvantage')
    Roll = Dice_Rolls.d20_Disadvantage()
    #print(Roll)

  else:
    #print('Rolling Normally')
    Roll = Dice_Rolls.d20()
    #print('Roll:',Roll)

  Establishing_Hierarchy.Current_Attack_Roll = Roll + Attack_Modifier
  #print(Establishing_Hierarchy.Current_Attack_Roll)

  #for i in Attacker.Effects['Self_Attacking']['Rolling'][Weapon.Type]:
  #  if i == ''


  x = Dice_Rolls.Roll(Weapon.Dice_Num,Weapon.Dice_Type) + Establishing_Hierarchy.Attack_Score(Attacker)
  #print('Initial Damage Roll:',x)
  y = Attack_Modifier

  #print(Attacker.Effects)

  if Weapon.Damage_Type == 'Bludgeoning' or Weapon.Damage_Type == 'Piercing' or Weapon.Damage_Type == 'Slashing':
    x = x + Attacker.Effects['Self_Dealing_Damage']['Bludgeoning'][0].Bonus
  
  #for i in Attacker.Effects['Self_Dealing_Damage'][Weapon.Dmg_Type]:
  #  x = x + Attacker.Effects['Self_Dealing_Damage'][Weapon.Dmg_Type][i]
  
  if Establishing_Hierarchy.Current_Attack_Roll > Armor_Class:
    if Roll in Attacker.Crit:
      damage = (x * 2) + y
    
      if str(Weapon.Dmg_Type.lower(),'res') in Defender.WRI:
        damage = damage/2
      elif str(Weapon.Dmg_Type.lower(),'immue') in Defender.WRI:
        damage = 0
      else: pass
      
      #print('Crit for',damage)

    else:
      damage = x + y
      if str(Weapon.Damage_Type.lower()+'res') in Defender.WRI:
        damage = damage/2
      elif str(Weapon.Damage_Type.lower()+'immue') in Defender.WRI:
        damage = 0
      else: pass

      #print('Hit for',damage)
  
  elif Establishing_Hierarchy.Current_Attack_Roll == Armor_Class:
    damage = (x + y)/2
    if str(Weapon.Damage_Type.lower()+'res') in Defender.WRI:
      damage = damage/2
    elif str(Weapon.Damage_Type.lower()+'immue') in Defender.WRI:
        damage = 0
    else: pass


    #print('Glancing Blow for',damage)

  else:
      #print('Miss')
      return 0





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


def Two_Weapon_Fighting_Attack_Bonus_Action(Attacker,Defender,Weapon):
  Weapon_Attack(Attacker,Defender,Weapon)
