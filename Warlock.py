import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data

# Warlock

Warlock = Establishing_Hierarchy.Class('Warlock',8,['Wisdom', 'Charisma'],2,['Light','Medium','Shields'],['Simple'],['Arcana','Deception','History','Intimidation','Investigation','Nature','Religion'],False,"Charisma",{"Fiend","Archfey","Fathomless","Genie","Celestial","Undying","Undead","Great_Old_One","Hexblade"},{"Pact_Magic","Eldritch_Invocations","Mystic_Arcanum(6th_Level)","Mystic_Arcanum(7th_Level)","Mystic_Arcanum(8th_Level)","Mystic_Arcanum(9th_Level)","Eldritch_Master"},"Charisma 13",Spell_Data.Warlock_Spell_List,'Full',
{
    
})


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

def Warlock_Starting_Skills(Player_Character):
  pass

def Warlock_Add_Inventory(Player_Character):
  pass


def Warlock_Spellcasting(Player_Character):
  pass

#Pact_Magic
# Blade
# Tome
# Chain
# Talisman

#Eldritch_Invocations
Eldritch_Invocations_Table = {
    'Level_Requirement': [],
    'Pact_Magic_Requirement': [],
    'Other_Prerequisites': []
}


#Mystic_Arcanum_Sixth

#Mystic_Arcanum_Seventh

#Mystic_Arcanum_Eighth

#Mystic_Arcanum_Nineth

#Eldritch_Master
def Warlock_First_Level(Player_Character):
    Warlock_Spellcasting(Player_Character)
    Player_Character.Saving_Throws.append(Warlock.Saving_Throws)
    Player_Character.Armor_Profs.append(Warlock.Armor_Profs)
    Warlock_Starting_Skills(Player_Character)
    Warlock_Add_Inventory(Player_Character)

    Player_Character.Instrument_Profs.append(Warlock.Tool_Profs)
    Player_Character.Weapon_Profs.append(Warlock.Weapon_Profs)


def Warlock_Level_One(Player_Character):
  pass

def Warlock_Level_Two(Player_Character):
  pass

def Warlock_Level_Three(Player_Character):
  pass

def Warlock_Level_Four(Player_Character):
  pass

def Warlock_Level_Five(Player_Character):
  pass

def Warlock_Level_Six(Player_Character):
  pass

def Warlock_Level_Seven(Player_Character):
  pass

def Warlock_Level_Eight(Player_Character):
  pass

def Warlock_Level_Nine(Player_Character):
  pass

def Warlock_Level_Ten(Player_Character):
  pass

def Warlock_Level_Eleven(Player_Character):
  pass

def Warlock_Level_Twelve(Player_Character):
  pass

def Warlock_Level_Thirteen(Player_Character):
  pass

def Warlock_Level_Fourteen(Player_Character):
  pass

def Warlock_Level_Fifteen(Player_Character):
  pass

def Warlock_Level_Sixteen(Player_Character):
  pass

def Warlock_Level_Seventeen(Player_Character):
  pass

def Warlock_Level_Eighteen(Player_Character):
  pass

def Warlock_Level_Nineteen(Player_Character):
  pass

def Warlock_Level_Twenty(Player_Character):
  pass


def Run_Warlock(Player_Character, Level):
  if Player_Character.First_Class == Warlock:
    Warlock_First_Level(Player_Character)
  else:
    pass

  Level = Player_Character.Levels.count(Warlock)
  if Level >= 1:
    Warlock_Level_One(Player_Character)
    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Warlock_Level_Two(Player_Character)
      if Level >= 3:
        Warlock_Level_Three(Player_Character)
        if Level >= 4:
          Warlock_Level_Four(Player_Character)
          if Level >= 5:
            Warlock_Level_Five(Player_Character)
            if Level >= 6:
              Warlock_Level_Six(Player_Character)
              if Level >= 7:
                Warlock_Level_Seven(Player_Character)
                if Level >= 8:
                  Warlock_Level_Eight(Player_Character)
                  if Level >= 9:
                    Warlock_Level_Nine(Player_Character)
                    if Level >= 10:
                      Warlock_Level_Ten(Player_Character)
                      if Level >= 11:
                        Warlock_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Warlock_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Warlock_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Warlock_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Warlock_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Warlock_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Warlock_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                        Warlock_Level_Eighteen(Player_Character)
                                        if Level >= 19:
                                          Warlock_Level_Nineteen(Player_Character)
                                          if Level == 20:
                                            Warlock_Level_Twenty(Player_Character)
  else:
    pass



# Hexblade
# Celestial
# Fiend
# Great Old One
# Fathomless
# Archfey
# Undead
# Undying

