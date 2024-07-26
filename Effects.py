from random import randrange
import Dice_Rolls
import Environment

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll

# Should I make a superclass called Effect with the attributes Prerequisite, Target, and Duration
# and then have each of the different effect types be child classes???

# in order for effects to influence dice rolls, I may need to redefine the dice rolls as well
# with tags that specify what they're for, so that the effects may be applied to them. 

# so we already have the functions for things like d20(), d20_Advantage(), and d20_Disadvantage()
# however the rolls for Ability checks, Saving throws, and Attack Rolls need a lot of work




# Common Functions
## Long Rest
def Long_Rest(Creature):
  print("Prior Hit Points:",Creature.Current_HP)
  Creature.Temp_HP = 0
  Creature.Current_HP = Creature.HP
  print("Current Hit Points:",Creature.Current_HP)
  # Need to add unconcsious conditions
  # Need to add the Creature's Long Rest Actions


def Long_Rest_Party(Party):
  for Creature in Party:
    Long_Rest(Creature)
  # Need a watch-shift mechanic  

## Short Rest
def Short_Rest(Player_Character):
  Hit_Dice_Type = Player_Character.Class.Hit_Dice
  Number_of_Hit_Dice = Player_Character.Level
  Hit_Dice_Rolled = randrange(0,Number_of_Hit_Dice,1)
  Health_Restored = Hit_Dice_Rolled * randrange(1,Hit_Dice_Type,1)
  Heal(Health_Restored,0,Player_Character)






Dice_Rolls.Ability_Check
Dice_Rolls.Attack_Roll
Dice_Rolls.Spell_Attack_Roll
Dice_Rolls.Weapon_Attack_Roll
Dice_Rolls.Ability_Attack_Roll
Dice_Rolls.Saving_Throw
Dice_Rolls.Damage_Roll

class Damage_Effect:
  def __init__(self,Damage_Form,Roll_Type,Damage_Type,Creatures_Targeted,Duration,Dice_Type,Dice_Number,Bonus_Damage,Attack_Type,Save_Type,Save_for_Half):
    self.Damage_Form = Damage_Form # Single target, AOE, etc
    self.Roll_Type = Roll_Type
    self.Damage_Type = Damage_Type
    self.Creatures_Targeted = Creatures_Targeted # list of creatures effected
    self.Duration = Duration #most likely instantaneous
    self.Dice_Type = Dice_Type
    self.Dice_Number = Dice_Number
    self.Bonus_Damage = Bonus_Damage
    self.Attack_Type = Attack_Type  # could be ranged weapon, melee weapon, melee spell, or ranged spell
    self.Save_Type = Save_Type  # str, dex, con, int, wis, cha, death
    self.Save_for_Half = Save_for_Half # if a creature saves, do they still take half damage examples: true, false



## Deal Damage
def Attempt_Deal_Damage(Damage_Effect,Defender,Attacker):
  Damage_Modifiers = []

  if str(Damage_Effect.Damage_Type,'immu') in Defender.WRI:
    # Need to check if the Attacker has an ability to overcome damage resistances
    Damage_Dealt = 0
  elif str(Damage_Effect.Damage_Type,'res') in Defender.WRI:
    # Need to check if the Attacker has an ability to overcome damage resistances
    Damage_Modifiers.append('x0.5')

  elif str(Damage_Effect.Damage_Type,'vul') in Defender.WRI:
    Damage_Modifiers.append('x2')
  else: pass

  Attacker_Options = {}
  Attacker.Effects['Self_Attacking']['Rolling']
  Attacker.Effects['Self_Attacking']['Hit']
  Attacker.Effects['Self_Attacking']['Miss']
  Attacker.Effects['Self_Imposing_Save']
  Attacker.Effects['Self_Dealing_Damage'][Damage_Effect.Damage_Type]

  # Current_Enemy_Saving_Throw
  Defender_Options = {}
  Defender.Reactions['Self_Being_Attacked']
  Defender.Reactions['Self_Taking_Damage'][Damage_Effect.Damage_Type]

  Defender.Effects['Self_Being_Attacked']
  Defender.Effects['Self_Taking_Damage'][Damage_Effect.Damage_Type]



  if Damage_Effect.Roll_Type == 'Saving Throw':
    
    Current_Enemy_Saving_Throw
    Current_Allied_Saving_Throw

    if Damage_Effect.Save_for_Half == True:
      pass


  elif Damage_Effect.Roll_Type == 'Attack Roll':
    pass
  

  elif Damage_Effect.Roll_Type == 'Ability Check':
    pass


  else: 
    pass


  # Check WRI
    # Immunity
    # Resistance
    # Vulnerability

  # Check Effects
    # Taking Damage
    
  # Check Reactions
    # Taking Damage



def Apply_Damage_Effect(Effect,Caller,Target):
  pass

