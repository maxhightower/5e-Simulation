import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data

# Wizard

Wizard = Establishing_Hierarchy.Class('Wizard',6,['Wisdom', 'Intelligence'],2,False,['Dagger','Dart','Sling','Quarter_Staff','Light_Crossbow'],['Arcana','History','Insight','Investigation','Medicine','Religion'],False,"Intelligence",["Abjuration","Conjuration","Chronurgy","Divination","Bladesinging","Evocation","Illusion","Necromancy","Transmutation","Scribes","War","Graviturgy","Enchantment"],["Arcane_Recovery","Spellcasting","Spell_Mastery","Signature_Spells"],"Intelligence 13",Spell_Data.Wizard_Spell_List,'Full',
{
    
})

def Wizard_Starting_Skills(Player_Character):
  pass

def Wizard_Add_Inventory(Player_Character):
  pass

Wizard_Spellcasting_Table = {
  'Wizard_Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
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

#Arcane_Recovery
def Use_Arcane_Recovery():
    pass

def Apply_Arcane_Recovery(Player_Character):
    Player_Character.Short_Rest_Options += Use_Arcane_Recovery()

#Spellcasting
def Wizard_Spellcasting(Player_Character):
  Player_Character.Spellcasting_Known['Wizard'] = Spell_Data.Wizard_Spell_List
  Player_Character.Class_Save_DCs['Wizard'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Int_Score) + 8 + Establishing_Hierarchy.levelToProficiency(Player_Character)
  
  #print("Spell Save DC =",Player_Character.Spell_Save_DC)
  #print("Actions Available:",Player_Character.Actions)
  #print(Player_Character.Spellcasting_Prepared)
  #Player_Character.Actions.append("Spells")            Need to define the action of casting later

    # Prepared Spellcasting
    # Ritual Spellcasting

#Spell_Mastery
def Apply_Spell_Mastery(Player_Character):
    Player_Character.At_Will_Spells
    Spell_Data.Wizard_Spell_List

#Signature_Spells
def Apply_Signature_Spells(Player_Character):
    Player_Character.Per_Use_Spells['1/short_rest']
    Spell_Data.Wizard_Spell_List

def Wizard_First_Level(Player_Character):
    Wizard_Spellcasting(Player_Character)
    Player_Character.Saving_Throws.append(Wizard.Saving_Throws)
    Player_Character.Armor_Profs.append(Wizard.Armor_Profs)
    Wizard_Starting_Skills(Player_Character)
    Wizard_Add_Inventory(Player_Character)

    Player_Character.Instrument_Profs.append(Wizard.Tool_Profs)
    Player_Character.Weapon_Profs.append(Wizard.Weapon_Profs)


def Wizard_Level_One(Player_Character):
  pass

def Wizard_Level_Two(Player_Character):
  pass

def Wizard_Level_Three(Player_Character):
  pass

def Wizard_Level_Four(Player_Character):
  pass

def Wizard_Level_Five(Player_Character):
  pass

def Wizard_Level_Six(Player_Character):
  pass

def Wizard_Level_Seven(Player_Character):
  pass

def Wizard_Level_Eight(Player_Character):
  pass

def Wizard_Level_Nine(Player_Character):
  pass

def Wizard_Level_Ten(Player_Character):
  pass

def Wizard_Level_Eleven(Player_Character):
  pass

def Wizard_Level_Twelve(Player_Character):
  pass

def Wizard_Level_Thirteen(Player_Character):
  pass

def Wizard_Level_Fourteen(Player_Character):
  pass

def Wizard_Level_Fifteen(Player_Character):
  pass

def Wizard_Level_Sixteen(Player_Character):
  pass

def Wizard_Level_Seventeen(Player_Character):
  pass

def Wizard_Level_Eighteen(Player_Character):
  pass

def Wizard_Level_Nineteen(Player_Character):
  pass

def Wizard_Level_Twenty(Player_Character):
  pass


def Run_Wizard(Player_Character, Level):
  if Player_Character.First_Class == Wizard:
    Wizard_First_Level(Player_Character)
  else:
    pass

  Level = Player_Character.Levels.count(Wizard)
  if Level >= 1:
    Wizard_Level_One(Player_Character)
    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Wizard_Level_Two(Player_Character)
      if Level >= 3:
        Wizard_Level_Three(Player_Character)
        if Level >= 4:
          Wizard_Level_Four(Player_Character)
          if Level >= 5:
            Wizard_Level_Five(Player_Character)
            if Level >= 6:
              Wizard_Level_Six(Player_Character)
              if Level >= 7:
                Wizard_Level_Seven(Player_Character)
                if Level >= 8:
                  Wizard_Level_Eight(Player_Character)
                  if Level >= 9:
                    Wizard_Level_Nine(Player_Character)
                    if Level >= 10:
                      Wizard_Level_Ten(Player_Character)
                      if Level >= 11:
                        Wizard_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Wizard_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Wizard_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Wizard_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Wizard_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Wizard_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Wizard_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                        Wizard_Level_Eighteen(Player_Character)
                                        if Level >= 19:
                                          Wizard_Level_Nineteen(Player_Character)
                                          if Level == 20:
                                            Wizard_Level_Twenty(Player_Character)
  else:
    pass


# Abjuration
# Abjurers Ward


# Bladesinging
# Blade Song

# Conjuration
# Conjure Item

# Benign Transposition

# Divination
# Potent

# Evocation
# Enchantment
# Illusion
# Scribes
# Necromancy
# Transmutation
# War Magic
# 

Abjuration = Establishing_Hierarchy.Subclass(Wizard,'Abjuration',[],False)
Bladesinging = Establishing_Hierarchy.Subclass(Wizard,'Bladesinging',[],False)
Conjuration = Establishing_Hierarchy.Subclass(Wizard,'Conjuration',[],False)
Divination = Establishing_Hierarchy.Subclass(Wizard,'Divination',[],False)
Evocation = Establishing_Hierarchy.Subclass(Wizard,'Evocation',[],False)
Enchantment = Establishing_Hierarchy.Subclass(Wizard,'Enchantment',[],False)
Illusion = Establishing_Hierarchy.Subclass(Wizard,'Illusion',[],False)
Scribes = Establishing_Hierarchy.Subclass(Wizard,'Scribes',[],False)
Necromancy = Establishing_Hierarchy.Subclass(Wizard,'Necromancy',[],False)
Transmutation = Establishing_Hierarchy.Subclass(Wizard,'Transmutation',[],False)
War_Magic = Establishing_Hierarchy.Subclass(Wizard,'War Magic',[],False)

Wizard_Subclasses = [Abjuration,Bladesinging,Conjuration,Divination,Evocation,Enchantment,Illusion,Scribes,Necromancy,Transmutation,War_Magic]
