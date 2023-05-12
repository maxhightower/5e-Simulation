import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data
import Armor_and_Weapons

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll


#(a) a rapier, (b) a longsword, or (c) any simple weapon
#(a) a diplomat's pack or (b) an entertainer's pack
#(a) a lute or (b) any other musical instrument
#Leather armor, and a dagger

Armor = [['Leather']]
Weapons = [['Rapier','Dagger'],['Longsword','Dagger'],['Simple Weapon','Dagger']]
Tools = [['Thieves Tools']]
Instruments = [['Lute'],['Musical Instrument']]
Packs = [["Diplomat's Pack"],["Entertainer's Pack"]]
Focus = []
Gold = ['5d4']

# Bard
Bard = Establishing_Hierarchy.Class("Bard",8,["Dexterity", "Charisma"],4,["Light"],["Simple","Hand_Crossbow","Longsword","Rapier","Shortsword"],["Any"],["Musical_Instruments"],"Charisma",["Eloquence","Glamour","Creation","Swords","Valor","Lore","Whispers"],["Bardic Inspiration","Spellcasting","Jack of All Trades","Song of Rest","Expertise","Bardic Inspiration","Font of Inspiration","Countercharm","Song of Rest","Expertise","Magical Secrets","Song of Rest","Magical Secrets","Bardic Inspiration","Song of Rest","Magical Secrets","Superior Inspiration"],"Charisma 13",Spell_Data.Bard_Spell_List,"Full",
{
  'Armor': Armor,
  'Weapons': Weapons,
  'Tools': Tools,
  'Instruments': Instruments,
  'Packs': Packs,
  'Focus': Focus,
  'Gold_Alternative': Gold
})


Bardic_Table = {
  'Level':              [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Inspiration_Dice':   [6,6,6,6,8,8,8,8,8,10,10,10,10,10,12,12,12,12,12,12],
  'Song_of_Rest_Dice':  [0,6,6,6,6,6,6,6,8, 8, 8, 8,10,10,10,10,12,12,12,12]
}


def Bard_Starting_Skills(Player_Character):
  Player_Character.Skill_Profs.append(Bard.Skill_Profs[:Bard.Starting_Skill_Number])
  #print(Player_Character.Skill_Profs)

def Bard_Starting_Items(Player_Character):
   
  Player_Character.Weapon_Equipped.append(Armor_and_Weapons.Rapier)
  Player_Character.Armor_Equipped.append(Armor_and_Weapons.Leather)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Dagger)
  Player_Character.Inventory['Instruments'].append('Lute')
  


def Bard_First_Level(Player_Character):
  Player_Character.Saving_Throws.append(Bard.Saving_Throws)
  Bard_Starting_Items(Player_Character)
  Bard_Starting_Skills(Player_Character)
  Player_Character.Armor_Profs.append(Bard.Armor_Profs)
  Player_Character.Instrument_Profs.append(Bard.Tool_Profs)
  Player_Character.Weapon_Profs.append(Bard.Weapon_Profs)


# Bardic Inspiration


