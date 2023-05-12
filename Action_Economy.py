import Establishing_Hierarchy as h
import Effects
import Dice_Rolls
import Conditions
import Character_Functions
import Monsters
import random
from random import randrange
import pandas as pd


def Check_Object(Object):
  if hasattr(Object, '__class__') == True:
    return str(type(Object))[17:33]
  else:
    return False

def Choose_Target(Creature,World,p):        # putting p there is a temporary solution and needs to be removed later
  
  if Creature in World:
    Target = World[randrange(0,len(p))]

    # need to check to make sure that we're not targeting ourselves
#    if monster_instances[Target].Instance == monster_instances[Creature].Instance and monster_instances[Target].Monster_ID == monster_instances[Creature].Monster_ID
    if Target == Creature:
      #will need to turn this into a more efficient code eventually, I just don't know how to do that right now
      Target = World[randrange(0,len(p))]
      return Target
    else:
      pass

  else:
    pass


def Take_Action(Creature,World):
  if Check_Object(Creature) == 'Player_Character':
    Action = Creature.Actions[random.randrange(0,len(Creature.Actions))]
    print(Action)
    return(Action)
  else:
    Action = Creature.Actions[random.randrange(0,len(Creature.Actions))]
    Choose_Target(Creature,World)
  #print(Target)
  print(Action)
  #return(Target)
  return(Action)



def Take_Bonus_Action(Creature):
  if Check_Object(Creature) == 'Player_Character':
    Bonus_Action = Creature.Bonus_Actions[random.randrange(0,len(Creature.Bonus_Actions))]
    print(Bonus_Action)
    return(Bonus_Action)
  else:
    Bonus_Action = Creature.Bonus_Actions[random.randrange(0,len(Creature.Bonus_Actions))]
    print(Bonus_Action)
    return(Bonus_Action)


def Take_Reaction(Creature):
  if Check_Object(Creature) == 'Player_Character':
    Reaction = Creature.Reactions[random.randrange(0,len(Creature.Reactions))]
    print(Reaction)
    return(Reaction)
  else:
    Reaction = Creature.Reactions[random.randrange(0,len(Creature.Reactions))]
    print(Reaction)
    return(Reaction)




# Creating a round in initiative
def Turns_in_Initiative(Party):
  Turns_in_Initiative = 0
  for Creature in Party:
    Turns_in_Initiative = Turns_in_Initiative + 1
  print("Turns in Combat:",Turns_in_Initiative)

def Initiative_Modifiers(Party):
  for Creature in Party:
    print(Creature,h.abilityScoreToModifier(Monsters.monster_primes[Creature].Dex_Score))



def Roll_Initiative(Party):
  Initiative_Order = {'Creatures': [],
                    'Initiatives': []}
  Runnable_Initiative_Order = []
  for Creature in Party:
    if Check_Object(Creature) == 'Player_Character':
      Roll = random.randrange(1,20) + h.abilityScoreToModifier(Creature.Dex_Score)
      Initiative_Order['Creatures'].append(Creature.Name)
      Initiative_Order['Initiatives'].append(Roll)
    else:
      Roll = random.randrange(1,20) + h.abilityScoreToModifier(Monsters.monster_primes[Creature].Dex_Score)
      Initiative_Order['Creatures'].append(Creature)
      Initiative_Order['Initiatives'].append(Roll)
    df = pd.DataFrame(Initiative_Order)
  df = pd.DataFrame.nlargest(df, 30, 'Initiatives',keep='first')
  print(df)
  Runnable_Initiative_Order = df['Creatures'].tolist()
  return Runnable_Initiative_Order


def Take_Turn(Creature):
  Take_Action(Creature)
  Take_Bonus_Action(Creature)

def Combat_Round(Party):
  Runnable_Initiative_Order = []
  x = Turns_in_Initiative(Party)
  Roll_Initiative(Party)
  Turn = {'Creature': [],'Action': [],'Bonus Action': []}
  for Creature in Runnable_Initiative_Order:
    Action = Take_Action(Creature)
    Bonus_Action = Take_Bonus_Action(Creature)
    Turn.update({'Creature': Creature})   #['Creature'][Creature] = Creature
    Turn.update({'Action': Action})   #['Action'][Creature] = Action
    Turn.update({'Bonus Action': Bonus_Action})   #['Bonus Action'][Creature] = Bonus_Action
  print(Turn)