#  x = Monsters.monster_primes[Creature].Temp_HP - Damage
#  if x > 0:
#    Monsters.monster_primes[Creature].Temp_HP = Monsters.monster_primes[Creature].Temp_HP - x
#  elif x < 0 and Monsters.monster_primes[Creature].Current_HP == Monsters.monster_primes[Creature].HP:
#    Monsters.monster_primes[Creature].Temp_HP = 0
#    Monsters.monster_primes[Creature].Current_HP = Monsters.monster_primes[Creature].HP + x
#  elif x < 0 and Monsters.monster_primes[Creature].Current_HP < Monsters.monster_primes[Creature].HP:
#    Monsters.monster_primes[Creature].Temp_HP = 0
#    Monsters.monster_primes[Creature].Current_HP = Monsters.monster_primes[Creature].Current_HP + x
#  else:
#    Monsters.monster_primes[Creature].Temp_HP = 0
#    Monsters.monster_primes[Creature].Current_HP = Monsters.monster_primes[Creature].Current_HP + x
#  print("Current Hit Points:",Monsters.monster_primes[Creature].Current_HP)
#  print("Temporary Hit Points:", Monsters.monster_primes[Creature].Temp_HP)




## Healing Effects
class Healing_Effect:
  def __init__(self,Prerequisite,Target,Duration,Healing_Type,Dice_Type,Dice_Number,Bonus):
    self.Prerequisite = Prerequisite
    self.Target = Target
    self.Duration = Duration
    self.Healing_Type = Healing_Type
    self.Dice_Type = Dice_Type
    self.Dice_Number = Dice_Number
    self.Bonus = Bonus

### Heal function
def Heal(HP,Temp_HP,Creature):
  print("Previous Hit Points:",Creature.Current_HP)
  if Creature.Current_HP + HP > Creature.HP and Creature.Allow_for_More_than_Max_HP == False:
    Creature.Current_HP = Creature.HP
    Creature.Temp_HP = Temp_HP
  else:
    Creature.Current_HP = Creature.Current_HP + HP
    Creature.Temp_HP = Temp_HP
  print("Current Hit Points:",Creature.Current_HP)
  print("Temporary Hit Points:",Creature.Temp_HP)


def Apply_Healing_Effect(Effect,Target):
  #Prerequisite,Target,Duration,Healing_Type,Dice_Type,Dice_Number,Bonus
  Healing_Amount = Dice_Rolls.Roll_Dice(Effect.Dice_Number,Effect.Dice_Type) + Effect.Bonus
  if Effect.Healing_Type == 'Temp HP':
    Heal(0,Healing_Amount,Target)
  else:
    Heal(Healing_Amount,0,Target)


### Above Maximum Hit Points
def Heal_Abv_Max(Effect,Target):
  pass

### Prevent Healing
def Prevent_Healing(Effect,Target):
  pass

### Reduce Maximum Hit Points
def Reduce_Max_HP(Effect,Target):
  pass





### Testing a Healing Effect
Restorative_Reagents = Healing_Effect('Use Object','Creature','Instantaneous','Temp HP',6,2,5)
def Roll_Healing_Effect(Effect):
  i = 0
  rolls = []
  for i in range(1,Effect.Dice_Number+1,1):
    roll = randrange(1,Effect.Dice_Type+1)
    i = i + roll
    rolls.append(roll)
  print(rolls)
  print(i)
  return i
#Roll_Healing_Effect(Restorative_Reagents)


### Applying Heal Function to a Healing Effect
def Restorative_Reagents_Function(Creature):
  x = Roll_Healing_Effect(Restorative_Reagents)
  Heal(0,x,Creature)







## Speed Effects
class Speed_Effect:
  def __init__(self,Prerequisite,Target,Duration,Speed_Type,Speed_Bonus,Speed_Set):
    self.Prerequisite = Prerequisite
    self.Target = Target
    self.Duration = Duration
    self.Speed_Type = Speed_Type
    self.Speed_Bonus = Speed_Bonus
    self.Speed_Set = Speed_Set

def Boost_Speed(Bonus,Type,Creature):
  Creatures_Normal_Speed = Creature.Speed
  Speed = Bonus + Creature.Speed[Type]
  Creature.Speed.update({Type: Speed})
  print("New",Type,"Speed:",Creature.Speed[Type])

def Add_Speed(Speed,Type,Creature):
  Creature_Normal_Speed = Creature.Speed
  Creature.Speed.update({Type: Speed})
  print("New",Type,"Speed:",Creature.Speed[Type])

### Testing a Speed Effect
Longstrider = Speed_Effect('Spell','Self','10 minutes','Walking',10,False)
### Testing different Speed Effect type
Fly = Speed_Effect('Spell','Creatures','10 minutes','Flying',False,60)

