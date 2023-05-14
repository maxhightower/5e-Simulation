# Creating the Heirarchy
import numpy as np
from random import randrange
import Dice_Rolls


##### Common Functions
def levelToProficiency(Player_Character):
  count = 0
  for i in Player_Character.Levels:
      if i != False:
        count = count + 1
      else:
        pass
  return np.floor(2 + (count - 1)/4)



def CRToProficiency(Monster):
  print(type(Monster.CR))
  return np.floor(2 + (Monster.CR - 1)/4)


def abilityScoreToModifier(Score):
  return int((Score-10)/2)                #there's currently an issue where it returns 9 as a 0 when it should be -1


Classes_Int_List = ['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard']

d6_Classes = [12,10]
d8_Classes = [0,2,3,4,6,9,11]
d10_Classes = [5,8,7]
d12_Classes = [2]

def Predicted_Hit_Points(Player_Character):
  # the first level the character gets their full hit dice plus con modifier
  First_Level_Hitpoints = 0
  First_Level_Hitpoints = Player_Character.First_Class.Hit_Dice + abilityScoreToModifier(Player_Character.Con_Score) 
  #print(First_Level_Hitpoints)
  Total_Average_Hit_Points = First_Level_Hitpoints
  #print(Total_Average_Hit_Points)

  for i in Player_Character.Levels:
    if i != False:
      Class_Average_Hitpoints = Dice_Rolls.Average_Roll(1,i.Hit_Dice,abilityScoreToModifier(Player_Character.Con_Score),0)
      #print(Class_Average_Hitpoints)
      Total_Average_Hit_Points = Total_Average_Hit_Points + Class_Average_Hitpoints
    else:
      pass
  #print(Total_Average_Hit_Points)
  return Total_Average_Hit_Points






#def Random_Hit_Points(Player_Character):         Need to update this to match the changes to Predicted Hit Points
#  i = Player_Character.Class.Hit_Dice
#  for i in range(1,Player_Character.Level,1):
#    roll = randrange(1,Player_Character.Class.Hit_Dice+1,1)
#    i = i + roll
#    print(roll)
#  hit_points = i + (abilityScoreToModifier(Player_Character.Con_Score) * Player_Character.Level)
#  print('Randomly Rolled Hit Points:',i)

def Choose_Target(Self_Creature,World,Effect):
  pass
  # I need a function that takes the world that the creatures is in and, 
  # based on the type of feature, chooses the type of creature appropriate
  # Effect Target Type Options:
  # Ally
  # Creature
  # Location
  # Object
  # Hostile
  # Target

def Spawn_Creature(Location,Creature):
  Creature.Location = Location


# Need a function that determines at what HP will the creature run away
def Self_Preservation_Line(Creature):
  if Creature.Int_Score or Creature.Wis_Score:
    Self_Preservation_Line = Creature.HP * .6
  elif Creature.Int_Score or Creature.Wis_Score:
    Self_Preservation_Line = Creature.HP * .3
  else:
    Self_Preservation_Line = Creature.HP * .1
  return Self_Preservation_Line


# Should have a dictionary defining senses as vague or precise
# or should this be a dictionary per creature so certain senses can be moved around via certain features such as Keen Smell...
Senses = {
  'Precise': ['Sight'],       # Darkvision
  'Imprecise': ['Hearing'],   # Tremorsense
  'Vague': ['Smell'],
  'Disfunctional': []         # Perhaps for if blinded or deafened...
}   # Uncertain: Blindsight, Truesight, Lifesense, Detect Thoughts, ESP

def Roll_Hit_Dice():
  pass
  #Creature.Hit_Dice_Number
  #Creature.Hit_Dice_Type

#def Count_Player_Levels(Player_Character):
#  for i in Player_Character.Levels:
#    if Player_Character.Levels.index(i) > 0:
#      count = 0
#      if Player_Character.Levels[i] != False:
#        count = int(count) + 1
#      else:
#        pass
#    elif i == False:
#      pass
#    else: pass
#  return count


