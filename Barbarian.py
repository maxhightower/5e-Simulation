import Establishing_Hierarchy
import Effects
import Character_Functions
import Character_Actions
from random import randrange
import Dice_Rolls
import Conditions
import Armor_and_Weapons


from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll



# (a) a greataxe or (b) any martial melee weapon
# (a) two handaxes or (b) any simple weapon
# An explorer's pack, and four javelins
# Alternatively, you may start with 2d4 × 10 gp to buy your own equipment.

Armor = []
Weapons = ['Greataxe','Javelin','Javelin','Javelin','Javelin','Handaxe','Handaxe'] #,['Greataxe','Javelin','Javelin','Javelin','Javelin','Simple Weapon'],['Martial Melee Weapon','Javelin','Javelin','Javelin','Javelin','Handaxe','Handaxe'],['Martial Melee Weapon','Javelin','Javelin','Javelin','Javelin','Simple Weapon']]
Packs = ["Explorer's Pack"]
Instruments = []
Tools = []
Focus = []
Gold = ['5d4']

# Barbarian
Barbarian = Establishing_Hierarchy.Class("Barbarian",12,['Constitution', 'Strength'],2,["Light","Medium","Shields"],["Simple","Martial"],["Animal_Handling","Athletics","Intimidation","Nature","Perception","Survival"],False,False,['Berserker'],["Rage","Unarmored Defense","Danger Sense","Reckless Attack","Extra Attack","Fast Movement","Feral Instinct","Brutal Critical","Relentless Rage","Brutal Critical","Persistent Rage","Brutal Critical","Indomitable Might","Primal Champion"],"Strength 13",False,False,
{
  'Armor': Armor,
  'Weapons': Weapons,
  'Tools': Tools,
  'Instruments': Instruments,
  'Packs': Packs,
  'Focus': Focus,
  'Gold_Alternative': Gold
})


def Barbarian_First_Level(Player_Character):
  Player_Character.Saving_Throws.append('Constitution')
  Player_Character.Saving_Throws.append('Strength')

  Barbarian_Add_Inventory(Player_Character)
  Barbarian_Starting_Skills(Player_Character)


def Barbarian_Add_Inventory(Player_Character):
  # step one: choose items or gold
  # lets assume items for now
  # no armor, so the next step is weapons
  
  Player_Character.Weapon_Equipped.append(Armor_and_Weapons.Greataxe)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Javelin)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Javelin)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Javelin)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Javelin)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Handaxe)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Handaxe)
  
  #for i in Barbarian.Starting_Equipment['Weapons']:      #[randrange(0,len(Barbarian.Starting_Equipment['Weapons']))]:
  #  # eventually I'll need to add a way for a player to choose the weapons
  #  if i == 'Simple Weapon':
  #    Player_Character.Inventory['Weapons'].append('Greatclub')   #Armor_and_Weapons.Simple_Weapons[randrange(0,len(Armor_and_Weapons.Simple_Weapons),1)]
  #  elif i == 'Martial Weapon':
  #    Player_Character.Inventory['Weapons'].append('Battleaxe')   #Armor_and_Weapons.Martial_Weapons[randrange(0,len(Armor_and_Weapons.Martial_Weapons),1)]
  #  elif i == 'Martial Melee Weapon':
  #    Player_Character.Inventory['Weapons'].append('Greatsword')   #Armor_and_Weapons.Martial_Melee_Weapons[randrange(0,len(Armor_and_Weapons.Martial_Melee_Weapons),1)]
  #  else:
  #    Player_Character.Inventory['Weapons'].append(i)

  Player_Character.Inventory['Packs'] += Barbarian.Starting_Equipment['Packs']

# Skills
def Barbarian_Starting_Skills(Player_Character):
  Player_Character.Skill_Profs.append(Barbarian.Skill_Profs[:Barbarian.Starting_Skill_Number])
  #print(Player_Character.Skill_Profs)

# Rage
Rage_Athletics_Check_Buff = Effects.Buff_Circumstance_Effect('Ability Checks','Self','Instantaneous','Athletics Check','Advantage:')
Rage_Strength_Save_Buff = Effects.Buff_Circumstance_Effect('Saving Throws','Self','Instantaneous','Strength Saving Throw','Advantage:')
  # will need to specify only melee stuff later on

Add_Spellcasting_Back = bool()