# Perhaps I should define a new Apply_Speed_Effect() function to simplify things...




class AC_Effect:
  def __init__(self,Prerequisite,Target,Duration,AC_Type,AC_Bonus):
    self.Prerequisite = Prerequisite
    self.Target = Target
    self.Duration = Duration
    self.AC_Type = AC_Type
    self.AC_Bonus = AC_Bonus

def Apply_AC_Effect(AC_Effect):
  AC_Effect.Target.AC = AC_Effect.Target.AC + AC_Effect.AC_Bonus

  def End_AC_Effect(AC_Effect):
    AC_Effect.Target.AC = AC_Effect.Target.AC - AC_Effect.AC_Bonus

  if AC_Effect.Duration == 'Instantaneous':
    pass
  elif AC_Effect.Duration == '1 Round':
    pass
  elif AC_Effect.Duration == '1 Minute':
    pass
  elif AC_Effect.Duration == '10 Minutes':
    pass
  elif AC_Effect.Duration == '1 Hour':
    pass
  else: pass


class Spell_Effect:
  def __init__(self,Prerequisite,Target,Duration,Spell,Level,Concentration):
    self.Prerequisite = Prerequisite
    self.Target = Target
    self.Duration = Duration
    self.Spell = Spell
    self.Level = Level
    self.Concentration = Concentration

def Apply_Spell_Effect():
  pass

# what defines a spell effect? what are we trying to address here? 
# spiritual weapon, creates an weapon that isn't targetable, yet can attack...
# 






## Buff Bonus Effects
class Buff_Bonus_Effect:
  def __init__(self,Target_Roll,Duration,Buff_Type,Dice_Type,Dice_Number,Bonus):
    self.Target_Roll = Target_Roll
      # Current_Allied_Ability_Check
      # Current_Allied_Attack_Roll
      # Current_Allied_Saving_Throw
      # Current_Allied_Damage_Roll

      # Current_Enemy_Ability_Check
      # Current_Enemy_Attack_Roll
      # Current_Enemy_Saving_Throw
      # Current_Enemy_Damage_Roll

    self.Duration = Duration
    self.Buff_Type = Buff_Type

    self.Dice_Type = Dice_Type
    self.Dice_Number = Dice_Number
    self.Bonus = Bonus


def Store_Buff_Bonus_Effect(Effect,Target,Effect_Key_One,Effect_Key_Two,Effect_Key_Three,Effect_Key_Four):
  if Effect_Key_One not in Target.Effects.keys():
    pass
  else:
    if Effect_Key_Two == False:
      Target.Effects[Effect_Key_One][str(Effect)] = Apply_Buff_Bonus_Effect(Effect,Effect.Target_Roll)
    else:

      if Effect_Key_Two not in Target.Effects[Effect_Key_One].keys():
        pass
      else:

        if Effect_Key_Three == False:
          Target.Effects[Effect_Key_Two][str(Effect)] = Apply_Buff_Bonus_Effect(Effect,Effect.Target_Roll)
        else: 
      
          if Effect_Key_Three not in Target.Effects[Effect_Key_One][Effect_Key_Two].keys():
            pass
          else:

            if Effect_Key_Four == False:
              Target.Effects[Effect_Key_Three][Effect.Name] = Apply_Buff_Bonus_Effect(Effect,Effect.Target_Roll)



def Apply_Buff_Bonus_Effect(Effect):
  if Effect.Target_Roll == Current_Allied_Ability_Check:
    Current_Allied_Ability_Check.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Allied_Attack_Roll:
    Current_Allied_Attack_Roll.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Allied_Saving_Throw:
    Current_Allied_Saving_Throw.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Allied_Damage_Roll:
    Current_Allied_Damage_Roll.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Enemy_Ability_Check:
    Current_Enemy_Ability_Check.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Enemy_Attack_Roll:
    Current_Enemy_Attack_Roll.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Enemy_Saving_Throw:
    Current_Enemy_Saving_Throw.Modifiers.append(Effect.Target_Roll.Modifiers) 

  elif Effect.Target_Roll == Current_Enemy_Damage_Roll:
    Current_Enemy_Damage_Roll.Modifiers.append(Effect.Target_Roll.Modifiers) 

  else:
    pass





class Buff_Replacement_Effect:
  def __init__(self,Prerequisite,Target,Duration,Buff_Type,Replacement):
    self.Prerequisite = Prerequisite
    self.Target = Target
    self.Duration = Duration
    self.Buff_Type = Buff_Type
    self.Replacement = Replacement

def Apply_Buff_Replacement_Effect(Effect,Type_One,Type_Two,Target):
  pass

def Remove_Buff_Replacement_Effect(Effect,Type_One,Type_Two,Target):
  pass









