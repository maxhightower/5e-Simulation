import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data
from random import randrange
import Dice_Rolls
import Armor_and_Weapons

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll

#from Terminal_Code_Attempt import Target
#Target_Placeholder = 'Placeholder'


# Cleric
#(a) a mace or (b) a warhammer (if proficient)
#(a) scale mail, (b) leather armor, or (c) chain mail (if proficient)
#(a) a light crossbow and 20 bolts or (b) any simple weapon
#(a) a priest's pack or (b) an explorer's pack
#A shield and a holy symbol

Armor = [['Scale Mail','Shield'],['Leather','Shield'],['Chain Mail','Shield']]
Weapons = [['Mace','Light Crossbow']],[['Mace','Simple Weapon']],[['Warhammer','Light Crossbow']],[['Warhammer','Simple Weapon']]
Tools = []
Instruments = []
Packs = [["Priest's Pack"],["Explorer's Pack"]]
Focus = [['Holy Symbol']]
Gold = ['5d4']


Cleric = Establishing_Hierarchy.Class("Cleric",8,["Wisdom", "Charisma"],2,["Light","Medium","Shields"],["Simple"],["History","Insight","Medicine","Persuasion","Religion"],False,"Wisdom",["Forge","Death","Tempest","Twilight","Light","Life","Nature","Grave","Peace","Order","War","Arcane","Knowledge"],["Spellcasting","Channel Divinity","Destory Undead","Divine Intervention"],"Wisdom 13",Spell_Data.Cleric_Spell_List,"Full",
{
  'Armor': Armor,
  'Weapons': Weapons,
  'Tools': Tools,
  'Instruments': Instruments,
  'Packs': Packs,
  'Spellcasting_Focus': Focus,
  'Gold_Alternative': Gold
})

# skills
def Cleric_Starting_Skills(Player_Character):
  Player_Character.Skill_Profs.append(Cleric.Skill_Profs[:Cleric.Starting_Skill_Number])
  #print(Player_Character.Skill_Profs)

def Cleric_Add_Inventory(Player_Character):
   
  Player_Character.Weapon_Equipped.append(Armor_and_Weapons.Mace)
  Player_Character.Armor_Equipped.append(Armor_and_Weapons.Scale_Mail)
  Player_Character.Armor_Equipped.append(Armor_and_Weapons.Shield)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Light_Crossbow)




# Spellcasting
Cleric_Spellcasting_Table = {
  'Cleric_Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Spell_Slots': {
    '1st': [2,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    '2nd': [0,0,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    '3rd': [0,0,0,0,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    '4th': [0,0,0,0,0,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3],
    '5th': [0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,3,3,3],
    '6th': [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2],
    '7th': [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2],
    '8th': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
    '9th': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]
  },
  'Cantrips_Known': [3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5]
}



def Cleric_Spellcasting(Player_Character):
  Player_Character.Spellcasting_Known['Cleric_Spells'] = Spell_Data.Cleric_Spell_List
  Player_Character.Class_Save_DCs['Cleric'] = {
    'Spell_Save_DC': Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score) + 8 + Establishing_Hierarchy.levelToProficiency(Player_Character)
  }

  Number_of_Spells_Prepareable = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score) + Player_Character.Levels.count(Cleric)

  #Arcane_Focus
  # if spells have a material component, and there isn't the material in inventory, if the character doesn't have an Arcane_Focus, remove the spell


  #Player_Character.Actions.append("Spells")            Need to define the action of casting later
  # 1 1
  # 3 2
  # 5 3
  # 7 4
  # 9 5
  # 11 6
  # 13 7
  # 15 8
  # 17 9 

  def Cleric_Prepare_Spells(Player_Character):
    Cleric_Spellcasting_Table['Spell_Slots'][Player_Character.Levels.count(Cleric)]
    Slots_Level_List = [1,3,5,7,9,11,13,15,17]
    Highest_Spell_Slot = Slots_Level_List[Player_Character.Levels.count(Cleric) + 1]

    Cleric_Spells_Preparable = Spell_Data.Cleric_Spell_List.query("Level <= Highest_Spell_Slot")
    print(Cleric_Spells_Preparable)
    if len(Player_Character.Spellcasting_Prepared) == Number_of_Spells_Prepareable:
      print('Maximum Number of Spells')
    else:
      for i in range(Number_of_Spells_Prepareable): 
        pass


