import Establishing_Hierarchy
import Spell_Data
import Spells
import Effects
import Character_Functions
import Character_Actions
import Armor_and_Weapons
import Dice_Rolls
import Backgrounds

import random

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll


Armor = [['Studded Leather'],['Scale Mail']]
Weapons = [['Simple Weapon','Simple Weapon']]
Tools = [['Thieves Tools']]
Instruments = []
Packs = [['Dungeoneers Pack']]
Focus = []
Gold = ['5d4']

Artificer = Establishing_Hierarchy.Class("Artificer",8,["Constitution","Intelligence"],2,["Light","Medium","Shields"],["Simple","Firearms"],["Arcana","History","Investigation","Medicine","Nature","Perception","Sleight_Of_Hand"],["Thieves","Tinkers","Artisan"],"Intelligence",['Alchemist','Armorer','Artillerist','Battle_Smith'],["Magical_Tinkering","Spellcasting","Infuse_Item","The_Right_Tool_for_the_Job","Tool_Expertise","Magic_Item_Adept","Magic_Item_Savant","Magic_Item_Master","Soul_of_Artifice"],"Intelligence 13",Spell_Data.Artificer_Spell_List,"Half",
{
  'Armor': Armor,
  'Weapons': Weapons,
  'Tools': Tools,
  'Instruments': Instruments,
  'Packs': Packs,
  'Focus': Focus,
  'Gold_Alternative': Gold
})


def Artificer_Inventory(Player_Character):
  #Artificer.Starting_Equipment
    # step one: choose items or gold
  # lets assume items for now
  # no armor, so the next step is weapons
  
  Player_Character.Armor_Equipped.append(Armor_and_Weapons.Scale_Mail)
  Player_Character.Weapon_Equipped.append(Armor_and_Weapons.Shortsword)
  Player_Character.Inventory['Tools'].append('Thieves Tools')
  
# Skills
def Artificer_Starting_Skills(Player_Character):
  Player_Character.Skill_Profs.append(Artificer.Skill_Profs[:Artificer.Starting_Skill_Number])          # need to make sure the character doesn't already have these skills before applying them
  print(Player_Character.Skill_Profs)

def Artificer_First_Level(Player_Character):
  Player_Character.Saving_Throws.append(Artificer.Saving_Throws)
  Artificer_Starting_Skills(Player_Character)
  Artificer_Inventory(Player_Character)
  Player_Character.Armor_Profs.append(Artificer.Armor_Profs)







# Magical Tinkering
#The object sheds bright light in a 5-foot radius and dim light for an additional 5 feet.
Magical_Tinkering_Light_Effect = Effects.Light_Effect('Placeholder',['Bright',5,'Dim',5],False,False,False)

#Whenever tapped by a creature, the object emits a recorded message that can be heard up to 10 feet away. You utter the message when you bestow this property on the object, and the recording can be no more than 6 seconds long.
Magical_Tinkering_Message_Effect = Effects.Share_Information_Effect('Placeholder','Placeholder')

#The object continuously emits your choice of an odor or a nonverbal sound (wind, waves, chirping, or the like). The chosen phenomenon is perceivable up to 10 feet away.
Magical_Tinkering_Odor_Effect = Effects.Illusory_Effect('Placeholder',['Odor','Noise'],'False','Any','Distract')

#A static visual effect appears on one of the object's surfaces. This effect can be a picture, up to 25 words of text, lines and shapes, or a mixture of these elements, as you like.
Magical_Tinkering_Visual_Effect = Effects.Illusory_Effect('Placeholder',['Visual'],'False','Any','Inform')


Magical_Item_Tinkering_Effects = [Magical_Tinkering_Light_Effect,Magical_Tinkering_Message_Effect,Magical_Tinkering_Odor_Effect,Magical_Tinkering_Visual_Effect]

#def Choose_Tinkerer_Effect(Player_Character):
#  Tinkerer_Effect = input('Magical Tinkering Effect: ')
#  return Tinkerer_Effect


#Magical_Item_Tinkering = Effects.Create_Item_Effect('Tinkered_Item',False,False,'Permanent','Inventory','Trinket',True,0,False,False,'Wood',False,False,'Tiny',False)
#def Apply_Magical_Tinkering(Player_Character): #action, permanent duration, can only have # upto INT modifier going at once

#  Player_Character.Actions['Magical_Tinkering'] = Use_Magical_Tinkering(Item)
#  Player_Character.Actions['End_Magical_Tinkering'] = End_Magical_Tinkering(Item)

#  Player_Character.Class_Resources['Artificer']['Magical_Tinkering_Usable'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)
#  Player_Character.Class_Resources['Artificer']['Magical_Tinkering_in_Use'] = 0

#  def Use_Magical_Tinkering(Item):
#    Item = Character_Functions.Choose_Item_in_Inventory(Player_Character)
#    Tinkerer_Effect = Choose_Tinkerer_Effect(Player_Character)

#    Player_Character.Class_Resources['Artificer']['Magical_Tinkering_Usable'] = Player_Character.Class_Resources['Artificer']['Magical_Tinkering_Usable'] - 1
#    Player_Character.Class_Resources['Artificer']['Magical_Tinkering_in_Use'] = Player_Character.Class_Resources['Artificer']['Magical_Tinkering_in_Use'] + 1

#    Effects.Create_Item_Effect(str('Tinkered Item:',str(Item),str(Tinkerer_Effect)),Item,True,'Permanent','In Inventory','Trinket',True,False,False,False,False,False,False,False,Tinkerer_Effect)


#  def End_Magical_Tinkering(Item):
#    Player_Character.Class_Resources['Artificer']['Magical_Tinkering_in_Use'] = Player_Character.Class_Resources['Artificer']['Magical_Tinkering_in_Use'] - 1
#    Player_Character.Class_Resources['Artificer']['Magical_Tinkering_Usable'] = Player_Character.Class_Resources['Artificer']['Magical_Tinkering_Usable'] + 1


# Spellcasting
def Artificer_Spellcasting(Player_Character):
  Artificer_Magic_Table = {
    'Artificer_Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    'Infusions_Known': [0,4,4,4,4,6,6,6,6, 8, 8, 8, 8,10,10,10,10,12,12,12],
    'Infused_Items':   [0,2,2,2,2,3,3,3,3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6],
    'Spell_Slots': [
                       [2,2,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
                       [0,0,0,0,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                       [0,0,0,0,0,0,0,0,2,2,3,3,3,3,3,3,3,3,3,3],
                       [0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,3,3,3,3],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2]
    ],
    'Cantrips_Known':  [2,2,2,2,2,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4]
  }

  Num_Artificer_Spells_Known = (Player_Character.Levels.count(Artificer) / 2) + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)

  Num_First_Level_Slots = Artificer_Magic_Table['Spell_Slots'][0][Player_Character.Levels.count(Artificer)-1]
  Num_Second_Level_Slots = Artificer_Magic_Table['Spell_Slots'][1][Player_Character.Levels.count(Artificer)-1]
  Num_Third_Level_Slots = Artificer_Magic_Table['Spell_Slots'][2][Player_Character.Levels.count(Artificer)-1]
  Num_Fourth_Level_Slots = Artificer_Magic_Table['Spell_Slots'][3][Player_Character.Levels.count(Artificer)-1]
  Num_Fifth_Level_Slots = Artificer_Magic_Table['Spell_Slots'][4][Player_Character.Levels.count(Artificer)-1]

  Player_Character.Spellcasting_Known['Artificer_Spells'] = Spell_Data.Artificer_Spell_List

  #check if the Class_Resources dictionary object Spell_Slots currently exists
  if Player_Character.Class_Resources['Spell_Slots'] == {}:
    Player_Character.Class_Resources['Spell Slots'] = {
      '1st': Num_First_Level_Slots,
      '2nd': Num_Second_Level_Slots,
      '3rd': Num_Third_Level_Slots,
      '4th': Num_Fourth_Level_Slots,
      '5th': Num_Fifth_Level_Slots,
      '6th': 0,
      '7th': 0,
      '8th': 0,
      '9th': 0
    }
    Player_Character.Class_Resources['Spell Slots'] = {
      '1st': Num_First_Level_Slots,
      '2nd': Num_Second_Level_Slots,
      '3rd': Num_Third_Level_Slots,
      '4th': Num_Fourth_Level_Slots,
      '5th': Num_Fifth_Level_Slots,
      '6th': 0,
      '7th': 0,
      '8th': 0,
      '9th': 0
    }
  else: 
    pass #will need to reference the multiclass spell table rules later

  if Player_Character.Class_Save_DCs.keys() != []:
    Player_Character.Class_Save_DCs['Artificer'] = {
      'Spell_Save_DC': Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score) + 8 + Player_Character.Prof_Bonus
    }

  def Artificer_Prepare_Spells(Player_Character):
      # what I want to do is to randomly choose Num_Spells_Known number of spells from the Artificer Spell List (minus the cantrips and too high level spells)
      # and then according to the Artificer_Magic_Table and then add them to the Prepared_Spells list

      x = [1,2]
      y = [0,1,2,3,4]
      for i in y:
        print(i)
        print(y)
        print(Artificer_Magic_Table['Spell_Slots'][i])
        if Artificer_Magic_Table['Spell_Slots'][i][Player_Character.Levels.count(Artificer)-1] not in x:
          pass
        else: 
          Highest_Spell_Slot_Castable = Artificer_Magic_Table['Spell_Slots'][i]

      Prepared_Spells = []

      def Spell_Filter(Spell):
        Spell.Base_Level > 0
        Spell.Base_Level < Highest_Spell_Slot_Castable 
      
    #  print(Spell_Data.Artificer_Spell_List)
    #  Prepared_Spells.append(random.sample(filter(Spell_Filter,Spell_Data.Artificer_Spell_List),Spells_Known))

      # Prepare Int Mod + Artificer Level / 2

  Player_Character.Long_Rest_Options['Change_Artificer_Spells'] = Artificer_Prepare_Spells(Player_Character)

  #Arcane_Focus
  # if spells have a material component, and there isn't the material in inventory, if the character doesn't have an Arcane_Focus, remove the spell




  


