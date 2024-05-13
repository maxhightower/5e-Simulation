import random
from random import randrange
import numpy as np

# ------------------------------- Defining the Dice Rolling Part ------------------------------- #
############ First to create a way to roll dice ############

# rolling any given number of dice for any type
def Roll_Dice(Number_of_Dice,Dice_Type):
  roll_results = []
  for i in range(Number_of_Dice):
    roll_results.append(randrange(1,Dice_Type))
  print(roll_results)
  return roll_results.sum()



############ Defining the Main d20_Roll Class and Subclasses ##################

class Roll:
  def __init__(self,Entity_Making,Dice_Type,Dice_Number):
    self.Entity_Making = Entity_Making

    self.Dice_Type = Dice_Type
    self.Dice_Number = Dice_Number

    self.Modifiers = {            # currently debating how these modifiers should work
      'Circumstances': [],
      'Bonus': [],
      'Penalties': []
    }
    
class d20_Roll(Roll):
  def __init__(self,Entity_Making,Dice_Type,Dice_Number):
    super().__init__(Entity_Making,Dice_Type,Dice_Number)
    self.Dice_Type = 20
    self.Dice_Number = 1

class Damage_Roll(Roll):
  def __init__(self,Dice_Type,Dice_Number,Entity_Making,Entity_Taking_Damage,Entity_Causing_Damage,Modifiers,Damage_Types):
    super().__init__(Entity_Causing_Damage,Dice_Type,Dice_Number)

    self.Entity_Taking_Damage = Entity_Taking_Damage
    self.Entity_Causing_Damage = Entity_Causing_Damage

    self.Modifiers = Modifiers
    self.Damage_Types = Damage_Types

    # final damage???


class Ability_Check(d20_Roll):
  def __init__(self,Dice_Type,Dice_Number,Entity_Making,Ability_Score,Skill_Type,Contested,Contested_Entity,Contested_Score,Contested_Skill,Modifiers):
    super().__init__(Entity_Making,Dice_Type,Dice_Number)

    self.Ability_Score = Ability_Score
    self.Skill_Type = Skill_Type
    
    self.Contested = bool()
    
    self.Contested_Entity = Contested_Entity
    self.Contested_Score = Contested_Score
    self.Contested_Skill = Contested_Skill

    self.Modifiers = Modifiers
    self.Circumstances = []

class Saving_Throw(d20_Roll):
  def __init__(self, Entity_Making, Save_Type, Entity_Imposing, DC, Modifiers):
    super().__init__(Entity_Making, Entity_Imposing, DC)
    self.Save_Type = Save_Type  # this is better than "Score" because Death saves don't include a score but some creatures get proficiency in them regardless
    self.Entity_Imposing = Entity_Imposing
    self.DC = DC
    self.Modifiers = Modifiers

    self.Circumstances = []


class Attack_Roll(d20_Roll):
  def __init__(self,Entity_Making,Attack_Target,Modifiers):
    super().__init__(Entity_Making, Attack_Target, Modifiers)
    self.Attack_Target = Attack_Target
    self.Modifiers = Modifiers
    self.Dice_Number = 1
    self.Dice_Type = 20
    self.Circumstances = []
    # the Attack Roll defines the Damage Roll 

    # the rolls need to be able to store Adv and Dis

################# Defining the Subclasses of Attack_Roll #####################
class Spell_Attack_Roll(Attack_Roll):
  def __init__(self,Entity_Making,Attack_Target,Modifiers,Spell):
    super().__init__(Entity_Making,Attack_Target,Modifiers)
    self.Spell = Spell
    self.Dice_Number = 1
    self.Dice_Type = 20

    # would this benefit from having the spell attribute?
    # what parts of the game would this require this?
        # any monster with Limited Magic Immunity will need to know the Spell Level
        # Counterspell

class Weapon_Attack_Roll(Attack_Roll):
  def __init__(self,Entity_Making,Attack_Target,Modifiers,Weapon):
    super().__init__(Entity_Making,Attack_Target,Modifiers)
    self.Weapon = Weapon
    self.Dice_Number = 1
    self.Dice_Type = 20

    def Define_Damage_Roll(Weapon_Attack_Roll):
      Damage_Roll(Weapon_Attack_Roll.Attack_Target,
                  Weapon_Attack_Roll.Entity_Making,
                  Weapon_Attack_Roll.Modifiers,
                  {
                    str(Weapon_Attack_Roll.Weapon.Damage_Type): [Weapon_Attack_Roll.Weapon.Dice_Type,Weapon_Attack_Roll.Weapon.Dice_Num]
                  }
                  )