def Feature_Bardic_Inspiration(Player_Character):
  Player_Character.Class_Resources['Bard']['Bardic_Charges'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Cha_Score)
  Dice_Size = Bardic_Table['Inspiration_Dice'][Player_Character.Levels.count(Bard)-1]
  Bardic_Inspiration = Effects.Buff_Bonus_Effect('Self','10_Minutes','Bonus',Dice_Size,1,0)
  
  # there isn't an ally at the moment to target with this so it's useless
  #Player_Character.Bonus_Action['Independent']['Barding_Inspiration'] = Grant_Bardic_Inspiration(Ally)

  def Grant_Bardic_Inspiration(Target):
    #if 'Self_Ability_Check' in Target.Effects.keys() == True:
    #  print(Target.Effects.keys())
    #  Target.Effects['Self_Ability_Check'].append('Apply_Bardic_Inspiration(Establishing_Hierarchy.Current_Ability_Check)')
    #else:
    #  Target.Effects['Self_Ability_Check'] = ['Apply_Bardic_Inspiration(Establishing_Hierarchy.Current_Ability_Check)']
    #  print(Target.Effects.keys())
    #  print(Target.Effects)


    if 'Self_Attacking' in Target.Effects.keys() == True:
      Target.Effects['Self_Attacking'].append('Apply_Bardic_Inspiration(Establishing_Hierarchy.Current_Attack_Roll)')
      print(Target.Effects)
    else:
      Target.Effects['Self_Attacking'] = ['Apply_Bardic_Inspiration(Establishing_Hierarchy.Current_Attack_Roll)']
      print(Target.Effects)

    #if 'Self_Making_Save' in Target.Effects.keys() == True:
    #  Target.Effects['Self_Making_Save'].append('Apply_Bardic_Inspiration(Establishing_Hierarchy.Current_Saving_Throw)')
    #else: 
    #  Target.Effects['Self_Making_Save'] = ['Apply_Bardic_Inspiration(Establishing_Hierarchy.Current_Saving_Throw)']
    #  print(Target.Effects)

  def Apply_Bardic_Inspiration(Current_Attack_Roll):
    Effects.Apply_Buff_Bonus_Effect(Bardic_Inspiration,Establishing_Hierarchy.Current_Attack_Roll)

    #Player_Character.Effects['Self_Ability_Check'].remove(Apply_Bardic_Inspiration(Current_Ability_Check))
    Player_Character.Effects['Self_Attacking'].remove(Apply_Bardic_Inspiration(Current_Attack_Roll))
    #Player_Character.Effects['Self_Making_Save'].remove(Apply_Bardic_Inspiration(Current_Saving_Throw))



# Spellcasting
Bard_Spellcasting_Table = {
  'Bard_Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
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

def Bard_Spellcasting(Player_Character):
    Player_Character.Spellcasting_Known['Bard_Spells'] = Spell_Data.Bard_Spell_List
    Spell_Save_DC = Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Cha_Score) + 8 + Establishing_Hierarchy.levelToProficiency(Player_Character)
    
    Player_Character.Class_Save_DCs['Bard'] = {
      'Spell_Save_DC': Spell_Save_DC
    }

  #Arcane_Focus
  # if spells have a material component, and there isn't the material in inventory, if the character doesn't have an Arcane_Focus, remove the spell

def Bard_Choose_Spells(Player_Character):
  pass


#Jack_of_All_Trades
def Jack_of_All_Trades(Player_Character):
    for i in Character_Functions.Skills:
        if i not in Player_Character.Skill_Profs or i not in Player_Character.Skill_Expertise:
            Player_Character.Skill_Half_Prof.append(i)

#Song_of_Rest
def Song_of_Rest(Player_Character):
    def Song_of_Rest_Short_Rest(Player_Character,Party):
      for Ally in Party:
        Effects.Short_Rest(Ally)
      

#Expertise
def Expertise(Player_Character):
  Player_Character.Skill_Expertise.append(Player_Character.Skill_Profs[0])
  Player_Character.Skill_Profs.remove[0]


#Bardic_Inspiration
#def Bardic_Inspiration(Player_Character):
  #Player_Character.Bonus_Actions.append("Bardic_Inspiration")
  #print(Player_Character.Bonus_Actions)
  #Bardic_Inspiration_Dice = 6
  #Bardic_Inspiration = Effects.Buff_Bonus_Effect(['Ability Check','Saving Throw','Attack Roll'],'Ally','10 minutes',20,Bardic_Inspiration_Dice,1,0)

#Font_of_Inspiration
def Apply_Font_of_Inspiration(Player_Character):
  Player_Character.Short_Rest_Options['Unlimited'].append(Use_Font_of_Inspiration)
  Player_Character.Long_Rest_Options['Font_of_Inspiration'] = Use_Font_of_Inspiration

def Use_Font_of_Inspiration(Player_Character):
  Player_Character.Class_Resources['Bard']['Bardic_Charges'] = Establishing_Hierarchy.abilityScoreToModifier(Player_Character)

#Countercharm
#def Apply_Countercharm(Player_Character):
#  Player_Character.Actions['Countercharm'] = Use_Countercharm()
#
#  def Use_Countercharm(Target):
#    Target.Circumstances['Saving Throws']['Frightened']
#    Target.Circumstances['Saving Throws']['Charmed']
#
#    Player_Character.Circumstances['Saving Throws']['Frightened']
#    Player_Character.Circumstances['Saving Throws']['Charmed']