Infusion_Strength_Table = {
  'Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Bonus': [1,1,1,1,1,1,1,1,1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
}

# Infuse Items
Artificer_Infusions = {
  'Infusion':            ['Arcane_Propulsion_Armor_Infusion','Armor_of_Magical_Strength','Boots_of_the_Winding_Path','Enhanced_Arcane_Focus','Enhanced_Defense','Enhanced_Weapon','Helm_of_Awareness','Homonculus_Servant','Mind_Sharpener','Radiant_Weapon','Repeating_Shot','Replicate_Magic_Item','Repulsion_Shield','Resistant_Armor','Returning_Weapon','Spell_Refueling_Ring'],
  'Level_Prerequisite':  [                                14,                          0,                          6,                      0,                 0,                0,                 10,                   0,               0,               6,               0,                     0,                 6,                6,                 0,                     6],
  'Attunement_Required': [                              True,                       True,                       True,                   True,             False,            False,               True,               False,           False,            True,            True,                 False,              True,             True,             False,                  True],
  'Item_Required':       [                           'Armor',                    'Armor',                    'Boots',   'Spellcasting Focus',['Armor','Shield'],         'Weapon',            'Armor',         'Gem 100gp',         'Armor',        'Weapon',        'Weapon',                 False,          'Shield',          'Armor',          'Weapon',                 False]
  }        # should infusions be create item effects, simply magical items, or enchant item effects???

#Arcane_Propulsion_Armor_Infusion = Effects.Create_Item_Effect()
#The wearer's walking speed increases by 5 feet.
#The armor includes gauntlets, each of which is a magic melee weapon that can be wielded only when the hand is holding nothing
# The wearer is proficient with the gauntlets, and each one deals 1d8 force damage on a hit and has the thrown property, with a normal range of 20 feet and a long range of 60 feet. 
# When thrown, the gauntlet detaches and flies at the attack's target, then immediately returns to the wearer and reattaches.

def Apply_Arcane_Propulsion_Armor_Infusion(Player_Character):
  Player_Character.Speed['Walking'] = Player_Character.Speed['Walking'] + 5 # perhaps this should be a speed effect later on

  Arcane_Propoulsion_Armor_Guantlets = Armor_and_Weapons.Weapon('Arcane_Propoulsion_Armor_Guantlets','Melee','Exotic',8,1,'Force',False,False,False,False,False,False,True,'20:60',False,False)
  Player_Character.Weapon_Profs.append('Exotic')
  Player_Character.Inventory['Magic Items']['Weapons'].append(Arcane_Propoulsion_Armor_Guantlets)


# Armor_of_Magical_Strength
#This armor has 6 charges. The wearer can expend the armor's charges in the following ways:
  #When the wearer makes a Strength check or a Strength saving throw, it can expend 1 charge to add a bonus to the roll equal to its Intelligence modifier.
  #If the creature would be knocked prone, it can use its reaction to expend 1 charge to avoid being knocked prone.
  #The armor regains 1d6 expended charges daily at dawn.

def Apply_Armor_of_Magical_Strength(Player_Character):
  Armor_of_Magical_Strength_Check_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Ability_Check,'Instantaneous','Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
  Armor_of_Magical_Strength_Save_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Saving_Throw,'Instantaneous','Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))

  Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] = 6

  def Recharage_Armor_of_Magical_Strength(Player_Character):
    Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] = Dice_Rolls.Roll_Dice(1,6)
    if Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] > 6:
      Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] = 6

  def Use_Armor_of_Magical_Strength_Check(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Armor_of_Magical_Strength_Check_Bonus)
    Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] = Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] - 1

  def Use_Armor_of_Magical_Strength_Save(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Armor_of_Magical_Strength_Save_Bonus)
    Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] = Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] - 1

  #def Use_Armor_of_Magical_Strength_Negate_Prone(Player_Character):
  #  Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] = Player_Character.Class_Resources['Artificer']['Armor_of_Magical_Strength_Charges'] - 1

  Player_Character.Long_Rest_Options['Recharge_Armor_of_Magical_Strength'] = Recharage_Armor_of_Magical_Strength(Player_Character)
  Player_Character.Effects['Self_Ability_Check']['Strength_Check']['Armor_of_Magical_Strength'] = Use_Armor_of_Magical_Strength_Check(Player_Character)
  Player_Character.Effects['Self_Saving_Throw']['Strength']['Armor_of_Magical_Strength'] = Use_Armor_of_Magical_Strength_Save(Player_Character)
  #Player_Character.Effects['Self_Being_Attacked']['Hit']['Armor_of_Magical_Strength'] = Use_Armor_of_Magical_Strength_Save(Player_Character)


#'Boots_of_the_Winding_Path'
# While wearing these boots, a creature can teleport up to 15 feet as a bonus action to an unoccupied space the creature can see. The creature must have occupied that space at some point during the current turn.

def Apply_Boots_of_the_Winding_Path(Player_Character):
  Boots_of_the_Winding_Path_Teleport = Effects.Move_Effect('Bonus Action',False,Player_Character,15,'Choice','Choice',True,False,False)

  def Use_Boots_of_the_Winding_Path(Player_Character):
    Effects.Apply_Move_Effect(Boots_of_the_Winding_Path_Teleport)

  Player_Character.Bonus_Actions['Independent']['Boots_of_the_Winding_Path'] = Use_Boots_of_the_Winding_Path(Player_Character)


#'Enhanced_Arcane_Focus'
#While holding this item, a creature gains a +1 bonus to spell attack rolls. In addition, the creature ignores half cover when making a spell attack.
#The bonus increases to +2 when you reach 10th level in this class.

def Apply_Enhanced_Arcane_Focus(Player_Character):
  Enhanced_Arcane_Focus_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Attack_Roll,'Instantaneous','Bonus',0,0,Infusion_Strength_Table['Bonus'][Player_Character.Levels.count(Artificer)])
  
  def Use_Enhanced_Arcane_Focus(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Enhanced_Arcane_Focus_Bonus)
  
  Player_Character.Effects['Self_Attacking']['Spell_Attack_Roll']['Enhanced_Arcane_Focus'] = Use_Enhanced_Arcane_Focus(Player_Character)


#'Enhanced_Defense'
#A creature gains a +1 bonus to Armor Class while wearing (armor) or wielding (shield) the infused item.
#The bonus increases to +2 when you reach 10th level in this class.

def Apply_Enhanced_Defense(Player_Character):
  Enhanced_Defense_Bonus = Effects.AC_Effect('Passive',Current_Enemy_Attack_Roll,'Instantaneous','Armor',Infusion_Strength_Table['Bonus'][Player_Character.Levels.count(Artificer)])
  
  def Use_Enhanced_Defense_Bonus(Player_Character):
    Effects.Apply_AC_Effect(Enhanced_Defense_Bonus,Player_Character)
                           
  Player_Character.Effects['Self_Being_Attacked']['Rolling']['Enhanced_Defense'] = Use_Enhanced_Defense_Bonus(Player_Character)



#'Enhanced_Weapon'
# This magic weapon grants a +1 bonus to attack and damage rolls made with it.
# The bonus increases to +2 when you reach 10th level in this class.

def Apply_Enhanced_Weapon(Player_Character):
  Enhanced_Weapon_Attack_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Attack_Roll,'Instantaneous','Bonus',0,0,Infusion_Strength_Table['Bonus'][Player_Character.Levels.count(Artificer)])
  Enhanced_Weapon_Attack_Damage = Effects.Buff_Bonus_Effect(Current_Allied_Damage_Roll,'Instantaneous','Damage',0,0,Infusion_Strength_Table['Bonus'][Player_Character.Levels.count(Artificer)])
  
  def Use_Enhanced_Weapon_Attack_Bonus(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Enhanced_Weapon_Attack_Bonus)
                           
  def Use_Enhanced_Weapon_Attack_Damage(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Enhanced_Weapon_Attack_Damage)


  Player_Character.Effects['Self_Attacking']['Rolling']['Enhanced_Weapon_Attack'] = Use_Enhanced_Weapon_Attack_Bonus(Player_Character)
  Player_Character.Effects['Self_Attacking']['Hit']['Enhanced_Weapon_Attack'] = Use_Enhanced_Weapon_Attack_Damage(Player_Character)



