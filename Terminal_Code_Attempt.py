import pandas
#import Character_Actions

import Species
import Monsters
import Backgrounds

Target_Creature = input('Target: ')
Target_Book = input('Source: ')

Target_ID = str(Target_Creature + ',' + Target_Book)
Target = Monsters.monster_primes[Target_ID]
#Cleric.Target_Placeholder = Target
print(Target)

#Player_Character.Actions.append(Character_Actions.Weapon_Attack(Player_Character,Target,Player_Character.Weapon_Equipped[0]))
#Player_Character.Bonus_Actions['Dependent']['Attack_Action'].append(Character_Actions.Two_Weapon_Fighting_Attack_Bonus_Action(Player_Character,Target,Player_Character.Weapon_Equipped[0]))



Target_Summary = {
    'Name': [Target.Name],
    'Book': [Target.Book],
    'HP': [Target.HP],
    'AC': [Target.AC],
    'CR': [Target.CR],
    'WRI': [Target.WRI]
}

Target_Summary2 = pandas.DataFrame.from_dict(Target_Summary)
print(Target_Summary2)


import CHARACTER_CREATOR


import Artificer
import Barbarian
import Bard
import Cleric
import Druid
import Fighter
import Monk
import Paladin
import Ranger
import Rogue
import Sorcerer
import Warlock
import Wizard




User_Name = input('Name: ')
User_Species = input('Race: ')
User_Background = input('Background: ')

User_Level = input('Level: ')

if User_Level == '1':
    User_Level_Data = 1
elif User_Level == '2':
    User_Level_Data = 2
elif User_Level == '3':
    User_Level_Data = 3
elif User_Level == '4':
    User_Level_Data = 4
elif User_Level == '5':
    User_Level_Data = 5
elif User_Level == '6':
    User_Level_Data = 6
elif User_Level == '7':
    User_Level_Data = 7
elif User_Level == '8':
    User_Level_Data = 8
elif User_Level == '9':
    User_Level_Data = 9
elif User_Level == '10':
    User_Level_Data = 10
elif User_Level == '11':
    User_Level_Data = 11
elif User_Level == '12':
    User_Level_Data = 12
elif User_Level == '13':
    User_Level_Data = 13
elif User_Level == '14':
    User_Level_Data = 14
elif User_Level == '15':
    User_Level_Data = 15
elif User_Level == '16':
    User_Level_Data = 16
elif User_Level == '17':
    User_Level_Data = 17
elif User_Level == '18':
    User_Level_Data = 18
elif User_Level == '19':
    User_Level_Data = 19
elif User_Level == '20':
    User_Level_Data = 20
else: 
    print('Unrecognized Level')



#if User_Level > 1:
#    User_Multiclass = input('Multiclass?: ')
#
#    if User_Multiclass == True:
#        User_Class_Number = input('Classes #: ')
#        User_Classes = []
#        for i in range(User_Class_Number):
#            User_Classes = input('')
#    else: pass
#
#else: pass

User_Class = input('Class: ')


if User_Species == 'Human':
    User_Species_Data = Species.Human
elif User_Species == 'Elf':
    User_Species_Data = Species.Elf
elif User_Species == 'Half Elf':
    User_Species_Data = Species.Half_Elf
else:
    pass

if User_Class == 'Barbarian':
    User_Class_Data = Barbarian.Barbarian
elif User_Class == 'Cleric':
    User_Class_Data = Cleric.Cleric
elif User_Class == 'Artificer':
    User_Class_Data = Artificer.Artificer
elif User_Class == 'Bard':
    User_Class_Data = Bard.Bard
elif User_Class == 'Druid':
    User_Class_Data = Druid.Druid
elif User_Class == 'Fighter':
    User_Class_Data = Fighter.Fighter
elif User_Class == 'Paladin':
    User_Class_Data = Paladin.Paladin
elif User_Class == 'Monk':
    User_Class_Data = Monk.Monk
elif User_Class == 'Rogue':
    User_Class_Data = Rogue.Rogue
elif User_Class == 'Ranger':
    User_Class_Data = Ranger.Ranger
elif User_Class == 'Sorcerer':
    User_Class_Data = Sorcerer.Sorcerer
elif User_Class == 'Warlock':
    User_Class_Data = Warlock.Warlock
elif User_Class == 'Wizard':
    User_Class_Data = Wizard.Wizard
else: 
    print('Unable to Find Class')

if User_Background == 'Acolyte':
    User_Background_Data = Backgrounds.Acolyte
elif User_Background == 'Urchin':
    User_Background_Data = Backgrounds.Urchin
elif User_Background == 'Soldier':
    User_Background_Data = Backgrounds.Soldier
elif User_Background == 'Sailor':
    User_Background_Data = Backgrounds.Sailor
elif User_Background == 'Pirate':
    User_Background_Data = Backgrounds.Pirate
elif User_Background == 'Sage':
    User_Background_Data = Backgrounds.Sage
elif User_Background == 'Outlander':
    User_Background_Data = Backgrounds.Outlander
elif User_Background == 'Noble':
    User_Background_Data = Backgrounds.Noble
elif User_Background == 'Knight':
    User_Background_Data = Backgrounds.Knight
elif User_Background == 'Hermit':
    User_Background_Data = Backgrounds.Hermit
