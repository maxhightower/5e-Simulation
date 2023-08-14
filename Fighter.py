import Establishing_Hierarchy
import Effects
import Character_Functions
import Dice_Rolls
import Spell_Data
import Action_Economy as a
import Armor_and_Weapons

from Dice_Rolls import Current_Allied_Ability_Check
from Dice_Rolls import Current_Allied_Attack_Roll
from Dice_Rolls import Current_Allied_Saving_Throw
from Dice_Rolls import Current_Allied_Damage_Roll

from Dice_Rolls import Current_Enemy_Ability_Check
from Dice_Rolls import Current_Enemy_Attack_Roll
from Dice_Rolls import Current_Enemy_Saving_Throw
from Dice_Rolls import Current_Enemy_Damage_Roll


# Fighter
#(a) chain mail or (b) leather armor, longbow, and 20 arrows
#(a) a martial weapon and a shield or (b) two martial weapons

#(a) a dungeoneer's pack or (b) an explorer's pack

# I'm going to need to go through and make a "Layout 1" and "Layout 2" option for fighters because it appears to have a ranged vs melee loadouts

Armor = [['Chain Mail','Shield'],['Leather','Shield']]
Weapons = [['Martial Weapon','Light Crossbow','Longbow']],[['Martial Weapon','Handaxe','Handaxe']],[['Martial Weapon','Martial Weapon','Light Crossbow']]
Tools = []
Instruments = []
Packs = [["Dungeoneer's Pack"],["Explorer's Pack"]]
Focus = []
Gold = ['5d4']

Fighter = Establishing_Hierarchy.Class("Fighter",10,["Constitution","Strength"],2,["Light","Medium","Heavy","Shields"],["Simple","Martial"],["Acrobatics","Animal_Handling","Athletics","History","Insight","Intimidation","Perception","Survival"],False,False,["Battle_Master","Champion","Echo_Knight","Cavalier","Arcane_Archer","Eldritch_Knight","Rune_Knight"],["Fighting_Style","Second_Wind","Action_Surge","Extra_Attack","Indomitable","Extra_Attack","Indomitable","Action_Surge","Extra_Attack"],"Strength 13" or "Dexterity 13",False,False,
{
  'Armor': Armor,
  'Weapons': Weapons,
  'Tools': Tools,
  'Instruments': Instruments,
  'Packs': Packs,
  'Spellcasting_Focus': Focus,
  'Gold_Alternative': Gold
})

# Fighting_Style

def Fighter_Add_Inventory(Player_Character):
  # step one: choose items or gold
  # lets assume items for now
  Player_Character.Armor_Equipped.append(Armor_and_Weapons.Chain_Mail)
  Player_Character.Armor_Equipped.append(Armor_and_Weapons.Shield)

  # next step is weapons
  
  Player_Character.Weapon_Equipped.append(Armor_and_Weapons.Longsword)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Handaxe)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Handaxe)
  Player_Character.Inventory['Weapons'].append(Armor_and_Weapons.Light_Crossbow)
  Player_Character.Inventory['Packs'] += Fighter.Starting_Equipment['Packs']

# Skills
def Fighter_Starting_Skills(Player_Character):
  Player_Character.Skill_Profs.append(Fighter.Skill_Profs[:Fighter.Starting_Skill_Number])



def Fighter_First_Level(Player_Character):
  Player_Character.Saving_Throws.append(Fighter.Saving_Throws)
  Fighter_Add_Inventory(Player_Character)
  Fighter_Starting_Skills(Player_Character)

# Second_Wind
def Apply_Second_Wind(Player_Character):
  Player_Character.Class_Resources['Fighter'] = {
    'Second_Wind': 1
  }
  Player_Character.Bonus_Actions['Independent'] = {
    'Second_Wind': Use_Second_Wind(Player_Character)
  }
  
  def Reset_Second_Wind(Player_Character):
    Player_Character.Class_Resources['Fighter']['Second_Wind'] = 1

  Player_Character.Short_Rest_Options['Unlimited'].append(Reset_Second_Wind(Player_Character))
  Player_Character.Long_Rest_Options['Second_Wind'] = Reset_Second_Wind(Player_Character)


