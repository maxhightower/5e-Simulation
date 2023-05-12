from random import randrange
import numpy as np


class Roll:
  def __init__(self,Entity_Making):
    self.Entity_Making = Entity_Making
    self.Dice_Type = 20
    self.Dice_Number = 1
    self.Modifiers = []
    
    #self.Roll_Type = Roll_Type    # ['Attack Roll', 'Ability Check', 'Saving Throw']

class Ability_Check(Roll):
  def __init__(self,Entity_Making,Score,Skill,Contested_Entity,Modifiers):
    super().__init__(Entity_Making)
    self.Score = Score
    self.Skill = Skill
    self.Contested = bool
    self.Contested_Entity = Contested_Entity
    self.Modifiers = Modifiers

class Attack_Roll(Roll):
  def __init__(self,Entity_Making,Attack_Type,Attack_Target,Modifiers):
    super().__init__(Entity_Making)
    self.Attack_Type = Attack_Type    # ['Weapon', 'Ability', 'Spell']
    self.Attack_Target = Attack_Target
    self.Modifiers = Modifiers

  # if it's a Weapon Attack
    #self.Weapon = Weapon
    #self.Target = Target

  # if it's an Ability
    #self.


  # if it's a Spell Attack

class Saving_Throw(Roll):
  def __init__(self,Entity_Making,Score,Entity_Imposing,DC,Modifiers):
    super().__init__(Entity_Making)
    self.Score = Score
    self.Entity_Imposing = Entity_Imposing
    self.DC = DC
    self.Modifiers

class Damage_Roll(Roll):
  def __init__(self,Entity_Taking_Damage,Entity_Causing_Damage,Modifiers,Dice_Num,Dice_Type,Damage_Type):
    self.Entity_Taking_Damage = Entity_Taking_Damage
    self.Entity_Causing_Damage = Entity_Causing_Damage
    self.Modifiers = Modifiers

def Run_Roll(Roll):
  for i in Roll.Modifiers:
    pass

  if Roll == Damage_Roll:
    Roll_Dice(Roll.Dice_Number,Roll.Dice_Type)

    if str(Roll.Damage_Type,'res') in Roll.Entity_Taking_Damage.WRI:
      pass
    elif str(Roll.Damage_Type,'immu') in Roll.Entity_Taking_Damage.WRI:
      pass
    elif str(Roll.Damage_Type,'vul') in Roll.Entity_Taking_Damage.WRI:
      pass
    else: pass

  elif Roll == Saving_Throw:
    Roll_Dice(Roll.Dice_Number,Roll.Dice_Type)


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


Current_Allied_Ability_Check = Ability_Check('Placeholder','Placeholder','Placeholder','Placeholder',[])
Current_Allied_Attack_Roll = Attack_Roll('Placeholder','Placeholder','Placeholder',[])
Current_Allied_Saving_Throw = Saving_Throw('Placeholder','Placeholder','Placeholder','Placeholder',[])
Current_Allied_Damage_Roll = Damage_Roll('Placeholder','Placeholder',[],'Placeholder','Placeholder','Placeholder')

Current_Enemy_Ability_Check = Ability_Check('Placeholder','Placeholder','Placeholder','Placeholder',[])
Current_Enemy_Attack_Roll = Attack_Roll('Placeholder','Placeholder','Placeholder',[])
Current_Enemy_Saving_Throw = Saving_Throw('Placeholder','Placeholder','Placeholder','Placeholder',[])
Current_Enemy_Damage_Roll = Damage_Roll('Placeholder','Placeholder',[],'Placeholder','Placeholder','Placeholder')



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

# rolling any given number of dice for any type??? Assuming I can do that
def Roll_Dice(Number_of_Dice,Dice_Type):
  return randrange(Number_of_Dice,Number_of_Dice * Dice_Type,1)




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


def Choose_Target(Creature,World):
  
  if Creature in World:
    Target = World[randrange(0,len())]

    # need to check to make sure that we're not targeting ourselves
#    if monster_instances[Target].Instance == monster_instances[Creature].Instance and monster_instances[Target].Monster_ID == monster_instances[Creature].Monster_ID
    if Target == Creature:
      #will need to turn this into a more efficient code eventually, I just don't know how to do that right now
      Target = World[randrange(0,len())]
      return Target
    else:
      pass

  else:
    pass
# how should choosing a target work? should it really be random?
# perhaps this should be based on the payoff matrix instead of simply a function
# where it chooses both the action, bonus action, movement, and target that has the highest payoff



# Need to add this to the new attack function
# where this checks if the target has a condition that grants advantage or disadvantage
# and then if both are in play, they cancel out
def Check_Target_Conditions(Target,Player_Character):
  if 'Restrained' in Target.Conditions:
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
  