Rage_Table = {
  'Level':        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,  20],
  'Rages':        [2,2,3,3,3,4,4,4,4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6,1000],
  'Bonus_Damage': [2,2,2,2,2,2,2,2,3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4,   4]
}


def Apply_Rage(Player_Character):
  Player_Character.Effects['Raging'] = {}
  Player_Character.Class_Resources['Barbarian'] = {}
  Player_Character.Class_Resources['Barbarian']['Raging'] = False
  Player_Character.Class_Resources['Barbarian']['Rage_Charges'] = Rage_Table['Rages'][Player_Character.Levels.count(Barbarian)-1]

  global Rage_Damage_Buff
  Rage_Damage_Buff = Effects.Buff_Bonus_Effect('Target','Instantaneous','Damage/Healing Roll',0,0,Rage_Table['Bonus_Damage'][Player_Character.Levels.count(Barbarian)-1]) 

  
  Player_Character.Bonus_Actions['Independent']['Rage'] = Activate_Rage
  Player_Character.Bonus_Actions['Dependent']['Raging'] = {}
  Player_Character.Bonus_Actions['Dependent']['Raging']['End_Rage'] = End_Rage

  def Reset_Rage_Charges(Player_Character):
    Player_Character.Class_Resources['Barbarian']['Rage_Charges'] = Rage_Table['Rages'][Player_Character.Levels.count(Barbarian)-1]

  Player_Character.Long_Rest_Options['Rage'] = Reset_Rage_Charges(Player_Character)

  #print("Bonus Actions:",Player_Character.Bonus_Actions)                  
  # Rage_Duration = '1_Minute'                                                # need to adjust this for Relentless Rage and Persistant Rage





def Activate_Rage(Player_Character):
  Player_Character.Class_Resources['Barbarian']['Raging'] = True

  Player_Character.Bonus_Actions['Independent'].pop('Rage')
  Player_Character.Class_Resources['Barbarian']['Rage_Charges'] = Player_Character.Class_Resources['Barbarian']['Rage_Charges'] - 1

  Player_Character.WRI.append('slashingres')
  Player_Character.WRI.append('bludgeoningres')
  Player_Character.WRI.append('piercingres')

  Player_Character.Effects['Self_Dealing_Damage']['Bludgeoning'] = [Rage_Damage_Buff]
  Player_Character.Effects['Self_Dealing_Damage']['Piercing'] = [Rage_Damage_Buff]
  Player_Character.Effects['Self_Dealing_Damage']['Slashing'] = [Rage_Damage_Buff]

  Effects.Apply_Buff_Circumstance_Effect(Rage_Strength_Save_Buff,Player_Character)
  Effects.Apply_Buff_Circumstance_Effect(Rage_Athletics_Check_Buff,Player_Character)

  if Character_Actions.Cast_Action() in Player_Character.Actions:
    Add_Spellcasting_Back = True
    Player_Character.Actions.remove(Character_Actions.Cast_Action())
  else:
    pass
  # I could have this set a timer that takes the End_Rage as a free action after 1 minute (in combat) passes


def End_Rage(Player_Character):
  Player_Character.Class_Resources['Barbarian']['Raging'] = False

  Player_Character.Bonus_Actions['Independent']['Rage'] = Activate_Rage

  if 'slashingres' in Player_Character.WRI:
    Player_Character.WRI.remove('slashingres')
    Player_Character.WRI.remove('bludgeoningres')
    Player_Character.WRI.remove('piercingres')
  else: pass

  Player_Character.Effects['Self_Dealing_Damage']['Bludgeoning'].remove(Rage_Damage_Buff)
  Player_Character.Effects['Self_Dealing_Damage']['Piercing'].remove(Rage_Damage_Buff)
  Player_Character.Effects['Self_Dealing_Damage']['Slashing'].remove(Rage_Damage_Buff)
  # remove Strength save buff
  # remove Athletics check buff
  if Add_Spellcasting_Back == True:
        Player_Character.Actions.append(Character_Actions.Cast_Action())
  else:
    pass





# Unarmored_Defense
def Barbarian_Unarmored_Defense(Player_Character):
  if "Light" not in Player_Character.Armor_Equipped and "Medium" not in Player_Character.Armor_Equipped and "Heavy" not in Player_Character.Armor_Equipped:
    Player_Character.AC = 10 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score) + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Con_Score)
    #print("Unarmored Defense:",Player_Character.Barbarian_Unarmored_Defense)