def Cleric_First_Level(Player_Character):
  Cleric_Spellcasting(Player_Character)
  Player_Character.Saving_Throws.append(Cleric.Saving_Throws)
  Player_Character.Armor_Profs.append(Cleric.Armor_Profs)
  Cleric_Starting_Skills(Player_Character)
  Cleric_Add_Inventory(Player_Character)

  Player_Character.Instrument_Profs.append(Cleric.Tool_Profs)
  Player_Character.Weapon_Profs.append(Cleric.Weapon_Profs)



#Channel_Divinity
def Apply_Channel_Divinity(Player_Character):
  Player_Character.Class_Resources['Total_Channel_Divinity'] = 1    # will replace 1 with the function to find the character's cleric level later
  Player_Character.Class_Resources['Current_Channel_Divinity'] = 1
  
  def Use_Turn_Undead(Target):
    if Player_Character.Class_Resources['Current_Channel_Divinity'] > 0:
      if Dice_Rolls.Saving_Throw(Target,"WIS") >= Player_Character.Class_Save_DCs['Cleric']:
        Target.Active_Conditions.append('Fleeing/Turned')
        Player_Character.Class_Resources['Current_Channel_Divinity'] = Player_Character.Class_Resources['Current_Channel_Divinity'] - 1
      else:
        Player_Character.Class_Resources['Current_Channel_Divinity'] = Player_Character.Class_Resources['Current_Channel_Divinity'] - 1
    else:
      print('No Channel Divinities Remaining')

  #Player_Character.Actions.append(Use_Turn_Undead(Target_Placeholder))
  #print(Player_Character.Actions)

Channel_Divinity_Table = {
  'Level':     [1,2,3,4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20],
  'Charges':   [0,1,1,1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3],
  'Undead_CR': [0,0,0,0,.5,.5,.5, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4]
}


#Destory_Undead  
def Destroy_Undead(Target,Player_Character):
    DC = Player_Character.Wis_Score + Player_Character.Prof_Bonus + 8
    if Dice_Rolls.Saving_Throw(Target,'Wisdom') < DC:
      Target.Active_Conditions.append('Turned')
    else:
      pass

def Apply_Destroy_Undead(Player_Character):

  Player_Character.Actions.append(Destroy_Undead())
  print(Player_Character.Actions)


#Divine_Intervention
def Divine_Intervention(Player_Character):

  def Roll_for_Divine_Intervention(Player_Character):
    Divine_Intervention_Roll = randrange(1,100)
    if Divine_Intervention_Roll <= Player_Character.Levels.count(Cleric):
      print('The Gods have viewed your plea benevolently. Ask, and your query shall be considered...')
    else:
      print('The heavens are silent...')

  Player_Character.Actions['Divine_Intervention'] = Roll_for_Divine_Intervention(Player_Character)

# perhaps I could make a class of entity called diety which could cast divine spells from anywhere...



def Apply_Potent_Spellcasting(Player_Character):
  Potent_Spellcasting_Bonus = Effects.Buff_Bonus_Effect('Cantrip Damage','Creature','Instantaneous','Damage',False,False,Player_Character.Spellcasting_Modifier)
  Player_Character.Effects['Dealing_Damage']['Cantrip']['Potent_Spellcasting'] = Use_Potent_Spellcasting(Player_Character)

  def Use_Potent_Spellcasting(Player_Character):
    Effects.Apply_Buff_Bonus_Effect(Potent_Spellcasting_Bonus,Player_Character)


def Apply_Divine_Strike(Player_Character):
  Divine_Strike_Bonus = Effects.Buff_Bonus_Effect()

  def Use_Divine_Strike(Player_Character):
    Effects.Apply_Buff_Bonus_Effect()

Cleric_Subclasses = ['Arcana','Death','Grave','Twilight','Trickery','Forge','Knowledge','Life','Light','Nature','War','Peace','Order','Tempest']

def Cleric_Choose_Subclass(Player_Character):
  Subclass = input('Subclass: ')
  if Subclass not in Cleric_Subclasses:
    print('Cleric Subclass Not Found')
  return Subclass



def Cleric_Level_One(Player_Character):
  Cleric_Spellcasting(Player_Character)


  # need to add a function that applies the saving throws from the class to the character