#'Helm_of_Awareness'



#'Homonculus_Servant'
#You learn intricate methods for magically creating a special homunculus that serves you. The item you infuse serves as the creature's heart, around which the creature's body instantly forms.
#You determine the homunculus's appearance. Some artificers prefer mechanical-looking birds, whereas some like winged vials or miniature, animate cauldrons.
#The homunculus is friendly to you and your companions, and it obeys your commands. See this creature's game statistics in the Homunculus Servant stat block, which uses your proficiency bonus (PB) in several places.
#In combat, the homunculus shares your initiative count, but it takes its turn immediately after yours. 
# It can move and use its reaction on its own, but the only action it takes on its turn is the Dodge action, unless you take a bonus action on your turn to command it to take another action. 
# That action can be one in its stat block or some other action. If you are incapacitated, the homunculus can take any action of its choice, not just Dodge.
#The homunculus regains 2d6 hit points if the mending spell is cast on it. If you or the homunculus dies, it vanishes, leaving its heart in its space.

def Apply_Homonculus_Servant(Player_Character):
  Homonculus_HP = 1 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score) + Player_Character.Levels.count(Artificer)
  Player_Character.Related_Stat_Blocks['Homonculus'] = Establishing_Hierarchy.Monster('Homonculus','Homonculus',False,Homonculus_HP,13,'Construct','Tiny',False,False,Player_Character.Prof_Bonus,['Dexterity'],['Perception','Stealth'],4,15,12,10,10,7,True,True,True,True,True,True,True,True,True)
  
  #Establishing_Hierarchy.Spawn_Creature('Origin',Player_Character.Related_Stat_Blocks['Homonculus'])


#'Mind_Sharpener'
#The infused item can send a jolt to the wearer to refocus their mind. 
# The item has 4 charges. 
# When the wearer fails a Constitution saving throw to maintain concentration on a spell, 
# the wearer can use its reaction to expend 1 of the item's charges to succeed instead. 
# The item regains 1d4 expended charges daily at dawn.

def Apply_Mind_Sharpener(Player_Character):
  Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] = 4
  Mind_Sharpener_Effect = Effects.Buff_Replacement_Effect(Current_Allied_Saving_Throw,Player_Character,'Instantaneous','Replacement',20)

  def Use_Mind_Sharpener(Player_Character):
    Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] = Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] - 1
    Effects.Apply_Buff_Replacement_Effect(Mind_Sharpener_Effect,False,False,False)

  def Recharge_Mind_Sharpener(Player_Character):
    Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] = Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] + Dice_Rolls.Roll_Dice(1,4)
    if Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] > 4:
      Player_Character.Class_Resources['Artificer']['Mind_Sharpener_Charges'] = 4


  Player_Character.Long_Rest_Options['Recharge_Mind_Sharpener'] = Recharge_Mind_Sharpener(Player_Character)
  Player_Character.Reactions['Allied_Saving_Throw']['Constitution']['Concentration'] = Use_Mind_Sharpener(Player_Character)   # perhaps I should futher specify the save into Roll, Pass, Fail, Crit Pass, Crit Fail...


#'Radiant_Weapon'
# This magic weapon grants a +1 bonus to attack and damage rolls made with it. 
# While holding it, the wielder can take a bonus action to cause it to shed bright light in a 30-foot radius and dim light for an additional 30 feet. 
# The wielder can extinguish the light as a bonus action.
# The weapon has 4 charges. 
# As a reaction immediately after being hit by an attack, 
# the wielder can expend 1 charge and cause the attacker to be blinded until the end of the attacker's next turn, 
# unless the attacker succeeds on a Constitution saving throw against your spell save DC. 
# The weapon regains 1d4 expended charges daily at dawn.

def Apply_Radiant_Weapon(Player_Character):
  Player_Character.Class_Resources['Artificer']['Radiant_Weapon_Charages'] = 4
  Radiant_Weapon_Light_Effect = Effects.Light_Effect(Player_Character.Location,'Bright',False,False)
  Radiant_Weapon_Attack_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Attack_Roll,'Instantaneous','Bonus',0,0,1)
  Radiant_Weapon_Damage_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Damage_Roll,'Instantaneous','Bonus',0,0,1)

  def Use_Radiant_Weapon_Attack_Bonus(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Radiant_Weapon_Attack_Bonus)
                           
  def Use_Radiant_Weapon_Attack_Damage(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Radiant_Weapon_Damage_Bonus)

  def Light_Radiant_Weapon(Player_Character):
    Effects.Apply_Light_Effect(Radiant_Weapon_Light_Effect)

  def Extinguish_Radiant_Weapon(Player_Character):
    pass

  def Radiant_Weapon_Reaction(Player_Character):
    Player_Character.Class_Resources['Artificer']['Radiant_Weapon_Charages'] = Player_Character.Class_Resources['Artificer']['Radiant_Weapon_Charages'] - 1
    Current_Enemy_Saving_Throw.DC = Player_Character.Class_Save_DCs['Artificer']['Spell_Save_DC']

  Player_Character.Effects['Self_Attacking']['Rolling']['Enhanced_Weapon_Attack'] = Use_Radiant_Weapon_Attack_Bonus(Player_Character)
  Player_Character.Effects['Self_Attacking']['Hit']['Enhanced_Weapon_Attack'] = Use_Radiant_Weapon_Attack_Damage(Player_Character)
  Player_Character.Bonus_Actions['Independent']['Light_Radiant_Weapon'] = Light_Radiant_Weapon(Player_Character)
  Player_Character.Bonus_Actions['Independent']['Extinguish_Radiant_Weapon'] = Extinguish_Radiant_Weapon(Player_Character)
  Player_Character.Reactions['Allied_Being_Attacked']['Hit']['Radiant_Weapon_Reaction'] = Radiant_Weapon_Reaction(Player_Character)


#'Repeating_Shot'
#This magic weapon grants a +1 bonus to attack and damage rolls made with it when it's used to make a ranged attack, and it ignores the loading property if it has it.
# If the weapon lacks ammunition, it produces its own, automatically creating one piece of magic ammunition when the wielder makes a ranged attack with it. 
# The ammunition created by the weapon vanishes the instant after it hits or misses a target.

def Apply_Repeating_Shot(Player_Character):
  pass


#'Replicate_Magic_Item'

#'Repulsion_Shield'
# A creature gains a +1 bonus to Armor Class while wielding this shield.
#The shield has 4 charges. 
# While holding it, the wielder can use a reaction immediately after being hit by a melee attack to expend 1 of the shield's charges and push the attacker up to 15 feet away. 
# The shield regains 1d4 expended charges daily at dawn.

def Apply_Repulsion_Shield(Player_Character):
  pass

#'Resistant_Armor'

def Apply_Resistant_Armor(Player_Character):
  pass

#'Returning_Weapon'

def Apply_Returning_Weapon(Player_Character):
  pass

#'Spell_Refueling_Ring'
def Apply_Spell_Refueling_Ring(Player_Character):
  pass

Item_Replicants = {
  '2': ['Alchemy Jug','Bag of Holding','Cap of Water Breathing','Goggles of Night','Rope of Climbing','Sending Stones','Wand of Magic Detection','Wand of Secrets'],
  '6': ['Boots of elvenkind','Cloak of elvenkind','Cloak of the manta ray','Eyes of charming','Gloves of thievery','Lantern of revealing','Pipes of haunting','Ring of water walking'],
  '10': ['Boots of striding and springing','Boots of the winterlands','Bracers of archery','Brooch of shielding','Cloak of protection','Eyes of the eagle','Gauntlets of ogre power','Gloves of missile snaring','Gloves of swimming and climbing','Hat of disguise','Headband of intellect','Helm of telepathy','Medallion of thoughts','Necklace of adaptation','Periapt of wound closure','Pipes of the sewers','Quiver of Ehlonna','Ring of jumping','Ring of mind shielding','Slippers of spider climbing','Ventilating lungs','Winged boots'],
  '14': ['Amulet of health','Arcane propulsion arm','Belt of hill giant strength','Boots of levitation','Boots of speed','Bracers of defense','Cloak of the bat','Dimensional shackles','Gem of seeing','Horn of blasting','Ring of free action','Ring of protection','Ring of the ram']
}

def Choose_Infusion(Player_Character):
  Infusion = input('Which Infusion: ')
  return Infusion


def Infuse_Item(Player_Character):
  Infuse_Item_Effect = Effects.Create_Item_Effect(str(Choose_Infusion(Player_Character)),False,False,'Permanent',Player_Character.Inventory,'Armor',True,0,0,False,False,False,False,False,False)
  Effects.Apply_Create_Item_Effect(Infuse_Item_Effect,Player_Character,False)

