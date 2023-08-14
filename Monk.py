import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data
import Dice_Rolls
import Conditions

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll


# Monk
Monk = Establishing_Hierarchy.Class("Monk",8,["Wisdom", "Dexterity"],2,False,["Simple","Shortswords"],["Acrobatics","Athletics","History","Insight","Religion","Stealth"],False,False,["Shadows","OpenHand","Kensei","Mercy"],["Unarmored_Defense","Martial_Arts","Ki","Dedicated_Weapon","Unarmored_Movement","Deflect_Missiles","Slow_Fall","Extra_Attack","Stunning_Strikes","Evasion","Stillness_of_Mind","Unarmored_Movement_Improvement","Purity_of_Body","Tongue_of_the_Sun_and_Moon","Diamond_Soul","Timeless_Body","Empty_Body","Perfect_Self"],["Dexterity 13" and "Wisdom 13"],False,False,
{
  
})

def Monk_Starting_Skills(Player_Character):
  pass

def Monk_Add_Inventory(Player_Character):
  pass

def Monk_First_Level(Player_Character):
  Player_Character.Saving_Throws.append(Monk.Saving_Throws)
  Player_Character.Armor_Profs.append(Monk.Armor_Profs)
  Monk_Starting_Skills(Player_Character)
  Monk_Add_Inventory(Player_Character)

  Player_Character.Instrument_Profs.append(Monk.Tool_Profs)
  Player_Character.Weapon_Profs.append(Monk.Weapon_Profs)

#Unarmored_Defense
def Monk_Unarmored_Defense(Player_Character):
  Player_Character.Monk_Unarmored_Defense = 10 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score) + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score)
  


#Martial_Arts
def Martial_Arts_Attack():
  pass

def Martial_Arts(Player_Character):
  Player_Character.Bonus_Actions['Independent']['Martial_Arts'] = Martial_Arts_Attack


Monk_Martial_Arts_Dice = {
  'Level':          [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19],
  'Dice_Type':      [4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8,10,10,10],
  'Movement_Bonus': [0,10,10,10,10,15,15,15,15,20,20,20,20,25,25,25,25,30,30]
}



Monk_Weapons = []

#Ki
def Use_Flurry_of_Blows():
  pass

def Use_Patient_Defense():
  pass

def Use_Step_of_the_Wind1():
  pass

def Use_Step_of_the_Wind2():
  pass


def Ki(Player_Character):

  Player_Character.Class_Resources['Monk'] = {'Ki': Player_Character.Levels.count(Monk)}
  Player_Character.Class_Save_DCs['Monk'] = {
    'Ki_Save_DC': 8 + Player_Character.Prof_Bonus + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score)
  }

  Player_Character.Bonus_Actions['Independent']['Flurry of Blows'] = Use_Flurry_of_Blows()
  Player_Character.Bonus_Actions['Independent']['Patient Defense'] = Use_Patient_Defense()
  Player_Character.Bonus_Actions['Independent']['Step of the Wind'] = Use_Step_of_the_Wind1()
  Player_Character.Bonus_Actions['Independent']['Step of the Wind 2'] = Use_Step_of_the_Wind2()

  def Reset_Ki(Player_Character):
    Player_Character.Class_Resources['Monk']['Ki'] = Player_Character.Levels.count(Monk)

  Player_Character.Short_Rest_Options['Unlimited'] = Reset_Ki(Player_Character)
  Player_Character.Long_Rest_Options['Ki'] = Reset_Ki(Player_Character)



#Dedicated_Weapon
def Apply_Dedicated_Weapon(Player_Character):

  def Use_Dedicated_Weapon(Weapon):
    Player_Character.Inventory['Weapons']

    Weapon_Choice = input('Which Weapon: ')

    Monk_Weapons.append(Weapon_Choice)
    Player_Character.Class_Resources['Monk']['Ki'] = Player_Character.Class_Resources['Monk']['Ki'] - 1

  Player_Character.Short_Rest_Options['Charges']['Dedicated_Weapon'] = {
    'Action': Use_Dedicated_Weapon('Weapon'),
    'Charges': 1
  }

#Unarmored_Movement
def Monk_Unarmored_Movement(Player_Character):
  pass


