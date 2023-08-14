import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data
import Character_Actions

# Ranger

Ranger = Establishing_Hierarchy.Class('Ranger',10,["Dexterity", "Strength"],2,["Light","Medium","Shields"],["Simple","Martial"],["Animal_Handling","Athletics","Insight","Investigation","Nature","Perception","Stealth","Survival"],False,"Wisdom",["Gloomstalker","Hunter","Beast_Master","Drake_Warden","Fey_Wanderer","Horizon_Walker","Monster_Slayer"],["Favored_Enemy","Natural_Explorer","Fighting_Style","Ranger_Spellcasting","Primeval_Awareness","Extra_Attack","Land's_Stride","Hide_in_Plain_Sight","Natural_Explorer_Improvement","Vanish","Feral_Sense","Foe_Slayer"],["Dexterity 13","Wisdom 13"],Spell_Data.Ranger_Spell_List,'Half',
{
    
})


def Ranger_Starting_Skills(Player_Character):
    pass

def Ranger_Add_Inventory(Player_Character):
    pass

def Ranger_First_Level(Player_Character):
    Player_Character.Saving_Throws.append(Ranger.Saving_Throws)
    Player_Character.Armor_Profs.append(Ranger.Armor_Profs)
    Ranger_Starting_Skills(Player_Character)
    Ranger_Add_Inventory(Player_Character)

    Player_Character.Instrument_Profs.append(Ranger.Tool_Profs)
    Player_Character.Weapon_Profs.append(Ranger.Weapon_Profs)