def Apply_Infuse_Item(Player_Character):
  Player_Character.Long_Rest_Options['Infuse_Item'] = Infuse_Item(Player_Character)
  


# The Right Tool for the Job (3rd level)
def Use_Right_Tool_for_the_Job(Player_Character):
  Tool_of_Choice = input('What tool do you want: ')
  if Tool_of_Choice in Backgrounds.Artisans_Tools:
    Player_Character.Inventory['Artisan_Tools'].append(Tool_of_Choice)
  else:
    print("Couldn't Find Artisan Tool")

def Apply_Right_Tool_for_the_Job(Player_Character):
  Player_Character.Short_Rest_Options['Unlimited']['Right_Tool_for_the_Job'] = Use_Right_Tool_for_the_Job(Player_Character)


# Tool Expertise (6th level)
  # proficiency is doubled for any ability check made with Tools

def Tool_Expertise(Player_Character):       # This may just go into the profs section instead of being an effect
  pass
  #Tool_Expertise_Buff = Effects.Buff_Bonus_Effect()
  #def Use_Tool_Expertise(Player_Character):
  #  Effects.Apply_Buff_Bonus_Effect(Tool_Expertise_Buff,Player_Character)
  #Player_Character.Effects += Use_Tool_Expertise()


# Flash of Genius (7th level)
def Apply_Flash_of_Genius(Player_Character):

  Player_Character.Class_Resources['Artificer'] = {'Flash_of_Genius_Charges': Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)}

  Flash_of_Genius_Check_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Ability_Check,'Instantaneous','Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))      
  Flash_of_Genius_Save_Bonus = Effects.Buff_Bonus_Effect(Current_Allied_Saving_Throw,'Instantaneous','Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))

  def Use_Flash_of_Genius_Check(Target):
    Effects.Apply_Buff_Bonus_Effect(Flash_of_Genius_Check_Bonus)
    Player_Character.Class_Resources['Artificer']['Flash_of_Genius_Charges'] = Player_Character.Class_Resources['Artificer']['Flash_of_Genius_Charges'] - 1
  Player_Character.Reactions['Allied_Ability_Check']['Flash_of_Genius'] = Use_Flash_of_Genius_Check(Current_Allied_Ability_Check)

  def Use_Flash_of_Genius_Save(Target):
    Effects.Apply_Buff_Bonus_Effect(Flash_of_Genius_Save_Bonus)
    Player_Character.Class_Resources['Artificer']['Flash_of_Genius_Charges'] = Player_Character.Class_Resources['Artificer']['Flash_of_Genius_Charges'] - 1
  Player_Character.Reactions['Allied_Saving_Throw']['Flash_of_Genius'] = Use_Flash_of_Genius_Save(Current_Allied_Saving_Throw)

  def Reset_Flash_of_Genius(Player_Character):
    Player_Character.Class_Resources['Artificer']['Flash_of_Genius_Charges'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)
  Player_Character.Long_Rest_Options['Flash_of_Genius'] = Reset_Flash_of_Genius(Player_Character)



# Magic Item Adept (10th level)
def Magic_Item_Adept(Player_Character):
  Player_Character.Attunement_Slots = 4


# Spell Storing Item (11th level)
def Apply_Spell_Storing_Item(Player_Character):
  # requires a short or long rest to do, not an action
  Items_Usable = []
  for Weapon in Player_Character.Inventory['Weapons']: # need to include Weapons_Equipped
    if Weapon.type == 'Simple' or Weapon.type == 'Martial':
      Items_Usable.append(Weapon)
    else: pass

  Spells_Storable = []
  
  for Spell in range(0,len(Player_Character.Spellcasting_Prepared['Artificer']),1):
    print(Player_Character.Spellcasting_Prepared['Artificer'][Spell].Name)
    print(Player_Character.Spellcasting_Prepared['Artificer'][Spell].Base_Level)
    if Player_Character.Spellcasting_Prepared['Artificer'][Spell].Base_Level < 3:
      Spells_Storable.append(Player_Character.Spellcasting_Prepared['Artificer'][Spell])
    
    else:
      pass

  def Store_Spell_in_Item(Player_Character):
    print(Items_Usable)
    Item_Choice = input('Which Item do you Infuse: ')
    print(Spells_Storable)
    Spell_Choice = input('Which Spell do you Infuse: ')

    Effects.Enchant_Item_Effect(Item_Choice,False,'Permanent',False,False,False,False,False,False,False,False,Spell_Choice)

  Player_Character.Long_Rest_Options['Store_Spell_in_Item'] = Store_Spell_in_Item(Player_Character)      # Change this to Player_Characters.Long_Rests


  def Hold_Spell_Stored_Item(Wielder):
    Wielder.Actions['Use_Spell_Stored_Item'] = Use_Spell_Stored_Item(Wielder)

    def Use_Spell_Stored_Item(Wielder):
      pass


  #Spell_Stored_Item = Establishing_Hierarchy.Object("Spell_Stored_Object",10,"Tiny",True)


# Magic Item Master (18th level)
def Magic_Item_Master(Player_Character):
  Player_Character.Attunement_Slots = 6
  print("Item Attunement Slots:",Player_Character.Attunement_Slots)

# Soul of Artifice (20th level)
def Apply_Soul_of_Artifice(Player_Character):
  Soul_of_Artifice = Effects.Healing_Effect('Activation','Self','Instantaneous','True',1,0,Player_Character.Attunement_Slots_Filled)

  # How does this work?
    # Bonus to saving throws?
    # Brought back from 0 to 1 HP?
  
  #Soul_of_Artifice = False

  def Use_Soul_of_Artifice(Player_Character):
    #Effects.Apply_Healing_Effect(Soul_of_Artifice,Player_Character)
    #Item_Choice = input('Which Attunement Do You Remove: ')
    pass

  try:
    Player_Character.Effects['Dependent']['Dropping_to_Zero']['Soul_of_Artifiec'] = Use_Soul_of_Artifice(Player_Character)
  except:
    Player_Character.Effects['Dependent'] = {
      'Dropping_to_Zero': {
        'Soul_of_Artifiec':Use_Soul_of_Artifice(Player_Character)
      }
    }


#if Player_Character.Current_HP is 0:
#  Player_Character.Attunement_Slots_Filled = Player_Character.Attunement_Slots_Filled - 1
#  Player_Character.Current_HP = 1
#   Prompt a user to pick an item to drop attunement with

def Artificer_Run_Subclass(Player_Character):
  Current_Subclass_Number = 9 - Player_Character.Subclasses.count(False)
  


  def Artificer_Choose_Subclass(Player_Character):
    Artificer_Choice = input('Which Subclass: ')
    
    if Artificer_Choice == 'Battle Smith' or Artificer_Choice == 'Battlesmith':
      Player_Character.Subclasses[Current_Subclass_Number] = Battle_Smith
      Apply_Battle_Smith(Player_Character)
      print(Battle_Smith.Feature)
      Battle_Smith.Feature['1']

    elif Artificer_Choice == 'Alchemist':
      Player_Character.Subclasses[Current_Subclass_Number] = Alchemist
      Apply_Alchemist(Player_Character)
      print(Alchemist.Feature)
      Alchemist.Feature['1']

    elif Artificer_Choice == 'Artillerist':
      Player_Character.Subclasses[Current_Subclass_Number] = Artillerist
      Apply_Artillerist(Player_Character)
      Artillerist.Feature['1']

    elif Artificer_Choice == 'Armorer':
      Player_Character.Subclasses[Current_Subclass_Number] = Armorer
      Apply_Armorer(Player_Character)
      Armorer.Feature['1']

    else:
      print('Cannot find Artificer Subclass',Artificer_Choice)


  
  if Player_Character.Levels.count(Artificer) >= 3:
    Artificer_Choose_Subclass(Player_Character)
  
  Current_Subclass_Location_in_Artificer = Artificer.Subclass.index(Player_Character.Subclasses[Current_Subclass_Number])

  if Player_Character.Levels.count(Artificer) >= 5:  # I know I had a logical reason for doing it like this but I'm having trouble remembering why # the intention was to avoid issues during multiclassing                    # so that if there was a different subclass taken first, we could still locate the Artificer subclass
    Artificer.Subclass[Current_Subclass_Location_in_Artificer].Feature['2']
  else:
    pass
  
  if Player_Character.Levels.count(Artificer) >= 9:    # But I already created the function Run_Battle_Smith
    Artificer.Subclass[Current_Subclass_Location_in_Artificer].Feature['3']
  else:
    pass

  if Player_Character.Levels.count(Artificer) >= 15:
    Artificer.Subclass[Current_Subclass_Location_in_Artificer].Feature['4']
  else:
    pass



def Artificer_Level_One(Player_Character):
  #Apply_Magical_Tinkering(Player_Character)
  Artificer_Spellcasting(Player_Character)
  # need to add a function that applies the saving throws from the class to the character

def Artificer_Level_Two(Player_Character):
  Apply_Infuse_Item(Player_Character)

def Artificer_Level_Three(Player_Character):
  Artificer_Run_Subclass(Player_Character)

def Artificer_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)