def Cleric_Level_Two(Player_Character):
  Apply_Channel_Divinity(Player_Character)
  Subclass = Cleric_Choose_Subclass(Player_Character)
  if Subclass == 'Arcana':
    pass
  elif Subclass == 'Death':
    pass
  elif Subclass == 'Grave':
    pass
  elif Subclass == 'Twilight':
    pass
  elif Subclass == 'Trickery':
    pass
  elif Subclass == 'Forge':
    pass
  elif Subclass == 'Knowledge':
    pass
  elif Subclass == 'Life':
    pass
  elif Subclass == 'Light':
    pass
  elif Subclass == 'Nature':
    pass
  elif Subclass == 'War':
    pass
  elif Subclass == 'Peace':
    pass
  elif Subclass == 'Order':
    pass
  elif Subclass == 'Tempest':
    pass
  else:
    print('Cleric Subclass Not Found')



def Cleric_Level_Three(Player_Character):
  pass

def Cleric_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)

def Cleric_Level_Five(Player_Character):
  pass

def Cleric_Level_Six(Player_Character):
  Subclass = Cleric_Choose_Subclass(Player_Character)
  if Subclass == 'Arcana':
    pass
  elif Subclass == 'Death':
    pass
  elif Subclass == 'Grave':
    pass
  elif Subclass == 'Twilight':
    pass
  elif Subclass == 'Trickery':
    pass
  elif Subclass == 'Forge':
    pass
  elif Subclass == 'Knowledge':
    pass
  elif Subclass == 'Life':
    pass
  elif Subclass == 'Light':
    pass
  elif Subclass == 'Nature':
    pass
  elif Subclass == 'War':
    pass
  elif Subclass == 'Peace':
    pass
  elif Subclass == 'Order':
    pass
  elif Subclass == 'Tempest':
    pass
  else:
    print('Cleric Subclass Not Found')

def Cleric_Level_Seven(Player_Character):
  pass

def Cleric_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)
  Subclass = Cleric_Choose_Subclass(Player_Character)
  if Subclass == 'Arcana':
    pass
  elif Subclass == 'Death':
    pass
  elif Subclass == 'Grave':
    pass
  elif Subclass == 'Twilight':
    pass
  elif Subclass == 'Trickery':
    pass
  elif Subclass == 'Forge':
    pass
  elif Subclass == 'Knowledge':
    pass
  elif Subclass == 'Life':
    pass
  elif Subclass == 'Light':
    pass
  elif Subclass == 'Nature':
    pass
  elif Subclass == 'War':
    pass
  elif Subclass == 'Peace':
    pass
  elif Subclass == 'Order':
    pass
  elif Subclass == 'Tempest':
    pass
  else:
    print('Cleric Subclass Not Found')

def Cleric_Level_Nine(Player_Character):
  pass

def Cleric_Level_Ten(Player_Character):
  Divine_Intervention(Player_Character)

def Cleric_Level_Eleven(Player_Character):
  pass

def Cleric_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Cleric_Level_Thirteen(Player_Character):
  pass

def Cleric_Level_Fourteen(Player_Character):
  pass

def Cleric_Level_Fifteen(Player_Character):
  pass

def Cleric_Level_Sixteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Cleric_Level_Seventeen(Player_Character):
  Subclass = Cleric_Choose_Subclass(Player_Character)
  if Subclass == 'Arcana':
    pass
  elif Subclass == 'Death':
    pass
  elif Subclass == 'Grave':
    pass
  elif Subclass == 'Twilight':
    pass
  elif Subclass == 'Trickery':
    pass
  elif Subclass == 'Forge':
    pass
  elif Subclass == 'Knowledge':
    pass
  elif Subclass == 'Life':
    pass
  elif Subclass == 'Light':
    pass
  elif Subclass == 'Nature':
    pass
  elif Subclass == 'War':
    pass
  elif Subclass == 'Peace':
    pass
  elif Subclass == 'Order':
    pass
  elif Subclass == 'Tempest':
    pass
  else:
    print('Cleric Subclass Not Found')


def Cleric_Level_Eighteen(Player_Character):
  pass

def Cleric_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Cleric_Level_Twenty(Player_Character):
  pass