class Ability_Attack_Roll(Attack_Roll):
  def __init__(self,Entity_Making,Attack_Target,Modifiers,Ability):
    super().__init__(Entity_Making,Attack_Target,Modifiers)
    self.Ability = Ability  # still not convinced about this one
    self.Dice_Number = 1
    self.Dice_Type = 20


###################### Defining How a Dice Roll is RUN ##########################

def Run_Roll(Roll):
  for i in Roll.Modifiers:
    pass

  if Roll == Damage_Roll:
    dice_roll = Roll_Dice(Roll.Dice_Number,Roll.Dice_Type)

    for i in Roll.Damage:
      if str(Roll.Damage_Type,'res') in Roll.Entity_Taking_Damage.WRI:
        dice_roll = dice_roll / 2
      elif str(Roll.Damage_Type,'immu') in Roll.Entity_Taking_Damage.WRI:
        dice_roll = 0
      elif str(Roll.Damage_Type,'vul') in Roll.Entity_Taking_Damage.WRI:
        dice_roll = dice_roll * 2

  elif Roll == Saving_Throw:
    Roll_Dice(Roll.Dice_Number,Roll.Dice_Type)
    Roll.Entity_Imposing
    Roll.Entity_Making

  elif Roll == Attack_Roll:
    Roll_Dice(Roll.Dice_Number,Roll.Dice_Type)


  elif Roll == Ability_Check:
    Roll_Dice(Roll.Dice_Number,Roll.Dice_Type)

    if Roll.Contested_Entity != False:
      pass
    else: pass

  else:
    pass



def Summarize_Roll(Roll):
  pass



def Reset_Current_Roll(Roll):
  for i in dir(Roll):
    dir(Roll)[i] = 'Placeholder'
  Roll.Dice_Type = 20
  Roll.Dice_Number = 1
  Roll.Modifiers = []


#---------------------------------- Creating Current Checks for Game State ---------------------------------- #

Current_Allied_Ability_Check = Ability_Check('Dice_Type',
                                             'Dice_Number',
                                             'Entity_Making',
                                             'Ability_Score',
                                             'Skill_Type',
                                             False,
                                             'Contested_Entity',
                                             'Contested_Score',
                                             'Contested_Skill',
                                              [])

Current_Allied_Attack_Roll = Attack_Roll('Entity_Making','Attack_Target',[])

Current_Allied_Saving_Throw = Saving_Throw('Entity_Making',
                                           'Save_Type',
                                           'Entity_Imposing',
                                           'DC',
                                           [])

Current_Allied_Damage_Roll = Damage_Roll('Dice_Type',
                                         'Dice_Number',
                                         'Entity_Making',
                                         'Entity_Taking_Damage',
                                         'Entity_Causing_Damage',
                                         [],
                                         [])

Current_Enemy_Ability_Check = Ability_Check('Dice_Type',
                                            'Dice_Number',
                                            'Entity_Making',
                                            'Ability_Score',
                                            'Skill_Type',
                                            False,
                                            'Contested_Entity',
                                            'Contested_Score',
                                            'Contested_Skill',
                                            [])


Current_Enemy_Attack_Roll = Attack_Roll('Entity_Making',
                                        'Attack_Target',
                                        [])

Current_Enemy_Saving_Throw = Saving_Throw('Entity_Making','Save_Type','Entity_Imposing','DC',[])
Current_Enemy_Damage_Roll = Damage_Roll('Dice_Type','Dice_Number','Entity_Making','Entity_Taking_Damage','Entity_Causing_Damage',[],[])



##### Defining the Dice Rolling Part
# normal
def d20():
  x = randrange(1,20)
  return x
  print(x)

# advantage
def d20_Advantage():
  x = randrange(1,20)
  y = randrange(1,20)
  result = max(x,y)
  print(x,y)
  return result

# disadvantage
def d20_Disadvantage():
  x = randrange(1,20)
  y = randrange(1,20)
  result = min(x,y)
  print(x,y)
  return result