def Use_Second_Wind(Player_Character):    # need to make it so that the resource can't be used once it's at 0
  Second_Wind = Effects.Healing_Effect('Bonus Action','Self','Instantaneous','HP',10,1,Player_Character.Levels.count(Fighter))
  Effects.Apply_Healing_Effect(Second_Wind,Player_Character)
  Player_Character.Class_Resources['Fighter']['Second_Wind'] = 0





Fighter_Resource_Table = {
  'Level':                [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Action_Surge_Charges': [0,1,1,1,1,1,1,1,1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
  'Indomitable_Charges':  [0,0,0,0,0,0,0,0,1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
}

#def Use_Action_Surge(Player_Character):
#  a.Take_Action(Player_Character,World)

#def Apply_Action_Surge(Player_Character):
#  Player_Character.Free_Actions['Independent'] =+ [Use_Action_Surge(Player_Character)]
#  Player_Character.Class_Resources['Fighter']['Action_Surge'] = Fighter_Resource_Table['Action_Surge_Charges'][Player_Character.Levels.count(Fighter)]
#  
#  def Reset_Action_Surge(Player_Character):
#      Player_Character.Class_Resources['Fighter']['Action_Surge'] = Fighter_Resource_Table['Action_Surge_Charges'][Player_Character.Levels.count(Fighter)]#

#  Player_Character.Short_Rest_Options['Unlimited'].append(Reset_Action_Surge(Player_Character))
#  Player_Character.Long_Rest_Options['Action_Surge'] = Reset_Action_Surge(Player_Character)




def Apply_Indomitable(Player_Character):
  Player_Character.Class_Resources['Fighter']['Indomitable'] = Fighter_Resource_Table['Indomitable_Charges'][Player_Character.Levels.count(Fighter)-1]

  def Use_Indomitable(Current_Allied_Saving_Throw):
    Indomitable = Effects.Buff_Replacement_Effect('Saving Throws','Self','Instantaneous','Replacement','Placeholder')
    Effects.Apply_Buff_Replacement_Effect(Indomitable,False,False,Player_Character)
    Player_Character.Class_Resources['Fighter'] = {'Indomitable': Player_Character.Class_Resources['Fighter']['Indomitable'] - 1 }

  Player_Character.Effects['Dependent'] = {'Self_Saving_Throw': Use_Indomitable(Current_Allied_Saving_Throw)}

  def Reset_Indomitable(Player_Character):
    Player_Character.Class_Resources['Fighter']['Indomitable'] = Fighter_Resource_Table['Indomitable_Charges'][Player_Character.Levels.count(Fighter)-1]

  Player_Character.Long_Rest_Options['Indomitable'] = Reset_Indomitable(Player_Character)



# Extra_Attack2
def Extra_Attack2(Player_Character):
  Player_Character.Attacks = 3

# Extra_Attack3
def Extra_Attack3(Player_Character):
  Player_Character.Attacks = 4



def Fighter_Level_One(Player_Character):
  Character_Functions.Choose_Fighting_Style(Player_Character)
  Apply_Second_Wind(Player_Character)

def Fighter_Level_Two(Player_Character):
  #Apply_Action_Surge(Player_Character)
  pass

def Fighter_Level_Three(Player_Character):
  pass

def Fighter_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Five(Player_Character):
  Character_Functions.Extra_Attack(Player_Character)

def Fighter_Level_Six(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Seven(Player_Character):
  pass

def Fighter_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Nine(Player_Character):
  Apply_Indomitable(Player_Character)

def Fighter_Level_Ten(Player_Character):
  pass

def Fighter_Level_Eleven(Player_Character):
  Extra_Attack2(Player_Character)

def Fighter_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Thirteen(Player_Character):
  pass

def Fighter_Level_Fourteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Fifteen(Player_Character):
  pass

def Fighter_Level_Sixteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Seventeen(Player_Character):
  pass

def Fighter_Level_Eighteen(Player_Character):
  pass

def Fighter_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Fighter_Level_Twenty(Player_Character):
  Extra_Attack3(Player_Character)




def Run_Fighter(Player_Character,Level):
  if Player_Character.First_Class == Fighter:
    Fighter_First_Level(Player_Character)
  else:
    pass


  Level = Player_Character.Levels.count(Fighter)
  if Level >= 1:
    Fighter_Level_One(Player_Character)
    #Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Fighter_Level_Two(Player_Character)
      if Level >= 3:
        Fighter_Level_Three(Player_Character)
        if Level >= 4:
          Fighter_Level_Four(Player_Character)
          if Level >= 5:
            Fighter_Level_Five(Player_Character)
            if Level >= 6:
              Fighter_Level_Six(Player_Character)
              if Level >= 7:
                Fighter_Level_Seven(Player_Character)
                if Level >= 8:
                  Fighter_Level_Eight(Player_Character)
                  if Level >= 9:
                    Fighter_Level_Nine(Player_Character)
                    if Level >= 10:
                      Fighter_Level_Ten(Player_Character)
                      if Level >= 11:
                        Fighter_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Fighter_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Fighter_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Fighter_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Fighter_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Fighter_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Fighter_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                      Fighter_Level_Eighteen(Player_Character)
                                      if Level >= 19:
                                        Fighter_Level_Nineteen(Player_Character)
                                        if Level == 20:
                                          Fighter_Level_Twenty(Player_Character)
  else:
    pass




# Arcane Archer

Arcane_Archer_Table = {
  'Level':   [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
  'Options': [0,0,2,]
}

#Arcane_Archer_Lore
def Arcane_Archer_Lore(Player_Character):
  pass

#Arcane_Shot
def Arcane_Shot(Player_Character):
  pass
#Magic_Arrow

#EverReady_Shot




# Battle Master
#Student_of_War
def Apply_Student_of_War(Player_Character):
  Player_Character.Artisans_Tools_Prof.append()

#Combat_Superiority
Combat_Superiority = {
  'Level':            [1,2,3,4,5,6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20],
  'Dice_Type':        [0,0,8,8,8,8,10,10,10,10,10,10,10,10,10,10,10,12,12,12],
  'Superiority_Dice': [0,0,4,5,5,6,6],
  'Maneuvers_Known':  [0,0,3,5,7,9,9]
}





def Maneuver_Ambush():
  pass

def Maneuver_Bait_and_Switch():
  pass

def Maneuver_Brace():
  pass

def Maneuver_Commanders_Strike():
  pass

def Maneuver_Commanding_Presence():
  pass

def Maneuver_Disarming_Attack():
  pass

def Maneuver_Distracting_Strike():
  pass

def Maneuver_Evasive_Footwork():
  pass

def Maneuver_Feinting_Attack():
  pass

def Maneuver_Grappling_Strike():
  pass

def Maneuver_Goading_Attack():
  pass

def Maneuver_Lunging_Attack():
  pass

def Maneuver_Maneuvering_Attack():
  pass

def Maneuver_Menacing_Attack():
  pass

def Maneuver_Parry():
  pass

def Maneuver_Precision_Attack():
  pass

def Maneuver_Pushing_Attack():
  pass

def Maneuver_Rally():
  pass

def Maneuver_Riposte():
  pass

def Maneuver_Sweeping_Attack():
  pass

def Maneuver_Trip_Attack():
  pass


Combat_Maneuvers = [
  'Ambush',
  'Bait and Switch',
  'Brace',
  'Commanders_Strike',
  'Commanding Presence',
  'Disarming Attack',
  'Distracting Strike',
  'Evasive Footwork',
  'Feinting Attack',
  'Grappling Strike',
  'Goading Attack',
  'Lunging Attack',
  'Maneuvering Attack',
  'Menacing Attack',
  'Parry',
  'Precision Attack',
  'Pushing Attack',
  'Rally',
  'Riposte',
  'Sweeping Attack',
  'Trip Attack'
]

def Apply_Combat_Superiority(Player_Character):
  Maneuver_Save_DC = 8 + Player_Character.Prof_Bonus + max(Player_Character.STR_Score,Player_Character.DEX_Score) 
  Player_Character.Class_Save_DC['Fighter']['Maneuver_Save_DC'] = Maneuver_Save_DC

  Superiority_Dice_Bonus_Effect = Effects.Buff_Bonus_Effect('','Instantaneous','Bonus',Combat_Superiority['Level'][Player_Character.Levels.count(Fighter)],1,0)
  Superioirity_Dice_AC_Effect = Effects.AC_Effect

  def Choose_Maneuvers(Player_Character):
    pass

  
  #Ambush

  #Bait and Switch
  
  #Brace
  
  #Commanders_Strike
  # lose one of your extra attacks, in exchange use bonus action to allow an ally to attack

  #Commanding Presence
  
  #Disarming Attack
  # when you hit an attack, add superiority dice to damage roll, target makes a strength save, on a fail they drop what they're holding
  Player_Character.Effects['Self_Attacking']['Hit']['Disarming Attack'] = Maneuver_Disarming_Attack()
  
  #Distracting Strike
  # 


  #Evasive Footwork
  
  #Feinting Attack
  
  #Grappling Strike
  
  #Goading Attack
  
  #Lunging Attack
  
  #Maneuvering Attack
  
  #Menacing Attack
  
  #Parry
  
  #Precision Attack
  
  #Pushing Attack
  
  #Rally
  
  #Riposte
  
  #Sweeping Attack
  
  #Trip Attack




#Know_Your_Enemy
def Apply_Know_Your_Enemy(Player_Character):
  pass

def Use_Know_Your_Enemy(Player_Character):
  pass
  # Social effect

#Relentless




# Champion
#Improved_Critical
def Apply_Improved_Critical(Player_Character):
  Player_Character.Crit.append(19)

#Remarkable_Athlete
def Apply_Remarkable_Athlete(Player_Character):
  pass

#Additional_Fighting_Style

#Superior_Critical
def Apply_Superior_Critical(Player_Character):
  Player_Character.Crit.append(18)
#Survivor

def Champion_One(Player_Character):
  Apply_Improved_Critical(Player_Character)

def Champion_Two(Player_Character):
  Apply_Remarkable_Athlete(Player_Character)







#Manifest_Echo
#Unleash_Incarnation
#Echo_Avatar
#Shadow_Martyr
#Reclaim_Potential
#Legion_of_One


#Bonus_Proficiency
#Born_to_the_Saddle
#Unwavering_Mark
#Warding_Maneuver
#Hold_the_Line
#Ferocious_Charger
#Vigilant_Defender

#Spellcasting
#Weapon_Bond
#War_Magic
#Eldritch_Strike
#Arcane_Charge
#Improved_War_Magic

#Bonus_Proficiencies
#Rune_Carver
#Giants_Might
#Runic_Shield
#Additional_Rune_Known
#Great_Stature
#Additional_Rune_Known
#Master_of_Runes 
#Additional_Runes_Known
#Runic_Juggernaut

Echo_Knight = Establishing_Hierarchy.Subclass(Fighter,[],False)
Arcane_Archer = Establishing_Hierarchy.Subclass(Fighter,[],False)
Eldritch_Knight = Establishing_Hierarchy.Subclass(Fighter,[],True)
Rune_Knight = Establishing_Hierarchy.Subclass(Fighter,[],False)
Cavalier = Establishing_Hierarchy.Subclass(Fighter,[],False)
Champion = Establishing_Hierarchy.Subclass(Fighter,[],False)
Samurai = Establishing_Hierarchy.Subclass(Fighter,[],False)
Battle_Master = Establishing_Hierarchy.Subclass(Fighter,[],False)

Fighter_Subclasses = [Echo_Knight,Arcane_Archer,Eldritch_Knight,Rune_Knight,Cavalier,Champion,Samurai,Battle_Master]
Fighter.Subclasses = Fighter_Subclasses