def Run_Cleric(Player_Character,Level):
  if Player_Character.First_Class == Cleric:
    Cleric_First_Level(Player_Character)
  else:
    pass


  Level = Player_Character.Levels.count(Cleric)
  if Level >= 1:
    Cleric_Level_One(Player_Character)
    if Level >= 2:
      Cleric_Level_Two(Player_Character)
      if Level >= 3:
        Cleric_Level_Three(Player_Character)
        if Level >= 4:
          Cleric_Level_Four(Player_Character)
          if Level >= 5:
            Cleric_Level_Five(Player_Character)
            if Level >= 6:
              Cleric_Level_Six(Player_Character)
              if Level >= 7:
                Cleric_Level_Seven(Player_Character)
                if Level >= 8:
                  Cleric_Level_Eight(Player_Character)
                  if Level >= 9:
                    Cleric_Level_Nine(Player_Character)
                    if Level >= 10:
                      Cleric_Level_Ten(Player_Character)
                      if Level >= 11:
                        Cleric_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Cleric_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Cleric_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Cleric_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Cleric_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Cleric_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Cleric_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Cleric_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Cleric_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Cleric_Level_Twenty(Player_Character)
  else:
    pass









#Arcana_Domain
Arcane_Domain_Spell_List = ['Detect_Magic', 'Magic_Missile', 'Magic_Weapon', 'Nystuls_Magic_Aura', 'Dispel_Magic', 'Magic_Circle', 'Arcane_Eye', 'Leomunds_Secret_Chest', 'Planar_Binding', 'Teleportation_Circle']

#Arcane_Initiate
def Apply_Arcane_Initiate(Player_Character):
  Player_Character.Skill_Profs.append('Arcana')
  Spell_Data.Wizard_Spell_List
  # you can add two cantrips from the wizard spell list and they use your cleric wisdom spellcasting scores

#Arcane_Abjuration
def Apply_Channel_Divinity_Arcane_Abjuration(Player_Character):
  pass

def Use_Channel_Divinity_Arcane_Abjuration():
  pass

#Spell_Breaker

#Potent_Spellcasting

#Arcane_Mastery




#Death_Domain
# false life, ray of sickness, blindness/deafness, ray of enfeeblement, animate dead, vampiric touch, blight, death ward, antilife shell, cloudkill

#Bonus_Proficiency
# martial weapons
def Death_Domain_Martial_Prof(Player_Character):
  Player_Character.Weapon_Prof.append('Martial')

#Reaper
# necromancy cantrip from any spell list
# necromancy cantrips that target one creature target two within 5ft of each other

#Touch_of_Death
# When the cleric hits a creature with a melee attack, the cleric can use Channel Divinity to deal extra necrotic damage to the target. 
# The damage equals 5 + twice his or her cleric level.

#Inescapable_Destruction
# Necrotic damage dealt by cleric spells and channel divinity ignores resistance to necrotic damage

#Divine_Strike
#Improved_Reaper



#Forge_Domain
# identify, searing smite, heat metal, magic weapon, elemental weapon, protection from energy, fabricate, wall of fire, animate objects, creation

#Bonus_Proficiency
# heavy armor
# smith's tools

def Forge_Domain_Bonus_Proficiencies(Player_Character):
  Player_Character.Armor_Profs.append('Heavy')
  Player_Character.Tool_Profs.append('Smiths Tools')

#Blessing_of_the_Forge
# simple or martial weapon OR suit of armor becomes +1 equivalent
def Apply_Blessing_of_the_Forge(Player_Character):
  pass

def Use_Blessing_of_the_Forge(Player_Character):
  pass

#Artisans_Blessing
def Apply_Artisans_Blessing(Player_Character):
  pass

def Use_Artisans_Blessing(Player_Character):
  pass


#Soul_of_the_Forge
# fire resistance
# while wearing heavy armor, +1 Ac
Soul_of_the_Forge_AC_Effect = Effects.AC_Effect('Heavy Armor','Self','Passive',False,1)
def Soul_of_the_Forge(Player_Character):
  Player_Character.WRI.append('fireres')
  #Player_Character.Effects

#Divine_Strike

#Saint_of_Forge_and_Fire
# immunity to fire damage
# while wearing heavy armor, resistance to bludgeoning, piercing, and slashing from nonmagical attacks

def Saint_of_Forge_and_Fire(Player_Character):
  if 'fireres' in Player_Character.WRI:
    Player_Character.WRI.remove('fireres')
  
  Player_Character.WRI.append('fireimmu')
  Player_Character.WRI.append('nonmagicalres')



