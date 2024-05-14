import Establishing_Hierarchy
#import Character_Functions
import random
import Backgrounds
import Species as s
import Armor_and_Weapons
import Dice_Rolls
#import Effects
#import Conditions
#import Spell_Data

import Artificer
from Artificer import Run_Artificer

import Barbarian
from Barbarian import Run_Barbarian

import Bard
from Bard import Run_Bard

import Cleric
from Cleric import Run_Cleric

import Druid
from Druid import Run_Druid

import Fighter
from Fighter import Run_Fighter

import Monk
from Monk import Run_Monk

import Paladin
from Paladin import Run_Paladin

import Ranger
from Ranger import Run_Ranger

import Rogue
from Rogue import Run_Rogue

import Sorcerer
from Sorcerer import Run_Sorcerer

import Warlock
from Warlock import Run_Warlock

import Wizard
from Wizard import Run_Wizard


def calc_health(character):
    #print('Calculating Health')
    if character.Levels[0] == Barbarian.Barbarian:
        HP = 12 + Establishing_Hierarchy.abilityScoreToModifier(character.Con_Score)
    else:
        HP = 10 + Establishing_Hierarchy.abilityScoreToModifier(character.Con_Score)
    #print('HP:',HP)
    return HP

# Testing Character Creation

#Omaro = Establishing_Hierarchy.Player_Character('Omaro',Fighter.Fighter,Species.Human,False,True,Backgrounds.Acolyte,[],[],[],[],[],[],[],10,10,10,10,10,10,[],[],True)

#print('Error After import Classes in Character Creator')

Score_Generation_Methods = ['Standard Array','Point Buy','Classic Roll','Hard Roll','Kamikaze']
def Use_Standard_Array():
    A_Score = 15
    B_Score = 14
    C_Score = 13
    D_Score = 12
    E_Score = 10
    F_Score = 8
    return [int(A_Score),int(B_Score),int(C_Score),int(D_Score),int(E_Score),int(F_Score)]


def Use_Point_Buy():
    Points = 27
    Score_Max = 15
    Score_Min = 8
    Score_Cost = {
        'Score': [8,9,10,11,12,13,14,15],
        'Cost': [0,1,2,3,4,5,7,9]
        }
    #A_Score = 
    #B_Score = 
    #C_Score = 
    #D_Score = 
    #E_Score = 
    #F_Score = 
    #Scores = [A_Score,B_Score,C_Score,D_Score,E_Score,F_Score]
    #return Scores

def Use_Classic_Roll():
    def Classic_Roll():
        Rolls = [Dice_Rolls.Roll(1,6),Dice_Rolls.Roll(1,6),Dice_Rolls.Roll(1,6),Dice_Rolls.Roll(1,6)]
        Rolls.remove(min(Rolls))
        Score_Result = sum(Rolls)
        return Score_Result
        # need to make it so that you can reroll 1's
    A_Score = Classic_Roll
    B_Score = Classic_Roll
    C_Score = Classic_Roll
    D_Score = Classic_Roll 
    E_Score = Classic_Roll
    F_Score = Classic_Roll
    return [int(A_Score),int(B_Score),int(C_Score),int(D_Score),int(E_Score),int(F_Score)]

def Use_Hard_Roll():
    def Hard_Roll():
        Rolls = [Dice_Rolls.Roll(1,6),Dice_Rolls.Roll(1,6),Dice_Rolls.Roll(1,6)]
        Score_Result = sum(Rolls)
        return Score_Result
        # need to make it so that you can reroll 1's
    A_Score = Hard_Roll
    B_Score = Hard_Roll
    C_Score = Hard_Roll
    D_Score = Hard_Roll 
    E_Score = Hard_Roll
    F_Score = Hard_Roll
    return [A_Score,B_Score,C_Score,D_Score,E_Score,F_Score]

def Use_Kamikaze():
    A_Score = Dice_Rolls.d20
    B_Score = Dice_Rolls.d20
    C_Score = Dice_Rolls.d20
    D_Score = Dice_Rolls.d20
    E_Score = Dice_Rolls.d20
    F_Score = Dice_Rolls.d20
    return [A_Score,B_Score,C_Score,D_Score,E_Score,F_Score]
# I want to make a function that can create a character simply from saying "oh they're a Human 13 Vengeance Paladin 7 Storm Sorcerer with an Acolyte Background"



#print('Error After Score Generation Methods')