def Calc_Armor_Class(Player_Character):
  AC = 10
  if Player_Character.Armor_Equipped == []:
    AC = 10 + abilityScoreToModifier(Player_Character.Dex_Score)
    return AC
  else:
    for i in range(len(Player_Character.Armor_Equipped)):
      if i == 'Shield':
        AC = AC + 2

    #if 'Shield' in Player_Character.Armor_Equipped:

    Player_Character.Armor_Equipped[0] 



def Attack_Score(Creature): # most of my problems are coming from this bit of code right here
  #print("Attack Score Creature:",Creature)
  if len(Creature.Weapon_Equipped) > 1:
    if Creature.Weapon_Equipped[0].Finesse == True:
      return int(max(abilityScoreToModifier(Creature.Str_Score),abilityScoreToModifier(Creature.Dex_Score)))
    else:
      return int(abilityScoreToModifier(Creature.Str_Score))
  else:
    if Creature.Weapon_Equipped[0].Finesse == True:
      return int(max(abilityScoreToModifier(Creature.Str_Score),abilityScoreToModifier(Creature.Dex_Score)))
    else:
      return int(abilityScoreToModifier(Creature.Str_Score))



def Calculate_Expected_Damage_for_RTH(Target,Creature,Attack,Damage_Dice_Num,Damage_Dice_Type,Damage_Bonus,Damage_Bonus2): # RTH standing for Roll to Hit; this function is also assuming normal circumstances
  if Attack == False:
    Damage_Modifiers = []
    Weapon = Creature.Weapon_Equipped[0]
    #print('RTH Creature:',Creature)
    Prob_to_Hit = (21 + Attack_Score(Creature) + Creature.Prof_Bonus - Target.AC) / 20

    Damage = Dice_Rolls.Average_Roll(Damage_Dice_Num,Damage_Dice_Type,Damage_Bonus,Damage_Bonus2)
    Expected_Damage = Damage * Prob_to_Hit

    Crit_Damage = (Dice_Rolls.Average_Roll(Damage_Dice_Num,Damage_Dice_Type,0,0) * 2) + Damage_Bonus
    Crit_Expected_Damage = Crit_Damage * 0.05 * len(Creature.Crit)

    Expected_Damage = Expected_Damage + Crit_Expected_Damage

    if str(Weapon.Damage_Type + 'res') in Target.WRI:
      Damage_Modifiers.append(0.5)

    elif str(Weapon.Damage_Type + 'immu') in Target.WRI:
      Damage_Modifiers.append(0)
    
    elif 'nonmagicalres' in Target.WRI:
      Damage_Modifiers.append(0.5)
    
    elif 'nonmagicalimmu' in Target.WRI:
      Damage_Modifiers.append(0)
    
    else:
      pass


    #if 'critimmu' in Target.WRI:
    #  Total_Expected_Damage = Expected_Damage

    # Glancing Blows can only occur when the Attack_Bonus is less than the AC
    if Attack_Score(Creature) < Target.AC:
      Damage_Modifiers.append(0.5)
    
    
    for i in range(len(Damage_Modifiers)):
      Total_Expected_Damage = Expected_Damage * Damage_Modifiers[i]

  else:
    pass
  return Expected_Damage

# what about a system where there's a dictionary for effects, and then a for loop that goes through 
# and finds what type of effect (attack roll vs damage modifier)

def Check_Save_Proficiencies(Creature,Save):
  Ability_Score = Dice_Rolls.Saving_Throws.loc[Save]
  #if Creature.Effects      will handle this when I do the same for ability_checks
  if Save in Creature.Saving_Throws:
    line = str(Creature,'.',Ability_Score)
    Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + Creature.Saving_Throws
  else:
    line = str(Creature,'.',Ability_Score)
    Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line))
  return Result