def Artificer_Level_Five(Player_Character):
  Artificer_Run_Subclass(Player_Character)

def Artificer_Level_Six(Player_Character):
  pass

def Artificer_Level_Seven(Player_Character):
  Apply_Flash_of_Genius(Player_Character)

def Artificer_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)

def Artificer_Level_Nine(Player_Character):
  Artificer_Run_Subclass(Player_Character)

def Artificer_Level_Ten(Player_Character):
  Magic_Item_Adept(Player_Character)

def Artificer_Level_Eleven(Player_Character):
  Apply_Spell_Storing_Item(Player_Character)

def Artificer_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Artificer_Level_Thirteen(Player_Character):
  pass

def Artificer_Level_Fourteen(Player_Character):
  pass

def Artificer_Level_Fifteen(Player_Character):
  Artificer_Run_Subclass(Player_Character)

def Artificer_Level_Sixteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Artificer_Level_Seventeen(Player_Character):
  pass

def Artificer_Level_Eighteen(Player_Character):
  Magic_Item_Master(Player_Character)

def Artificer_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Artificer_Level_Twenty(Player_Character):
  Apply_Soul_of_Artifice(Player_Character)

Artificer_Features = [Artificer_Level_One, Artificer_Level_Two, Artificer_Level_Seven, Artificer_Level_Ten, Artificer_Level_Eleven, Artificer_Level_Eighteen, Artificer_Level_Twenty]

#def Run_Artificer(Player_Character):
#  for Player_Character.level in Artificer_Features:
#    Player_Character.level(Player_Character)

def Run_Artificer(Player_Character,Level):
  #print('here 0')
  if Player_Character.First_Class == Artificer:
    #print('here 1')
    Artificer_First_Level(Player_Character)
  else:
    #print('here 2')
    pass


  Level = Player_Character.Levels.count(Artificer)
  if Level >= 1:
    Artificer_Level_One(Player_Character)
    if Level >= 2:
      Artificer_Level_Two(Player_Character)
      if Level >= 3:
        Artificer_Level_Three(Player_Character)
        if Level >= 4:
          Artificer_Level_Four(Player_Character)
          if Level >= 5:
            Artificer_Level_Five(Player_Character)
            if Level >= 6:
              Artificer_Level_Six(Player_Character)
              if Level >= 7:
                Artificer_Level_Seven(Player_Character)
                if Level >= 8:
                  Artificer_Level_Eight(Player_Character)
                  if Level >= 9:
                    Artificer_Level_Nine(Player_Character)
                    if Level >= 10:
                      Artificer_Level_Ten(Player_Character)
                      if Level >= 11:
                        Artificer_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Artificer_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Artificer_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Artificer_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Artificer_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Artificer_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Artificer_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Artificer_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Artificer_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Artificer_Level_Twenty(Player_Character)
  else:
    pass

Battle_Smith = Establishing_Hierarchy.Subclass(Artificer,[],False)
print(Artificer.Subclass)
#Artificer.Subclass.remove(Artificer.Subclass[3])
Artificer.Subclass.append(Battle_Smith)

# Tools of the Trade
def Battle_Smith_Tools_of_the_Trade(Player_Character):
  Player_Character.Tool_Profs.append("Smiths_Tools")



#Battle_Smith_Spells
def Battle_Smith_Spells(Player_Character):
  try:
    Player_Character.Spellcasting_Prepared['Artificer'].append(Spells.Spells_Dict["Shield"],Spells.Spells_Dict["Thunderwave"],Spells.Spells_Dict["Scorching Ray"],Spells.Spells_Dict["Shatter"],Spells.Spells_Dict["Fireball"],Spells.Spells_Dict["Wind Wall"],Spells.Spells_Dict["Wall of Ice"],Spells.Spells_Dict["Wall of Fire"],Spells.Spells_Dict["Cone of Cold"],Spells.Spells_Dict["Wall of Force"])
  except:
    Player_Character.Spellcasting_Prepared = {
      'Artificer': [Spells.Spells_Dict["Shield"],Spells.Spells_Dict["Thunderwave"],Spells.Spells_Dict["Scorching Ray"],Spells.Spells_Dict["Shatter"],Spells.Spells_Dict["Fireball"],Spells.Spells_Dict["Wind Wall"],Spells.Spells_Dict["Wall of Ice"],Spells.Spells_Dict["Wall of Fire"],Spells.Spells_Dict["Cone of Cold"],Spells.Spells_Dict["Wall of Force"]]
    }




#Battle_Ready
def Battle_Ready(Player_Character):
  Player_Character.Weapon_Profs.append('Martial')
  Player_Character.Usable_Attack_Score['Magical'].append(Player_Character.Int_Score)


#Steel_Defender
def Apply_Steel_Defender(Player_Character):
  try:
    Player_Character.Class_Resources['Artificer']['Steel_Defenders'] = 1
  except:
    Player_Character.Class_Resources['Artificer'] = {
      'Steel_Defenders': 1
    }

  def Create_Steel_Defender(Player_Character):
    Steel_Defender_HP = 2 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score) + (5 * Player_Character.Level_Count)
    Steel_Defender = Establishing_Hierarchy.Monster("Steel_Defender",'Steel_Defender','Tashas Cauldron of Everything',Steel_Defender_HP,15,"Construct","Medium",Player_Character.Level_Count,True,Player_Character.Prof_Bonus,["Dexterity","Constitution"],["Athletics","Perception"],14,12,14,4,10,6,{},[],False,[],True,True,True,True,True,True,True,True,True)
    Player_Character.Related_Stat_Blocks['Companion'] = Steel_Defender
    Player_Character.Class_Resources['Artificer']['Steel_Defenders'] = 0

    Player_Character.Related_Stat_Blocks['Companion'].Actions = {
      'Independent': {
        'Dodge': Character_Actions.Dodge_Action(Player_Character.Related_Stat_Blocks['Companion']),
      },
      'Dependent': {'Command_Steel_Defender': {},'Player_Character_Incapacitated':{}}
    }

          #'Force_Empowered_Rend': Use_Force_Empowered_Rend(Player_Character),
          #'Repair': Repair(Player_Character)
  Player_Character.Long_Rest_Options['Create_Steel_Defender'] = Create_Steel_Defender(Player_Character)

  # Force-Empowered Rend. Melee Weapon Attack: your spell attack modifier to hit, reach 5 ft., one target you can see. Hit: 1d8 + PB force damage.
  def Apply_Force_Empowered_Rend(Player_Character):
    Player_Character.Related_Stat_Blocks['Companion'].Actions['Dependent']['Command_Steel_Defender']['Force_Empowered_Rend'] = Use_Force_Empowered_Rend(Player_Character)

    def Use_Force_Empowered_Rend(Player_Character):
      Player_Character.Related_Stat_Blocks['Companion']
      #Force_Empowered_Rend_Damage = 



  # Repair (3/Day). The magical mechanisms inside the defender restore 2d8 + PB hit points to itself or to one construct or object within 5 feet of it.
  def Apply_Repair(Player_Character):
    Repair_Heal_Effect = Effects.Healing_Effect('Construct','Self','Instantaneous','True',2,8,Player_Character.Prof_Bonus)
    def Recharge_Repair(Player_Character):
      try:
        Player_Character.Related_Stat_Blocks['Companion']['Resources'] = {
          'Repair': 3
        }
      except:
        Player_Character.Related_Stat_Blocks['Companion']['Resources']['Repair'] = 3
    Player_Character.Related_Stat_Blocks['Companion'].Long_Rest_Options['Recharge_Repair'] = Recharge_Repair(Player_Character)
    
    def Repair(Player_Character):
      Player_Character.Related_Stat_Blocks['Companion']['Resources']['Repair'] = Player_Character.Related_Stat_Blocks['Companion']['Resources']['Repair'] - 1
      Effects.Apply_Healing_Effect(Repair_Heal_Effect,Player_Character.Related_Stat_Blocks['Companion'])

    Player_Character.Related_Stat_Blocks['Companion'].Actions['Dependent']['Repair']['Force_Empowered_Rend'] = Repair(Player_Character)

  # Deflect Attack. The defender imposes disadvantage on the attack roll of one creature it can see that is within 5 feet of it, provided the attack roll is against a creature other than the defender.
  def Apply_Deflect_Attack(Player_Character):
    def Use_Deflect_Attack(Player_Character):
      if Current_Enemy_Attack_Roll.Attack_Target != Player_Character.Related_Stat_Blocks['Companion']:
        Current_Enemy_Attack_Roll.Circumstances.append('Disadvantage')
      else:
        print("Can't Deflect Attacks Targeting Self")

    Player_Character.Related_Stat_Blocks['Companion'].Reactions = {
      'Deflect_Attack': Use_Deflect_Attack(Player_Character)
    }
  # if the player gets incapacitated, the Steel Defender can take any action...perhaps I need some if statements for Conditions...