elif User_Background == 'Guild Merchant1':
    User_Background_Data = Backgrounds.Guild_Merchant1
elif User_Background == 'Guild Merchant2':
    User_Background_Data = Backgrounds.Guild_Merchant2
elif User_Background == 'Guild Artisan':
    User_Background_Data = Backgrounds.Guild_Artisan
elif User_Background == 'Folk Hero':
    User_Background_Data = Backgrounds.Folk_Hero
elif User_Background == 'Gladiator':
    User_Background_Data = Backgrounds.Gladiator
elif User_Background == 'Entertainer':
    User_Background_Data = Backgrounds.Entertainer
elif User_Background == 'Criminal':
    User_Background_Data = Backgrounds.Criminal
elif User_Background == 'Spy':
    User_Background_Data = Backgrounds.Spy
elif User_Background == 'Charlatan':
    User_Background_Data = Backgrounds.Charlatan
else: 
    print('Unable to Find Background')


Player_Character = CHARACTER_CREATOR.Create_Character(User_Name,'Standard Array',User_Species_Data,False,User_Class_Data,User_Background_Data,User_Level_Data)

Player_Character_Summary = {
    'Name': [Player_Character.Name],
    'HP': [Player_Character.HP],
    'AC': [Player_Character.AC],
    'Prof Bonus': [Player_Character.Prof_Bonus]
}

CHARACTER_CREATOR.Find_the_Best_Armor(Player_Character)

#Player_Character_Summary2 = pandas.DataFrame.from_dict(Player_Character_Summary)
#print(Player_Character_Summary2)


import Character_Actions
Player_Character.Actions['Attack'] = Character_Actions.Weapon_Attack




Player_Character.Bonus_Actions['Dependent']['Attack_Action']['Two_Weapon_Fighting'] = Player_Character.Actions['Attack'] = Character_Actions.Weapon_Attack

Player_Character.Effects['Self_Attacking'] = {
    'Rolling': {}
}

Player_Character.Effects['Self_Dealing_Damage'] = {
    'Piercing': {},
    'Bludgeoning': {},
    'Slashing': {}
#    'Fire': {},
#    'Cold': {},
#    'Lightning': {},
#    'Thunder': {},
#    'Poison': {},
#    'Acid': {},
#    'Necrotic': {},
#    'Radiant': {},
#    'Force': {},
#    'Psychic': {}
}


#Barbarian.Activate_Rage(Player_Character)

def Player_Character_Sheet(Player_Character):

    # Description Info
    #print(Player_Character.Name)
    #print(Player_Character.Species)

    # Code to print Class Levels and Subclasses


    # Stats
    #print(Player_Character.HP)
    #print(Player_Character.AC)
    #print(Player_Character.Saving_Throws)

    # Need a section that says if Spellcaster: Spells and if Martial: Weapons and Damage
    
    #print(Player_Character.Class_Save_DCs['Bard'])


    #print(Player_Character.Actions)
    #print(Player_Character.Bonus_Actions)
    #print(Player_Character.Effects)
    #print(Player_Character.Class_Resources)
    #print(Player_Character.Levels)

    #print(Player_Character.Related_Stat_Blocks)

    Player_Character_Summary = {
    'Name': [Player_Character.Name],
    #'Race': [Player_Character.Species['Name']],
    'HP': [Player_Character.HP],
    'AC': [Player_Character.AC],
    'Prof Bonus': [Player_Character.Prof_Bonus]}
    Player_Character_Summary2 = pandas.DataFrame.from_dict(Player_Character_Summary)
    print(Player_Character_Summary2)
    
    print('')

    Player_Scores_Summary = {
        'Strength': [Player_Character.Str_Score],
        'Dexterity': [Player_Character.Dex_Score],
        'Constitution': [Player_Character.Con_Score],
        'Intelligence': [Player_Character.Int_Score],
        'Wisdom': [Player_Character.Wis_Score],
        'Charisma': [Player_Character.Cha_Score]
        }
    Player_Scores_Summary2 = pandas.DataFrame.from_dict(Player_Scores_Summary)
    print(Player_Scores_Summary2)

    #print('')

    #Player_Saving_Throws_Summary = {
    #    'Strength': [Player_Character.Saving_Throws[0]],
    #    'Dexterity': [Player_Character.Saving_Throws[1]],
    #    'Constitution': [Player_Character.Saving_Throws[2]],
    #    'Intelligence': [Player_Character.Saving_Throws[3]],
    #    'Wisdom': [Player_Character.Saving_Throws[4]],
    #    'Charisma': [Player_Character.Saving_Throws[5]]
    #    }
    #Player_Saving_Throws_Summary2 = pandas.DataFrame.from_dict(Player_Saving_Throws_Summary)
    #print(Player_Saving_Throws_Summary2)


Player_Character_Sheet(Player_Character)

#print(Player_Character.Saving_Throws[0])

def Consider_Options(Player_Character,Target):
    # lets print every option that the character has 
    for Action in Player_Character.Actions:
        print(Action)

    #Player_Character.Bonus_Actions
    #Player_Character.Effects


    #Target.AC
    #Target.HP
    #Target.WRI
    #Target.Saving_Throws
    #Target.Str_Score
    #Target.Dex_Score
    #Target.Con_Score
    #Target.Int_Score
    #Target.Wis_Score
    #Target.Cha_Score
Consider_Options(Player_Character,Target)