# Danger_Sense
def Danger_Sense(Player_Character):
  if Player_Character.Active_Conditions != "blinded" or "deafened" or "incapacitated":
    Danger_Sense = Effects.Buff_Circumstance_Effect('Saving Throws','Self','Instantaneous','Dexterity Saving Throw','Advantage: ')
    Effects.Apply_Buff_Circumstance_Effect(Danger_Sense,Player_Character)


# Reckless_Attack
Reckless_Attack = Effects.Buff_Circumstance_Effect('Attack Rolls','Self','Instantaneous','Attack Rolls','Advantage: ')

def Reckless_Attack(Player_Character):
  Effects.Apply_Buff_Circumstance_Effect(Reckless_Attack,Player_Character)
  Player_Character.Active_Conditions['Others']['Attack Rolls'] += ['Advantage']




Fast_Movement_Effect = Effects.Speed_Effect('Passive','Self','Contingent','Any',10,False)

def Fast_Movement(Player_Character):
  if "Light" not in Player_Character.Armor_Equipped and "Medium" not in Player_Character.Armor_Equipped and "Heavy" not in Player_Character.Armor_Equipped:
    Effects.Boost_Speed(10,'Walking',Player_Character)
      #later I need to change this to any movement speed that isn't 0

Feral_Instinct = Effects.Buff_Circumstance_Effect('Initiative Rolls','Self','Instantaneous','Initiative Rolls','Advantage: ')
def Apply_Feral_Instinct(Player_Character):
  Effects.Apply_Buff_Circumstance_Effect(Feral_Instinct,Player_Character)


Brutal_Critical1 = Effects.Buff_Bonus_Effect('Target','Instantaneous','Increased Damage',False,1,False)  # Brutal Critical needs work
def Brutal_Critical(Current_Allied_Damage_Roll):
  Effects.Apply_Buff_Bonus_Effect(Brutal_Critical1)
  # ['Attack Roll','Critical Hit'],

# Starting at 11th level, your rage can keep you fighting despite grievous wounds. 
# If you drop to 0 hit points while you're raging and don't die outright, you can make a DC 10 Constitution saving throw. 
# If you succeed, you drop to 1 hit point instead.

# Each time you use this feature after the first, the DC increases by 5. 
# When you finish a short or long rest, the DC resets to 10.

Relentless_Rage_DC = 10
Relentless_Rage_Effect = Effects.Buff_Replacement_Effect('Gets Downed' and 'Raging','Self','Instantaneous','Healing',1)           # Relentless Rage needs work
def Apply_Relentless_Rage(Player_Character):
  Player_Character.Effects['Raging'] = {
    'Self_Drops_to_Zero':Activate_Relentless_Rage
  }
  Relentless_Rage_Uses = 0 
  Player_Character.Class_Save_DCs['Barbarian']['Relentless_Rage'] = 10 + Relentless_Rage_Uses * 5

def Activate_Relentless_Rage(Player_Character):
  Effects.Apply_Buff_Replacement_Effect(Relentless_Rage_Effect)
  Relentless_Rage_Uses = Relentless_Rage_Uses + 1

#Brutal_Critical
Brutal_Critical2 = Effects.Buff_Bonus_Effect('Target','Instantaneous','Increased Damage',False,2,False)
def Apply_Brutal_Critical2(Current_Allied_Damage_Roll):
  Effects.Apply_Buff_Bonus_Effect(Brutal_Critical2)
#['Attack Roll','Critical Hit'],

#Persistent_Rage
def Persistent_Rage(Player_Character):
  Rage_Duration = 'Special'
  # Rage ends if Unconscious or if you choose to end it 


#Brutal_Critical
Brutal_Critical3 = Effects.Buff_Bonus_Effect('Target','Instantaneous','Increased Damage',False,3,False)
def Apply_Brutal_Critical3(Current_Allied_Damage_Roll):
  Effects.Apply_Buff_Bonus_Effect(Brutal_Critical3)
# ['Attack Roll','Critical Hit'],

#Indomitable_Might
def Indomitable_Might(Player_Character):
  Indomitable_Might = Effects.Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Strength Ability Check',Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Str_Score))
  Effects.Apply_Buff_Replacement_Effect(Indomitable_Might)


#Primal_Champion
def Primal_Champion(Player_Character):
  if (Player_Character.Str_Score + 4) > 24:
    Player_Character.Str_Score = 24
  else:
    Player_Character.Str_Score = Player_Character.Str_Score + 4
  
  if (Player_Character.Con_Score + 4) > 24:
    Player_Character.Con_Score = 24
  else:
    Player_Character.Con_Score = Player_Character.Con_Score + 4