class Buff_Circumstance_Effect:
  def __init__(self,Prerequisite,Target,Duration,Buff_Type,Circumstances):
    self.Prerequisite = Prerequisite
    self.Target = Target
    self.Duration = Duration
    self.Buff_Type = Buff_Type
    self.Circumstances = Circumstances

def Apply_Buff_Circumstance_Effect(Effect,Target):                  # this is going to need some actual attention later
  Circumstances = (Effect.Circumstances + Effect.Buff_Type)
  Target.Circumstances
  
  ({Effect.Prerequisite: Circumstances})



def Remove_Buff_Circumstance_Effect(Effect,Target):
  pass

# Testing Buff Circumstance Effect
Danger_Sense = Buff_Circumstance_Effect('Saving Throws','Self','Instantaneous','Dexterity Saving Throw','Advantage: ')

def Reset_Circumstances(Creature):
  Creature.Circumstances.update({
        'Attack Rolls': False,
        'Ability Checks': False,
        'Saving Throws': False
    })



Effect_Types = ['Healing','Speed','AC','Spell Effect','Buff: Bonus','Buff: Replacement','Buff: Circumstance','Special']
Effect_Prerequisites = ['Attack Roll','Spell','Ability Check','Saving Throw','Use Object','Damage Type','Weapon']
Effect_Targets = ['Self','Ally','Hostile','Creatures','Target']
Effect_Durations = ['Instantaneous','1_Round','1_Minute','10_Minutes','1_Hour','8_Hours','24_Hours']












#Cannot Regain Hitpoints
class Cannot_Heal_Effect:
  def __init__(self):
    self



#Reduced Maximum Hitpoints
class Reduced_Maximum_Hitpoint_Effect:
  def __init__(self,Amount,Reset_Type,Heal_Type):
    self.Amount = Amount
    self.Reset_Type = Reset_Type  # long rest, short rest, etc
    self.Heal_Type = Heal_Type # which spells or abilities can affect this

#Condition Effect
class Condition_Effect:
  def __init__(self,):
    self

#Action Economy Effect
class Action_Economy_Effect:
  def __init__(self,):
    # what are the different types of Action Economy Effects?
    # removing reactions
    # having to choose between Action, Movement, or Bonus Action
    self

#Death Effect - stablizing, death ward
class Death_Type_Effect:
  def __init__(self,):
    self


#WRI Effect
class WRI_Effect:
  def __init__(self,):
    self

#Gravity Effect
class Gravity_Effect:
  def __init__(self,):
    self

#Size Effect
class Size_Effect:
  def __init__(self,):
    self

#Sensory_Effect
class Sensory_Effect:
  def __init__(self,):
    self

#Inventory_Effect
class Inventory_Effect:
  def __init__(self,):
    self

#Polymorph_Effect
class Transform_Effect:
  def __init__(self,Name,
               Replace_Mental_Stats,
               Meld_with_Weapons, Meld_with_Items, Meld_with_Armor,
               Keep_Class_Benefits, Keep_Racial_Benefits, Keep_Other_Source_Benefits,
               Keep_Skills, Keep_Saving_Throws,
               Add_Skills, Add_Saving_Throws,
               New_Form):
    
    self.Name = Name
    self.Replace_Mental_Stats = bool

    self.Meld_with_Weapons = bool
    self.Meld_with_Items = bool
    self.Meld_with_Armor = bool

    self.Keep_Class_Benefits = bool
    self.Keep_Racial_Benefits = bool
    self.Keep_Other_Source_Benefits = bool

    self.Keep_Skills = bool
    self.Keep_Saving_Throws = bool

    self.Add_Skills = bool
    self.Add_Saving_Throws = bool

    self.New_Form = New_Form