#Deflect_Missiles
def Apply_Deflect_Missiles(Player_Character):
  def Use_Deflect_Missiles(Player_Character):
    Effects.Buff_Bonus_Effect(Current_Enemy_Damage_Roll,'Instantaneous','Damage Debuff',1,10,Player_Character.Levels.count(Monk))

  def Use_Deflect_Missiles_Throw(Player_Character):
    
    Player_Character.Class_Resources['Monk']['Ki'] = Player_Character.Class_Resources['Monk']['Ki'] - 1

  Player_Character.Reactions['Self_Being_Attacked'] = {'Ranged_Attack_Roll': {'Deflect_Missiles': Use_Deflect_Missiles(Player_Character)}}


  Player_Character.Free_Actions['Dependent'] = {'Deflect Missile': Use_Deflect_Missiles_Throw(Player_Character)}



#Slow_Fall
def Use_Slow_Fall(Player_Character):
  Slow_Fall_Damage_Reduction = Effects.Buff_Bonus_Effect(Current_Enemy_Damage_Roll,'Instantaneous','Damage Reduction',0,0,Player_Character.Levels.count(Monk))

def Apply_Slow_Fall(Player_Character):
  Player_Character.Reactions['Fall_Damage'] = {'Slow_Fall': Use_Slow_Fall(Player_Character)}


#Stunning_Strikes
#def Apply_Stunning_Strikes(Player_Character):
#  def Use_Stunning_Strikes(Current_Allied_Attack_Roll):
#    #if Dice_Rolls.Roll_Dice(1,20) + Establishing_Hierarchy.abilityScoreToModifier(Current_Allied_Attack_Roll.Attack_Target.Wis_Score) <= Player_Character['Class_Save_DCs']['Ki_Save_DC']:
#    Conditions.Stun(Current_Allied_Attack_Roll.Attack_Target)

#    Player_Character.Class_Resources['Monk']['Ki'] = Player_Character.Class_Resources['Monk']['Ki'] - 1

#  Player_Character.Effects['Self_Attacking']['Stunning_Strike'] = Use_Stunning_Strikes(Current_Allied_Attack_Roll)


#Evasion
def Apply_Evasion(Player_Character):
  Evasion_Effect = Effects.Buff_Replacement_Effect('None',Current_Enemy_Damage_Roll,'Instantaneous','Damage Reduction',Current_Enemy_Damage_Roll/2)
  Player_Character.Effects['Self_Saving_Throws'] = {'Dexterity': Use_Evasion(Current_Enemy_Damage_Roll)}

  def Use_Evasion(Current_Enemy_Damage_Roll):
    Effects.Apply_Buff_Replacement_Effect(Evasion_Effect,False,False,Current_Enemy_Damage_Roll)

#Stillness_of_Mind
def Apply_Stillness_of_Mind(Player_Character):
  Player_Character.Actions['Stillness_of_Mind'] = Use_Stillness_of_Mind(Player_Character)



def Use_Stillness_of_Mind(Player_Character):
  if 'charmed' in Player_Character.Active_Conditions['Self']:
    Player_Character.Active_Conditions['Self'].remove('charmed')

  if 'frightened' in Player_Character.Active_Conditions['Self']:
    Player_Character.Active_Conditions['Self'].remove('frightened')


#Unarmored_Movement_Improvement
def Unarmored_Movement_Improvement(Player_Character):
  pass


#Purity_of_Body
# immunity to disease, poison, and poisoned conditions
def Apply_Purity_of_Body(Player_Character):
  Player_Character.WRI.append('poisonimmu')
  Player_Character.WRI.append('poisonedimmu')
  Player_Character.WRI.append('diseaseimmu')

#Tongue_of_the_Sun_and_Moon
def Apply_Tongue_of_the_Sun_and_Moon(Player_Character):
  pass

#Diamond_Soul
def Apply_Diamond_Soul(Player_Character):
  Player_Character.Saving_Throws.append("Strength")
  Player_Character.Saving_Throws.append("Constitution")
  Player_Character.Saving_Throws.append("Intelligence")
  Player_Character.Saving_Throws.append("Charisma")
  Player_Character.Saving_Throws.append("Death")

  def Use_Diamond_Soul(Player_Character):
    Effects.Apply_Buff_Replacement_Effect(Diamond_Soul_Effect,False,False,Current_Allied_Saving_Throw)

  Player_Character.Effects['Self_Saving_Throw'] = Use_Diamond_Soul(Player_Character)                                                         # needs updating

  Diamond_Soul_Effect = Effects.Buff_Replacement_Effect('None',Current_Allied_Saving_Throw,'Instantaneous','Reroll','Placeholder')


#Timeless_Body
def Apply_Timeless_Body(Player_Character):
  pass

# perhaps I could do ageimmu
# but what about not needing food or water?

#Empty_Body
def Empty_Body(Player_Character):
  Player_Character.Per_Use_Spells['1/long rest'].append("Astral_Projection")                     # need to be able to cast with Ki points



