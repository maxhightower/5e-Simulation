import Dice_Rolls
import Establishing_Hierarchy
import Character_Functions
#import Effects
import operator
import random
import Armor_and_Weapons
import pandas as pd
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

combat_log = pd.DataFrame(columns=[
                                   'Combat Round',
                                   'Action Number',
                                   'Action Time', # action, bonus action, reaction, etc
                                   'Action Name', # attack, cast spell, dodge, etc
                                   'Action Type', # attack, support, heal, control, etc
                                   'Target',
                                   'Current Allied Ability Check',
                                   'Current Allied Attack Roll',
                                   'Current Allied Saving Throw',
                                   'Current Allied Damage Roll',
                                   'Current Enemy Ability Check',
                                   'Current Enemy Attack Roll',
                                   'Current Enemy Saving Throw',
                                   'Current Enemy Damage Roll',
                                   ])



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

def Attack_Action(Actor,Combat_Situation,combat_log):
  Equip_Weapon(Actor,Choose_Best_Weapon(Actor))
  Weapon = Actor.Weapon_Equipped[0]
  Target = Dice_Rolls.Choose_Target_Offense(Actor,Combat_Situation)
  Actor.Target_List.append(Target)
  return Enact_Attack(Actor,Target,Weapon,Combat_Situation,combat_log)