def Apply_Transform_Effect(Target,Effect,New_Form):
  Old_Str = Target.Str_Score
  Old_Dex = Target.Dex_Score
  Old_Con = Target.Con_Score
  Old_Int = Target.Int_Score
  Old_Wis = Target.Wis_Score
  Old_Cha = Target.Cha_Score

  Old_Size = Target.Size
  Old_HP = Target.Current_Hp
  Old_AC = Target.AC
  Old_Speed = Target.Speed
  Old_WRI = Target.WRI
  Old_Actions = Target.Actions
  Old_Bonus_Actions = Target.Bonus_Actions
  Old_Effects = Target.Effects
  Old_Free_Actions = Target.Free_Actions

  Target.Size = New_Form.Size
  Target.Current_HP = New_Form.HP
  Target.AC = New_Form.AC
  Target.Speed = New_Form.Speed
  Target.WRI = New_Form.WRI
  Target.Actions = New_Form.Actions
  
  # import Species                            # Will need to use this to apply the racial features such as WRI and Senses
  # Apply_Species(New_Form,Target.Species)

  if Effect.Meld_with_Weapons == True:
    Old_Weapons_Equipped = Target.Weapons_Equipped
    Target.Weapons_Equipped = []
  else:
    pass

  if Effect.Meld_with_Items == True:
    Old_Inventory = Target.Inventory
    Target.Inventory = {}
  else:
    pass

  # the question is how do I want to deal with c
  if Effect.Replace_Mental_Stats == False:
    pass
  else:
    Target.Int_Score = New_Form.Int_Score
    Target.Wis_Score = New_Form.Wis_Score
    Target.Cha_Score = New_Form.Cha_Score


  def End_Transformed_Effect(Target):
    Target.Str_Score = Old_Str
    Target.Dex_Score = Old_Dex
    Target.Con_Score = Old_Con
    Target.Int_Score = Old_Int
    Target.Wis_Score = Old_Wis
    Target.Cha_Score = Old_Cha

    Target.Size = Old_Size
    Target.Current_Hp = Old_HP
    Target.AC = Old_AC
    Target.Speed = Old_Speed
    Target.WRI = Old_WRI
    Target.Actions = Old_Actions
    Target.Bonus_Actions = Old_Bonus_Actions
    Target.Effects = Old_Effects
    Target.Free_Actions = Old_Free_Actions

    Target.Weapons_Equipped = Old_Weapons_Equipped
    Target.Inventory = Old_Inventory


#Modify_Information_Effect
class Modify_Information_Effect:
  def __init__(self,):
    self

#Arcane_Effect = Antimagic, Glyph, Symbol
class Arcane_Effect:
  def __init__(self,):
    self

#Dimensional_Effect
class Dimensional_Effect:
  def __init__(self,):
    self



# Illusory Effects
  # What types of illusory effects should be options?
    # Sound - Loud, Quiet
    # Image - 
    # perhaps I could quantify the "presence" of an illusion based on the level?
  # What are the purposes of an Illusion?
    # Scare Away
    # Lure
    # Gather Info
    # Restrain
    # Bluff
    # Concealment
    # Charm
  # What needs to be attributes of an Illusory_Effect?
    # What can the illusion produce? [Sound,Image,Temperature,Smell,Tactile]
    # Can the image change? Malleable = True,False
    # Which Creatures can Detect the Illusion? [Target_Only,Creatures,Any]



class Illusory_Effect:
  def __init__(self,Location,Senses_Produced,Malleable,Percievable_Type,Purpose):
    self.Location = Location
    self.Senses_Produced = Senses_Produced #[Sound,Image,Temperature,Smell,Tactile]
    self.Malleable = False
    self.Percievable_Type = Percievable_Type #[Target_Only,Creatures,Any]
    self.Purpose = Purpose # [Scare_Away,Lure,Gather_Info,Restrain,Bluff,Concealment,Charm]

  def Apply_Illusory_Effect(Effect,World):
    for Creature in World:
      if 'Truesight' in Creature.Senses.index():
        pass
      else: pass



#Terrain Effects
class Terrain_Effect:
  def __init__(self,Origin,Locations,AOE,Type):
    self.Origin = Origin
    self.Locations = Locations
    self.AOE = AOE
    self.Type = Type # ['Difficult','Normal','Air','Water','Occupied']

# Need something that considers AOE and Size

def Apply_Terrain_Effect(Effect):
  pass
  # will need to find each coordinate inside the area formed by the locations


# Move Effect
  # Should Teleport be a move_effect?
  # Move Effects need a couple of attributes:
    # Forced Movement = True,False
    # Distance
    # 
class Move_Effect:
  def __init__(self,World,Forced_Movement,Target,Caller,Distance,Direction,End_Location,Teleportation,Prompts_Opportunity_Attacks,Shunts_to_Nearest):
    self.World = World
    self.Forced_Movement = bool()
    self.Target = Target
    self.Caller = Caller
    self.Distance = Distance  # if distance is stored as [x,y,z]
    self.Direction = Direction  # "Away"
    self.End_Location = End_Location
    self.Teleportation = bool()
    self.Prompts_Opportunity_Attacks = bool()
    self.Shunts_to_Nearest = bool()

def Apply_Move_Effect(Effect):
  Target_First_Location = Effect.Target.Location 
  Difference_in_Locations = Effect.Caller.Location - Target_First_Location

  Movement_Through_Regular_Terrain = 0
  Movement_Through_Difficult_Terrain = 0

  if Effect.Direction == "Away":
    # now to find the direction they're facing
    if Difference_in_Locations[0] > 0:
      pass
    elif Difference_in_Locations[1] > 0:
      pass
    else: pass

  else: # the attacker will have to choose
    Choices = ['North','South','East','West','Up','Down']

  # if Teleportation is false, won't I have to check the terrain that a creature is passing through?
  if Effect.Teleportation == False:
    # need to check each coordinate between the start location and the end location
    for space in Effect.World.Space.index:
      if space.Coordinates >= Target_First_Location and space.Coordinates <= Effect.End_Location:  # need to adjust this later
        if space.Fill_Type == "Occupied":
          Movement_Through_Difficult_Terrain = Movement_Through_Difficult_Terrain + 1
        elif space.Fill_Type == "Unoccupied":
          Movement_Through_Regular_Terrain = Movement_Through_Regular_Terrain + 1
        else: pass
      else: pass

    
    pass