#Grave_Domain
# bane, false life, gentle repose, ray of enfeeblement, revivify, vampiric touch, blight, death ward, antilife shell, raise dead

#Circle_of_Mortality
# Spare the dying

#Eyes_of_the_Grave
# location of undead within 60ft

#Path_to_the_Grave
# 30ft becomes vulnerable to all of the damage from the next attack that hits the creature
#Sentinel_at_Deaths_Door
#Potent_Spellcasting
#Keeper_of_Souls




#Knowledge_Domain
# Command, Identify, Augury, suggestion, nondetection, speak with dead, arcane eye, confusion, legend lore, scrying

#Blessings_of_Knowledge
# Arcana, History, Nature., or Religion (pick 2 profs) proficiency is doubled for both ability checks

#Knowledge_of_the_Ages
# adds a proficiency in a skill or tool for 10 minutes

#Read_Thoughts
#Potent_Spellcasting
#Visions_of_the_Past



#Life_Domain
# Bless, Cure Wounds, Lesser Restoration, Spiritual Weapon, Beacon of Hope, Revivify, Death Ward, Guardian of Faith, Mass Cure Wounds, Raise Dead

#Bonus_Proficiency
# heavy armor

#Disciple_of_Life
#Preserve_Life
#Blessed_Healer
#Divine_Strike
#Supreme_Healing


#Light_Domain
# burning hands, faerie fire, flaming sphere, scorching ray, daylight, fireball, guardian of faith, wall of fire, flame strike, scrying
#Bonus_Cantrip
def Apply_Bonus_Cantrip_Light(Player_Character):
  pass

#Warding_Flare
def Apply_Warding_Flare(Player_Character):
  Player_Character.Reactions['Self_Being_Attacked']['Warding_Flare'] = Use_Warding_Flare

def Use_Warding_Flare(Player_Character):
  pass

#Radiance_of_the_Dawn
def Apply_Radiance_of_the_Dawn(Player_Character):
  pass

def Use_Apply_Radiance_of_the_Dawn(Player_Character):
  pass

#Improved_Flare
def Apply_Improved_Flare(Player_Character):
  Player_Character.Reactions['Ally_Being_Attacked']['Warding_Flare'] = Use_Warding_Flare

#Potent_Spellcasting
#Corona_of_Light


#Nature_Domain
# animal friendship, speak with animals, barkskin, spike growth, plant growth, wind wall, dominate beast, grasping vine, insect plague, tree stride

#Acolyte_of_Nature

#Bonus_Proficiency
# heavy armor
def Apply_Nature_Bonus_Proficiencies(Player_Character):
  Player_Character.Armor_Profs.append('Heavy')

#Charm_Animals_and_Plants
#Dampen_Elements
#Divine_Strikes
#Master_of_Nature



#Order_Domain
# command, heroism, hold person, zone of truth, mass healing word, slow, compulsion, locate creature, commune, dominate person
#Bonus_Proficiencies
# heavy armor
# intimidation or persuasion

#Voice_of_Authority
#Orders_Demand
#Embodiment_of_the_Law
#Divine_Strike
#Orders_Wrath


#Peace_Domain
# heroism, sanctuary, aid, warding bond, beacon of hope, aura of purity, Otiluke's resilient sphere, greater restoration, Rary's telepathic bond

#Implement_of_Peace
# Insight, Performance, or Persuasion

#Emboldening_Bond
#Balm_of_Peace
#Protective_Bond
#Potent_Spellcasting
#Expansive_Bond



#Tempest_Domain
# spells = fog cloud, thunderwave, gust of wind, shatter, call lightning, sleet storm, control water, ice storm, destructive wave, insect plague

#Bonus_Proficiencies
def Apply_Tempest_Bonus_Proficiencies(Player_Character):
  Player_Character.Armor_Profs.append('Heavy')

#Wrath_of_the_Storm
def Apply_Wrath_of_the_Storm(Player_Character):
  Player_Character.Class_Resources['Cleric']['Wrath_of_the_Storm'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score)
  Player_Character.Reactions['Taking_Damage']['Wrath_of_the_Storm'] = Use_Wrath_of_the_Storm

def Use_Wrath_of_the_Storm(Player_Character):
  Player_Character.Class_Resources['Cleric']['Wrath_of_the_Storm'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score) - 1