#Song_of_Rest
def Song_of_Rest(Player_Character):
  pass


#Expertise = Feature()
def Expertise(Player_Character):
  if len(Player_Character.Skill_Profs) < 2:
    pass
  else:
    Player_Character.Skill_Expertise.append(Player_Character.Skill_Profs[0])
    Player_Character.Skill_Profs.remove(Player_Character.Skill_Profs[0])


#Magical_Secrets = Feature()
def Magical_Secrets(Player_Character):
  pass



#Superior_Inspiration = Feature()


def Bard_Choose_Subclass(Player_Character):
  pass


def Bard_Level_One(Player_Character):
  Player_Character.Class_Resources['Bard'] = {}
  Feature_Bardic_Inspiration(Player_Character)
  Bard_Spellcasting(Player_Character)

def Bard_Level_Two(Player_Character):
  Jack_of_All_Trades(Player_Character)

def Bard_Level_Three(Player_Character):
  Bard_Choose_Subclass(Player_Character)
  Expertise(Player_Character)

def Bard_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)

def Bard_Level_Five(Player_Character):
  Apply_Font_of_Inspiration(Player_Character)

def Bard_Level_Six(Player_Character):
  #Apply_Countercharm(Player_Character)
  pass

def Bard_Level_Seven(Player_Character):
  pass

def Bard_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)

def Bard_Level_Nine(Player_Character):
  pass

def Bard_Level_Ten(Player_Character):
  Expertise(Player_Character)
  Magical_Secrets(Player_Character)

def Bard_Level_Eleven(Player_Character):
  pass

def Bard_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Bard_Level_Thirteen(Player_Character):
  pass

def Bard_Level_Fourteen(Player_Character):
  Magical_Secrets(Player_Character)

def Bard_Level_Fifteen(Player_Character):
  pass

def Bard_Level_Sixteen(Player_Character):
  pass

def Bard_Level_Seventeen(Player_Character):
  pass

def Bard_Level_Eighteen(Player_Character):
  Magical_Secrets(Player_Character)

def Bard_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Bard_Level_Twenty(Player_Character):
  pass

Bard_Features = [Bard_Level_One, Bard_Level_Two, Bard_Level_Seven, Bard_Level_Ten, Bard_Level_Eleven, Bard_Level_Eighteen, Bard_Level_Twenty]

#def Run_Bard(Player_Character):
#  for Player_Character.Level in Bard_Features:
#    Player_Character.Level(Player_Character)

def Run_Bard(Player_Character,Level):
  #print('here 0')
  if Player_Character.First_Class == Bard:
    #print('here 1')
    Bard_First_Level(Player_Character)
  else:
    #print('here 2')
    pass


  Level = Player_Character.Levels.count(Bard)
  if Level >= 1:
    Bard_Level_One(Player_Character)
    #Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Bard_Level_Two(Player_Character)
      if Level >= 3:
        Bard_Level_Three(Player_Character)
        if Level >= 4:
          Bard_Level_Four(Player_Character)
          if Level >= 5:
            Bard_Level_Five(Player_Character)
            if Level >= 6:
              Bard_Level_Six(Player_Character)
              if Level >= 7:
                Bard_Level_Seven(Player_Character)
                if Level >= 8:
                  Bard_Level_Eight(Player_Character)
                  if Level >= 9:
                    Bard_Level_Nine(Player_Character)
                    if Level >= 10:
                      Bard_Level_Ten(Player_Character)
                      if Level >= 11:
                        Bard_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Bard_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Bard_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Bard_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Bard_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Bard_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Bard_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Bard_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Bard_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Bard_Level_Twenty(Player_Character)
  else:
    pass


#Mote_of_Potential
#Mote_Ability_Check = Effects.Buff_Replacement_Effect()
#Mote_Attack_Roll = Effects.Spell_Effect()
#Mote_Saving_Throw = Effects.Healing_Effect()