#Light_Effect
  # Darkness is considered a Light_Effect

class Light_Effect:
  def __init__(self,World,Locations,Type,Magical,Sunlight):    # does this need an area tag?
    self.World = World
    self.Locations = Locations
    self.Type = Type #['Bright','Dim','Darkness']
    self.Magical = bool()
    self.Sunlight = bool()

def Apply_Light_Effect(Effect):
  Effect.Location
  for i in Effect.World.Space:
    if i in Effect.Locations:
      Effect.World.Space[i].Light = Effect.Type
    else: pass


# Water Breathing Effect
class Adapted_Environment_Effect:
  def __init__(self,Target,Environment,Time):
    self.Target = Target
    self.Environment = Environment  # standard ones are 'Air', 'Suffocating', 'Water'
    self.Time = Time

def Apply_Adapted_Environment_Effect(Effect):
  # first need to try as if the environment already exists
  Old_Target_Environment_Time = Effect.Target.Adapted_Environment[Environment]
  #try:    
  Effect.Target.Adapted_Environment[Environment] = Effect.Time
  #except:
  #  Effect.Target.Adapted_Environment

  def Reset_Adapted_Environment_Effect():
    Effect.Target.Adapted_Environment[Environment] = Old_Target_Environment_Time

# Add Natural Weapons
class Add_Natural_Action_Effect:
  def __init__(self,Target,Action_Name,Use_Action_Function_Name,Action_Type,Action_Path,Damage_Dice,Damage_Dice_Number,Damage_Type):
    self.Target = Target
    self.Action_Name = Action_Name
    self.Use_Action_Function_Name = Use_Action_Function_Name
    self.Action_Type = Action_Type

    self.Action_Path = Action_Path # something similar to the Monster Actions spreadsheet

    self.Damage_Dice = Damage_Dice
    self.Damage_Dice_Number = Damage_Dice_Number
    self.Damage_Type = Damage_Type
    

  def Apply_Natural_Action_Effect(Effect):
    def Use_Action_Function_Name():
      #str(str(Effect.Action_Name),'_Effect') = Damage_Effect()
      pass
    Effect.Target.Actions[Effect.Action_Name] = Use_Action_Function_Name()




# Share Information
class Share_Information_Effect:
  def __init__(self,From,To):
    self.From = From
    self.To = To


# Create Magic Item (such as goodberry and magic stone)
class Create_Item_Effect:
  def __init__(self,Item_Name,Item_Needed,Replaces_Item,Duration,Placement_Type,Item_Type,Magic,Item_Weight,Charges,Recharge_Type,Item_Material,Item_HP,Item_AC,Item_Size,Added_Effects):
    self.Item_Name = Item_Name
    self.Item_Needed = Item_Needed
    self.Replaces_Item = bool()
    self.Duration = Duration
    self.Placement_Type = Placement_Type # is it spawned in a location or added to inventory?

    self.Item_Type = Item_Type  # Item_Types = []
    self.Magic = bool()
    self.Item_Weight = Item_Weight
    self.Charges = Charges
    self.Recharge_Type = Recharge_Type
    self.Item_Material = Item_Material
    self.Item_HP = Item_HP
    self.Item_AC = Item_AC
    self.Item_Size = Item_Size

    self.Added_Effects = []
    # Need something for creatures to be proficient with it

def Apply_Create_Item_Effect(Effect,Holder,Item_if_Needed):
  if Effect.Item_Needed == True:
    if Effect.Replaces_Item == True:
        Holder.Inventory.remove(Item_if_Needed)
    else:
        pass
  else:
    Holder.Inventory['Other'].append(Effect.Item_Name)


class Enchant_Item_Effect:
  def __init__(self,Item_Enchanted,Replaces_Item,Duration,AC,Attack_Bonus,Damage_Bonus,Bonus_Damage,Item_Material,Item_HP,Item_AC,Item_Size,Spell_Infused):
    self.Item_Enchanted = Item_Enchanted
    self.Replaces_Item = Replaces_Item
    
    self.Duration = Duration
    self.AC = AC
    self.Attack_Bonus = Attack_Bonus
    self.Damage_Bonus = Damage_Bonus
    self.Bonus_Damage = Bonus_Damage

    self.Item_Material = Item_Material
    self.Item_HP = Item_HP
    self.Item_AC = Item_AC
    self.Item_Size = Item_Size
    self.Spell_Infused = Spell_Infused