def Enact_Attack(Actor,Target,Weapon,combat_situation,new_combat_log):

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
  #damage_roll = Dice_Rolls.Damage_Roll(Weapon.Dice_Type,Weapon.Dice_Num,Actor,Target,Weapon,Establishing_Hierarchy.Attack_Score(Actor),Weapon.Damage_Type)
  # use the function Convert_Roll_to_Int to convert the roll x to an integer
  damage_roll = Dice_Rolls.Roll_Dice(Weapon.Dice_Type,Weapon.Dice_Num)
  y = Attack_Modifier


  if Weapon.Damage_Type == 'Bludgeoning' or Weapon.Damage_Type == 'Piercing' or Weapon.Damage_Type == 'Slashing':
    try:
      x = x + Actor.Effects['Self_Dealing_Damage']['Bludgeoning'][0].Bonus
    except:
      pass
  #for i in Actor.Effects['Self_Dealing_Damage'][Weapon.Dmg_Type]:
  #  x = x + Actor.Effects['Self_Dealing_Damage'][Weapon.Dmg_Type][i]
  
  if Establishing_Hierarchy.Current_Attack_Roll > Armor_Class:
    if Roll in Actor.Crit:
      result = 'Critical Hit'
      damage = (damage_roll * 2) + y
      if str(Weapon.Dmg_Type.lower(),'res') in Target.WRI:
        damage = damage/2
      elif str(Weapon.Dmg_Type.lower(),'immue') in Target.WRI:
        damage = 0
      else: pass
     
    else:
      result = 'Hit'
      damage = damage_roll + y
      if str(Weapon.Damage_Type.lower()+'res') in Target.WRI:
        damage = damage/2
      elif str(Weapon.Damage_Type.lower()+'immue') in Target.WRI:
        damage = 0
      else: pass
      
  elif Establishing_Hierarchy.Current_Attack_Roll == Armor_Class:
    result = 'Glancing Blow'
    damage = (damage_roll + y)/2
    if str(Weapon.Damage_Type.lower()+'res') in Target.WRI:
      damage = damage/2
    elif str(Weapon.Damage_Type.lower()+'immue') in Target.WRI:
        damage = 0
    else: pass
    
  else:
      damage = 0
      result = 'Miss'
  
   # it's going to return the information needed to update the combat log
  #return 'Action','Attack','Offense',Target, damage
        
  if len(new_combat_log) == 0:
    combat_round = 0
  else:
    combat_round = combat_round + 1
        
  Target.Current_HP = Target.Current_HP - damage
  
  action_number = 'Undetermined'
  
  action_time = 'Action'
  action_name = 'Attack'
  action_type = 'Offense'
  # the target is the last entity in the Actor.Target_List

  target = Actor.Target_List[-1].Name

  # create a dictionary called new_round
  new_round = {'Combat Round': combat_round,
                'Action Number': action_number,
                'Action Time': action_time,
                'Action Name': action_name,
                'Action Type': action_type,
                'Target': target,
                'Action Result': result,
                'Current Allied Ability Check': Dice_Rolls.Current_Allied_Ability_Check,
                'Current Allied Attack Roll': Dice_Rolls.Current_Allied_Attack_Roll,
                'Current Allied Saving Throw': Dice_Rolls.Current_Allied_Saving_Throw,
                'Current Allied Damage Roll': Dice_Rolls.Current_Allied_Damage_Roll,
                'Current Enemy Ability Check': Dice_Rolls.Current_Enemy_Ability_Check,
                'Current Enemy Attack Roll': Dice_Rolls.Current_Enemy_Attack_Roll,
                'Current Enemy Saving Throw': Dice_Rolls.Current_Enemy_Saving_Throw,
                'Current Enemy Damage Roll': Dice_Rolls.Current_Enemy_Damage_Roll,
                }
  
  # using Actor.Name create  new columns for Acting True and add them to the dict
  new_round[Actor.Name + ' Acting True'] = 1
  new_round[Actor.Name + ' Current_HP'] = Actor.Current_HP
  new_round[Actor.Name + ' Temp_HP'] = Actor.Temp_HP
  new_round[Actor.Name + ' Size'] = Actor.Size
  new_round[Actor.Name + ' Walking Speed'] = Actor.Speed['Walking']
  new_round[Actor.Name + ' Flying Speed'] = Actor.Speed['Flying']
  new_round[Actor.Name + ' Str_Score'] = Actor.Str_Score
  new_round[Actor.Name + ' Dex_Score'] = Actor.Dex_Score
  new_round[Actor.Name + ' Con_Score'] = Actor.Con_Score
  new_round[Actor.Name + ' Int_Score'] = Actor.Int_Score
  new_round[Actor.Name + ' Wis_Score'] = Actor.Wis_Score
  new_round[Actor.Name + ' Cha_Score'] = Actor.Cha_Score
  new_round[Actor.Name + ' Active_Conditions'] = Actor.Active_Conditions
  new_round[Actor.Name + ' Concentrating'] = Actor.Concentrating
  #new_round[Actor.Name + ' Location'] = Actor.Location
  # using combat_situation create new columns for Acting False and add them to the dict

  for i in range(len(combat_situation)):
    if combat_situation[i] == Actor:
      pass
    else:
 
      new_round[combat_situation[i].Name + ' Acting True'] = 0
      new_round[combat_situation[i].Name + ' Current_HP'] = combat_situation[i].Current_HP
      new_round[combat_situation[i].Name + ' Temp_HP'] = combat_situation[i].Temp_HP
      new_round[combat_situation[i].Name + ' Size'] = combat_situation[i].Size
      new_round[combat_situation[i].Name + ' Walking Speed'] = combat_situation[i].Speed['Walking']
      new_round[combat_situation[i].Name + ' Flying Speed'] = combat_situation[i].Speed['Flying']
      new_round[combat_situation[i].Name + ' Str_Score'] = combat_situation[i].Str_Score
      new_round[combat_situation[i].Name + ' Dex_Score'] = combat_situation[i].Dex_Score
      new_round[combat_situation[i].Name + ' Con_Score'] = combat_situation[i].Con_Score
      new_round[combat_situation[i].Name + ' Int_Score'] = combat_situation[i].Int_Score
      new_round[combat_situation[i].Name + ' Wis_Score'] = combat_situation[i].Wis_Score
      new_round[combat_situation[i].Name + ' Cha_Score'] = combat_situation[i].Cha_Score
      new_round[combat_situation[i].Name + ' Active_Conditions'] = combat_situation[i].Active_Conditions
      new_round[combat_situation[i].Name + ' Concentrating'] = combat_situation[i].Concentrating
      #new_round[i.Name + ' Location'] = i.Location
    

  # attach the new_round dictionary to the combat_log_new dataframe using concat
  new_combat_log = pd.concat([new_combat_log,pd.DataFrame(new_round)],ignore_index=False)
  # drop the duplicates from the new_combat_log based on the columns with only ints and floats
  new_combat_log = new_combat_log[~new_combat_log.duplicated(subset=[col for col in new_combat_log.columns if new_combat_log[col].dtype in ['int64','float64']])]

  return new_combat_log


import numpy as np