Barbarian_Subclasses = ['Ancestral Protectors','Beast','Berserker','Storm Herald','Totem Warrior','Zealot','Wild Magic']


def Choose_Barbarian_Subclass(Player_Character):
  #Subclass = input('Subclass: ')
  Subclass = 'print'
  if Subclass not in Barbarian_Subclasses:
    #print('Barbarian Subclass Not Found')
    pass
  return Subclass


def Barbarian_First_Level(Player_Character):
  Player_Character.Saving_Throws.append(Barbarian.Saving_Throws)
  Barbarian_Starting_Skills(Player_Character)
  Barbarian_Add_Inventory(Player_Character)

def Barbarian_Level_One(Player_Character):
  Apply_Rage(Player_Character)
  Barbarian_Unarmored_Defense(Player_Character)
  #print('Barbarian Level One')

def Barbarian_Level_Two(Player_Character):
  Danger_Sense(Player_Character)
  #print('Barbarian Level Two')

def Barbarian_Level_Three(Player_Character):
  Subclass = Choose_Barbarian_Subclass(Player_Character)
  if Subclass == 'Ancestral Protectors':
    Apply_Ancestral_Protectors(Player_Character)
  elif Subclass == 'Beast':
    pass
  elif Subclass == 'Berserker':
    Apply_Frenzy(Player_Character)
  elif Subclass == 'Storm Herald':
    pass
  elif Subclass == 'Totem Warrior':
    pass
  elif Subclass == 'Zealot':
    pass
  elif Subclass == 'Wild Magic':
    pass


def Barbarian_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)


def Barbarian_Level_Five(Player_Character):
  Character_Functions.Extra_Attack(Player_Character)
  Fast_Movement(Player_Character)

def Barbarian_Level_Six(Player_Character):
  Subclass = Choose_Barbarian_Subclass(Player_Character)
  if Subclass == 'Ancestral Protectors':
    pass
  elif Subclass == 'Beast':
    pass
  elif Subclass == 'Berserker':
    pass
  elif Subclass == 'Storm Herald':
    pass
  elif Subclass == 'Totem Warrior':
    pass
  elif Subclass == 'Zealot':
    pass
  elif Subclass == 'Wild Magic':
    pass

def Barbarian_Level_Seven(Player_Character):
  Apply_Feral_Instinct(Player_Character)

def Barbarian_Level_Eight(Player_Character):
  pass

def Barbarian_Level_Nine(Player_Character):
  Brutal_Critical(Player_Character)

def Barbarian_Level_Ten(Player_Character):
  Subclass = Choose_Barbarian_Subclass(Player_Character)
  if Subclass == 'Ancestral Protectors':
    pass
  elif Subclass == 'Beast':
    pass
  elif Subclass == 'Berserker':
    pass
  elif Subclass == 'Storm Herald':
    pass
  elif Subclass == 'Totem Warrior':
    pass
  elif Subclass == 'Zealot':
    pass
  elif Subclass == 'Wild Magic':
    pass

def Barbarian_Level_Eleven(Player_Character):
  Apply_Relentless_Rage(Player_Character)

def Barbarian_Level_Twelve(Player_Character):
  pass

def Barbarian_Level_Thirteen(Player_Character):
  Apply_Brutal_Critical2(Player_Character)

def Barbarian_Level_Fourteen(Player_Character):
  Subclass = Choose_Barbarian_Subclass(Player_Character)
  if Subclass == 'Ancestral Protectors':
    pass
  elif Subclass == 'Beast':
    pass
  elif Subclass == 'Berserker':
    pass
  elif Subclass == 'Storm Herald':
    pass
  elif Subclass == 'Totem Warrior':
    pass
  elif Subclass == 'Zealot':
    pass
  elif Subclass == 'Wild Magic':
    pass

def Barbarian_Level_Fifteen(Player_Character):
  # Persistent Rage
  pass

def Barbarian_Level_Sixteen(Player_Character):
  pass

def Barbarian_Level_Seventeen(Player_Character):
  Apply_Brutal_Critical3(Player_Character)

def Barbarian_Level_Eighteen(Player_Character):
  pass

def Barbarian_Level_Nineteen(Player_Character):
  Indomitable_Might(Player_Character)