# Curses/Madness
  # how would I deal with certain curses/madnesses that require more categorical/narrative actions to take place...
  # perhaps I could monitor experience gained...



# Change_Appearance

# Improved_Crit
class Improved_Critical:
  def __init__(self,Extra_Damage_Dice,Bonus_Damage,Extra_Attack):
    self.Extra_Damage_Dice = Extra_Damage_Dice
    self.Bonus_Damage = Bonus_Damage
    self.Extra_Attack = Extra_Attack

# Increased_Crit
class Increased_Crit:
  def __init__(self,New_Crit_Values):
    self.New_Crit_Values = New_Crit_Values

  def Apply_Increased_Crit(Creature,Effect):
    Current_Crit_Range = Creature.Crit
    if Effect.New_Crit_Values in Current_Crit_Range:
      pass
    else:
      # I'm going to eventually need a for loop here that checks which numbers are or aren't in the list
      # but for now, I'm fine simply appending it
      Creature.Crit.append(Effect.New_Crit_Values)


# Gravity Shift
  # New Point
  # Do I need to define normal gravity conditions and fall damage?

# Summon_Effect
  # Creatures that can be summoned

class Summon_Effect:
  def __init__(self,Location,Creature_Options,Creature_Choice,Number_of_Summons):
    self.Location = Location        # should I do something where if there are multiple creatures, choose multiple locations?
                                    # and then I'll need to check if the space is unoccupied and contains enough size to fit
    self.Creature_Options = []
    self.Creature_Choice = Creature_Choice
    self.Number_of_Summons = Number_of_Summons

def Apply_Summon_Effect(Location,Creature_Choice):
  Creature_Choice.Location = Location


# Create Creature Effect: find familiar, find steed, find greater steed

class Create_Entity_Effect:
  def __init__(self,Location,):
    self.Location = Location


# Sense Effect
class Sense_Effect:
  def __init__(self,name):
    self.name = name






######################################################################

#Experimental_Elixer_Healing = Healing_Effect('Consume Potion','Creature','Instantaneous','True',4,2,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
#Second_Wind = Healing_Effect('Bonus Action','Self','Instantaneous','HP',10,1,Player_Character.level)
#Mote_Saving_Throw = Healing_Effect()

#Healing_Effect(,)
# Prerequisites: 'Consume Potion', 'Bonus Action'
  # Should the prerequisite be the function being called? What about when there's an object that calls the function? 
# Targets: 'Creature','Self'
# Duration: 'Instantaneous'
# Healing_Type: 'True','HP'
  # from here on out I think I'll use HP and Temp_HP
# Dice_Type: 4, 10
# Dice_Number: 2, 1
# Bonus: 'Int_Score', 'Level'



#Experimental_Elixir_Swiftness = Speed_Effect('Consume Potion','Creature','1_Hour','Walking',10,False)
#Experimental_Elixir_Flight = Speed_Effect('Consume Potion','Creature','10_Minutes','Flying',0,10)
#Fast_Movement_Effect = Speed_Effect('Passive','Self','Contingent','Any',10,False)

#Speed_Effect(,)
# Prerequisites: 'Consume Potion', 'Passive' 
# Targets: 'Creature','Self'
# Duration: '1_Hour', '10_Minutes', 'Contingent'
  # What does contingent mean in terms of applying the effect?
# Speed_Type: 'Walking', 'Flying', 'Any'
# Speed_Bonus: 10, 0
# Speed_Set: False, 10

Experimental_Elixir_Resilience = AC_Effect('Consume Potion','Creature','10_Minutes','Passive',1)


# Experimental_Elixir_Boldness = Buff_Bonus_Effect('Consume Potion','Creature','1_Minute','Attack Roll' or 'Saving Throw',4,1,0)
#Alchemical_Savant_Effect = Buff_Bonus_Effect(['Fire Damage','Necrotic Damage','Acid Damage','Poison Damage','Healing'],'Creature','Instantaneous','Roll Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
#Flash_of_Genius_Bonus = Buff_Bonus_Effect('Ability Check' or 'Saving Throw','Ally','Instantaneous','Buff Roll',0,0,Player_Character.Int_Score)
#Rage_Damage_Buff = Buff_Bonus_Effect('Attack Roll','Target','Instantaneous','Damage/Healing Roll',0,0,2) 
#Brutal_Critical1 = Buff_Bonus_Effect(['Attack Roll','Critical Hit'],'Target','Instantaneous','Increased Damage',False,1,False)
#Brutal_Critical2 = Buff_Bonus_Effect(['Attack Roll','Critical Hit'],'Target','Instantaneous','Increased Damage',False,2,False)
#Brutal_Critical3 = Buff_Bonus_Effect(['Attack Roll','Critical Hit'],'Target','Instantaneous','Increased Damage',False,3,False)
#Bardic_Inspiration_Effect = Buff_Bonus_Effect('Granted','Ally','10_Minutes',['Ability Check','Attack Roll','Saving Throw'],1,6,0) #should effects have a charge attribute?
#Aura_of_Protection_Bonus = Buff_Bonus_Effect('Saving Throw','Ally','Passive','Saving Throw',0,0,Bonus)
#Sneak_Attack_Effect = Buff_Bonus_Effect(['Attack Roll','Hit'],'Creature','Instantaneous','Damage',6,X,0)