#Destructive_Wrath
def Maximum_Damage_Roll(Dice_Number,Dice_Type):
  Result = Dice_Number * Dice_Type
  return Result

#Thunderbolt_Strike
Thunderbolt_Strike_Effect = Effects.Move_Effect('Large or Smaller Creature',True,'Target',10,'Away',False,False,False,False,False)
def Apply_Thunderbolt_Strike(Player_Character):
  Player_Character.Effects['Self_Dealing_Damage']['Thunder']['Thunderbolt_Strike'] = Use_Thunderbolt_Strike
  Player_Character.Effects['Self_Dealing_Damage']['Lightning']['Thunderbolt_Strike'] = Use_Thunderbolt_Strike

def Use_Thunderbolt_Strike(Player_Character):
  pass

#Divine_Strike
#Stormborn
def Apply_Stormborn(Player_Character):
  Player_Character.Speed['Flying'] = Player_Character.Speed['Walking']

#Trickery_Domain
# charm person, disguise self, mirror image, pass without trace, blink, dispel magic, dimension door, polymorph, dominate person, modify memory
#Blessing_of_the_Trickster
#Invoke_Duplicity
#Cloak_of_Shadows
#Divine_Strike
#Improved_Duplicity

#Twilight_Domain
# faerie fire, sleep, moonbeam, see invisibility, aura of vitality, Leomund's tiny hut, aura of life, greater invisibility, circle of power, mislead
#Bonus_Proficiencies
# martial weapons and heavy armor
#Eyes_of_Night

#Vigilant_Blessing

#Twilight_Sanctuary
#Steps_of_Night
#Divine_Strike
#Twilight_Shroud


#War_Domain
War_Domain_Spells = ['divine favor', 'shield of faith', 'magic weapon', 'spiritual weapon', "crusader's mantle", 'spirit guardians', 'freedom of movement', 'stoneskin', 'flame strike', 'hold monster']

#Bonus_Proficiencies
def Apply_Bonus_Proficiencies(Player_Character):
  Player_Character.Armor_Prof.append('Heavy')
  Player_Character.Weapon_Prof.append('Martial')

#War_Priest
  # lets you make an attack as a bonus action a number of times equal to your wisdom modifier

#Guided_Strike
Guided_Strike_Buff = Effects.Buff_Bonus_Effect('Self','Instantaneous','Bonus',False,False,10)

def Use_Guided_Strike(Target):
  Effects.Apply_Buff_Bonus_Effect(Guided_Strike_Buff,Target)

def Apply_Guided_Strike(Player_Character):
  Player_Character.Effects.append(Use_Guided_Strike)

#War_Gods_Blessing
War_Gods_Blessing_Buff = Effects.Buff_Bonus_Effect('Creature','Instantaneous','Bonus',False,False,10)

def Use_War_Gods_Blessing(Target):
  Effects.Apply_Buff_Bonus_Effect(War_Gods_Blessing_Buff,Target)

def Apply_War_Gods_Blessing(Player_Character):
  Player_Character.Effects.append(Use_War_Gods_Blessing)

#Divine_Strike
#Avatar_of_Battle

Arcana = Establishing_Hierarchy.Subclass(Cleric,'Arcana',[],False)
Death = Establishing_Hierarchy.Subclass(Cleric,'Death',[],False)
Grave = Establishing_Hierarchy.Subclass(Cleric,'Grave',[],False)
Knowledge = Establishing_Hierarchy.Subclass(Cleric,'Knowledge',[],False)
Forge = Establishing_Hierarchy.Subclass(Cleric,'Forge',[],False)
Life = Establishing_Hierarchy.Subclass(Cleric,'Life',[],False)
Light = Establishing_Hierarchy.Subclass(Cleric,'Light',[],False)
War = Establishing_Hierarchy.Subclass(Cleric,'War',[],False)
Tempest = Establishing_Hierarchy.Subclass(Cleric,'Tempest',[],False)
Trickery = Establishing_Hierarchy.Subclass(Cleric,'Trickery',[],False)
Twilight = Establishing_Hierarchy.Subclass(Cleric,'Twilight',[],False)

Cleric_Subclasses = [Arcana,Death,Grave,Knowledge,Forge,Life,Light,War,Tempest,Trickery,Twilight]
Cleric.Subclasses = Cleric_Subclasses