# Actions
# Move
def Move(Actor,combat_situation,combat_log_new):
  print('2')
  current_location = Actor.Location
  other_entity_locations = {}
  for i in combat_situation:
    if i == Actor:
      pass
    else:
      other_entity_locations[i] = i.Location
  
  # check the distances between the Actor and the other entities
  distances = {}
  for i in other_entity_locations:
    distances[i] = np.linalg.norm(np.array(current_location) - np.array(other_entity_locations[i]))


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
def Dodge_Action(Actor,Combat_Situation,Combat_Log):
  Actor.Circumstances['Attack Rolls'] = 'Disadvantage'
  Actor.Circumstances['Saving Throws'] = 'Advantage'

  if len(combat_log) == 0:
    log_id = 0
  else:
    log_id = log_id + 1
        
  if len(combat_log) == 0:
    combat_round = 0
  else:
    combat_round = combat_round + 1

  action_number = 'Undetermined'
  
  action_time = 'Action'
  action_name = 'Dodge'
  action_type = 'Defense'


  # create a dictionary called new_round
  new_round = {'Combat Round': combat_round,
                'Action Number': action_number,
                'Action Time': action_time,
                'Action Name': action_name,
                'Action Type': action_type,
                'Target': Actor.Name,
                'Action Result': 'Dodge',
                'Current Allied Ability Check': Dice_Rolls.Current_Allied_Ability_Check,
                'Current Allied Attack Roll': Dice_Rolls.Current_Allied_Attack_Roll,
                'Current Allied Saving Throw': Dice_Rolls.Current_Allied_Saving_Throw,
                'Current Allied Damage Roll': Dice_Rolls.Current_Allied_Damage_Roll,
                'Current Enemy Ability Check': Dice_Rolls.Current_Enemy_Ability_Check,
                'Current Enemy Attack Roll': Dice_Rolls.Current_Enemy_Attack_Roll,
                'Current Enemy Saving Throw': Dice_Rolls.Current_Enemy_Saving_Throw,
                'Current Enemy Damage Roll': Dice_Rolls.Current_Enemy_Damage_Roll,
                }

  # using Actor.Name create  new columns for Acting True and add them to the dict
  new_round[Actor.Name + ' Acting True'] = 1
  new_round[Actor.Name + ' Current_HP'] = Actor.Current_HP
  new_round[Actor.Name + ' Temp_HP'] = Actor.Temp_HP
  new_round[Actor.Name + ' Size'] = Actor.Size
  new_round[Actor.Name + ' Walking Speed'] = Actor.Speed['Walking']
  new_round[Actor.Name + ' Flying Speed'] = Actor.Speed['Flying']
  new_round[Actor.Name + ' Str_Score'] = Actor.Str_Score
  new_round[Actor.Name + ' Dex_Score'] = Actor.Dex_Score
  new_round[Actor.Name + ' Con_Score'] = Actor.Con_Score
  new_round[Actor.Name + ' Int_Score'] = Actor.Int_Score
  new_round[Actor.Name + ' Wis_Score'] = Actor.Wis_Score
  new_round[Actor.Name + ' Cha_Score'] = Actor.Cha_Score
  new_round[Actor.Name + ' Active_Conditions'] = Actor.Active_Conditions
  new_round[Actor.Name + ' Concentrating'] = Actor.Concentrating
  # using combat_situation create new columns for Acting False and add them to the dict
  for i in Combat_Situation:
    if i == Actor:
      pass
    else:
      new_round[i.Name + ' Acting True'] = 0
      new_round[i.Name + ' Current_HP'] = i.Current_HP
      new_round[i.Name + ' Temp_HP'] = i.Temp_HP
      new_round[i.Name + ' Size'] = i.Size
      new_round[i.Name + ' Walking Speed'] = i.Speed['Walking']
      new_round[i.Name + ' Flying Speed'] = i.Speed['Flying']
      new_round[i.Name + ' Str_Score'] = i.Str_Score
      new_round[i.Name + ' Dex_Score'] = i.Dex_Score
      new_round[i.Name + ' Con_Score'] = i.Con_Score
      new_round[i.Name + ' Int_Score'] = i.Int_Score
      new_round[i.Name + ' Wis_Score'] = i.Wis_Score
      new_round[i.Name + ' Cha_Score'] = i.Cha_Score
      new_round[i.Name + ' Active_Conditions'] = i.Active_Conditions
      new_round[i.Name + ' Concentrating'] = i.Concentrating
  
  # attach the new_round dictionary to the combat_log_new dataframe using concat
  new_combat_log = pd.concat([combat_log,pd.DataFrame(new_round,index=[0])],ignore_index=True)


  return new_combat_log

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