def Check_Skill_Proficiencies(Creature,Skill,Ability_Score):
  prof_list = [Creature.Proficiency,Creature.Half_Proficiency,Creature.Expertise]
  for i in prof_list:
    if Skill in 0:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + Creature.Prof_Bonus
    elif Skill in 1:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + (Creature.Prof_Bonus / 2)
    elif Skill in 2:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + (Creature.Prof_Bonus * 2)
    else:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line))
  return Result


# Ability Check
def Ability_Check(Creature,Skill,Ability_Score):
  #if Creature.Effects[]          I want to put a line here that will check the creature for any effect that could influence the ability check

  if str('Advantage:' + Skill) in Creature.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Advantage(Creature)
  elif str('Disadvantage:' + Skill) in Creature.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Disadvantage(Creature)
  else:
    Roll = Dice_Rolls.d20(Creature)

  Result = Check_Skill_Proficiencies(Creature,Skill,Ability_Score)

  print(Roll)
  print(Result)


# Contested Ability Check
def Contested_Ability_Check(Creature1,Creature2,Skill,Ability_Score):
  #if Creature.Effects[]          I want to put a line here that will check the creature for any effect that could influence the ability check
  if str('Advantage:' + Skill) in Creature1.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Advantage()
  elif str('Disadvantage:' + Skill) in Creature1.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Disadvantage()
  else:
    Roll = Dice_Rolls.d20()
  Creature1_Result = Dice_Rolls.Check_Skill_Proficiencies(Creature1,Skill,Ability_Score) + Roll

  if str('Advantage:' + Skill) in Creature2.Circumstances['Ability Checks']:      #if Creature.Effects[]          I want to put a line here that will check the creature for any effect that could influence the ability check
    Roll = Dice_Rolls.d20_Advantage()
  elif str('Disadvantage:' + Skill) in Creature2.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Disadvantage()
  else:
    Roll = Dice_Rolls.d20()
  Creature2_Result = Check_Skill_Proficiencies(Creature2,Skill,Ability_Score) + Roll

  if Creature1_Result > Creature2_Result:
    pass
  else:
    pass


# Saving Throw
def Saving_Throw(Creature,Save):
  if str('Advantage: ' + Save + ' Saving Throws') in Creature.Circumstances['Saving Throws']:
    Roll = Dice_Rolls.d20_Advantage(Creature)
  elif str('Disadvantage: ' + Save + ' Saving Throws') in Creature.Circumstances['Saving Throws']:
    Roll = Dice_Rolls.d20_Disadvantage(Creature)
  else:
    Roll = Dice_Rolls.d20(Creature)

  Result = Dice_Rolls.Check_Save_Proficiencies(Creature,Save)

  print(Roll)
  print(Result)




####### Defining the Heirarchy
class World:
  def __init__(self,Parties,Environment):
    self.Parties = []
    self.Environment = Environment
  # I could have an attribute that's the distance of each creature from each other



class Party:
  def __init__(self,List,Allied):
    self.List = []
    self.Allied = bool()

class Entity:
  def __init__(self,AC,HP):
    self.AC = AC
    self.HP = HP
    # Damage Immunities
    # Damage Resistances
    # Damage Vulnerabilities
    # Condition Immunities


