import Establishing_Hierarchy
import Effects
import Character_Functions
import Spell_Data
import Dice_Rolls
import Character_Actions

# Rogue

Rogue = Establishing_Hierarchy.Class('Rogue',8,['Dexterity', 'Intelligence'],4,["Light"],["Simple","Hand_Crossbow",'Longsword','Rapier','Shortsword'],["Acrobatics",'Athletics','Deception','Insight','Intimidation','Investigation','Perception','Performance','Persuasion','Sleight_Of_Hand','Stealth'],["Theives_Tools"],False,{"Arcane_Trickster","Assassin","Inquisitive","Mastermind","Phantom","Scout","Soulknife","Swashbuckler","Thief"},{"Expertise","Sneak_Attack","Thieves'_Cant","Cunning_Action","Uncanny_Dodge","Expertise","Evasion","Reliable_Talent","Blindsense","Slippery_Mind","Elusive","Stroke_of_Luck"},["Dexterity 13"],False,False,
{
    
})

def Rogue_Starting_Skills(Player_Character):
    pass

def Rogue_Add_Inventory(Player_Character):
   pass


def Rogue_First_Level(Player_Character):
    Player_Character.Saving_Throws.append(Rogue.Saving_Throws)
    Player_Character.Armor_Profs.append(Rogue.Armor_Profs)
    Rogue_Starting_Skills(Player_Character)
    Rogue_Add_Inventory(Player_Character)

    Player_Character.Instrument_Profs.append(Rogue.Tool_Profs)
    Player_Character.Weapon_Profs.append(Rogue.Weapon_Profs)


#Expertise

#Sneak_Attack
Sneak_Attack_Table = {          # I need to make a function that finds the character level in the dictionary and returns the corresponding number
    'Level':    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    'Dice_Num': [1,1,2,2,3,3,4,4,5, 5, 6, 6, 7, 7, 8, 8, 9, 9,10,10]
}

def Apply_Sneak_Attack(Player_Character):
    def Use_Sneak_Attack():
            Sneak_Attack_Effect = Effects.Buff_Bonus_Effect('Attack Roll','Creature','Instantaneous','Damage',Player_Character.Levels.count(Rogue),6,0)
            Effects.Apply_Buff_Bonus_Effect(Sneak_Attack_Effect,)
    Player_Character.Effects['Dependent']['Self_Attacking']['Hit']['Sneak_Attack'] = Use_Sneak_Attack



#Thieves_Cant
def Apply_Thieves_Cant(Player_Character):
    Player_Character.Languages.append('Thieves Cant')

#Cunning_Action
def Apply_Cunning_Action(Player_Character):
    Player_Character.Bonus_Actions['Independent'] += (Character_Actions.Move(),Character_Actions.Hide_Action(),Character_Actions.Disengage_Action())
    print(Player_Character.Bonus_Actions)

#Uncanny_Dodge
def Use_Uncanny_Dodge():
    Uncanny_Dodge = Effects.Buff_Bonus_Effect()

def Apply_Uncanny_Dodge(Player_Character):
    Player_Character.Reactions['Taking_Damage']['Uncanny_Dodge'] = Use_Uncanny_Dodge()

#Expertise


#Evasion
#Evasion_Effect = Effects.              what type would evasion be since it's dividing the damage in half dependent if it's an AOE and Dex or not
def Use_Evasion():
    Evasion = Effects.Buff_Bonus_Effect()                   # would this be replacement or reduction???

def Apply_Evasion(Player_Character):
    Player_Character.Effects['Self_Saving_Throw']['Dexterity']['Evasion'] = Use_Evasion()

#Reliable_Talent
Reliable_Talent_Effect = Effects.Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Placeholder',10)
def Apply_Reliable_Talent(Player_Character):
   pass

def Use_Reliable_Talent(Player_Character):
   pass

#Blindsense
def Apply_Blindsense(Player_Character):
    Player_Character.Senses['Imprecise']['Blindsight'] = 30

#Slippery_Mind
def Apply_Slippery_Mind(Player_Character):
    Player_Character.Saving_Throws.append('Wisdom')


#Elusive

#Stroke_of_Luck
#Stroke_of_Luck_Ranged = Effects.
    # it doesn't say what it replaces it with, it just says "you can turn a miss into a hit"
Stroke_of_Luck_Ability_Check = Effects.Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Placeholder',20)
def Apply_Storke_of_Luck(Player_Character):
  pass

