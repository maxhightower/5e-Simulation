import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data
import pandas as pd
import Monsters

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll


# Druid
#(a) a wooden shield or (b) any simple weapon
#(a) a scimitar or (b) any simple melee weapon
#Leather armor, an explorer's pack, and a druidic focus

Armor = [['Leather','Shield']]
Weapons = [['Scimitar']],[['Simple Weapon']]
Tools = []
Instruments = []
Packs = [["Explorer's Pack"]]
Focus = [['Druidic Focus']]
Gold = ['2d4']

Druid = Establishing_Hierarchy.Class("Druid",8,["Wisdom", "Intelligence"],2,["Light","Medium","Shields"],["Club","Dagger","Dart","Javelin","Mace","Quarter_Staff","Scimitar","Sickle","Sling","Spear"],["Arcana","Animal_Handling","Insight","Medicine","Nature","Perception","Religion","Survival"],["Herbalism_Kit"],"Wisdom",["Moon","Shepherds","Stars","Wildfire","Land","Spores"],["Druidic","Spellcasting","Wild_Shape","Wild_Shape_Improvement","Timeless_Body","Beast_Spells","Archdruid"],"Wisdom 13",Spell_Data.Druid_Spell_List,"Full",
{
  'Armor': Armor,
  'Weapons': Weapons,
  'Tools': Tools,
  'Instruments': Instruments,
  'Packs': Packs,
  'Spellcasting_Focus': Focus,
  'Gold_Alternative': Gold
})


def Druid_Starting_Skills(Player_Character):
  pass

def Druid_Add_Inventory(Player_Character):
  pass

def Druid_First_Level(Player_Character):
  Druid_Spellcasting(Player_Character)
  Player_Character.Saving_Throws.append(Druid.Saving_Throws)
  Player_Character.Armor_Profs.append(Druid.Armor_Profs)
  Druid_Starting_Skills(Player_Character)
  Druid_Add_Inventory(Player_Character)

  Player_Character.Instrument_Profs.append(Druid.Tool_Profs)
  Player_Character.Weapon_Profs.append(Druid.Weapon_Profs)


#Druidic
def Druidic(Player_Character):
  Player_Character.Language_Profs.append("Druidic")

Druid_Spellcasting_Table = {
  'Druid_Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
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

#Spellcasting
def Druid_Spellcasting(Player_Character):
  Player_Character.Spellcasting_Known['Druid_Spells'] = Spell_Data.Druid_Spell_List
  Player_Character.Class_Save_DCs['Druid'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score) + 8 + Establishing_Hierarchy.levelToProficiency(Player_Character)

  #Arcane_Focus
  # if spells have a material component, and there isn't the material in inventory, if the character doesn't have an Arcane_Focus, remove the spell

  
  #print("Spell Save DC =",Player_Character.Spell_Save_DC)
  #print("Actions Available:",Player_Character.Actions)
  #print(Player_Character.Spells_Known)
  #Player_Character.Actions.append("Spells")


def Druid_Prepare_Spells(Player_Character):
  Number_of_Spells_Preparable = Player_Character.Levels.count(Druid) + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score)





#Wild_Shape

Available_Wildshape_Forms = Monsters.Creatures.query("Type == 'Beast'")
#print(Available_Wildshape_Forms)

def Apply_Wildshape(Player_Character):
  Player_Character.Class_Resources['Druid'] = {
    'Wildshape_Charges': Wild_Shape_Table['Charges'][Player_Character.Levels.count(Druid)-1]
      }
  Wild_Shape_Duration = Player_Character.Levels.count(Druid) / 2

#def Choose_Wildshape_Form(Player_Character):
#  pass


def Activate_Wildshape(Player_Character,Form):
  Wildshape = Effects.Transform_Effect('Wildshape',False,True,True,True,True,True,True,True,True,True,True,Form)
  Player_Character.Class_Resources['Druid']['Wildshape_Charges'] = Player_Character.Class_Resources['Druid']['Wildshape_Charges'] - 1

  Effects.Apply_Transform_Effect(Player_Character,Wildshape,Form)

def End_Wildshape(Player_Character):
  Effects.End_Transformed_Effect(Player_Character)


Wild_Shape_Table = {
  'Level':                            [                          1,                          2,          3,          4,          5,          6,          7,     8,     9,    10,    11,    12,    13,    14,    15,    16,    17,    18,    19,    20],
  'Charges':                          [                          0,                          2,          2,          2,          2,          2,          2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,  1000],
  'Wildshape_CR':                     [                          0,                        .25,        .25,         .5,         .5,         .5,         .5,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
  'Wildshape_Limitations':            [['No Swimming','No Flying'],['No Swimming','No Flying'],'No Flying','No Flying','No Flying','No Flying','No Flying','None','None','None','None','None','None','None','None','None','None','None','None','None'],
  'Moon_Druid_Wildshape_CR':          [                          0,                          1,          1,          1,          1,          2,          2,     2,     3,     3,     3,     4,     4,     4,     5,     5,     5,     6,     6,     6],
  'Moon_Druid_Wildshape_Limitations': [['No Swimming','No Flying'],['No Swimming','No Flying'],'No Flying','No Flying',     'None',     'None',     'None','None','None','None','None','None','None','None','None','None','None','None','None','None']
}



#Timeless_Body

#Beast_Spells

#Archdruid

def Druid_Level_One(Player_Character):
  Druidic(Player_Character)
  Druid_Spellcasting(Player_Character)

def Druid_Level_Two(Player_Character):
  Apply_Wildshape(Player_Character)

def Druid_Level_Three(Player_Character):
  pass

def Druid_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)