Ranger_Spellcasting_Table = {
  'Ranger_Level': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
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

def Ranger_Spellcasting(Player_Character):
  pass



Ranger_Features = {
  'Level':              [1,2,3,4,5,6,14],
  'Favored_Foes':       [1,1,1,1,1,2,3],
  'Favored_Enemy_Dice': [4,1,1,1,1,6,8],
  'Favored_Terrains':   [1,1,1,1,1,2,3]
}

#Favored_Enemy
Favored_Enemy_Dict = {
  'Creatures': {
    'Types':     ['Aberrations','Beasts','Celestials','Constructs', 'Dragons','Elementals',   'Fey',  'Fiends','Giants','Monstrosities','Oozes','Plants','Undead','Humanoid'],
    'Languages': [    'Abyssal','Sylvan', 'Celestial',    'Modron','Draconic',    'Primal','Sylvan','Infernal', 'Giant',     'Draconic','','Sylvan','Deep Speech','Humanoid'],
    },
  'Humanoids': {
    'Types':     ['Orcs','Gnolls','Goblins','Tritons','Elves','Half-Elves','Dwarves','Humans','Dragonborn','Leonin','Tabaxi','Aasimar','Shifters','Aarakocra','Changeling','Gnome','Genasi','Gith','Halfling','Tiefling'],
    'Languages': ['Orcish', ]
  }
}

Natural_Environments = ['Arctic','Coastal','Desert','Forest','Grassland','Mountain','Swamp','Underdark']

def Add_Favored_Enemy(Player_Character):
  Favored_Enemy_Type = input('Favored Enemy: ')
  Player_Character.Circumstances['Ability Checks']['Survival'][Favored_Enemy_Type] = 'Advantage '
  Player_Character.Circumstances['Ability Checks']['Intelligence'][str(Favored_Enemy_Type)] = 'Advantage '
  Player_Character.Languages.append(Favored_Enemy_Dict['Creatures']['Languages'][Favored_Enemy_Type])


def Apply_Favored_Foe(Player_Character):
  Favored_Foe_Effect = Effects.Buff_Bonus_Effect('Target','Instantaneous','Damage',Ranger_Features['Favored_Enemy_Dice'][Player_Character.Levels.count(Ranger)],1,0)
  #Player_Character.Effects['Self_Attacking']['Hit']['Favored_Foe'] = Use_Favored_Foe(Target)
  Player_Character.Class_Resources['Ranger']['Favored_Foe_Charges'] = Player_Character.Prof_Bonus
  Player_Character.Long_Rest_Options['Favored_Foe'] = Reset_Favored_Foe(Player_Character)

  def Use_Favored_Foe(Target):
    Player_Character.Concentrating = True
    Player_Character.Class_Resources['Ranger']['Favored_Foe_Charges'] = Player_Character.Class_Resources['Ranger']['Favored_Foe_Charges'] - 1
    Player_Character.Effects['Self_Attacking']['Hit'].remove('Favored_Foe')
    Player_Character.Effects['Self_Attacking']['Hit']['Favored_Foe_Damage'] = Activate_Favored_Foe(Target)

    def Activate_Favored_Foe(Target):
      Effects.Apply_Buff_Bonus_Effect(Favored_Foe_Effect,Target)

  def Reset_Favored_Foe(Player_Character):
    Player_Character.Class_Resources['Ranger']['Favored_Foe_Charges'] = Player_Character.Prof_Bonus

#Natural_Explorer
def Apply_Natural_Explorer(Player_Character):
  def Add_Natural_Explorer_Terrain(Player_Character):
    Favored_Terrain_Type = input('Favored Terrain')
#  Favored_Terrain_Type 



# Deft Explorer



#Ranger_Spellcasting
def Apply_Ranger_Spellcasting(Player_Character):
  Player_Character.Spellcasting_Known['Ranger_Spells'] = Spell_Data.Ranger_Spell_List



#Primeval_Awareness
def Apply_Primeval_Awareness(Player_Character):
  Player_Character.Actions['Primeval_Awareness'] = Use_Primeval_Awareness(Player_Character)

def Use_Primeval_Awareness(Player_Character):
  pass



#Lands_Stride

#Hide_in_Plain_Sight
def Apply_Hide_in_Plain_Sight(Player_Character):
  pass

def Use_Hide_in_Plain_Sight(Player_Character):
  pass


#Natural_Explorer_Improvement

#Vanish
def Apply_Vanish(Player_Character):
    Player_Character.Bonus_Actions['Independent']['Hide'] = Character_Actions.Hide_Action(Player_Character,'Placeholder','Placeholder')

#Feral_Sense
def Apply_Feral_Sense(Player_Character):
  Player_Character.Senses['Precise']['Feral_Sense'] = 30


#Foe_Slayer
def Apply_Foe_Slayer(Player_Character):
  Foe_Slayer_Damage = Effects.Buff_Bonus_Effect('Target','Instantaneous','Damage',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score))
  Foe_Slayer_Bonus = Effects.Buff_Bonus_Effect('Target','Instantaneous','Bonus',0,0,Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score))
  Player_Character.Class_Resources['Ranger']['Foe_Slayer_Effect'] = 1
  Player_Character.Round_Options['Foe_Slayer'] = Reset_Foe_Slayer(Player_Character)
  #Player_Character.Effects['Self_Attacking']['Rolling']['Foe_Slayer'] = Use_Foe_Slayer_Bonus(Target)
  #Player_Character.Effects['Self_Attacking']['Hit']['Foe_Slayer'] = Use_Foe_Slayer_Damage(Target)

  def Use_Foe_Slayer_Damage(Target):
    Effects.Apply_Buff_Bonus_Effect(Foe_Slayer_Damage,Target)
    Player_Character.Class_Resources['Ranger']['Foe_Slayer_Effect'] = Player_Character.Class_Resources['Ranger']['Foe_Slayer_Effect'] - 1

  def Use_Foe_Slayer_Bonus(Target):
    Effects.Apply_Buff_Bonus_Effect(Foe_Slayer_Damage,Target)
    Player_Character.Class_Resources['Ranger']['Foe_Slayer_Effect'] = Player_Character.Class_Resources['Ranger']['Foe_Slayer_Effect'] - 1

  def Reset_Foe_Slayer(Player_Character):
    Player_Character.Class_Resources['Ranger']['Foe_Slayer_Effect'] = 1



def Choose_Subclass(Player_Character):
  pass




def Ranger_First_Level(Player_Character):
  pass

def Ranger_Level_One(Player_Character):
  #Add_Favored_Enemy(Player_Character)
  Apply_Favored_Foe(Player_Character)


def Ranger_Level_Two(Player_Character):
  Character_Functions.Choose_Fighting_Style(Player_Character)
  Apply_Ranger_Spellcasting(Player_Character)

def Ranger_Level_Three(Player_Character):
  Choose_Subclass(Player_Character)

def Ranger_Level_Four(Player_Character):
  Character_Functions.ASI(Player_Character)

def Ranger_Level_Five(Player_Character):
  Character_Functions.Extra_Attack(Player_Character)

def Ranger_Level_Six(Player_Character):
  pass

def Ranger_Level_Seven(Player_Character):
  pass

def Ranger_Level_Eight(Player_Character):
  Character_Functions.ASI(Player_Character)

def Ranger_Level_Nine(Player_Character):
  pass

def Ranger_Level_Ten(Player_Character):
  pass

def Ranger_Level_Eleven(Player_Character):
  pass

def Ranger_Level_Twelve(Player_Character):
  Character_Functions.ASI(Player_Character)

def Ranger_Level_Thirteen(Player_Character):
  pass

def Ranger_Level_Fourteen(Player_Character):
  pass

def Ranger_Level_Fifteen(Player_Character):
  pass

