import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data

# Paladin

Paladin = Establishing_Hierarchy.Class('Paladin',10,["Wisdom", "Charisma"],2,["Light","Medium","Heavy","Shields"],["Simple","Martial"],["Athletics","Insight","Intimidation","Medicine","Persuasion","Religion"],False,"Charisma",["Conquest","Redemption","Watchers","Ancients","Glory","Devotion","Crown","Vengeance"],{"Divine_Sense","Lay_On_Hands","Divine_Smite","Fighting_Style","Paladin_Spellcasting","Divine_Health","Extra_Attack","Aura_of_Protection","Aura_of_Courage","Improved_Divine_Smite","Cleansing_Touch","Aura_Improvements"},["Strength 13","Charisma 13"],Spell_Data.Paladin_Spell_List,'Half',
{
  
})


def Paladin_Starting_Skills(Player_Character):
    pass

def Paladin_Add_Inventory(Player_Character):
    pass

def Paladin_First_Level(Player_Character):
    Player_Character.Saving_Throws.append(Paladin.Saving_Throws)
    Player_Character.Armor_Profs.append(Paladin.Armor_Profs)
    Paladin_Starting_Skills(Player_Character)
    Paladin_Add_Inventory(Player_Character)

    Player_Character.Instrument_Profs.append(Paladin.Tool_Profs)
    Player_Character.Weapon_Profs.append(Paladin.Weapon_Profs)



#Divine_Sense
def Use_Divine_Sense():
  pass

def Apply_Divine_Sense(Player_Character):
  Player_Character.Actions.append(Use_Divine_Sense)
  print(Player_Character.Action)

#Lay_On_Hands
def Use_Lay_On_Hands(Target,Amount):
  Lay_on_Hands = Effects.Healing_Effect()
  Effects.Apply_Healing_Effect()

def Apply_Lay_On_Hands(Player_Character):
  Player_Character.Actions.append(Use_Lay_On_Hands())
  Lay_on_Hands_Pool = Player_Character.Level * 5
  print(Player_Character.Actions)


#Divine_Smite
def Use_Divine_Smite():
  pass

def Apply_Divine_Smite(Player_Character):
  # a player needs to be able to choose a spell slot and get damage based on it
  # and then if the target is a fiend or undead deals extra damage
  pass

#Fighting_Style

Paladin_Spellcasting_Table = {
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
#Paladin_Spellcasting



#Divine_Health
def Apply_Divine_Health(Player_Character):
    Player_Character.WRI.append('diseaseimmu')


#Extra_Attack
#Character_Functions.Extra_Attack(Player_Character)

#Aura_of_Protection
def Apply_Aura_of_Protection(Player_Character):
    Bonus = Player_Character.Cha_Score
    Aura_of_Protection_Bonus = Effects.Buff_Bonus_Effect('Saving Throw','Ally','Passive','Saving Throw',0,0,Bonus)





#Aura_of_Courage

#Improved_Divine_Smite = Feature()

#Cleansing_Touch = Feature()

#Aura_Improvements = Feature()


def Paladin_Level_One(Player_Character):
  pass

def Paladin_Level_Two(Player_Character):
  pass

def Paladin_Level_Three(Player_Character):
  Apply_Divine_Health(Player_Character)

def Paladin_Level_Four(Player_Character):
  pass

def Paladin_Level_Five(Player_Character):
  pass

def Paladin_Level_Six(Player_Character):
  pass

def Paladin_Level_Seven(Player_Character):
  pass

def Paladin_Level_Eight(Player_Character):
  pass

def Paladin_Level_Nine(Player_Character):
  pass

def Paladin_Level_Ten(Player_Character):
  pass

def Paladin_Level_Eleven(Player_Character):
  pass

def Paladin_Level_Twelve(Player_Character):
  pass

def Paladin_Level_Thirteen(Player_Character):
  pass

def Paladin_Level_Fourteen(Player_Character):
  pass

def Paladin_Level_Fifteen(Player_Character):
  pass

def Paladin_Level_Sixteen(Player_Character):
  pass

def Paladin_Level_Seventeen(Player_Character):
  pass

def Paladin_Level_Eighteen(Player_Character):
  pass

def Paladin_Level_Nineteen(Player_Character):
  pass

def Paladin_Level_Twenty(Player_Character):
  pass


def Run_Paladin(Player_Character,Level):
  if Player_Character.First_Class == Paladin:
    Paladin_First_Level(Player_Character)
  else:
    pass

  Level = Player_Character.Levels.count(Paladin)
  if Level >= 1:
    Paladin_Level_One(Player_Character)
    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Paladin_Level_Two(Player_Character)
      if Level >= 3:
        Paladin_Level_Three(Player_Character)
        if Level >= 4:
          Paladin_Level_Four(Player_Character)
          if Level >= 5:
            Paladin_Level_Five(Player_Character)
            if Level >= 6:
              Paladin_Level_Six(Player_Character)
              if Level >= 7:
                Paladin_Level_Seven(Player_Character)
                if Level >= 8:
                  Paladin_Level_Eight(Player_Character)
                  if Level >= 9:
                    Paladin_Level_Nine(Player_Character)
                    if Level >= 10:
                      Paladin_Level_Ten(Player_Character)
                      if Level >= 11:
                        Paladin_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Paladin_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Paladin_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Paladin_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Paladin_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Paladin_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Paladin_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                        Paladin_Level_Eighteen(Player_Character)
                                        if Level >= 19:
                                          Paladin_Level_Nineteen(Player_Character)
                                          if Level == 20:
                                            Paladin_Level_Twenty(Player_Character)
  else:
    pass



#Ancients
def Ancients_Spells(Player_Character):
    Player_Character.Spellcasting_Prepared.append("Armor_of_Agathys","Command","Hold_Person","Spiritual_Weapon","Bestow_Curse","Fear","Dominate_Beast","Stone_Skin","Cloud_Kill","Dominate_Person")


#Conquest
#Crown
#Devotion
#Glory
#Oathbreaker
#Redemption
#Vengeance
#Watchers