def Druid_Level_Five(Player_Character):
  pass

def Druid_Level_Six(Player_Character):
  pass

def Druid_Level_Seven(Player_Character):
  pass

def Druid_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)

def Druid_Level_Nine(Player_Character):
  pass

def Druid_Level_Ten(Player_Character):
  pass

def Druid_Level_Eleven(Player_Character):
  pass

def Druid_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Druid_Level_Thirteen(Player_Character):
  pass

def Druid_Level_Fourteen(Player_Character):
  pass

def Druid_Level_Fifteen(Player_Character):
  pass

def Druid_Level_Sixteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Druid_Level_Seventeen(Player_Character):
  pass

def Druid_Level_Eighteen(Player_Character):
  pass
  # Timless Body
  # Beast Spells

def Druid_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Druid_Level_Twenty(Player_Character):
  pass
  # Archdruid


#def Run_Druid(Player_Character):
#  for Player_Character.level in Druid_Features:
#    Player_Character.level(Player_Character)


def Run_Druid(Player_Character,Level):
  if Player_Character.First_Class == Druid:
    Druid_First_Level(Player_Character)
  else:
    pass


  Level = Player_Character.Levels.count(Druid)
  if Level >= 1:
    Druid_Level_One(Player_Character)
    #Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Druid_Level_Two(Player_Character)
      if Level >= 3:
        Druid_Level_Three(Player_Character)
        if Level >= 4:
          Druid_Level_Four(Player_Character)
          if Level >= 5:
            Druid_Level_Five(Player_Character)
            if Level >= 6:
              Druid_Level_Six(Player_Character)
              if Level >= 7:
                Druid_Level_Seven(Player_Character)
                if Level >= 8:
                  Druid_Level_Eight(Player_Character)
                  if Level >= 9:
                    Druid_Level_Nine(Player_Character)
                    if Level >= 10:
                      Druid_Level_Ten(Player_Character)
                      if Level >= 11:
                        Druid_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Druid_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Druid_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Druid_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Druid_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Druid_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Druid_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Druid_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Druid_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Druid_Level_Twenty(Player_Character)
  else:
    pass








## Druids
#Balm_of_the_Summer_Court
#Hearth_of_Moonlight_and_Shadow 
#Hidden_Paths
#Walker_in_Dreams

#Circle_of_Spore_Spells
#Halo_of_Spores
#Symbiotic_Entity
#Fungal_Infestation
#Spreading_Spores
#Fungal_Body

#Star_Map
#Starry_Form
#Cosmic_Omen
#Twinkling_Constellations
#Full_of_Stars

#Bonus_Cantrip
#Natural_Recovery
#Circle_of_the_Land_Spells
#Lands_Stride 
#Natures_Ward
#Natures_Sanctuary

#Combat_Wild_Shape

Moon_Druid_Wild_Shape_CR_Table = {'Level': [2,4,6,8,9,12,15,18], 'CR': [1,1,2,2,3,4,5,6],'Limitation': [['No Flying','No Swimming'],'No Flying','No Flying','','','','','']}
Moon_Druid_Wild_Shape_CR_Table = pd.DataFrame(Moon_Druid_Wild_Shape_CR_Table)
#print(Moon_Druid_Wild_Shape_CR_Table)

#Circle_Forms
#Primal_Strike
#Elemental_Wild_Shape 
#Thousand_Forms

#Speech_of_the_Woods
#Spirit_Totem
#Mighty_Summoner
#Guardian_Spirit
#Faithful_Summons

#Circle_of_Wildfire_Spells = Feature()
#Summon_Wildfire_Spirit = Feature()
#Enhanced_Bond = Feature()
#Cauterizing_Flames = Feature()
#Blazing_Revival = Feature()


Dreams = Establishing_Hierarchy.Subclass(Druid,[],False)
Moon = Establishing_Hierarchy.Subclass(Druid,[],False)
Wildfire = Establishing_Hierarchy.Subclass(Druid,[],False)
Stars = Establishing_Hierarchy.Subclass(Druid,[],False)
Spores = Establishing_Hierarchy.Subclass(Druid,[],False)
Shepherd = Establishing_Hierarchy.Subclass(Druid,[],False)

Druid_Subclasses = [Dreams,Moon,Wildfire,Stars,Spores,Shepherd]
Druid.Subclasses = Druid_Subclasses