class Object(Entity):
  def __init__(self,
               
               # standard identifiers
                    # perhaps I'll need a Object ID
               Name, # the common item name or magic item name example: greatsword
               Type, # the standard types examples: weapon, armor, potion, trade good, vehicle, 
               Size, # if it's a weapon, the size creature intended for, otherwise, how much space the item fills examples: large, medium, etc
               Classification, # the way that 5e tools separates objects examples: mundane, magic, variant
               Rarity,

               # further identifiers, not every object has these so some will be homebrewed
               Material, # examples: steel, adamantine, mithral
               Weight,   # measured in lbs
               GP_Value, # 
               
               Consumable, # is the item 

               Charges,
               Recharge_Type,
               Upon_0_Charges,
               Results_When_Consumed # example: produces a glass flask
               ):


    self.Name = Name
    self.Type = Type    # Object Types = [Weapon,Armor,Trade_Good,Vehicle,]
    self.Size = Size    # Sizes =  Miniscule = 
                        #          Tiny = 1.25ft x 1.25ft
                        #          Small = 2.5ft x 2.5ft
                        #          Medium = 5ft x 5ft
                        #          Large = 10ft x 10ft
                        #          Huge = 15ft x 15ft
                        #          Gargantuan = 20ft x 20ft
                        #          Colossal = 25+ x 25+
    self.Classification = Classification
    self.Material = Material
    self.Weight = Weight

    self.GP_Value = GP_Value
    self.Consumable = False
    self.Results_When_Consumed = Results_When_Consumed
    self.Magical = False
    self.Rarity = Rarity        # Rarity Types = [Common,Uncommon,Rare,Very Rare,Legendary,Artifact]
    self.Cursed = False
    self.Spellcasting_Focus = False
    
    
    self.Sentient = bool()      # if this is the case, shouldn't it then be a Creature???
      # an object can have many of the same features as a creature (statistics, actions, etc)
      # the way I'm going to solve this issue is by having an attribute for each of these features in the object class





class Weapon(Object):
  def __init__(self,Name,Type,Size,Material,Rarity,GP_Value):
    super().__init__(Name,Type,Size,Material,Rarity,GP_Value)
    


class Armor(Object):
  def __init__(self,Name,Type,Size,Material,GP_Value,Rarity):
    super().__init__(Name,Type,Size,Material,GP_Value,Rarity)


class Trade_Good(Object):
  def __init__(self,Name,Type,Size,Material,GP_Value,Rarity):
    super().__init__(Name,Type,Size,Material,GP_Value,Rarity)


class Vehicle(Object):
  def __init__(self,Name,Type,Size,Material,GP_Value,Rarity):
    super().__init__(Name,Type,Size,Material,GP_Value,Rarity)



class Object_Instance(Object):
  def __init__(self,Name,Size,Material,Type,GP_Value,Rarity,Status,Location,Carrier):
    super().__init__(Name,Size,Material,Type,GP_Value,Rarity)
    self.Status = Status        # broken, disenchanted, 
    self.Location = Location    # if not in inventory
    self.Carrier = Carrier      # who's inventory is it in




## Object Rules
Object_Armor_Class = {
    'Material': ['Cloth','Paper','Rope','Crystal','Glass','Ice','Wood','Bone','Stone','Iron','Steel','Mithral','Adamantine'],
    'AC': [11,11,11,13,13,13,15,15,17,19,19,21,23]}
Object_Hit_Points = {
    'Size': ['Tiny','Tiny','Small','Small','Medium','Medium','Large','Large'],
    'Durability': ['Fragile','Resilient','Fragile','Resilient','Fragile','Resilient','Fragile','Resilient'],
    'Hit Dice': ['1d4','2d4','1d6','3d6','1d8','4d8','1d10','5d10']}






