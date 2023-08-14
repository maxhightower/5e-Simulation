import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data

# Sorcerer

Sorcerer = Establishing_Hierarchy.Class('Sorcerer',6,['Constitution', 'Charisma'],2,False,['Dagger','Dart','Sling','Quarter_Staff','Light_Crossbow'],['Arcana','Deception','Insight','Intimidation','Persuasion','Religion'],False,"Charisma",["Draconic","Wild_Magic","Aberrant_Mind","Clockwork_Soul","Shadow","Storm","Divine_Soul"],["Spellcasting","Font_of_Magic","Metamagic","Metamagic","Metamagic","Sorcerous_Restoration"],["Charisma 13"],Spell_Data.Sorcerer_Spell_List,'Full',
{
    
})


def Sorcerer_Starting_Skills(Player_Character):
  pass

def Sorcerer_Add_Inventory(Player_Character):
  pass


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


#Spellcasting
def Sorcerer_Spellcasting(Player_Character):
  Player_Character.Spellcasting_Known['Sorcerer'] = Spell_Data.Sorcerer_Spell_List


#Font_of_Magic
# switching between spell slots and sorcery points

Sorcery_Point_Conversion_Table = {
    'Spell_Slot_Level': [1,2,3,4,5],
    'Sorcery_Point_Amount': [2,3,5,6,7]
}


#Metamagic
Metamagic_Dictionary = {
    'Level':             [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    'Metamagic_Options': [0,0,2,2,2,2,2,2,2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4],
    'Sorcery_Points':    [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
}

def Apply_Font_of_Magic(Player_Character):
    Player_Character.Class_Resources['Sorcerer']['Sorcery_Points'] = Player_Character.Levels.count(Sorcerer)

def Use_Convert_Spell_Slots(Option, Spell_Slot, Sorcery_Points):
  if Option == 'Spell_to_Point':
    pass

  elif Option == 'Point_to_Spell':
    pass

  else:
    pass

def Subtle_Spell():
  pass

def Heightened_Spell():
  pass

def Twinned_Spell():
  pass

def Quickened_Spell():
  pass

def Careful_Spell():
  pass

def Seeking_Spell():
  pass

def Transmuted_Spell():
  pass

def Extended_Spell():
  pass

def Distanced_Spell():
  pass

def Empowered_Spell():
  pass


Metamagic_Options = {
    'Subtle_Spell'
    'Heightened_Spell'   # disadvantage on the first save
    'Twinned_Spell'
    'Quickened_Spell'
    'Careful_Spell'
    'Seeking_Spell'
    'Transmuted_Spell'
    'Extended_Spell'    # double duration
    'Distanced_Spell'   # double distance
    'Empowered_Spell'    # reroll 1s on damage
}


# Magical Guidance

#Metamagic
def Apply_Metamagic(Player_Character):
  pass

def Choose_Metamagic(Player_Character):
  pass

def Use_Metamagic(Player_Character):
  pass


#Metamagic

#Sorcerous_Restoration

def Sorcerer_First_Level(Player_Character):
    Sorcerer_Spellcasting(Player_Character)
    Player_Character.Saving_Throws.append(Sorcerer.Saving_Throws)
    Player_Character.Armor_Profs.append(Sorcerer.Armor_Profs)
    Sorcerer_Starting_Skills(Player_Character)
    Sorcerer_Add_Inventory(Player_Character)

    Player_Character.Instrument_Profs.append(Sorcerer.Tool_Profs)
    Player_Character.Weapon_Profs.append(Sorcerer.Weapon_Profs)


def Sorcerer_Level_One(Player_Character):
  pass

def Sorcerer_Level_Two(Player_Character):
  pass

def Sorcerer_Level_Three(Player_Character):
  pass

def Sorcerer_Level_Four(Player_Character):
  pass

def Sorcerer_Level_Five(Player_Character):
  pass

def Sorcerer_Level_Six(Player_Character):
  pass

def Sorcerer_Level_Seven(Player_Character):
  pass

def Sorcerer_Level_Eight(Player_Character):
  pass

def Sorcerer_Level_Nine(Player_Character):
  pass

def Sorcerer_Level_Ten(Player_Character):
  pass

def Sorcerer_Level_Eleven(Player_Character):
  pass

def Sorcerer_Level_Twelve(Player_Character):
  pass

def Sorcerer_Level_Thirteen(Player_Character):
  pass

def Sorcerer_Level_Fourteen(Player_Character):
  pass

def Sorcerer_Level_Fifteen(Player_Character):
  pass

def Sorcerer_Level_Sixteen(Player_Character):
  pass

def Sorcerer_Level_Seventeen(Player_Character):
  pass

def Sorcerer_Level_Eighteen(Player_Character):
  pass

def Sorcerer_Level_Nineteen(Player_Character):
  pass

def Sorcerer_Level_Twenty(Player_Character):
  pass


def Run_Sorcerer(Player_Character, Level):
  if Player_Character.First_Class == Sorcerer:
    Sorcerer_First_Level(Player_Character)
  else:
    pass

  Level = Player_Character.Level_Count
  if Level >= 1:
    Sorcerer_Level_One(Player_Character)
    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Sorcerer_Level_Two(Player_Character)
      if Level >= 3:
        Sorcerer_Level_Three(Player_Character)
        if Level >= 4:
          Sorcerer_Level_Four(Player_Character)
          if Level >= 5:
            Sorcerer_Level_Five(Player_Character)
            if Level >= 6:
              Sorcerer_Level_Six(Player_Character)
              if Level >= 7:
                Sorcerer_Level_Seven(Player_Character)
                if Level >= 8:
                  Sorcerer_Level_Eight(Player_Character)
                  if Level >= 9:
                    Sorcerer_Level_Nine(Player_Character)
                    if Level >= 10:
                      Sorcerer_Level_Ten(Player_Character)
                      if Level >= 11:
                        Sorcerer_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Sorcerer_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Sorcerer_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Sorcerer_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Sorcerer_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Sorcerer_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Sorcerer_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                        Sorcerer_Level_Eighteen(Player_Character)
                                        if Level >= 19:
                                          Sorcerer_Level_Nineteen(Player_Character)
                                          if Level == 20:
                                            Sorcerer_Level_Twenty(Player_Character)
  else:
    pass



Aberrant_Mind = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Clockwork = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Divine = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Lunar = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Shadow = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Storm = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Genie = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
    # Djinn
    # Efreeti
    # Marid
    # Dao
Draconic = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
Wild_Magic = Establishing_Hierarchy.Subclass(Sorcerer,[],False)