def Use_Stroke_of_Luck(Player_Character):
  Effects.Apply_Buff_Replacement_Effect(Stroke_of_Luck_Ability_Check,False,False,False)


def Rogue_Level_One(Player_Character):
  pass

def Rogue_Level_Two(Player_Character):
  pass

def Rogue_Level_Three(Player_Character):
  pass

def Rogue_Level_Four(Player_Character):
  pass

def Rogue_Level_Five(Player_Character):
  pass

def Rogue_Level_Six(Player_Character):
  pass

def Rogue_Level_Seven(Player_Character):
  pass

def Rogue_Level_Eight(Player_Character):
  pass

def Rogue_Level_Nine(Player_Character):
  pass

def Rogue_Level_Ten(Player_Character):
  pass

def Rogue_Level_Eleven(Player_Character):
  pass

def Rogue_Level_Twelve(Player_Character):
  pass

def Rogue_Level_Thirteen(Player_Character):
  pass

def Rogue_Level_Fourteen(Player_Character):
  pass

def Rogue_Level_Fifteen(Player_Character):
  pass

def Rogue_Level_Sixteen(Player_Character):
  pass

def Rogue_Level_Seventeen(Player_Character):
  pass

def Rogue_Level_Eighteen(Player_Character):
  pass

def Rogue_Level_Nineteen(Player_Character):
  pass

def Rogue_Level_Twenty(Player_Character):
  pass


def Run_Rogue(Player_Character, Level):
  if Player_Character.First_Class == Rogue:
    Rogue_First_Level(Player_Character)
  else:
    pass

  Level = Player_Character.Levels.count(Rogue)
  if Level >= 1:
    Rogue_Level_One(Player_Character)
    Establishing_Hierarchy.Count_Player_Levels(Player_Character)
    if Level >= 2:
      Rogue_Level_Two(Player_Character)
      if Level >= 3:
        Rogue_Level_Three(Player_Character)
        if Level >= 4:
          Rogue_Level_Four(Player_Character)
          if Level >= 5:
            Rogue_Level_Five(Player_Character)
            if Level >= 6:
              Rogue_Level_Six(Player_Character)
              if Level >= 7:
                Rogue_Level_Seven(Player_Character)
                if Level >= 8:
                  Rogue_Level_Eight(Player_Character)
                  if Level >= 9:
                    Rogue_Level_Nine(Player_Character)
                    if Level >= 10:
                      Rogue_Level_Ten(Player_Character)
                      if Level >= 11:
                        Rogue_Level_Eleven(Player_Character)
                        if Level >= 12:
                          Rogue_Level_Twelve(Player_Character)
                          if Level >= 13:
                            Rogue_Level_Thirteen(Player_Character)
                            if Level >= 14:
                              Rogue_Level_Fourteen(Player_Character)
                              if Level >= 15:
                                Rogue_Level_Fifteen(Player_Character)
                                if Level >= 16:
                                  Rogue_Level_Sixteen(Player_Character)
                                  if Level >= 17:
                                    Rogue_Level_Seventeen(Player_Character)
                                    if Level >= 18:
                                        Rogue_Level_Eighteen(Player_Character)
                                        if Level >= 19:
                                          Rogue_Level_Nineteen(Player_Character)
                                          if Level == 20:
                                            Rogue_Level_Twenty(Player_Character)
  else:
    pass


# Arcane Trickster
def Apply_Spellcasting(Player_Character):
   pass

def Apply_Mage_Hand_Legerdemain(Player_Character):
   pass

def Apply_Magical_Ambush(Player_Character):
   pass

def Apply_Versatile_Trickster(Player_Character):
   pass

def Apply_Spell_Thief(Player_Character):
   pass

# Assassin
def Apply_Assassinate(Player_Character):
   pass

def Apply_Bonus_Proficiencies(Player_Character):
   pass

def Apply_Infiltration_Expertise(Player_Character):
   pass

def Apply_Imposter(Player_Character):
   pass

def Apply_Death_Strike(Player_Character):
   pass




# Inquisitive
def Apply_Eye_for_Deceit(Player_Character):
   pass
def Apply_Eye_for_Detail(Player_Character):
   pass
def Apply_Insightful_Fighting(Player_Character):
   pass
def Apply_Steady_Eye(Player_Character):
   pass
def Apply_Unerring_Eye(Player_Character):
   pass
def Apply_Eye_for_Weakness(Player_Character):
   pass

# Mastermind

# Phantom

# Scout

# Soulknife

# Swashbuckler

# Thief