class Player_Character:
  def __init__(self,Name,First_Class,Species,Subspecies,Levels,Background,Skill_Profs,Skill_Expertise,Tool_Profs,Weapon_Equipped,Armor_Equipped,Language_Profs,Senses,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Spellcasting_Prepared,Item_Attunements,Inventory,Related_Stat_Blocks):
    self.Name = Name
    self.First_Class = First_Class
    
    self.Species = Species
    self.Subspecies = Subspecies

    self.Size = 'Medium'
    self.Speed = {
        'Walking': 30,
        'Flying': 0,
        'Swimming': 0,
        'Burrowing': 0,
        'Climbing': 0,
        'Flyhover': 0}
    
    self.Str_Score = Str_Score
    self.Dex_Score = Dex_Score
    self.Con_Score = Con_Score
    self.Int_Score = Int_Score
    self.Wis_Score = Wis_Score
    self.Cha_Score = Cha_Score
    
    self.Levels = [
      First_Class,    # Barbarian
      False,
      False,            # I could do a level up function and in it would be an if statement for selecting a subclass
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ]                    # an option that I have for multiclassing is to have an attribute for each level that gets assigned to a class
                                          # and then the total class and subclass allocation is determined based on the summation of the attributes

    self.Level_Count = sum(1 for n in self.Levels if n != False)

    self.Subclasses = [ # the most subclasses a character could have in theory is 9 
                        # Cleric, Warlock, and Sorcerer at level 1; Druid and Wizard at level 2; means 5 subclasses by level 7, 
                        # that leaves 4 additional since 13 (levels remaining) / 3 = 4          5 + 4 = 9
                        # so I only need 9 items in the list
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ]

    self.Hit_Dice_Types = [
      First_Class.Hit_Dice,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ]
    self.Hit_Dice_Number = len(self.Hit_Dice_Types)
    self.HP = Predicted_Hit_Points(self)
    self.Temp_HP = 0
    self.Current_HP = self.HP
    self.Allow_for_More_than_Max_HP = False

    self.AC = 10 + abilityScoreToModifier(Dex_Score)              # This one needs to be corrected eventually
    self.Background = Background

    self.Prof_Bonus = levelToProficiency(self)        # This function is going to need an update based on the new level system
  
    self.Skill_Half_Prof = []                     
    self.Skill_Profs = []
    self.Skill_Expertise = []
    
    self.Tool_Profs = []
    self.Artisans_Tools_Prof = []
    self.Instrument_Profs = []
    
    self.Vehicle_Profs = []
    self.Game_Profs = []

    self.Weapon_Profs = []
    self.Weapon_Equipped = []
    
    self.Armor_Profs = []
    self.Armor_Equipped = []
    self.Apperal_Adorned = []
    
    self.Language_Profs = []
    self.Senses = {
      'Precise': {
        'Sight': 2000,
      },
      'Imprecise': {
        'Hearing': 70,
      },
      'Vague': {
        'Smell': 20,
      }
    }         
    
    

    self.Saving_Throws = []

    self.Actions = {

    }
                    #   'Character_Actions.Cast_Action()' the Cast Action needs to be added via the spellcasting feature
                    
                    # Dice_Rolls.Hide_Action(),         # Not important for Simple Probability Assistant
                    # Dice_Rolls.Dash_Action(),         # Not important for Simple Probability Assistant
                    # Dice_Rolls.Help_Action(),         # Not important for Simple Probability Assistant
                    # Dice_Rolls.Search_Action(),       # Not important for Simple Probability Assistant
                    #Dice_Rolls.Disengage(),
                    #'Improvise',
                    #'Ready an Action',
                    #'Activate an Item',
                    #'Disarm',
                    #'Shove',
                    #'Shove Aside',
                    #'Use an Object',
                    #'Investigate for Illusion',
                    #'Influence'

    self.Reactions = {
                      'Enemy_Leaves_Melee_Range': {},
                      'Enemy_Casts_Spell': {},
                      'Ready_Action': {},

                      'Allied_Ability_Check': {},
                      'Allied_Attack_Roll': {},
                      'Allied_Taking_Damage': {},
                      'Allied_Saving_Throw': {},
                      
                      'Enemy_Attack_Roll': {},
                      'Enemy_Ability_Check': {},
                      'Enemy_Taking_Damage': {},
                      'Enemy_Saving_Throw': {}

    }
  
    self.Bonus_Actions = {
      'Independent': {
      
      },
      #'Character_Actions.Cast_Bonus_Action()'],
      'Dependent': {
        'Attack_Action': {
      
        }
        #'Cast_Action': []
        #'Dash_Action': [],
      }     # eventually I could use a for loop, for each Action that the player_character has and then use something to find the action's location in a list
    }

    self.Free_Actions = {
      'Dependent': {},
      'Independent': {}
    }
                                  # Free Actions vs Effects


    self.Effects = {            
        #'Self_Attacking': {
          #'Rolling': {
            #'Archery': []
            #'Great Weapon Fighting': []
            #'Dueling': []
            # },
          #'Hit': {
            # 
          #},
          #'Miss': []
        #},
        #'Self_Being_Attacked': {
          #'Crit': [],
          # 'Hit': [], 
        # },
    

        #'Self_Imposing_Save': [],
        #'Self_Making_Save': {
        #  'Any': [],
        #  'Strength': [],
        #  'Dexterity': [],
        #  'Constitution': [],
        #  'Intelligence': [],
        #  'Wisdom': [],
        #  'Charisma': [],
        #  'Death': []
        #},

        #'Ally_Attacking': {'Hit': [],'Miss': []},

        #'Ally_Being_Attacked': [],
        
        #'Ally_Imposing_Save': [],
        #'Ally_Making_Save': [],

        #'Self_Ability_Check': [],
        #'Ally_Ability_Check': [],
        #'Enemy_Ability_Check': [],

        #'Self_Dealing_Damage': {
        #  'Piercing': [],
        #  'Bludgeoning': [],
        #  'Slashing': [],
        #  'Fire': [],
        #  'Cold': [],
        #  'Lightning': [],
        #  'Thunder': [],
        #  'Poison': [],
        #  'Acid': [],
        #  'Necrotic': [],
        #  'Radiant': [],
        #  'Force': [],
        #  'Psychic': []
        #},
        #'Self_Taking_Damage': {
        #  'Piercing': [],
        #  'Bludgeoning': [],
        #  'Slashing': [],
        #  'Fire': [],
        #  'Cold': [],
        #  'Lightning': [],
        #  'Thunder': [],
        #  'Poison': [],
        #  'Acid': [],
        #  'Necrotic': [],
        #  'Radiant': [],
        #  'Force': [],
        #  'Psychic': [],
        #},
        
        #'Ally_Dealing_Damage': [],
        #'Ally_Taking_Damage': [],

        #'Self_Drops_to_Zero': [],
        #'Ally_Drops_to_Zero': [],

        # Self_Social_Conversation
    }

      # There could be effects that are mandatory to apply, such as those based on conditions...
      # There could be effects that are one-time use charges, and thus resource management is needed, such as bardic inspiration

    self.Long_Rest_Options = {
      
    }
    self.Short_Rest_Options = {
      'Unlimited': [Roll_Hit_Dice],
      'Charges': {}
    }

    self.One_Minute_Options = {
      'Unlimited': [],
      'Charges': []
    }
    self.Round_Reset_Options = {
      
    }

    self.Active_Conditions = {
      'Self': [],

      'Others': {
        'Attack_Rolls': [],
        'Ability_Checks': []
      }
    }         # should be a dictionary for conditions on self and on certain creatures however I'm unsure how to make that work without a relevant environment 

    self.Circumstances = {
        'Attack Rolls': {},
        'Ability Checks': {},

        'Saving Throws': {
          'Strength': [],
          'Dexterity': [],
          'Constitutions': [],
          'Intelligence': [],
          'Wisdom': {
            'Frightened': [],
            'Charmed': []
          },
          'Charisma': [],
          'Death': []
        }
    }


    self.At_Will_Spells = []
    self.Per_Use_Spells = {
      '1/long_rest': {},
      '1/short_rest': {}}
    self.Spellcasting_Known = {}
    self.Spellcasting_Prepared = {}

    self.Class_Resources = {
      # 'Barbarian': {
      #    ['Rage_Charges']: 
      # }
    }
    self.Class_Save_DCs = {
      # 'Barbarian': {
      #   'Relentless_Rage': 10
      # }
    }


    self.Concentrating = False
    self.Attunement_Slots = 3
    self.Item_Attunements = []
    self.Attunement_Slots_Filled = len(self.Item_Attunements)
    self.WRI = [] # should this be a dictionary so I can identify the source of a WRI so it can be removed if needed?

    self.Attacks = 1
    self.Usable_Attack_Score = {
      'Non-Magical': [Str_Score,Dex_Score],
      'Magical': [Str_Score,Dex_Score],
    }
    self.Crit = [20]
    
    self.Location = ()


    self.Inventory = {    # calculate the weight
      'Magic Items': {
        'Armor': [],
        'Weapons': [],
        'Other': []
      },

      'Armor': [],
      'Weapons': [],
      'Treasure': [],

      'Vehicles': [],
      'Instruments': [],
      'Tools': [],
      'Artisan_Tools': [],
      'Games': [],

      'Packs': [],
      'Apparel': [],
      'Storage': [],
      'Identifying_Items': [],
      'Currency': [],
      'Other': []
    }

    self.Jump_Height = 3 + abilityScoreToModifier(self.Str_Score)
    self.Jump_Distance = self.Str_Score
    self.Carrying_Capacity = self.Str_Score * 15

    self.Memory = {   # perhaps I could use the pickle module
      # thinking about how this should be organized...
      # perhaps it could be a dataframe of creatures encountered in order
      # except that Joey said it may be best to be unstructured
      # so perhaps a very long string could be constructed of things that has been encountered
      # What gets recorded in memory?
        # Combat
          # Creatures?
        # Adventure
        # Social
        # Current Situation: the spell that made me think of this was Detect Good and Evil
        # perhaps what I could do is have a list of things that happen in an encounter. 
        # or it could be a dictionary that goes 


        # index is considered the order of events
        'Combat_Encounters': {
          'Damage Dealt':       [],
          'Damage Type':        [],
          'Damage Healed':      [],
          'Effect Dealt':       [],
          'Effect Used':        [],
          'Effect Removed':     [],
          'Condition Dealt':    [],
          'Condition Removed':  [],
          'Creature Causing':   [],
          'Creature Receiving': []
        },

        'Social_Encounters': {
      
        },

        'Exploration': {
          # perhaps travel and exploration could be stored as vectors
        }
    }
    self.Related_Stat_Blocks = {
      'Familiar': 'None',
      'Steed': 'None',
      'Homonculus': 'None',
      'Companion': 'None',
      'Summons': {},
      'Dominated_Creatures': {},
      'Other': 'None',
    }



