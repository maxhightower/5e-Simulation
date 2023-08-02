import Effects
#import Spell_Data

global Current_Attack_Roll
global Current_Ability_Check
global Current_Saving_Throw
global Current_Damage_Roll


Skills = ["Athletics",
          "Acrobatics","Sleight_of_Hand","Stealth",
          "Arcana","History","Investigation","Nature","Religion",
          "Animal_Handling","Insight","Medicine","Perception","Survival",
          "Deception","Intimidation","Performance","Persuasion"]

Ability_Checks = {'Check': ["Athletics","Acrobatics","Sleight_of_Hand","Stealth","Arcana","History","Investigation","Nature","Religion","Animal_Handling","Insight","Medicine","Perception","Survival","Deception","Intimidation","Performance","Persuasion",'Initiative'],
                  'Ability_Score': ['Strength','Dexterity','Dexterity','Dexterity','Intelligence','Intelligence','Intelligence','Intelligence','Intelligence','Wisdom','Wisdom','Wisdom','Wisdom','Wisdom','Charisma','Charisma','Charisma','Charisma','Dexterity']}

Saves = ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma','Death']

Saving_Throws = {'Save': ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma','Death'],
                 'Ability_Score': ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma','None']}

def Roll_Gold(string):
  string.split()




# Extra Attack
def Extra_Attack(Player_Character):
  Player_Character.Attacks = 2

#Fighting Style
Fighting_Styles = ["Archery","Blessed_Warrior","Blind_Fighting","Defense","Druidic_Warrior","Dueling","Great_Weapon_Fighting","Interception","Protection","Superior_Technique","Thrown_Weapon_Fighting","Two_Weapon_Fighting","Unarmed_Fighting"]

def Choose_Fighting_Style(Player_Character):
  pass


def Choose_Item_in_Inventory(Player_Character):
  for i in Player_Character.Inventory:
    for j in i:
      print(i[j])
  Item = input('Which Item:')

#Archery_Fighting_Style_Attack_Bonus = Effects.Buff_Bonus_Effect('Target','Instantaneous','Attack Roll',False,False,2)
#Archery_Fighting_Style_Damage_Bonus = Effects.Buff_Bonus_Effect('Target','Instantaneous','Damage',False,False,2)

#def Archery_Fighting_Style(Player_Character):
  # will I need to make a tag on each attack that says whether I adds this bonus to to it?
    # well it would only need to be ranged weapon attacks
  # perhaps I could do something where each attack is like a formula
  # so Attack = Dice + Score + Proficiency + Fighting_Style 
  # or maybe I could have a tag on the character class that are placeholders for each of these fighting styles, similar to the extra attack attribute
#  Player_Character.Effects['Self_Attacking']['Rolling']['Bow'] = Archery_Fighting_Style_Attack_Bonus
#  Player_Character.Effects['Self_Attacking']['Hit']['Bow'] = Archery_Fighting_Style_Damage_Bonus

#def Blessed_Warrior_Fighting_Style(Player_Character):
#  Spell_Data.Cleric_Spell_List
#  Player_Character.Spellcasting_Prepared 


def Blind_Fighting_Style(Player_Character):
  Player_Character.Senses.append('Blindsight 10')
  # Within that range, you can effectively see anything that isn't behind total cover, even if you're blinded or in darkness. 
  # Moreover, you can see an invisible creature within that range, unless the creature successfully hides from you.

Defense_Fighting_Style_Effect = Effects.AC_Effect('Armor Equipped','Self','Passive',False,1)
def Defense_Fighting_Style(Player_Character):
  Player_Character.Effects['Passive']['Wearing_Armor']['Defense_Fighting_Style'] = Effects.Apply_AC_Effect(Defense_Fighting_Style,Player_Character)


def Druidic_Warrior_Fighting_Style(Player_Character):
  pass

Dueling_Fighting_Style_Effect = Effects.Buff_Bonus_Effect('Self','Instantaneous','Attack',False,False,2)
def Dueling_Fighting_Style(Player_Character):
  Player_Character.Effects['Self_Dealing_Damage'][Player_Character.Weapon_Equipped.Damage_Type]['Dueling_Fighting_Style'] = Effects.Apply_Buff_Bonus_Effect(Dueling_Fighting_Style_Effect)

Great_Weapon_Fighting_Style_Effect = Effects.Buff_Replacement_Effect(['Melee Weapon','Two-Handed'],'Damage Roll','Instantaneous','Replacement','Placeholder') 
def Great_Weapon_Fighting_Style(Player_Character):
  Player_Character.Effects['Self_Dealing_Damage'][Player_Character.Weapon_Equipped.Damage_Type]['Great_Weapon_Fighting_Style'] = Effects.Apply_Buff_Replacement_Effect(Great_Weapon_Fighting_Style_Effect,False,False,Player_Character)


def Interception_Fighting_Style(Player_Character):
  Interception_Damage_Reduction = Effects.Buff_Bonus_Effect('Damage','Instantaneous','Reduction',10,1,Player_Character.Prof_Bonus)
  Player_Character.Reactions['Interception'] = Effects.Apply_Buff_Bonus_Effect(Interception_Damage_Reduction,Current_Damage_Roll)
  
def Protection_Fighting_Style(Player_Character):
  pass

def Superior_Technique_Fighting_Style(Player_Character):
  pass

def Thrown_Weapon_Fighting_Style(Player_Character):
  pass

def Two_Weapon_Fighting_Style(Player_Character):
  pass

def Unarmed_Fighting_Style(Player_Character):
  pass



def ASI(Player_Character):
  #print('Running ASI Code Here')
  choice = input("Feat or ASI: ")
  if choice == "ASI":
    print("Strength:",Player_Character.Str_Score)
    print("Dexterity:",Player_Character.Dex_Score)
    print("Constitution:",Player_Character.Con_Score)
    print("Intelligence:",Player_Character.Int_Score)
    print("Wisdom:",Player_Character.Wis_Score)
    print("Charisma:",Player_Character.Cha_Score)
    distribution = input("+2 or +1:+1? ")
    if distribution == "+2" or "2":
      score = input("Choose a Stat \n1:Strength\n2:Dexterity\n3:Constitution\n4:Intelligence\n5:Wisdom\n6:Charisma \n")

      if score == "1":
        #print("Character Functions line 120")
        Player_Character.Str_Score += 2
        print("Strength:" + str(Player_Character.Str_Score))

      elif score == "2":
        Player_Character.Dex_Score += 2
        print("Dexterity:",Player_Character.Dex_Score)

      elif score == "3":
        Player_Character.Con_Score +=  2
        print("Constitution:",Player_Character.Con_Score)

      elif score == "4":
        Player_Character.Int_Score += 2
        print("Intelligence:",Player_Character.Int_Score)

      elif score == "5":
        Player_Character.Wis_Score += 2
        print("Wisdom: ",Player_Character.Wis_Score)

      elif score == "6":
        Player_Character.Cha_Score += 2
        print("Charisma:",Player_Character.Cha_Score)
      else:
        print("Fail")

    elif distribution == "+1:+1" or "1" or "1:1" or "+1":
      score1 = input("Choose your first stat \n1:Strength\n2:Dexterity\n3:Constitution\n4:Intelligence\n5:Wisdom\n6:Charisma \n")
      score2 = input("Choose your second stat \n1:Strength\n2:Dexterity\n3:Constitution\n4:Intelligence\n5:Wisdom\n6:Charisma \n")
      if score1 == "1":
        print("Character Functions line 149")
        Player_Character.Str_Score += 2
        print("Strength:" + str(Player_Character.Str_Score))

      elif score1 == "2":
        Player_Character.Dex_Score += 2
        print("Dexterity:",Player_Character.Dex_Score)

      elif score1 == "3":
        Player_Character.Con_Score +=  2
        print("Constitution:",Player_Character.Con_Score)

      elif score1 == "4":
        Player_Character.Int_Score += 2
        print("Intelligence:",Player_Character.Int_Score)

      elif score1 == "5":
        Player_Character.Wis_Score += 2
        print("Wisdom: ",Player_Character.Wis_Score)

      elif score1 == "6":
        Player_Character.Cha_Score += 2
        print("Charisma:",Player_Character.Cha_Score)
      if score2 == "1":
        print("Test")
        Player_Character.Str_Score += 2
        print("Strength:" + str(Player_Character.Str_Score))

      elif score2 == "2":
        Player_Character.Dex_Score += 2
        print("Dexterity:",Player_Character.Dex_Score)

      elif score2 == "3":
        Player_Character.Con_Score +=  2
        print("Constitution:",Player_Character.Con_Score)

      elif score2 == "4":
        Player_Character.Int_Score += 2
        print("Intelligence:",Player_Character.Int_Score)

      elif score2 == "5":
        Player_Character.Wis_Score += 2
        print("Wisdom: ",Player_Character.Wis_Score)

      elif score2 == "6":
        Player_Character.Cha_Score += 2
        print("Charisma:",Player_Character.Cha_Score)
  elif choice == "Feat":
    Feat = input('Which Feat: \n1:Aberrant_Dragonmark \n2:Alert \n3:Artificer_Initiate \n4:Athlete \n5:Bountiful_Luck') # eventually this list will have a script to generate it based on the prerequisites in the dictionary below




Feats_Dict = {
  'Name':                       ['Aberrant_Dragonmark','Alert','Artificer_Initiate','Athlete','Bountiful_Luck','Charger','Chef','Crossbow_Expert','Crusher','Defensive_Duelist','Divinely_Favored','Dragon_Fear','Dragon_Hide','Drow_High_Magic','Dual_Wielder','Dungeon_Delver','Durable','Dwarven_Fortitude','Eldritch_Adept','Elemental_Adept'],
  'Species_Prerequisite':       [                False,  False,               False,    False,      'Halfling',    False, False,            False,    False,              False,             False, 'Dragonborn', 'Dragonborn',           'Drow',         False,           False,    False,            'Dwarf',           False,            False],
  'Size_Prerequisite':          [                False,  False,               False,    False,           False,    False, False,            False,    False,              False,             False,        False,        False,            False,         False,           False,    False,              False,           False,            False],
  'Background_Prerequisite':    [                False,  False,               False,    False,           False,    False, False,            False,    False,              False,             False,        False,        False,            False,         False,           False,    False,              False,           False,            False],
  'Campaign_Prerequisite':      [                False,  False,               False,    False,           False,    False, False,            False,    False,              False,     'Dragonlance',        False,        False,            False,         False,           False,    False,              False,           False,            False],
  'Level_Prerequisite':         [                False,  False,               False,    False,           False,    False, False,            False,    False,              False,                 4,        False,        False,            False,         False,           False,    False,              False,           False,            False],
  'Feature_Prerequisite':       [                False,  False,               False,    False,           False,    False, False,            False,    False,              False,             False,        False,        False,            False,         False,           False,    False,              False,  'Spellcasting',   'Spellcasting'],
  'Ability_Score_Prerequisite': [                False,  False,               False,    False,           False,    False, False,            False,    False,           'DEX:13',             False,        False,        False,            False,         False,           False,    False,              False,           False,            False],
  'Proficiency_Prerequisite':   [                False,  False,               False,    False,           False,    False, False,            False,    False,              False,             False,        False,        False,            False,         False,           False,    False,              False,           False,            False]
}

# Feats

def Feat_Choice_Apply_Score(*Scores):
  for i in Scores:
    print(i)


#Aberrant Dragonmark
#Actor
  # Increase Charisma by 1, to a maximum of 20.
  # You have advantage on Charisma (Deception) and Charisma (Performance) checks when trying to pass yourself off as a different person.
  # You can mimic the speech of another person or the sounds made by other creatures. 
    # You must have heard the person speaking, 
    # or heard the creature make the sound, for at least 1 minute. 
    # A successful Wisdom (Insight) check contested by your Charisma (Deception) check allows a listener to determine that the effect is faked.

def Apply_Actor_Feat(Player_Character):
  Player_Character.CHA_Score + 1 

#Adept of the Black Robes
#Adept of the Red Robes
#Adept of the White Robes


#Alert
Alert_Bonus_Effect = Effects.Buff_Bonus_Effect('Self','Instantaneous','Initiative',False,False,5)
def Alert_Feat(Player_Character):
  Player_Character.Circumstances
  Player_Character.WRI.append('Surprisedimmu')
  Effects.Apply_Buff_Bonus_Effect(Alert_Bonus_Effect,'Self','Initiative',False,False)

  # need to add creatures can't have advantage when unseen



#Artificer Initiate
#Athlete
  # Increase your Strength or Dexterity by 1, to a maximum of 20.
  # When you are prone, standing up uses only 5 feet of your movement.
  # Climbing doesn't cost you extra movement.
  # You can make a running long jump or a running high jump after moving only 5 feet on foot, rather than 10 feet.

def Apply_Athlete_Feat(Ability_Choice,Player_Character):
  if Ability_Choice == 'STR':
    if Player_Character.STR_Score + 1 > 20:
      print('Strength Score Capped, applying bonus to Constitution')
      Player_Character.CON_Score = Player_Character.CON_Score + 1
    elif Player_Character.CON_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.STR_Score + 1
  else:
    if Player_Character.CON_Score + 1 > 20:
      print('Constitution Score Capped, applying bonus to Strength')
    elif Player_Character.STR_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.CON_Score + 1

# For the sake of the Simple Probability Assistant, the other features don't matter
# Athlete doesn't add a climbing speed, rather, climbing doesn't cost you extra movement
#def Athlete_Stand_Up(Player_Character):



#Bountiful Luck

#Charger
  # When you use your action to Dash, you can use a bonus action to make one melee weapon attack or to shove a creature.
  # If you move at least 10 feet in a straight line immediately before taking this bonus action, 
  # you either gain a +5 bonus to the attack's damage roll (if you chose to make a melee attack and hit) or push the target up to 10 feet away from you (if you chose to shove and you succeed).



def Apply_Charger_Feat(Player_Character):
  Player_Character.Bonus_Action['Dependent']['Dash']['Charger_Attack'] = Use_Charger_Attack()

def Use_Charger_Attack():
  pass

#Chef

#Crossbow Expert
  #You ignore the loading quality of crossbows with which you are proficient.
  #Being within 5 feet of a hostile creature doesn't impose disadvantage on your ranged attack rolls.
  #When you use the Attack action and attack with a one-handed weapon, you can use a bonus action to attack with a hand crossbow you are holding.

def Apply_Crossbow_Expert(Player_Character):
  Player_Character.Bonus_Action['Dependent']['Attack']['One_Handed_Weapon'] = Use_Crossbow_Expert_Attack()

def Use_Crossbow_Expert_Attack():
  pass

#Crusher
  # Increase your Strength or Constitution by 1, to a maximum of 20.
  # Once per turn, when you hit a creature with an attack that deals bludgeoning damage, you can move it 5 feet to an unoccupied space, provided the target is no more than one size larger than you.
  # When you score a critical hit that deals bludgeoning damage to a creature, attack rolls against that creature are made with advantage until the start of your next turn.

Crusher_Move_Effect = Effects.Move_Effect(['Attack Roll','Bludgeoning Damage'],True,'Target',5,'Any','End Location',False,False,False,False)
Crusher_Crit_Effect = Effects.Buff_Circumstance_Effect(['Attack Roll','Hit','Bludgeoning Damage'],'Target','1_Round','Attack Roll','Advantage')

def Apply_Crusher_Feat(Ability_Choice,Player_Character):
  if Ability_Choice == 'STR':
    if Player_Character.STR_Score + 1 > 20:
      print('Strength Score Capped, applying bonus to Constitution')
      Player_Character.CON_Score = Player_Character.CON_Score + 1
    elif Player_Character.CON_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.STR_Score + 1
  else:
    if Player_Character.CON_Score + 1 > 20:
      print('Constitution Score Capped, applying bonus to Strength')
    elif Player_Character.STR_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.CON_Score + 1
  
  Player_Character.Effects['Dealing_Damage']['Bludgeoning'] = Effects.Apply_Move_Effect(Crusher_Move_Effect)
  Player_Character.Effects['Self_Attacking']['Crit']['Bludgeoning'] = Effects.Apply_Buff_Circumstance_Effect(Crusher_Crit_Effect,'Target')

#Defensive Duelist
  # When you are wielding a finesse weapon with which you are proficient and another creature hits you with a melee attack, you can use your reaction to add your proficiency bonus to your AC for that attack, potentially causing the attack to miss you.



def Apply_Defensive_Duelist(Player_Character):
  Defensive_Duelist_AC_Buff = Effects.AC_Effect('Reaction','Self','Instantaneous',False,Player_Character.Prof_Bonus)
  # Check if the weapon Player is wielding is Finesse
  # Check if the weapon Player is wielding is Proficient
  Player_Character.Reactions


#Divinely Favored
#Dragon Fear
  #Increase your Strength, Constitution, or Charisma by 1, to a maximum of 20.
  #Instead of exhaling destructive energy, you can expend a use of your Breath Weapon trait to roar, forcing each creature of your choice within 30 feet of you to make a Wisdom saving throw (DC 8 + your proficiency bonus + your Charisma modifier). A target automatically succeeds on the save if it can't hear or see you. On a failed save, a target becomes frightened of you for 1 minute. If the frightened target takes any damage, it can repeat the saving throw, ending the effect on itself on a success.


def Apply_Dragon_Fear(Ability_Choice,Player_Character):
  if Ability_Choice == 'STR':
    if Player_Character.STR_Score + 1 > 20:
      print('Strength Score Capped, applying bonus to Constitution')
      Player_Character.CON_Score = Player_Character.CON_Score + 1
    elif Player_Character.CON_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.STR_Score + 1
  elif Ability_Choice == 'CHA':
    if Player_Character.STR_Score + 1 > 20:
      print('Strength Score Capped, applying bonus to Constitution')
      Player_Character.CON_Score = Player_Character.CON_Score + 1
    elif Player_Character.CON_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.STR_Score + 1
  else:
    if Player_Character.CON_Score + 1 > 20:
      print('Constitution Score Capped, applying bonus to Strength')
    elif Player_Character.STR_Score + 1 > 20:
      print('Unable to take Feat, Both scores Capped')
      pass
    else:
      Player_Character.STR_Score = Player_Character.CON_Score + 1


#Dragon Hide
  #Increase your Strength, Constitution, or Charisma by 1, to a maximum of 20.
  #Your scales harden. While you aren't wearing armor, you can calculate your AC as 13 + your Dexterity modifier. You can use a shield and still gain this benefit.
  #You grow retractable claws from the tips of your fingers. Extending or retracting the claws requires no action. The claws are natural weapons, which you can use to make unarmed strikes. If you hit with them, you deal slashing damage equal to 1d4 + your Strength modifier, instead of the normal bludgeoning damage for an unarmed strike.

#Drow High Magic
  #You learn more of the magic typical of dark elves. You learn the detect magic spell and can cast it at will, without expending a spell slot. You also learn levitate and dispel magic, each of which you can cast once without expending a spell slot. You regain the ability to cast those two spells in this way when you finish a long rest. Charisma is your spellcasting ability for all three spells.

#Dual Wielder
  #You gain a +1 bonus to AC while you are wielding a separate melee weapon in each hand.
  #You can use two-weapon fighting even when the one-handed melee weapons you are wielding aren't light.
  #You can draw or stow two one-handed weapons when you would normally be able to draw or stow only one.

#Dungeon Delver
  # Dungeon Delver isn't useful for Simple Probability Assistant


#Durable
  # Increase your Constitution score by 1, to a maximum of 20.
  # When you roll a Hit Die to regain hit points, the minimum number of hit points you regain from the roll equals twice your Constitution modifier (minimum of 2).

#Dwarven Fortitude
  # Increase your Constitution score by 1, to a maximum of 20.
  # Whenever you take the Dodge action in combat, you can spend one Hit Die to heal yourself. Roll the die, add your Constitution modifier, and regain a number of hit points equal to the total (minimum of 1).


#Eldritch Adept
#Elemental Adept

#Elven Accuracy
#Fade Away
#Fey Teleportation
#Fey Touched
#Fighting Initiate
#Flames of Phlegethos
#Gift of the Chromatic Dragon
#Gift of the Gem Dragon
#Gift of the Metallic Dragon
#Grappler
#Great Weapon Master
#Gunner
#Healer
#Heavily Armored
#Heavy Armor Master
#Infernal Constitution
#Initiate of High Sorcery
#Inspiring Leader
#Keen Mind
#Knight of the Crown
#Knight of the Rose
#Knight of the Sword
#Lightly Armored
#Linguist
#Lucky
#Mage Slayer
#Magic Initiate
#Martial Adept
#Medium Armor Master
#Metamagic Adept
#Mobile
#Moderately Armored
#Mounted Combatant
#Observant
#Orcish Fury
#Piercer
#Poisoner
#Polearm Master
#Prodigy
#Resilient
#Revenant Blade
#Ritual Caster
#Savage Attacker
#Second Chance
#Sentinel
#Shadow Touched
#Sharpshooter
#Shield Master
#Skill Expert
#Skilled
#Skulker
#Slasher
#Spell Sniper
#Squat Nimbleness
#Squire of Solamnia
#Strixhaven Initiate
#Strixhaven Mascot
#Svirfneblin Magic
#Tavern Brawler
#Telekinetic
#Telepathic
#Tough
#War Caster
#Weapon Master
#Wood Elf Magic