def Barbarian_Level_Twenty(Player_Character):
  Primal_Champion(Player_Character)



Barbarian_Features = [Barbarian_Level_One, Barbarian_Level_Two, Barbarian_Level_Three, Barbarian_Level_Four, Barbarian_Level_Five, Barbarian_Level_Six, Barbarian_Level_Seven, Barbarian_Level_Eight, Barbarian_Level_Nine, Barbarian_Level_Ten, Barbarian_Level_Eleven, Barbarian_Level_Twelve, Barbarian_Level_Thirteen, Barbarian_Level_Fourteen, Barbarian_Level_Fifteen, Barbarian_Level_Sixteen, Barbarian_Level_Seventeen, Barbarian_Level_Eighteen, Barbarian_Level_Nineteen, Barbarian_Level_Twenty]

def Run_Barbarian(Player_Character,Level):
  #print('here 0')
  if Player_Character.First_Class == Barbarian:
    #print('here 1')
    Barbarian_First_Level(Player_Character)
  else:
    #print('here 2')
    pass

  #print('here 3')
  #print('A Levels:',Player_Character.Levels)
  #print('A Levels[0]:',Player_Character.Levels[0])
  #print('A Levels.index(0):',Player_Character.Levels.index(0))

  #for i in Player_Character.Levels:
  #  # print('B Levels[i]:',Player_Character.Levels[i])              Type Error: list indicies must be int or slices, not Class
  #  print('B Levels.index(i):',Player_Character.Levels.index(i))
  #  print("B i's value is:",i)
  #  print("B Index's value is:", Player_Character.Levels.index(i))
    
 

  #int_count = int(count)

  #for int_count in Barbarian_Features:
  #  Barbarian_Features[count](Player_Character)       # TypeError: list indices must be integers or slices, not function
  #  print('Ran:',Barbarian_Features[count])

  #for Levels in Barbarian_Features:
  #  Barbarian_Features[Levels](Player_Character)

  Level = Player_Character.Levels.count(Barbarian)
  if Level >= 1:
    Barbarian_Level_One(Player_Character)
    #Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Barbarian_Level_Two(Player_Character)
      if Level >= 3:
        Barbarian_Level_Three(Player_Character)
        if Level >= 4:
          Barbarian_Level_Four(Player_Character)
          if Level >= 5:
            Barbarian_Level_Five(Player_Character)
            if Level >= 6:
              Barbarian_Level_Six(Player_Character)
              if Level >= 7:
                Barbarian_Level_Seven(Player_Character)
                if Level >= 8:
                  Barbarian_Level_Eight(Player_Character)
                  if Level >= 9:
                    Barbarian_Level_Nine(Player_Character)
                    if Level >= 10:
                      Barbarian_Level_Ten(Player_Character)
                      if Level >= 11:
                        Barbarian_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Barbarian_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Barbarian_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Barbarian_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Barbarian_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Barbarian_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Barbarian_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Barbarian_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Barbarian_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Barbarian_Level_Twenty(Player_Character)
  else:
    pass


#Ancestral_Protectors
Ancestral_Guardians = Establishing_Hierarchy.Subclass(Barbarian,'Ancestral Guardians',['Ancestral_Protectors','Spirit_Shield','Consult_the_Spirits','Vengeful_Ancestors'],False)

Ancestral_Protectors_Attack_Debuff = Effects.Buff_Circumstance_Effect('Attack Rolls','Target','1 round','Attack Rolls','Disadvantage: ')
#Ancestral_Protectors_Damage_Debuff = Buff_Bonus_Effect()

def Use_Ancestral_Protectors(Target):
  Effects.Apply_Buff_Circumstance_Effect(Ancestral_Protectors_Attack_Debuff,Target)

def Apply_Ancestral_Protectors(Player_Character):
  Player_Character.Class_Resources['Barbarian']['Ancestral_Protectors']
  #Player_Character.Effects['Raging']['Self_Attacking']['Hit'] = Use_Ancestral_Protectors(Target)



  #define the Ancestral_Debuff which gives them disadvantage on attacks
  # against other creatures besides you, AND gives creatures damaged by them
  # resistance to those attacks
  # if Rage ends, that debuff ends
  # that debuff also ends
    # The first creature you attack in a turn
    # has their attacks hindered

#Spirit_Shield