#  def Apply_Command_Steel_Defender(Player_Character):


#    def Use_Command_Steel_Defender(Player_Character):
      #Player_Character.Related_Stat_Blocks['Companion']
#      pass

      # I should have it that using this then adds the functions to the dictionary of the Steel Defender

#    Player_Character.Bonus_Actions['Independent']['Command_Steel_Defender'] = Use_Command_Steel_Defender(Player_Character)
#  Apply_Command_Steel_Defender(Player_Character)


#Extra_Attack

#Arcane_Jolt

# When either you hit a target with a magic weapon attack or your steel defender hits a target, you can channel magical energy through the strike to create one of the following effects:
  #The target takes an extra 2d6 force damage.
  #Choose one creature or object you can see within 30 feet of the target. Healing energy flows into the chosen recipient, restoring 2d6 hit points to it.

#You can use this energy a number of times equal to your Intelligence modifier (minimum of once), but you can do so no more than once on a turn. You regain all expended uses when you finish a long rest.

def Apply_Arcane_Jolt(Player_Character):
  Arcane_Jolt_Damage_Effect = Effects.Buff_Bonus_Effect(Current_Allied_Damage_Roll,'Instantaneous','Damage',2,6,0)
  Arcane_Jolt_Healing_Effect = Effects.Healing_Effect('Activation','Target','Instantaneous',True,2,6,0)
  Player_Character.Class_Resources['Artificer']['Arcane_Jolt_Uses'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)
  
  def Use_Arcane_Jolt_Damage(Player_Character):
    Player_Character.Class_Resources['Artificer']['Arcane_Jolt_Uses'] = Player_Character.Class_Resources['Artificer']['Arcane_Jolt_Uses'] - 1
    Effects.Apply_Buff_Bonus_Effect(Arcane_Jolt_Damage_Effect)
  
  try:
    Player_Character.Effects['Self_Attacking']['Hit']['Arcane_Jolt_Damage'] = Use_Arcane_Jolt_Damage(Player_Character)
    Player_Character.Related_Stat_Blocks['Companion'].Effects['Self_Attacking']['Hit']['Arcane_Jolt_Damage'] = Use_Arcane_Jolt_Damage(Player_Character)
  except:
    Player_Character.Effects['Self_Attacking'] = {'Hit': {'Arcane_Jolt_Damage': Use_Arcane_Jolt_Damage(Player_Character)}}
    Player_Character.Related_Stat_Blocks['Companion'].Effects['Self_Attacking'] = {'Hit': {'Arcane_Jolt_Damage': Use_Arcane_Jolt_Damage(Player_Character)}}


  def Use_Arcane_Jolt_Healing(Player_Character):
    Player_Character.Class_Resources['Artificer']['Arcane_Jolt_Uses'] = Player_Character.Class_Resources['Artificer']['Arcane_Jolt_Uses'] - 1
    Effects.Apply_Healing_Effect(Arcane_Jolt_Healing_Effect,Player_Character)

  Player_Character.Effects['Self_Attacking']['Hit']['Arcane_Jolt_Healing'] = Use_Arcane_Jolt_Healing(Player_Character)
  Player_Character.Related_Stat_Blocks['Companion'].Effects['Self_Attacking']['Hit']['Arcane_Jolt_Healing'] = Use_Arcane_Jolt_Healing(Player_Character)

  def Reset_Arcane_Jolt(Player_Character):
    Player_Character.Class_Resources['Artificer']['Arcane_Jolt_Uses'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)

  Player_Character.Long_Rest_Options['Arcane_Jolt'] = Reset_Arcane_Jolt(Player_Character)

#Improved_Defender
# The extra damage and the healing of your Arcane Jolt both increase to 4d6.
# Your steel defender gains a +2 bonus to Armor Class.
# Whenever your steel defender uses its Deflect Attack, the attacker takes force damage equal to 1d4 + your Intelligence modifier.