class Monster:
  def __init__(self,Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spellcasting_Prepared,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Long_Rest_Options,Short_Rest_Options,Resources,Speeds,Languages,Features,WRI,Spawn_Inventory):
    self.Monster_ID = Monster_ID
    self.Name = Name
    self.Book = Book
    self.HP = HP
    self.AC = AC
    self.Type = Type
    self.Size = Size
    self.CR = CR
    self.XP = XP
    self.Prof_Bonus = Prof_Bonus
    self.Saving_Throws = []
    self.Skill_Profs = []
    self.Str_Score = Str_Score
    self.Dex_Score = Dex_Score
    self.Con_Score = Con_Score
    self.Int_Score = Int_Score
    self.Wis_Score = Wis_Score
    self.Cha_Score = Cha_Score
    self.Actions = {}
    self.Reactions = {}
    self.Bonus_Actions = {}
    self.Free_Actions = {}
    self.Effects = {}


    self.At_Will_Spells = {}
    self.Per_Use_Spells = {
      '1/long_rest': {},
      '2/long_rest': {},
      '3/long_rest': {}
    }
    self.Spellcasting_Known = {}
    self.Spellcasting_Prepared = {}
    
    
    self.Spell_Save_DC = Spell_Save_DC
    self.Attunement_Slots = 3
    self.Attunement_Slots_Filled = 0

    self.Long_Rest_Options = {
      
    }
    self.Short_Rest_Options = {
      'Unlimited': [Roll_Hit_Dice],
      'Charges': {}
    }
    self.Resources = {}
    self.Speed = {
        'Walking': 30,
        'Flying': 0,
        'Swimming': 0,
        'Burrowing': 0,
        'Climbing': 0,
        'Flyhover': 0
    }

    self.Languages = []
    self.Features = []
    self.WRI = WRI
    self.Circumstances = {
        'Attack Rolls': False,
        'Ability Checks': False,
        'Saving Throws': False
    }
    self.Senses = []
    self.Spawn_Inventory = Spawn_Inventory
    #{
    #  'Magic Items': [],
    #  'Armor': [],
    #  'Weapons': []
    #}