def Ranger_Level_Sixteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Ranger_Level_Seventeen(Player_Character):
  pass

def Ranger_Level_Eighteen(Player_Character):
  pass

def Ranger_Level_Nineteen(Player_Character):
  Character_Functions.ASI(Player_Character)

def Ranger_Level_Twenty(Player_Character):
  Apply_Foe_Slayer(Player_Character)


def Run_Ranger(Player_Character,Level):
  if Player_Character.First_Class == Ranger:
    Ranger_First_Level(Player_Character)
  else:
    pass

  Level = Player_Character.Levels.count(Ranger)
  if Level >= 1:
    Ranger_Level_One(Player_Character)
    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Ranger_Level_Two(Player_Character)
      if Level >= 3:
        Ranger_Level_Three(Player_Character)
        if Level >= 4:
          Ranger_Level_Four(Player_Character)
          if Level >= 5:
            Ranger_Level_Five(Player_Character)
            if Level >= 6:
              Ranger_Level_Six(Player_Character)
              if Level >= 7:
                Ranger_Level_Seven(Player_Character)
                if Level >= 8:
                  Ranger_Level_Eight(Player_Character)
                  if Level >= 9:
                    Ranger_Level_Nine(Player_Character)
                    if Level >= 10:
                      Ranger_Level_Ten(Player_Character)
                      if Level >= 11:
                        Ranger_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Ranger_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Ranger_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Ranger_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Ranger_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Ranger_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Ranger_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                        Ranger_Level_Eighteen(Player_Character)
                                        if Level >= 19:
                                          Ranger_Level_Nineteen(Player_Character)
                                          if Level == 20:
                                            Ranger_Level_Twenty(Player_Character)
  else:
    pass



# Beast Master
def Apply_Rangers_Companion(Player_Character):
  pass

#def Apply_Primal_Companion(Player_Character):
#  pass

def Apply_Exceptional_Training(Player_Character):
  pass

def Apply_Bestial_Fury(Player_Character):
  pass

def Apply_Share_Spells(Player_Character):
  pass



# Drakewarden
def Apply_Draconic_Gift(Player_Character):
  pass

def Apply_Drake_Companion(Player_Character):
  pass

def Apply_Bond_of_Fang_and_Scale(Player_Character):
  pass

def Drakes_Breath(Player_Character):
  pass

def Perfected_Bond(Player_Character):
  pass




# Fey Wanderer
def Apply_Dreadful_Strikes(Player_Character):
  pass

def Apply_Fey_Wanderer_Magic(Player_Character):
  pass

def Apply_Otherworldly_Glamour(Player_Character):
  pass

def Apply_Beguilding_Twist(Player_Character):
  pass

def Apply_Fey_Reinforcements(Player_Character):
  pass

def Apply_Misty_Wanderer(Player_Character):
  pass



# Gloomstalker
def Apply_Gloomstalker_Magic(Player_Character):
  pass

def Apply_Dread_Ambusher(Player_Character):
  pass

def Apply_Umbral_Sight(Player_Character):
  pass

def Apply_Iron_Mind(Player_Character):
  pass

def Apply_Stalkers_Fury(Player_Character):
  pass

def Apply_Shadowy_Dodge(Player_Character):
  pass



# Horizon Walker
def Apply_Horizon_Walker_Magic(Player_Character):
  pass

def Apply_Detect_Portal(Player_Character):
  pass

def Apply_Planar_Warrior(Player_Character):
  pass

def Apply_Ethereal_Step(Player_Character):
  pass

def Apply_Distant_Strike(Player_Character):
  pass

def Apply_Spectral_Defense(Player_Character):
  pass




# Hunter
def Apply_Hunters_Prey(Player_Character):
  pass

def Apply_Defensive_Tactics(Player_Character):
  pass

def Apply_Multiattack(Player_Character):
  pass

def Apply_Superior_Hunters_Defense(Player_Character):
  pass



# Monster Slayer
def Apply_Monster_Slayer_Magic(Player_Character):
  pass

def Apply_Hunters_Sense(Player_Character):
  pass

def Apply_Slayers_Prey(Player_Character):
  pass

def Apply_Supernatural_Defense(Player_Character):
  pass

def Apply_Magic_Users_Nemesis(Player_Character):
  pass

def Apply_Slayers_Counter(Player_Character):
  pass




# Swarmkeeper
def Apply_Gathered_Swarm(Player_Character):
  pass

def Apply_Swarmkeeper_Magic(Player_Character):
  pass

def Apply_Writhing_Tide(Player_Character):
  pass

def Apply_Mighty_Swarm(Player_Character):
  pass

def Apply_Swarming_Dispersal(Player_Character):
  pass