#Buff_Bonus_Effect(,)
# Prerequisites: 'Consume Potion', ['Fire Damage','Necrotic Damage','Acid Damage','Poison Damage','Healing'], 'Ability Check' or 'Saving Throw','Attack Roll',['Attack Roll','Critical Hit'],'Granted','Saving Throw',['Attack Roll','Hit']
      # so is the list for AND or OR?
# Targets: 'Creature', 'Ally', 'Target'
# Durations: '1_Minute', 'Instantaneous', '10_Minutes', 'Passive'
# Buff_Types: 'Attack Roll' or 'Saving Throw', 'Roll Bonus', 'Buff Roll', 'Damage/Healing Roll', 'Increased Damage', 'Saving Throw', 'Damage' 
  # Definitely need to define the syntax of the functions
# Dice_Type: 4, 0, 6, 
# Dice_Number: 1, 0, False, X
  # Need to clarify the syntax of the functions
# Bonus: Int_Score, 0, 2, False, Bonus


Experimental_Elixir_Transformation = Spell_Effect('Consume Potion','Creature','10_Minutes','Alter Self',2,False)
#Mote_Attack_Roll = Spell_Effect()


Ancestral_Protectors_Attack_Debuff = Buff_Circumstance_Effect('Attack Rolls','Target','1 round','Attack Rolls','Disadvantage: ')
Rage_Athletics_Check_Buff = Buff_Circumstance_Effect('Ability Checks','Self','Instantaneous','Athletics Check','Advantage:')
Rage_Strength_Save_Buff = Buff_Circumstance_Effect('Saving Throws','Self','Instantaneous','Strength Saving Throw','Advantage:')
Danger_Sense = Buff_Circumstance_Effect('Saving Throws','Self','Instantaneous','Dexterity Saving Throw','Advantage: ')
Reckless_Attack = Buff_Circumstance_Effect('Attack Rolls','Self','Instantaneous','Attack Rolls','Advantage: ')
Feral_Instinct = Buff_Circumstance_Effect('Initiative Rolls','Self','Instantaneous','Initiative Rolls','Advantage: ')
Keen_Smell = Buff_Circumstance_Effect('Ability Check','Self','Instantaneous','Perception Check','Advantage: ')
Blinded = Buff_Circumstance_Effect('Attack Rolls','Self','Instantaneous','Attack Rolls','Disadvantage')
Poisoned = Buff_Circumstance_Effect(['Attack Rolls','Ability Checks'],'Self','Instantaneous',['Attack Rolls','Ability Checks'],'Disadvantage')

#Buff_Circumstance_Effect(,)

# Prerequisites: 'Attack Rolls', 'Ability Checks', 'Saving Throws', 'Initiative Rolls', ['Attack Rolls','Ability Checks']
# Target: 'Target', 'Self'
# Duration: '1 round', 'Instantaneous'
# Buff_Type: 'Attack Rolls', 'Athletics Check', 'Strength Saving Throw', 'Dexterity Saving Throw', 'Initiative Rolls', 'Perception Check', ['Attack Rolls','Ability Checks']
# Circumstance: 'Disadvantage: ', 'Advantage: ', 'Advantage:', 'Disadvantage'


#Indomitable = Buff_Replacement_Effect('Saving Throws','Self','Instantaneous','Replacement',Character_Functions.Saving_Throw(Player_Character,Score))
#Reliable_Talent_Effect = Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Placeholder',10)
Stroke_of_Luck_Ability_Check = Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Placeholder',20)
#Indomitable_Might = Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Strength Ability Check',Player_Character.Str_Score)
#Mote_Ability_Check = Buff_Replacement_Effect()
Relentless_Rage_Effect = Buff_Replacement_Effect('Gets Downed' and 'Raging','Self','Instantaneous','Healing',1)

#Buff_Replacement_Effect(,)
# Prerequisites: 'Saving Throws', 'Ability Check', 'Gets Downed' and 'Raging'
# Target: 'Self'
# Duration: 'Instantaneous'
# Buff_Type: 'Replacement', 'Placeholder', 'Strength Ability Check', 'Healing'
# Replacement: Saving_Throw(), 10, 20, Str_Score, 1