#  def __str__(self):
#    return str(Name)

class Monster_Instance(Monster):
  #Monster_ID,Name,HP,AC,Type,Size,CR,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Active_Conditions
  def __init__(self,Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Spawn_Inventory,Instance,Monster_Instance_ID,Current_HP,Location,Active_Conditions,Life_Status,Inventory,Concentrating):
    super().__init__(Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Spawn_Inventory)
    self.Instance = Instance
    self.Monster_Instance_ID = Monster_Instance_ID
    self.Current_HP = Current_HP
    self.Temp_HP = 0
    self.Location = () 
    self.Active_Conditions = {

    }
    self.Life_Status = 'Alive'        #Life status can be either Alive, Stable, Down, or Dead
    self.Memory = {}
    self.Inventory = {}
    self.Concentrating = False

  #def Get_Environmental_Circumstances(self,World):
  #  self.Circumstances = {}
  #  for World.Creature in World:
      

# Only Monster_Instances and Sentient_Objects can learn and remember things, while all Player_Characters can
  # although this does bring up the concept of sentient object instances
  # and the concept of knowledge and experience being associated with a player_characters level

# How do I want memory to work???
# Should a creature remember every time it gets hit? every action that a creature can take?
# Or should the amount of data that is stored be proportional to the creature's intelligence?