def Apply_Improved_Defender(Player_Character):
  Arcane_Jolt_Damage_Effect = Effects.Buff_Bonus_Effect(Current_Allied_Damage_Roll,'Instantaneous','Damage',4,6,0)
  Arcane_Jolt_Healing_Effect = Effects.Healing_Effect('Activation','Target','Instantaneous',True,4,6,0)


  Deflect_Attack_Damage = Effects.Buff_Bonus_Effect(Current_Enemy_Attack_Roll.Entity_Making,'Instantaneous','Damage',1,4,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
  
  def Use_Deflect_Attack_Damage(Player_Character):
    Player_Character.Related_Stat_Blocks['Companion'].Effects['Use_Deflect'] = {}
    Player_Character.Related_Stat_Blocks['Companion'].Effects['Use_Deflect']['Deflect_Damage_Back'] = Effects.Apply_Buff_Bonus_Effect(Deflect_Attack_Damage)
  
  try: 
    Player_Character.Related_Stat_Blocks['Companion'].Effects['Self_Being_Attacked']['Deflect']['Deflect_Attack_Damage'] = Use_Deflect_Attack_Damage(Player_Character)
  except:
    Player_Character.Related_Stat_Blocks['Companion'].Effects['Self_Being_Attacked'] = {'Deflect': {'Deflect_Attack_Damage': Use_Deflect_Attack_Damage(Player_Character)}}

def Battle_Smith_One(Player_Character):
  print('Battle Smith One ran')
  Battle_Smith_Tools_of_the_Trade(Player_Character)
  Battle_Smith_Spells(Player_Character)
  Battle_Ready(Player_Character)
  Apply_Steel_Defender(Player_Character)


def Battle_Smith_Two(Player_Character):
  Character_Functions.Extra_Attack(Player_Character)

def Battle_Smith_Three(Player_Character):
  Apply_Arcane_Jolt(Player_Character)

def Battle_Smith_Four(Player_Character):
  Apply_Improved_Defender(Player_Character)

def Apply_Battle_Smith(Player_Character):
  Battle_Smith.Feature = {
    '1': Battle_Smith_One(Player_Character),
    '2': Battle_Smith_Two(Player_Character),
    '3': Battle_Smith_Three(Player_Character),
    '4': Battle_Smith_Four(Player_Character)
  }

  def Run_Battle_Smith(Player_Character):
    if Player_Character.Levels.count(Artificer) >= 3:
      Battle_Smith.Feature['1']
    
    if Player_Character.Levels.count(Artificer) >= 5:
      Battle_Smith.Feature['2']

    if Player_Character.Levels.count(Artificer) >= 9:
      Battle_Smith.Feature['3']

    if Player_Character.Levels.count(Artificer) >= 15:
      Battle_Smith.Feature['4']



Artillerist = Establishing_Hierarchy.Subclass(Artificer,[],False)
#Artificer.Subclass.remove('Artillerist')
Artificer.Subclass.append(Artillerist)

# Tools of the Trade
def Artillerist_Tools_of_the_Trade(Player_Character):
  Player_Character.Tool_Profs.append("Woodcarver_Tools")

#Artillerist_Spells
def Artillerist_Spells(Player_Character):
  Player_Character.Spellcasting_Prepared.append(Spells.Spells_Dict("Shield"),Spells.Spells_Dict("Thunderwave"),Spells.Spells_Dict("Scorching_Ray"),Spells.Spells_Dict("Shatter"),Spells.Spells_Dict("Fireball"),Spells.Spells_Dict("Wind_Wall"),Spells.Spells_Dict("Ice_Wall"),Spells.Spells_Dict("Wall_of_Fire"),Spells.Spells_Dict("Cone_of_Cold"),Spells.Spells_Dict("Wall_of_Force"))
  print(Player_Character.Spellcasting_Prepared)

#Eldritch_Cannon
def Apply_Eldritch_Cannon(Player_Character):
  Eldritch_Cannon_AC = 18
  Eldritch_Cannon_WRI = ["Poisonimmu","Psychicimmu","Proneimmu","Paralyzedimmu","Petrifiedimmu","Stunnedimmu","Blindedimmu","Deafenedimmu","Restrainedimmu","Unconsciousimmu","Incapacitatedimmu","Grappledimmu","Charmedimmu","Frightenedimmu","Exhaustionimmu"]
  Player_Character.Class_Resources['Artificer']['Eldritch_Cannons_Created'] = 0

  Eldritch_Cannon = Establishing_Hierarchy.Monster('Eldritch Cannon','Eldritch Cannon',"Tasha's Cauldron of Everything",5*Player_Character.Level,18,'Construct',['Tiny','Small'],False,False,Player_Character.Prof_Bonus,[],[],10,10,10,10,10,10,{},False,False,False,False,False,False,False,{'Walking':15},False,False,["Poisonimmu","Psychicimmu","Proneimmu","Paralyzedimmu","Petrifiedimmu","Stunnedimmu","Blindedimmu","Deafenedimmu","Restrainedimmu","Unconsciousimmu","Incapacitatedimmu","Grappledimmu","Charmedimmu","Frightenedimmu","Exhaustionimmu"],False)
  
  def Create_Eldritch_Cannon(Player_Character):
    Flamethrower_Effect = Effects.Damage_Effect('AOE',True,'Instantaneous','Fire','Instantaneous',8,2,0,False,'Dexterity',True)
    Force_Ballista_Damage_Effect = Effects.Damage_Effect('AOE',True,'Force',True,'Instantaneous',8,2,0,'Ranged Weapon',False,False)
    Force_Ballista_Push_Effect = Effects.Move_Effect('Hit',True,True,5,'Away',True,False,False,False)
    Protector_Effect = Effects.Healing_Effect('Use',Player_Character,'Instantaneous','Temp HP',8,1,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
    
    def Activate_Flamethrower(Player_Character):
      Effects.Apply_Damage_Effect(Flamethrower_Effect)

    def Activate_Force_Ballista(Player_Character):
      Effects.Apply_Damage_Effect(Force_Ballista_Damage_Effect,Player_Character,True)
      Effects.Apply_Move_Effect(Force_Ballista_Push_Effect)

    def Activate_Protector(Player_Character):
      Effects.Apply_Healing_Effect(Protector_Effect,Player_Character)

    if Player_Character.Class_Resources['Artificer']['Eldritch_Cannons_Created'] >= 1:
      Player_Character.Class_Resources
    else:
      Player_Character.Class_Resources['Artificer']['Eldritch_Cannons_Created'] = Player_Character.Class_Resources['Artificer']['Eldritch_Cannons_Created'] + 1
    
      Eldritch_Cannon_Options = ['Flamethrower','Force_Ballista','Protector']
      Eldritch_Cannon_Choice = input('What type of Eldritch Cannon: ')
      if Eldritch_Cannon_Choice not in Eldritch_Cannon_Options:
        print('Eldritch Cannon Option Not Found')
      elif Eldritch_Cannon_Choice == 'Flamethrower':
        Eldritch_Cannon.Actions['Dependent']['Commanded']['Flamethrower'] = Activate_Flamethrower(Player_Character)
      elif Eldritch_Cannon_Choice == 'Force_Ballista':
        Eldritch_Cannon.Actions['Dependent']['Commanded']['Force_Ballista'] = Activate_Force_Ballista(Player_Character)
      elif Eldritch_Cannon_Choice == 'Protector':
        Eldritch_Cannon.Actions['Dependent']['Commanded']['Protector'] = Activate_Protector(Player_Character)
      else: pass

      Player_Character.Inventory['Magic Items']['Weapons'].append(Eldritch_Cannon)

  Player_Character.Actions['Create_Eldritch_Cannon'] = Create_Eldritch_Cannon(Player_Character)

  def Activate_Eldritch_Cannon(Player_Character):
    # Should it move?
    # Should it attack?
    # for now we'll just have it make an attack
    Eldritch_Cannon.Actions['Dependent']['Commanded']
    pass


  Player_Character.Bonus_Actions['Independent']['Activate_Eldritch_Cannon'] = Activate_Eldritch_Cannon(Player_Character)

#Arcane_Firearm
def Apply_Arcane_Firearm(Player_Character):
  Arcane_Firearm_Damage_Effect = Effects.Buff_Bonus_Effect(Current_Allied_Damage_Roll,'Instantaneous','Damage',8,1,0)
  #adds a d8 to damage rolls from Artificer spells
  def Use_Arcane_Firearm(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Arcane_Firearm_Damage_Effect)
  Player_Character.Effects['Self_Dealing_Damage']['Spells']['Artificer_Spells']['Arcane_Firearm'] = Use_Arcane_Firearm(Player_Character)

#Explosive_Cannon
def Apply_Explosive_Cannon(Player_Character):
  def Detonate_Eldritch_Cannon(Player_Character):
    pass

  Player_Character.Actions["Detonate_Eldritch_Cannon"] = Detonate_Eldritch_Cannon(Player_Character)

#Fortified_Position
# can't do this one fully until I do distance and location
# need to define covers
def Fortified_Position(Player_Character):
  pass



def Artillerist_One(Player_Character):
  Artillerist_Tools_of_the_Trade(Player_Character)
  Artillerist_Spells(Player_Character)
  Apply_Eldritch_Cannon(Player_Character)

def Artillerist_Two(Player_Character):
  Apply_Arcane_Firearm(Player_Character)

def Artillerist_Three(Player_Character):
  Apply_Explosive_Cannon(Player_Character)

def Artillerist_Four(Player_Character):
  Fortified_Position(Player_Character)




def Apply_Artillerist(Player_Character):
  Artillerist.Feature = [Artillerist_One(Player_Character),Artillerist_Two(Player_Character),Artillerist_Three(Player_Character),Artillerist_Four(Player_Character)]

  def Run_Artillerist(Player_Character):
    if Player_Character.Levels.count(Artificer) >= 3:
      Artillerist.Feature[0]
    
    if Player_Character.Levels.count(Artificer) >= 5:
      Artillerist.Feature[1]

    if Player_Character.Levels.count(Artificer) >= 9:
      Artillerist.Feature[2]

    if Player_Character.Levels.count(Artificer) >= 15:
      Artillerist.Feature[3]





Armorer = Establishing_Hierarchy.Subclass(Artificer,[],False)
#Artificer.Subclass.remove('Armorer')
Artificer.Subclass.append(Armorer)

#Tools of the Trade
def Armorer_Tools_of_the_Trade(Player_Character):
  Player_Character.Armor_Profs.append("Heavy")
  Player_Character.Tool_Profs.append("Smiths_Tools")
  print(Player_Character.Tool_Profs)
  print(Player_Character.Armor_Profs)

#Armorer_Spells
def Armorer_Spells(Player_Character):
  Player_Character.Spellcasting_Prepared.append(Spells.Spells_Dict("Magic_Missile"),Spells.Spells_Dict("Thunderwave"),Spells.Spells_Dict("Mirror_Image"),Spells.Spells_Dict("Shatter"),Spells.Spells_Dict("Hypnotic_Pattern"),Spells.Spells_Dict("Lightning_Bolt"),Spells.Spells_Dict("Fire_Shield"),Spells.Spells_Dict("Greater_Invisibility"),Spells.Spells_Dict("Passwall"),Spells.Spells_Dict("Wall_of_Force"))
  print(Player_Character.Spellcasting_Prepared)

#Arcane_Armor
#Arcane_Armor_Item = Establishing_Hierarchy.Object('Arcane_Armor',True,True,'Armor',False,False)

#Create_Arcane_Armor = Effects.Create_Item_Effect('Arcane_Armor',)



def Don_Arcane_Armor(Player_Character):
  pass

def Doff_Arcane_Armor(Player_Character):
  pass

#def Apply_Arcane_Armor(Player_Character):
#  Player_Character.Actions.append(Create_Arcane_Armor)
#  
#  Player_Character.Actions.append(Don_Arcane_Armor(Player_Character))
#  Player_Character.Actions.append(Doff_Arcane_Armor(Player_Character))
#  print(Player_Character.Actions)
#
#  Player_Character.Bonus_Actions.append("Deploy_Helment_Arcane_Armor")
#  Player_Character.Bonus_Actions.append("Retract_Helment_Arcane_Armor")
#  print(Player_Character.Bonus_Actions)


#Armor_Model
def Armor_Model(Player_Character):
  Choice = "idk right now"
  Options = ["Guardian","Infiltrator"]
  if Choice == "Guardian":
    def Armor_Model_Guardian(Player_Character):
      #"Thunder_Guantlets"
      Thunder_Guantlets = Establishing_Hierarchy.Weapon()

      #"Defensive_Field"
      Player_Character.Bonus_Actions.append("Arcane_Armor_Defensive_Field")
      print(Player_Character.Bonus_Actions)
      Field_Temp_HP = Player_Character.Level
      # Effect for the thunder guantlet
      # Effect for the defensive field
      # would the effects go under the player_character or the weapon???


  else:
    def Armor_Model_Infiltrator(Player_Character):
      #"Lightning_Launcher"
      Lightning_Launcher = Establishing_Hierarchy.Weapon()
      #"Powered_Steps"
      Player_Character.Speed = Player_Character.Speed + 5
      #"Dampening_Field"
      # advantage on stealth checks


#Extra_Attack



#Armor_Modifications

#Perfected_Armor
#def Perfected_Armor(Player_Character):

def Armorer_One(Player_Character):
  Armorer_Tools_of_the_Trade(Player_Character)
  Armorer_Spells(Player_Character)


def Armorer_Two(Player_Character):
  Character_Functions.Extra_Attack(Player_Character)

def Armorer_Three(Player_Character):
  pass

def Armorer_Four(Player_Character):
  pass


def Apply_Armorer(Player_Character):
  Armorer.Feature = [Armorer_One(Player_Character),Armorer_Two(Player_Character),Armorer_Three(Player_Character),Armorer_Four(Player_Character)]

  def Run_Armorer(Player_Character):
    if Player_Character.Levels.count(Artificer) >= 3:
      Armorer.Feature[0]
    
    if Player_Character.Levels.count(Artificer) >= 5:
      Armorer.Feature[1]

    if Player_Character.Levels.count(Artificer) >= 9:
      Armorer.Feature[2]

    if Player_Character.Levels.count(Artificer) >= 15:
      Armorer.Feature[3]



Alchemist = Establishing_Hierarchy.Subclass(Artificer,[],False)
#Artificer.Subclass.remove('Alchemist')
Artificer.Subclass.append(Alchemist)

## Alchemist
# Tool_Profiencies
def Alchemist_Tool_Proficiencies(Player_Character):
  Player_Character.Tool_Profs.append("Alchemist_Supplies")
  print(Player_Character.Tool_Profs)

#Alchemist_Spells
def Alchemist_Spells(Player_Character):
  try:
    Player_Character.Spellcasting_Prepared['Artificer'].append(Spells.Spells_Dict("Healing Word"),Spells.Spells_Dict("Ray of Sickness"),Spells.Spells_Dict("Flaming Sphere"),Spells.Spells_Dict("Melf's Acid Arrow"),Spells.Spells_Dict("Gaseous Form"),Spells.Spells_Dict("Mass Healing Word"),Spells.Spells_Dict("Blight"),Spells.Spells_Dict("Death Ward"),Spells.Spells_Dict("Cloud Kill"),Spells.Spells_Dict("Raise Dead"))
  except:
    Player_Character.Spellcasting_Prepared = {
      'Artificer': [Spells.Spells_Dict["Healing Word"],Spells.Spells_Dict["Ray of Sickness"],Spells.Spells_Dict["Flaming Sphere"],Spells.Spells_Dict["Melf's Acid Arrow"],Spells.Spells_Dict["Gaseous Form"],Spells.Spells_Dict["Mass Healing Word"],Spells.Spells_Dict["Blight"],Spells.Spells_Dict["Death Ward"],Spells.Spells_Dict["Cloudkill"],Spells.Spells_Dict["Raise Dead"]]
    }
  
  print(Player_Character.Spellcasting_Prepared)



#Experimental_Elixirs
Experimental_Elixirs_dict = {
  'Level':          [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Long_Rest_Prep': [0,0,1,1,1,2,2,2,2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3]
}  


def Apply_Experimental_Elixirs(Player_Character):
  Experimental_Elixir = Establishing_Hierarchy.Object('Experimental_Elixir',True,'Tiny','Potion',False,False)
  Experimental_Elixer_Healing = Effects.Healing_Effect('Consume Potion','Creature','Instantaneous','True',2,4,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
  Experimental_Elixir_Swiftness = Effects.Speed_Effect('Consume Potion','Creature','1_Hour','Walking',10,False)
  Experimental_Elixir_Resilience = Effects.AC_Effect('Consume Potion','Creature','10_Minutes','Passive',1)
  Experimental_Elixir_Boldness_Attack = Effects.Buff_Bonus_Effect(Current_Allied_Attack_Roll,'1_Minute','Attack Roll',1,4,0)
  Experimental_Elixir_Boldness_Save = Effects.Buff_Bonus_Effect(Current_Allied_Saving_Throw,'1_Minute','Saving Throw',1,4,0)
  Experimental_Elixir_Flight = Effects.Speed_Effect('Consume Potion','Creature','10_Minutes','Flying',0,10)
  Experimental_Elixir_Transformation = Effects.Spell_Effect('Consume Potion','Creature','10_Minutes','Alter Self',2,False)

  try: 
    Player_Character.Class_Resources['Artificer']['Experimental_Elixirs'] = Experimental_Elixirs_dict['Long_Rest_Prep'][Player_Character.Levels.count(Artificer)-1]
  except:
    Player_Character.Class_Resources['Artificer'] = {
      'Experimental_Elixirs': Experimental_Elixirs_dict['Long_Rest_Prep'][Player_Character.Levels.count(Artificer)-1]
    }

  def Create_Experimental_Elixer_Free(Player_Character):
    pass

  def Create_Experimental_Elixir_Spell_Slot(Player_Character):
    pass

  def Consume_Experimental_Elixir(Creature):
    pass

  Player_Character.Actions['Consume_Elixir'] = Consume_Experimental_Elixir(Player_Character)
  Player_Character.Actions['Create_Elixir_Free'] = Create_Experimental_Elixer_Free(Player_Character)
  Player_Character.Actions['Create_Elixir_Spell_Slot'] = Create_Experimental_Elixir_Spell_Slot(Player_Character)


# Apply Experimental Elixir to Character
# Create an Experimental Elixir
# Drink an Experimental Elixir




#Alchemical_Savant
def Apply_Alchemical_Savant(Player_Character):
  Alchemical_Savant_Effect = Effects.Buff_Bonus_Effect(Current_Allied_Damage_Roll,'Instantaneous','Roll Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
  
  def Use_Alchemical_Savant():
    Effects.Apply_Buff_Bonus_Effect(Alchemical_Savant_Effect)
  
  try:
    Player_Character.Effects['Self_Dealing_Damage']['Fire'] = Use_Alchemical_Savant()
    Player_Character.Effects['Self_Dealing_Damage']['Acid'] = Use_Alchemical_Savant()
    Player_Character.Effects['Self_Dealing_Damage']['Necrotic'] = Use_Alchemical_Savant()
    Player_Character.Effects['Self_Dealing_Damage']['Poison'] = Use_Alchemical_Savant()
    Player_Character.Effects['Self_Healing'] = Use_Alchemical_Savant()
  except:
    Player_Character.Effects['Self_Dealing_Damage'] = {'Fire': Use_Alchemical_Savant(),
                                                       'Acid': Use_Alchemical_Savant(),
                                                       'Necrotic': Use_Alchemical_Savant(),
                                                       'Poison': Use_Alchemical_Savant(),
    }
    Player_Character.Effects['Self_Healing'] = Use_Alchemical_Savant()




#Restorative_Reagents
def Apply_Restorative_Reagents(Player_Character):
  Player_Character.Per_Use_Spells['Intelligence_Modifier'] = {
    'Lesser_Restoration': Spells.Spells_Dict["Lesser Restoration"]
  }
  # I've got no clue how the Lesser Restoration part of Restorative Reagents should be handled since it's a resource and a spell but doesn't use spell slots
  Player_Character.Class_Resources['Artificer']['Restorative_Reagent_Spell_Uses'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score)


  Restorative_Reagents_Temp_HP = Effects.Healing_Effect('','Creature','Unspecified','Temp',2,6,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score))
  def Use_Restorative_Reagents_Temp_HP(Player_Character):
    Effects.Apply_Healing_Effect(Restorative_Reagents_Temp_HP,Player_Character)
  Player_Character.Effects['Consume_Experimental_Elixir'] = {'Restorative_Reagents': Use_Restorative_Reagents_Temp_HP(Player_Character)}

#Chemical_Mastery
def Chemical_Master(Player_Character):
  Player_Character.WRI.append("Poisonres")
  Player_Character.WRI.append("Acidres")
  Player_Character.WRI.append("Poisonedimmu")
  try:
    Player_Character.Per_Use_Spells['1/long_rest']['Greater_Restoration'] = Spells.Spells_Dict["Greater Restoration"]
  except:
    Player_Character.Per_Use_Spells['1/long_rest'] = {
      'Greater_Restoration': Spells.Spells_Dict["Greater Restoration"]
    }

  try:
    Player_Character.Per_Use_Spells['1/long_rest']['Heal'] = Spells.Spells_Dict["Heal"]
  except:
    Player_Character.Per_Use_Spells['1/long_rest'] = {
      'Greater_Restoration': Spells.Spells_Dict["Heal"]
    }



def Alchemist_One(Player_Character):
  Alchemist_Tool_Proficiencies(Player_Character)
  Alchemist_Spells(Player_Character)
  Apply_Experimental_Elixirs(Player_Character)

def Alchemist_Two(Player_Character):
  Apply_Alchemical_Savant(Player_Character)

def Alchemist_Three(Player_Character):
  Apply_Restorative_Reagents(Player_Character)

def Alchemist_Four(Player_Character):
  Chemical_Master(Player_Character)


def Apply_Alchemist(Player_Character):
  print('Apply Alchemist')
  Alchemist.Feature = {
    '1': Alchemist_One(Player_Character),
    '2': Alchemist_Two(Player_Character),
    '3': Alchemist_Three(Player_Character),
    '4': Alchemist_Four(Player_Character)
  }

  def Run_Alchemist(Player_Character):
    if Player_Character.Levels.count(Artificer) >= 3:
      Alchemist.Feature[0]
    
    if Player_Character.Levels.count(Artificer) >= 5:
      Alchemist.Feature[1]

    if Player_Character.Levels.count(Artificer) >= 9:
      Alchemist.Feature[2]

    if Player_Character.Levels.count(Artificer) >= 15:
      Alchemist.Feature[3]