def Average_Roll(Number_of_Dice,Dice_Type,Bonus,Bonus2):
  #total = 0
  #for i in range(len(Effects.keys())):
  #  total = total + Effects[Effects.keys()[i]]

  if type(Bonus2) == int:
    Bonus2_Num = Bonus2
  else:
    Bonus2_Num = Bonus2.Bonus

  #print('In Average Roll:',Number_of_Dice)
  sequence_B = [Dice_Type,1]
  sequence = [Number_of_Dice * (sum(sequence_B)/2),Bonus,Bonus2_Num]
  return sum(sequence)




##### Defining Ability Checks
### So what needs to go into an ability check? 
# Obviously it needs to tell if the creature has circumstances such as advantage or disadvantage
# Certain, common ability checks have defined proficiencies, which are independent of ability scores
# And there are certain things that let the creature choose the skill that is used in the contested check
# There's no proficiency, proficiency, half proficiency, and expertise
# And then any bonuses or replacements it can use
# There are also custom skills but I can get into that later...

# I may need to add some features that tag certain ability checks based on Sight, Sound, and whatnot so that Blinded, Deafened, and what not can be applied






##### Defining Attacks and Attack Rolls
# What's making this Attack Action and Attack Roll stuff so difficult?
# Well for starters, there's different kinds of attacks: melee weapon, ranged weapon, spells, target, aoe, etc.
# And so for a creature to attack, after choosing to attack, they need to decide HOW and WHO
# how many enemies is the creature facing? do they attack one at a time or rely on their aoe if available? 
# then the procedure for each specific attack has to commence
# And then there's conditions, and effects, and what not

# perhaps the best option is to create a class for Actions and then to define them...but then having a subclass as a callable function...


# I could make a payoff matrix based that assigns weighted probabilities to certain actions based on ability scores and actions available




Action_Types = ['Normal_Melee_Weapon','Natural_Melee_Weapon','Normal_Ranged_Weapon','Natural_Ranged_Weapon',]

class Action:
  def __init__(self,Name,Type,Method):
    self.Name = Name
    self.Type = Type            
    self.Method = Method

class Attack:
  def __init__(self,Name,Type,Method):
    self.Name = Name
    self.Type = Type
    self.Method = Method
    self.Magical = False

class Weapon_Attack(Attack):
  def __init__(self,Name,Type,Method,Creature,Weapon,Magical):
    super().__init__(Name,Type,Method)
    self.Creature = Creature
    self.Weapon = Weapon
    self.Weapon_Size = 'Medium'
    self.Magical = Magical
    # range
    # extra damage
    # weapon variant

class Natural_Weapon(Attack):
  def __init__(self,Name,Type,Method,Creature,Weapon,Weapon_Size,Magical):
    super().__init__(Name,Type,Method)           


# Something that I just realized is that not all actions from Creatures_and_Actions are attacks
# meaning that in theory I could define actions...or attacks...
# except that some Target effects are used in multiattacks, so even if they're not attacks, they get treated as them...


def Choose_Target_Offense(Actor,Combat_Situation):
  # randomly choose a creature in the list Combat_Situation that isn't Actor
  target = random.choice(Combat_Situation)
  return target

def Choose_Target_Support(Actor,Combat_Situation):
  # randomly choose a creature in the list Combat_Situation that isn't Actor
  target = np.random.choice(Combat_Situation)
  return target

# Need to add this to the new attack function
# where this checks if the target has a condition that grants advantage or disadvantage
# and then if both are in play, they cancel out
def Check_Target_Conditions(Actor,Target):
  if 'Restrained' in Target.Conditions['Self']:
    # restrained results in attacks against target having advantage and disadvantage on dexterity saves
    pass

  elif 'Grappled' in Target.Conditions:
    pass

  elif 'Prone' in Target.Conditions:
    pass

  elif 'Blind' in Target.Conditions:
    #Player_Character.Circumstances
    pass
  elif 'Invisible' in Target.Conditions:
    pass

  elif 'Paralyzed' in Target.Conditions:
    pass

  elif 'Petrified' in Target.Conditions:
    pass
  
  elif 'Stunned' in Target.Conditions:
    pass
  
  elif 'Unconcsious' in Target.Conditions:
    pass

  elif 'Charmed' in Target.Conditions:
    pass

  elif 'Frightened' in Target.Conditions:
    pass

  else:
    pass
  