def Apply_Spirit_Shield(Player_Character):
  Spirit_Shield = Effects.Buff_Bonus_Effect('Creature','Instantaneous','Reduction',6,Player_Character.Levels.count(Barbarian),0)

  def Use_Spirit_Shield(Target):
    Effects.Apply_Buff_Bonus_Effect(Spirit_Shield)

  #Player_Character.Reactions['Ally_Taking_Damage'] = Use_Spirit_Shield(Target)


Ancestral_Guardians_Table = {
  'Level':              [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Spirit_Shield_Dice': [0,0,2,2,2,2,2,2,2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4]
}

#Consult_the_Spirits
def Consult_the_Spirits(Player_Character):
  Player_Character.Spellcasting_Ability = "Wisdom"
  Player_Character.Spells_Castable.append("Augury","Clairvoyance")

#Vengeful_Ancestors
def Vengeful_Ancestors(Player_Character):
#  Retaliation_Damage = Damage_Reduction
  Damage_Type = "Force"




#Beast
def Apply_Beastial_Rage(Player_Character):
  # remove the old rage definition and fit character with this one instead
  pass

def Activate_Bestial_Rage(Player_Character):
  # Choose one of the three forms
  # if statement for each
  pass
    #		Bite
    #		Claws
    #		Tail

def Apply_Bestial_Soul(Player_Character):
  pass

def Use_Bestial_Soul(Player_Character):
  pass

#	Bestial Soul
#		Swimming
#		Climbing
#		Jumping

#	Infectious Fury
def Apply_Infectious_Fury(Player_Character):
  Player_Character.Class_Resources['Barbarian']['Infectious_Fury'] = 8 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Con_Score) + Player_Character.Prof_Bonus
  
  def Use_Infectious_Fury(Target):
    pass

  #Player_Character.Effects['Raging']['Self_Dealing_Damage'] =+ Use_Infectious_Fury(Target)

#	Call the Hunt
def Apply_Call_the_Hunt(Player_Character):
  pass

def Use_Call_the_Hunt(Player_Character):
  pass



#### Berserker
Berserker = Establishing_Hierarchy.Subclass(Barbarian,'Berserker',['Apply_Frenzy','Apply_Mindless_Rage','Apply_Intimidating_Presence','Apply_Retaliation'],False)

#	Frenzy
def Apply_Frenzy(Player_Character):
  Player_Character.Effects['Raging'] += [Use_Frenzy]

def Frenzied_End_Rage(Player_Character):
  End_Rage(Player_Character)
  Player_Character.Active_Conditions.append('Exhaustion')

def Frenzied_Attack():
  Character_Actions.Attack_Action()       # not the actual attack action rather a weapon attack

def Use_Frenzy(Player_Character):
  Player_Character.Bonus_Actions['Dependent']['Raging'].remove(End_Rage)
  Player_Character.Bonus_Actions['Dependent']['Raging'] += [Frenzied_End_Rage]
  Player_Character.Bonus_Actions['Dependent']['Raging']['Frenzied'] += [Frenzied_Attack]

#	Mindless Rage
def Apply_Mindless_Rage(Player_Character):
  Player_Character.Bonus_Actions['Independent'].remove(Activate_Rage)
  Player_Character.Bonus_Actions['Independent'].apply(Activate_Mindless_Rage)
  Player_Character.Bonus_Actions['Dependent']['Raging'].remove(End_Rage)
  Player_Character.Bonus_Actions['Dependent']['Raging'].append(End_Mindless_Rage)

def Activate_Mindless_Rage(Player_Character):
  Activate_Rage(Player_Character)
  Player_Character.WRI.append('charmedimmu')
  Player_Character.WRI.append('frightenedimmu')

def End_Mindless_Rage(Player_Character):
  End_Rage(Player_Character)
  Player_Character.WRI.remove('charmedimmu')
  Player_Character.WRI.remove('frightenedimmu')

#	Intimidating Presence
def Apply_Intimidating_Presence(Player_Character):
  Player_Character.Actions.append(Use_Intimidating_Presence)
  def Use_Intimidating_Presence(Target):
    DC = 8 + Player_Character.Prof_Bonus + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.CHA_Score)
    Dice_Rolls.Saving_Throw(Target,'Wisdom')
    Conditions.Frighten(Target)

#	Retaliation
def Apply_Retaliation(Player_Character):
  Player_Character.Reactions['Taking_Damage'].append(Use_Retaliation)

def Use_Retaliation(Player_Character):
  Character_Actions.Attack_Action           # not the actual attack action rather a weapon attack