# Begining the Party Characters

class Class:
  def __init__(self,Name,Hit_Dice,Saving_Throws,Starting_Skill_Number,Armor_Profs,Weapon_Profs,Skill_Profs,Tool_Profs,Spellcasting_Ability,Subclasses,Features,MultiClassing_Requirement,Spell_List,Caster_Type,Starting_Equipment):
    self.Name = Name
    self.Hit_Dice = Hit_Dice
    self.Saving_Throws = []     # need to make sure the saving throws get appended to the 
    self.Starting_Skill_Number = Starting_Skill_Number
    self.Armor_Profs = []
    self.Weapon_Profs = []
    self.Skill_Profs = []
    self.Tool_Profs = []
    self.Spellcasting_Ability = Spellcasting_Ability
    self.Subclass = []
    self.Features = []
    self.MultiClassing_Requirement = []
    self.Spell_List = []
    self.Caster_Type = Caster_Type
    self.Starting_Equipment = {
      'Armor': [],
      'Weapons': [],
      'Packs': [],
      'Tools': [],
      'Instruments': []}
    #Player_Character.Spell_Save_DC = abilityScoreToModifier(Spellcasting_Ability) + Prof_Bonus + 8



class Subclass(Class):
  def __init__(self,Class,Feature,Spellcasting_Ability):
    self.Class = Class
    self.Feature = Feature
    self.Spellcasting_Ability = Spellcasting_Ability


def Choose_Subclass(Player_Character,Class,Method,Subclass):
  if Method == 'Random':
    Subclass_Choice = Class.Subclasses[randrange(0,Class.Subclasses,1)] 
  else:
    if Subclass not in Class.Subclasses:
      pass
    else:
      Subclass_Choice = Subclass

  # I need to be able to see which classes can take a subclass in
  Classes = list(set(Player_Character.Levels))
  for i in Classes:
    if str(i) == 'Cleric':
      pass
    elif str(i) == 'Druid':
      pass
    elif str(i) == 'Sorcerer':
      pass
    elif str(i) == 'Warlock':
      pass
    else:
      pass


# perhaps the conditions of each entity should be a dictionary instead of a list, with a list representing each creature in the environment
# so for reckless, the creature that calls the function gains advantage, but then so does everyone else when attacking them