#def Mote_of_Potential_Bardic_Inspiration(Player_Character):
#  Player_Character.Effects.append(Mote_Ability_Check, Mote_Attack_Roll, Mote_Saving_Throw)

#Performance_of_Creation
#Performance_of_Creation_Object_Forms = []

#def Performance_of_Creation(Player_Character):
#  Player_Character.Actions.append(Performance_of_Creation)
#  Item_GP_Value = 20 * Player_Character.Level
#  Item_Duration = Player_Character.Prof_Bonus
  #Object_of_Performance_of_Creation = Effects.Create_Item_Effect('Object_of_Creation',False,False,Item_Duration,'Location','item type',False,'weight',False,False,'material')
    # perhaps this isn't the best way of going about this feature. 
    # What if instead I gave the bard a list of all the nonmagical objects from the excel sheet that are less than or equal to their GP Value
        # I could also add additional options of various materials, sizes, and options such as walls, vehicles, etc from the Ultimate RPG List
    # 

#Animating_Performance
#def Animating_Performance(Player_Character):
#  Player_Character.Actions.append(Animating_Performance)
  # should I spawn an entity of a dancing sword? or should I enchant the object that's already in the environment
  # for the Player Character Probability part, I can simplify it to Dancing Sword
  
#Creative_Crescendo





#Silver_Tongue

def Apply_Silver_Tongue(Player_Character):
  Silver_Tongue_Effect = Effects.Buff_Replacement_Effect('<10',Player_Character,'Instantaneous',False,10)
  Player_Character.Effects['Self_Ability_Check']['Persuasion']['Silver_Tongue'] = Use_Silver_Tongue
  Player_Character.Effects['Self_Ability_Check']['Deception']['Silver_Tongue'] = Use_Silver_Tongue

  def Use_Silver_Tongue():
    Effects.Apply_Buff_Replacement_Effect(Silver_Tongue_Effect,False,False,False)



#Unsettling_Words
#Unfailing_Inspiration
#Universal_Speech
#Infectious_Inspiration

#Mantle_of_Inspiration
#Enthralling_Performance
#Mantle_of_Majesty
#Unbreakable_Majesty

#Bonus_Proficiencies
#Cutting_Words
#Additional_Magical_Secrets
#Peerless_Skill

#Guiding_Whispers
#Spiritual_Focus
#Tales_from_Beyond
#Spirit_Session
#Mystical_Connection

#Bonus_Proficiencies
#Fighting_Style
#Blade_Flourish
#Extra_Attack

#Masters_Flourish
#Bonus_Proficiencies
#Combat_Inspiration
#Extra_Attack
#Battle_Magic


#Psychic_Blades
Psychic_Blades_Table = {
  'Level':    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Dice_Num': [0,0,2,2,3,3,3,3,3, 5, 5, 5, 5, 5, 8, 8, 8, 8, 8, 8] 
}

def Apply_Psychic_Blades(Player_Character):
  Player_Character.Effects['Self_Attacking']['Hit']['Psychic_Blades'] = Use_Psychic_Blades
  Psychic_Blades_Effect = Effects.Buff_Bonus_Effect('Target','Instantaneous','Damage',6,Psychic_Blades_Table['Dice_Num'][Player_Character.Levels.count(Bard)],0)

  def Use_Psychic_Blades():
    Player_Character.Class_Resources['Bardic_Charges'] = Player_Character.Class_Resources['Bardic_Charges'] - 1

#Words_of_Terror
def Apply_Words_of_Terror(Player_Character):
  Player_Character.Effects['Self_Social_Encounter']['1_Minute']
  Player_Character.Class_Resources['Bard']['Words_of_Terror'] = 1
  Player_Character.Short_Rest_Options['Unlimited'] = Reset_Words_of_Terror(Player_Character)
  Player_Character.Long_Rest_Options['Words_of_Terror'] = Reset_Words_of_Terror(Player_Character)

  def Reset_Words_of_Terror(Player_Character):
    Player_Character.Class_Resources['Bard']['Words_of_Terror'] = 1

  def Use_Words_of_Terror(Target):
    Player_Character.Class_Resources['Bard']['Words_of_Terror'] = 0
    

#Mantle_of_Whispers
#Shadow_Lore