#Storm Herald (Desert, Sea, Tundra)
global Storm
def Choose_Storm_Herald(Player_Character):
  Storm = input('Storm Herald Choice: ')
  return Storm

def Desert_Aura(Player_Character):
  pass
def Sea_Aura(Player_Character):
  pass
def Tundra_Aura(Player_Character):
  pass


def Desert_Soul(Player_Character):
  pass
def Sea_Soul(Player_Character):
  pass
def Tundra_Soul(Player_Character):
  pass


def Shielding_Desert(Player_Character):
  pass
def Shielding_Sea(Player_Character):
  pass
def Shielding_Tundra(Player_Character):
  pass


def Raging_Desert(Player_Character):
  pass
def Raging_Sea(Player_Character):
  pass
def Raging_Tundra(Player_Character):
  pass

Storm_Herald_Table = {
  'Level':         [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Desert_Damage': [],
  'Sea_Dice':      [],
  'Tundra_TempHP': [], 
}


def Storm_Aura(Player_Character):
  Player_Character.Class_Saving_Throws['Barbarian']['Storm_Aura'] = 8 + Player_Character.Prof_Bonus + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Con_Score)
  # need to remove the old version of rage since now it deals damage when activated
  

  Storm = Choose_Storm_Herald(Player_Character)
  if Storm == 'Desert':
    Desert_Aura(Player_Character)
  elif Storm == 'Sea':
    Sea_Aura(Player_Character)
  elif Storm == 'Tundra':
    Tundra_Aura(Player_Character)
  else:
    print('Unable to Find Subclass')


  def Storm_Soul(Player_Character):
    if Storm == 'Desert':
      Desert_Soul(Player_Character)
    elif Storm == 'Sea':
      Sea_Soul(Player_Character)
    elif Storm == 'Tundra':
      Tundra_Soul(Player_Character)
    else:
      print('Unable to Find Subclass')


  def Shielding_Storm(Player_Character):
    if Storm == 'Desert':
      Shielding_Desert(Player_Character)
    elif Storm == 'Sea':
      Shielding_Sea(Player_Character)
    elif Storm == 'Tundra':
      Shielding_Tundra(Player_Character)
    else:
      print('Unable to Find Subclass')


  def Raging_Storm(Player_Character):
    if Storm == 'Desert':
      Raging_Desert(Player_Character)
    elif Storm == 'Sea':
      Raging_Sea(Player_Character)
    elif Storm == 'Tundra':
      Raging_Tundra(Player_Character)
    else:
      print('Unable to Find Subclass')




#Totem Warrior
#	Spirit Seeker
#	Totem Spirit
#		Bear
#		Eagle
#		Elk
#		Tiger
#		Wolf
#	Aspect of the Beast
#		Bear
#		Eagle
#		Elk
#		Tiger
#		Wolf
#	Spirit Walker
#	Totemic Attunement
#		Bear
#		Eagle
#		Elk
#		Tiger
#		Wolf

#Zealot
#	Divine Fury
def Divine_Fury(Player_Character):
  Radiant_or_Necrotic = input('Radiant or Necrotic Damage: ')
  Divine_Fury_Damage = Effects.Buff_Bonus_Effect('Target','Instantaneous','Damage',6,1,Player_Character.Levels.count(Barbarian))
  #Player_Character.Effects['Raging']['First_Attack']['Divine_Fury'] = Apply_Divine_Fury(Target)

  def Apply_Divine_Fury(Target):
    Effects.Apply_Buff_Bonus_Effect(Divine_Fury_Damage)

#	Warrior of the Gods
def Warrior_of_the_Gods(Player_Character):
  pass

#	Fanatical Focus
def Fanatical_Focus(Player_Character):
  pass

#	Zealous Presence
def Zealous_Presence(Player_Character):
  pass

#	Rage Beyond Death
def Rage_Beyond_Death(Player_Character):
  pass



#Wild Magic
#	Magic Awareness
def Magic_Awareness(Player_Character):
  pass

#	Wild Surge
def Wild_Surge(Player_Character):
  pass

#	Bolstering Magic
def Bolstering_Magic(Player_Character):
  pass

#	Unstable Backlash
def Unstable_Backlash(Player_Character):
  pass

#	Controlled Surge
def Controlled_Surge(Player_Character):
  pass


Barbarian_Subclasses = [Berserker,Ancestral_Guardians]
Barbarian.Subclasses = Barbarian_Subclasses