#Perfect_Self



def Choose_Subclass(Player_Character):
  pass


def Monk_Level_One(Player_Character):
  Monk_Unarmored_Defense(Player_Character)
  Martial_Arts(Player_Character)

def Monk_Level_Two(Player_Character):
  Ki(Player_Character)
  Apply_Dedicated_Weapon(Player_Character)
  Monk_Unarmored_Movement(Player_Character)

def Monk_Level_Three(Player_Character):
  Apply_Deflect_Missiles(Player_Character)

def Monk_Level_Four(Player_Character):
  Apply_Slow_Fall(Player_Character)
  Character_Functions.ASI(Player_Character)

def Monk_Level_Five(Player_Character):
  Character_Functions.Extra_Attack(Player_Character)
 # Apply_Stunning_Strikes(Player_Character)

def Monk_Level_Six(Player_Character):
  pass

def Monk_Level_Seven(Player_Character):
  Apply_Stillness_of_Mind(Player_Character)

def Monk_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)

def Monk_Level_Nine(Player_Character):
  Apply_Purity_of_Body(Player_Character)

def Monk_Level_Ten(Player_Character):
  pass

def Monk_Level_Eleven(Player_Character):
  pass

def Monk_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Monk_Level_Thirteen(Player_Character):
  pass

def Monk_Level_Fourteen(Player_Character):
  Apply_Diamond_Soul(Player_Character)

def Monk_Level_Fifteen(Player_Character):
  pass

def Monk_Level_Sixteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Monk_Level_Seventeen(Player_Character):
  pass

def Monk_Level_Eighteen(Player_Character):
  pass

def Monk_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Monk_Level_Twenty(Player_Character):
  pass


def Run_Monk(Player_Character,Level):
  if Player_Character.First_Class == Monk:
    Monk_First_Level(Player_Character)
  else:
    pass


  Level = Player_Character.Levels.count(Monk)
  if Level >= 1:
    Monk_Level_One(Player_Character)
#    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Monk_Level_Two(Player_Character)
      if Level >= 3:
        Monk_Level_Three(Player_Character)
        if Level >= 4:
          Monk_Level_Four(Player_Character)
          if Level >= 5:
            Monk_Level_Five(Player_Character)
            if Level >= 6:
              Monk_Level_Six(Player_Character)
              if Level >= 7:
                Monk_Level_Seven(Player_Character)
                if Level >= 8:
                  Monk_Level_Eight(Player_Character)
                  if Level >= 9:
                    Monk_Level_Nine(Player_Character)
                    if Level >= 10:
                      Monk_Level_Ten(Player_Character)
                      if Level >= 11:
                        Monk_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Monk_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Monk_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Monk_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Monk_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Monk_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Monk_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Monk_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Monk_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Monk_Level_Twenty(Player_Character)
  else:
    pass




## Monks
#Shadow_Arts

Shadow_Arts_Table = {
  'Spell':   ['Minor_Illusion','Pass_Without_Trace','Darkness'],
  'Ki_Cost': [               0,                   2,         2]
}

def Apply_Shadow_Arts(Player_Character):
  pass

#Shadow_Step
def Apply_Shadow_Step(Player_Character):
  Player_Character.Bonus_Action['Independent']['Shadow_Step'] = Use_Shadow_Step

def Use_Shadow_Step(Player_Character):
  pass

#Cloak_of_Shadows

#Opportunist

#Path_of_the_Kensei 
#One_with_the_Blade 
#Sharpen_the_Blade 
#Unerring_Accuracy 

#Open_Hand_Technique 
#Wholeness_of_Body 
#Tranquility 
#Quivering_Palm 

#Implements_of_Mercy 
#Hand_of_Healing 
#Hand_of_Harm 
#Physicians_Touch 
#Flurry_of_Healing_and_Harm 
#Hand_of_Ultimate_Mercy 

Shadow = Establishing_Hierarchy.Subclass(Monk,'Shadow',[],False)
Mercy = Establishing_Hierarchy.Subclass(Monk,'Mercy',[],False)
Open_Hand = Establishing_Hierarchy.Subclass(Monk,'Open Hand',[],False)
Kensei = Establishing_Hierarchy.Subclass(Monk,'Kensei',[],False)
Astral_Self = Establishing_Hierarchy.Subclass(Monk,'Astral Self',[],False)

Monk_Subclasses = [Shadow,Mercy,Open_Hand,Kensei,Astral_Self]
Monk.Subclasses = Monk_Subclasses