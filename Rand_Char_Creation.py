import torch 
import numpy as np
import random

import Species as S
import Backgrounds
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
import Establishing_Hierarchy
import CHARACTER_CREATOR

Class_List = [Barbarian.Barbarian,Cleric.Cleric,Artificer.Artificer,Bard.Bard,Druid.Druid,Fighter.Fighter,Paladin.Paladin,Monk.Monk,Rogue.Rogue,Ranger.Ranger,Sorcerer.Sorcerer,Warlock.Warlock,Wizard.Wizard]
Class_Subclass_Level = {
    'Artificer': 3,
    'Barbarian': 3,
    'Bard': 3,
    'Cleric': 1,
    'Druid': 2,
    'Fighter': 3,
    'Monk': 3,
    'Paladin': 3,
    'Ranger': 3,
    'Rogue': 3,
    'Sorcerer': 1,
    'Warlock': 1,
    'Wizard': 2
}

def Generate_Random_Character():
    Name = "John_Smith"
    Species = random.choice(S.Species_List)
    print(Species.Name)
    Background = random.choice(Backgrounds.Background_Options)
    print(Background.Name)


    Level = random.randint(1,20)
    print('Level:',Level)

    Num_Classes_to_Take = random.randint(1,min(Level,len(Class_List)-1))
    print('Different Classes:',Num_Classes_to_Take)

    Class_Level_Allocation = []
    Levels_Remaining = Level - Num_Classes_to_Take

    if Num_Classes_to_Take == 1:
        Class_Level_Allocation.append(Level)
    elif Num_Classes_to_Take == Level:
        for i in range(0,Num_Classes_to_Take,1):
            Class_Level_Allocation.append(1)
    else:
        for i in range(0,Num_Classes_to_Take,1): # for each class they're taking
            
            Class_Level_Allocation.append(1) # give it one level
            if Levels_Remaining > 0:
                a = random.randint(0,Levels_Remaining)
                Class_Level_Allocation[i] = Class_Level_Allocation[i] + a
                Levels_Remaining = Levels_Remaining - Class_Level_Allocation[i]
            else:
                pass

            if sum(Class_Level_Allocation) < Level and i == Num_Classes_to_Take-1:
                a = random.randint(0,Level-sum(Class_Level_Allocation))
                Class_Level_Allocation[i] = Class_Level_Allocation[i] + a
            
            if sum(Class_Level_Allocation) > Level:
                print('Too many levels taken')


    print('Class Level Allocation:',Class_Level_Allocation)

    Class_Choices = []
    Personal_Class_List = [Barbarian.Barbarian,Cleric.Cleric,Artificer.Artificer,Bard.Bard,Druid.Druid,Fighter.Fighter,Paladin.Paladin,Monk.Monk,Rogue.Rogue,Ranger.Ranger,Sorcerer.Sorcerer,Warlock.Warlock,Wizard.Wizard]

    for i in range(0,Num_Classes_to_Take,1):
        Class = random.choice(Personal_Class_List)
        print(Class.Name)
        Class_Choices.append([Class])
        Personal_Class_List.remove(Class)
        Levels_Remaining = Levels_Remaining - 1

        if Class_Level_Allocation[i] >= Class_Subclass_Level[Class.Name]:
            Subclass = random.choice(Class.Subclasses)
            print(Subclass.Name)
            Class_Choices[i].append(Subclass)

    #print(Class_Choices)
    for i in Class_Choices:
        print(i)
    # need to make it so that they can't take two classes twice


    list_of_scores = CHARACTER_CREATOR.Use_Standard_Array()
    Strength = list_of_scores[random.randint(0,len(list_of_scores)-1)]
    list_of_scores.remove(Strength)
    Dexterity = list_of_scores[random.randint(0,len(list_of_scores)-1)]
    list_of_scores.remove(Dexterity)
    Constitution = list_of_scores[random.randint(0,len(list_of_scores)-1)]
    list_of_scores.remove(Constitution)
    Intelligence = list_of_scores[random.randint(0,len(list_of_scores)-1)]
    list_of_scores.remove(Intelligence)
    Wisdom = list_of_scores[random.randint(0,len(list_of_scores)-1)]
    list_of_scores.remove(Wisdom)
    Charisma = list_of_scores[random.randint(0,len(list_of_scores)-1)]
    list_of_scores.remove(Charisma)
    
    Name = Establishing_Hierarchy.Player_Character(Name,Class,Species,False,Level,Background,True,True,True,True,True,True,True,Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,True,True,True,True)

    Name.One_Minute_Options['Unlimited']

    for i in range(Level):
        if Class == Artificer.Artificer:
            Name.Levels[i] = Artificer.Artificer
        elif Class == Barbarian.Barbarian:
            Name.Levels[i] = Barbarian.Barbarian
        elif Class == Bard.Bard:
            Name.Levels[i] = Bard.Bard
        elif Class == Cleric.Cleric:
            Name.Levels[i] = Cleric.Cleric
        elif Class == Druid.Druid:
            Name.Levels[i] = Druid.Druid
        elif Class == Fighter.Fighter:
            Name.Levels[i] = Fighter.Fighter
        elif Class == Monk.Monk:
            Name.Levels[i] = Monk.Monk
        elif Class == Paladin.Paladin:
            Name.Levels[i] = Paladin.Paladin
        elif Class == Ranger.Ranger:
            Name.Levels[i] = Ranger.Ranger
        elif Class == Rogue.Rogue:
            Name.Levels[i] = Rogue.Rogue
        elif Class == Sorcerer.Sorcerer:
            Name.Levels[i] = Sorcerer.Sorcerer
        elif Class == Warlock.Warlock:
            Name.Levels[i] = Warlock.Warlock
        elif Class == Wizard.Wizard:
            Name.Levels[i] = Wizard.Wizard
        else:
            pass

    Name.HP = Establishing_Hierarchy.Predicted_Hit_Points(Name)
    Name.Prof_Bonus = Establishing_Hierarchy.levelToProficiency(Name)

    Artificer_Levels = Name.Levels.count(Artificer.Artificer)
    Barbarian_Levels = Name.Levels.count(Barbarian.Barbarian)
    Bard_Levels = Name.Levels.count(Bard.Bard)
    Cleric_Levels = Name.Levels.count(Cleric.Cleric)
    Druid_Levels = Name.Levels.count(Druid.Druid)
    Fighter_Levels = Name.Levels.count(Fighter.Fighter)
    Monk_Levels = Name.Levels.count(Monk.Monk)
    Paladin_Levels = Name.Levels.count(Paladin.Paladin)
    Ranger_Levels = Name.Levels.count(Ranger.Ranger)
    Rogue_Levels = Name.Levels.count(Rogue.Rogue)
    Sorcerer_Levels = Name.Levels.count(Sorcerer.Sorcerer)
    Warlock_Levels = Name.Levels.count(Warlock.Warlock)
    Wizard_Levels = Name.Levels.count(Wizard.Wizard)

    if Artificer_Levels > 0:
        Artificer.Run_Artificer(Name,Artificer_Levels,Subclass)
    if Barbarian_Levels > 0:
        Barbarian.Run_Barbarian(Name,Barbarian_Levels,Subclass)
    if Bard_Levels > 0:
        Bard.Run_Bard(Name,Bard_Levels,Subclass)
    if Cleric_Levels > 0:
        Cleric.Run_Cleric(Name,Cleric_Levels,Subclass)
    if Druid_Levels > 0:        
        Druid.Run_Druid(Name,Druid_Levels,Subclass)
    if Fighter_Levels > 0:
        Fighter.Run_Fighter(Name,Fighter_Levels)
    if Monk_Levels > 0:
        Monk.Run_Monk(Name,Monk_Levels)
    if Paladin_Levels > 0:
        Paladin.Run_Paladin(Name,Paladin_Levels)
    if Ranger_Levels > 0:
        Ranger.Run_Ranger(Name,Ranger_Levels)
    if Rogue_Levels > 0:
        Rogue.Run_Rogue(Name,Rogue_Levels)
    if Sorcerer_Levels > 0:
        Sorcerer.Run_Sorcerer(Name,Sorcerer_Levels)
    if Warlock_Levels > 0:
        Warlock.Run_Warlock(Name,Warlock_Levels)
    if Wizard_Levels > 0:
        Wizard.Run_Wizard(Name,Wizard_Levels)
    
    Backgrounds.Take_Background(Background,Name)
    S.Apply_Species(Species,Name)
    
    return Name

Generate_Random_Character()

# I want to use pytorch to create a function that will take all of a character's actions, bonus actions, spells, and effects and iteratively go through every possibly option and then return the option that deals the most damage
# first I'll need to consider how to organize that into a tensor
# the character can only choose one of each action, bonus action, and reaction, but can choose many effects depending on the action types...
# so I'll need to create a tensor that has a place for action choice, bonus action choice, reaction choice, and then a place for a sub-tensor to store the effects of each action-type
# so the tensor will be 4xN, where the rows represent Action, Bonus Action, Free Action, Reaction, and the columns are their own tensor that represents the effects of each action-type