def Create_Character(character_name,Score_Generation_Method,Species,Subspecies,Class,Background,Level):
    #print('Error after defining Create Character')
    # x = 'name = "John"\nprint(name)'
    # exec(x)

    # I'm going to have to use Exec to take Name as a usable User Input feature
    
    # Could I have Create_Character nested within a second function that takes the Callable name, and all the other attributes needed???
    
    # I may have to run the whole thing in an exec function 

    print('Create Character Function - Class:',Class)
    if Score_Generation_Method == 'Standard Array':
        listl = Use_Standard_Array()
    elif Score_Generation_Method == 'Point Buy':
        listl = Use_Point_Buy()
    elif Score_Generation_Method == 'Classic Roll':
        listl = Use_Classic_Roll()
    elif Score_Generation_Method == 'Hard Roll':
        listl = Use_Hard_Roll()
    elif Score_Generation_Method == 'Kamikaze':
        listl = Use_Kamikaze()
    else:
        print('Unrecognizable Score Generation Method')

    '''
    Quick_Builds = {
        'Artificer': ['Intelligence','Constitution','Dexterity','Wisdom','Strength','Charisma'],
        'Barbarian': ['Strength','Constitution','Dexterity','Wisdom','Charisma','Intelligence'],
        'Bard': ['Charisma','Dexterity','Constitution','Intelligence','Wisdom','Strength'],
        'Cleric': ['Wisdom','Constitution','Strength','Dexterity','Charisma','Intelligence'],
        'Druid': ['Wisdom','Constitution','Dexterity','Strength','Charisma','Intelligence'],
        'Fighter': ['Strength','Dexterity','Constitution','Wisdom','Intelligence','Charisma'],
        'Monk': ['Dexterity','Wisdom','Constitution','Strength','Charisma','Intelligence'],
        'Paladin': ['Strength','Charisma','Constitution','Dexterity','Wisdom','Intelligence'],
        'Ranger': ['Dexterity','Wisdom','Strength','Constitution','Intelligence','Charisma'],
        'Rogue': ['Dexterity','Intelligence','Charisma','Constitution','Wisdom','Strength'],
        'Sorcerer': ['Charisma','Constitution','Dexterity','Intelligence','Wisdom','Strength'],
        'Warlock': ['Charisma','Constitution','Dexterity','Wisdom','Intelligence','Strength'],
        'Wizard': ['Intelligence','Constitution','Dexterity','Wisdom','Charisma','Strength']}
    try: 
        for x, y in Quick_Builds.items():
            if x == str(Class):
                for i in range(len(y)):
                    if y[i] == 'Strength':
                        Strength = int(listl[i])
                        #print('Strength = ',Strength)
                    elif y[i] == 'Dexterity':
                        Dexterity = int(listl[i])
                        #print('Dexterity = ',Dexterity)
                    elif y[i] == 'Constitution':
                        Constitution = int(listl[i])
                        #print('Constitution = ',Constitution)
                    elif y[i] == 'Intelligence':
                        Intelligence = int(listl[i])
                        #print('Intelligence = ',Intelligence)
                    elif y[i] == 'Wisdom':
                        Wisdom = int(listl[i])
                        #print('Wisdom = ',Wisdom)
                    elif y[i] == 'Charisma':
                        Charisma = int(listl[i])
                        #print('Charisma = ',Charisma)
                    else:
                        pass
    except:
    '''
    # randomly assign the scores from listl and remove each score from the list
    Strength = random.choice(listl)
    listl.remove(Strength)

    Dexterity = random.choice(listl)
    listl.remove(Dexterity)

    Constitution = random.choice(listl)
    listl.remove(Constitution)

    Intelligence = random.choice(listl)
    listl.remove(Intelligence)

    Wisdom = random.choice(listl)
    listl.remove(Wisdom)

    Charisma = listl[0]


    #print('Error after Quick Builds')

    character_name = Establishing_Hierarchy.Player_Character(
        character_name,
        Class,    # I need to put a function that accesses the class from the appropriate file
        Species,
        Subspecies,
        True,     # I need to make a decision about how the dictionary of levels and the class attribute works
        Background,
        True,     # skill profs
        True,     # skill expertise
        True,     # tool profs
        True,     # weapon equipped
        True,     # armor equipped
        True,
        Strength,                  # For the ability scores, I need to know how they're getting AND allocating the scores 
        Dexterity,
        Constitution,
        Intelligence,
        Wisdom,
        Charisma,
        True, # Spellcasting Prepared
        True, # Item Attunements
        True, # Inventory
        True, 
        #True # Related Stat Blocks
        )

    character_name.HP = calc_health(character_name)
    character_name.Current_HP = character_name.HP

    character_name.Actions['Don Shield'] = Armor_and_Weapons.Don_Armor(Armor_and_Weapons.Shield,character_name)
    character_name.Actions['Doff Shield'] = Armor_and_Weapons.Doff_Armor(Armor_and_Weapons.Shield,character_name)
    
    #Name.Bonus_Actions[]
    #Name.Reactions[]
    character_name.One_Minute_Options['Unlimited']

    for i in range(Level):
        if Class == Artificer.Artificer:
            character_name.Levels[i] = Artificer.Artificer

        elif Class == Barbarian.Barbarian:
            character_name.Levels[i] = Barbarian.Barbarian
            #print('Assigning Class:',i)

        elif Class == Bard.Bard:
            character_name.Levels[i] = Bard.Bard
            #print('Assigning Class:',i)

        elif Class == Cleric.Cleric:
            character_name.Levels[i] = Cleric.Cleric
            #print('Assigning Class:',i)

        elif Class == Druid.Druid:
            character_name.Levels[i] = Druid.Druid

        elif Class == Fighter.Fighter:
            character_name.Levels[i] = Fighter.Fighter
        elif Class == Monk.Monk:
            character_name.Levels[i] = Monk.Monk
        elif Class == Paladin.Paladin:
            character_name.Levels[i] = Paladin.Paladin
        elif Class == Ranger.Ranger:
            character_name.Levels[i] = Ranger.Ranger
        elif Class == Rogue.Rogue:
            character_name.Levels[i] = Rogue.Rogue
        elif Class == Sorcerer.Sorcerer:
            character_name.Levels[i] = Sorcerer.Sorcerer
        elif Class == Warlock.Warlock:
            character_name.Levels[i] = Warlock.Warlock
        elif Class == Wizard.Wizard:
            character_name.Levels[i] = Wizard.Wizard
        else:
            pass

    #character_name.HP = Establishing_Hierarchy.Predicted_Hit_Points(character_name)
    character_name.Prof_Bonus = Establishing_Hierarchy.levelToProficiency(character_name)
    #Name.AC = 

    #print('Error After for i in Name.Levels')


    # need to make a series of if else statements to determine which run_class functions to use
    Artificer_Levels = character_name.Levels.count(Artificer.Artificer)
    Barbarian_Levels = character_name.Levels.count(Barbarian.Barbarian)
    #print('Barbarian Levels:',Barbarian_Levels)
    Bard_Levels = character_name.Levels.count(Bard.Bard)
    Cleric_Levels = character_name.Levels.count(Cleric.Cleric)
    Druid_Levels = character_name.Levels.count(Druid.Druid)
    Fighter_Levels = character_name.Levels.count(Fighter.Fighter)
    Monk_Levels = character_name.Levels.count(Monk.Monk)
    Paladin_Levels = character_name.Levels.count(Paladin.Paladin)
    Ranger_Levels = character_name.Levels.count(Ranger.Ranger)
    Rogue_Levels = character_name.Levels.count(Rogue.Rogue)
    Sorcerer_Levels = character_name.Levels.count(Sorcerer.Sorcerer)
    Warlock_Levels = character_name.Levels.count(Warlock.Warlock)
    Wizard_Levels = character_name.Levels.count(Wizard.Wizard)


    #print('Error After Class_Levels defining')

    if Artificer_Levels > 0:
        Run_Artificer(character_name,Artificer_Levels)
    if Barbarian_Levels > 0:
        Run_Barbarian(character_name,Barbarian_Levels)
    if Bard_Levels > 0:
        Run_Bard(character_name,Bard_Levels)
    if Cleric_Levels > 0:
        Run_Cleric(character_name,Cleric_Levels)
    if Druid_Levels > 0:        
        Run_Druid(character_name,Druid_Levels)
    if Fighter_Levels > 0:
        Run_Fighter(character_name,Fighter_Levels)
    if Monk_Levels > 0:
        Run_Monk(character_name,Monk_Levels)
    if Paladin_Levels > 0:
        Run_Paladin(character_name,Paladin_Levels)
    if Ranger_Levels > 0:
        Run_Ranger(character_name,Ranger_Levels)
    if Rogue_Levels > 0:
        Run_Rogue(character_name,Rogue_Levels)
    if Sorcerer_Levels > 0:
        Run_Sorcerer(character_name,Sorcerer_Levels)
    if Warlock_Levels > 0:
        Run_Warlock(character_name,Warlock_Levels)
    if Wizard_Levels > 0:
        Run_Wizard(character_name,Wizard_Levels)
    
    #print('Applied Barbarian!')

    Backgrounds.Take_Background(Background,character_name)
    #print('Applied Background!')

    #print('Error After Take_Background()')

    s.Apply_Species(Species,character_name)
    #print('Applied Species!')


    #print('Error After Apply_Species()')

    #print('Summarize Player:',Name.Name)
    #print('Class:',Name.Levels[0].Name)
    #print('Level:',Name.Level_Count)
    #print('Hitpoints:', Name.HP)
    #print('Strength:',Name.Str_Score)
    #print('Dexterity:',Name.Dex_Score)
    #print('Constitution:',Name.Con_Score)
    #print('Intelligence:',Name.Int_Score)
    #print('Wisdom:',Name.Wis_Score)
    #print('Charisma:',Name.Cha_Score)

    #print(Omaro.Actions)
    #print(Omaro.Bonus_Actions)
    #print(Omaro.Effects)
    # I need an if else statement that runs the appropriate class function IF it is the first level
    # and I need to be able to run similar functions if the class ISN"T the first level
    
    #print('Error in Create_Character')
    
    return character_name

#Omaro = Create_Character('Omaro','Standard Array',s.Human,False,Barbarian.Barbarian,Backgrounds.Acolyte,3)

# I can currently run Barbarian upto until Brutal Critical
#print('Actions:',Omaro.Actions)
#print('Effect Keys:',Omaro.Effects.keys())
#print('Independent Bonus Actions:',Omaro.Bonus_Actions['Independent'])
#print('Dependent Bonus Actions:',Omaro.Bonus_Actions['Dependent']['Attack_Action'])
#print('Dependent Bonus Actions:',Omaro.Bonus_Actions['Dependent']['Raging'])

#print('Resources:',Omaro.Class_Resources)
#print('Skills:',Omaro.Skill_Profs)
#print('Saves:',Omaro.Saving_Throws)
#print('Reactions:',Omaro.Reactions)

#for i in Omaro.Reactions:

#print('Inventory:',Omaro.Inventory)
#print('Inventory Instruments',Omaro.Inventory['Instruments'])


# Current Issues
# Why does a level 1 character have a 159 hitpoints
# Why does entering level 3 return level 1 Barbarian
# Barbarian Skill Profs aren't working
# Barbarian Saves aren't working

def Find_the_Best_Armor(Player_Character):
        AC_Possibilities = {
            'Armor': [],
            'AC': []
        }

        if len(Player_Character.Armor_Equipped) == 0:
            pass
        else:
            Player_Character.Inventory['Armor'].append(Player_Character.Armor_Equipped[0])

        if Barbarian.Barbarian in Player_Character.Levels:
            Unarmored_AC = 10 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score) + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Con_Score)
            # can wear a shield 
        elif Monk.Monk in Player_Character.Levels:
            Unarmored_AC = 10  + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score) + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Wis_Score)
            # cannot wear a shield
        else:
            Unarmored_AC = 10 + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score)
        
        for i in Player_Character.Inventory['Armor']:
            if i.Type not in Player_Character.Armor_Profs:
                # should armor that a character isn't proficient in be considered?
                # should there be a calculation if the benefits outweigh the costs?
                pass
            else:
                if i.Add_Dex == True:
                    if i.Dex_Limit == True:
                        if i.Base_AC + 2 > Unarmored_AC:
                            AC_Possibilities['Name'].append(i)
                            AC_Possibilities['AC'].append(i.Base_AC + 2)
                            print('AC:',AC_Possibilities)
                    else: 
                        if i.Base_AC + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score) > Unarmored_AC:
                            AC_Possibilities['Name'].append(i)
                            AC_Possibilities['AC'].append(i.Base_AC + Establishing_Hierarchy.abilityScoreToModifier(Player_Character.Dex_Score))
                            print('AC:',AC_Possibilities)
                else:
                    if i.Base_AC > Unarmored_AC:
                        AC_Possibilities['Name'].append(i)
                        AC_Possibilities['AC'].append(i.Base_AC)
                        print('AC:',AC_Possibilities)
        #print('AC:',AC_Possibilities)

available_species = [s.Human,s.Dwarf,s.Elf] #s.Halfling,s.Dragonborn,s.Gnome,s.Half_Elf,s.Half_Orc,s.Tiefling]
available_subspecies = []
available_classes = [Artificer, Barbarian, Bard]
available_backgrounds = [Backgrounds.Acolyte,Backgrounds.Criminal,Backgrounds.Folk_Hero,Backgrounds.Noble,Backgrounds.Sage,Backgrounds.Soldier]
available_levels = [1]

# create a function that randomly creates level one characters
def Random_Character():
    #print('Creating Random Character...')
    # generate a random name using 'a' and four random numbers
    name = 'a' + str(random.randint(1000,9999))
    # randomly 
    species = random.choice(available_species)
    sub_species = False
    class_choice = random.choice(available_classes)
    print('Character_Creator - Random Character Function - Class Choice: ',class_choice)
    background = random.choice(available_backgrounds)
    level = 1

    #print('Generated ',name)
    #print('Class: ',class_choice)
    return Create_Character(name,'Standard Array',species,sub_species,class_choice,background,level)


# test the Random_Character function
Random_Character()