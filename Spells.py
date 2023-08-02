from Spell_Data import Spells
import Effects
import Dice_Rolls
import numpy as py

class Spell:
   def __init__(self,Name,School,Base_Level,Ritual,Casting_Time,Target_Type,Target_Range,Num_Targets,Target_Area,Target_Requirements,
                Somatic,Verbal,Material,Cost,Concentration,Duration,Roll_Type,Save_Score,Half_Dmg_on_Save,Damage_Heal_Effect,Damage_Type,Healing_Type,
                Gives_Options,Effect_Type,Num_Damage_Dice,Damage_Dice,Flat_Damage,First_Damage_Type,Bonus_Num_Damage_Dice,Bonus_Damage_Dice,Bonus_Damage_Type,
                Condition_Inflicted,Requires_Sight,Requires_Pathing,Page_Num,Cantrip_Scaling,Upcastable,Upcast_Type,Upcast_Increase_Per,Average_Damage_at_Base,
                Subsequent_Action,Subsequent_Action_Effect,Spell_End_Condition,Class_Lists,Sourcebook,Method,Method_Process,Method_Target):
        self.Name = Name
        self.School = School
        self.Base_Level = Base_Level
        self.Ritual = bool()
        self.Casting_Time = Casting_Time
        self.Target_Type = Target_Type                          # I may need to redo the target system in accordance with the environment locations     
        self.Target_Range = Target_Range
        self.Num_Targets = Num_Targets
        self.Somatic = bool()
        self.Verbal = bool()
        self.Material = bool()
        self.Cost = Cost
        self.Concentration = bool()
        self.Duration = Duration
        self.Roll_Type = Roll_Type
        self.Save_Score = Save_Score
        self.Half_Dmg_on_Save = bool()
        self.Damage_Heal_Effect = Damage_Heal_Effect
        self.Damage_Type = Damage_Type
        self.Healing_Type = Healing_Type
        self.Gives_Options = bool()
        self.Effect_Type = Effect_Type
        self.Num_Damage_Dice = Num_Damage_Dice
        self.Damage_Dice = Damage_Dice
        self.Flat_Damage = Flat_Damage                  # I could make a list in excel like target1+3d8fire,target2+3d8fire,target3+3d8fire
        self.First_Damage_Type = First_Damage_Type      # and then I could use string manipulation to generate the needed code...
        self.Bonus_Num_Damage_Dice = Bonus_Num_Damage_Dice
        self.Bonus_Damage_Dice = Bonus_Damage_Dice
        self.Bonus_Damage_Type = Bonus_Damage_Type
        self.Condition_Inflicted = []
        self.Requires_Sight = bool()
        self.Requires_Pathing = bool()
        self.Page_Num = int()
        self.Cantrip_Scaling = bool()
        self.Upcastable = bool()
        self.Upcast_Type = Upcast_Type
        self.Upcast_Increase_Per = Upcast_Increase_Per
        self.Average_Damage_at_Base = int()
        self.Subsequent_Action = Subsequent_Action
        self.Subsequent_Action_Effect = []
        self.Spell_End_Condition = []
        self.Class_Lists = []
        self.Sourcebook = Sourcebook
        self.Method = Method
        self.Method_Process = Method_Process
        self.Method_Target = Method_Target




#Shield_Buff = Effects.AC_Effect('Reaction','Self','1_Round',False,5)
#def Shield(Caster):
#        Effects.Apply_AC_Effect(Shield_Buff,Caster)

#def Firebolt(Target,Caster):
#        Caster.Level


Spells_Dict = {}
for ind in Spells.index:
        Name = Spells.iloc[ind,0]
        #print(Name)
        School = Spells.iloc[ind,2]
        Base_Level = Spells.iloc[ind,1]
        Ritual = Spells.iloc[ind,3]
        Casting_Time = Spells.iloc[ind,4]
#Target_Type = 

        Verbal_Component = Spells.iloc[ind,23]
        Somatic_Componenet = Spells.iloc[ind,24]
        Material_Component = Spells.iloc[ind,25]

        Concentration = Spells.iloc[ind,30]
        Duration = Spells.iloc[ind,31]
        Roll_Type = Spells.iloc[ind,32]

        Save_Score = Spells.iloc[ind,36]
        Half_Dmg_on_Save = Spells.iloc[ind,37]
        Damage_Heal_Effect = Spells.iloc[ind,38]
        Damage_Type = Spells.iloc[ind,39]
        Healing_Type = Spells.iloc[ind,40]
        
        Gives_Options = Spells.iloc[ind,41]
        Effect_Type = Spells.iloc[ind,42]
        #print(Effect_Type)
        #print(type(Effect_Type))
        #print('1:',Spells.iloc[ind,44])
        #print('2:',type(Spells.iloc[ind,44]))

        Num_Damage_Dice = Spells.iloc[ind,44]

        if type(Spells.iloc[ind,45]) == py.float64:
                Damage_Dice = Spells.iloc[ind,45]
        else:
                Damage_Dice = Spells.iloc[ind,45]


        Flat_Damage = Spells.iloc[ind,46]                 # I could make a list in excel like target1+3d8fire,target2+3d8fire,target3+3d8fire
        First_Damage_Type = Spells.iloc[ind,47]           # and then I could use string manipulation to generate the needed code...
        Bonus_Num_Damage_Dice = Spells.iloc[ind,48]
        Bonus_Damage_Dice = Spells.iloc[ind,49]
        Bonus_Damage_Type = Spells.iloc[ind,50]
        Condition_Inflicted = Spells.iloc[ind,51]
        Requires_Sight = Spells.iloc[ind,52]
        Requires_Pathing = Spells.iloc[ind,53]
        Page_Num = Spells.iloc[ind,54]
        Cantrip_Scaling = Spells.iloc[ind,55]
        Upcastable = Spells.iloc[ind,56]
        Upcast_Type = Spells.iloc[ind,57]
        Upcast_Increase_Per = Spells.iloc[ind,58]
        Average_Damage_at_Base = Spells.iloc[ind,59]

        Subsequent_Action = Spells.iloc[ind,61]
        Subsequent_Action_Effect = Spells.iloc[ind,62]
        Spell_End_Condition = Spells.iloc[ind,63]

        Class_List = []
        Is_Artificer_Spell = Spells.iloc[ind,64]
        #print(type(Is_Artificer_Spell))
        if Is_Artificer_Spell != 'Artificer':
              pass
              #print('False')
        else: 
               #print('True')
               Class_List.append('Artificer')
        Is_Bard_Spell = Spells.iloc[ind,65]
        if Is_Bard_Spell != 'Bard':
              pass
        else: 
               Class_List.append('Bard')
        Is_Cleric_Spell = Spells.iloc[ind,66]
        if Is_Cleric_Spell != 'Cleric':
              pass
        else: 
               Class_List.append('Cleric')
        Is_Druid_Spell = Spells.iloc[ind,67]
        if Is_Druid_Spell != 'Druid':
              pass
        else: 
               Class_List.append('Druid')
        Is_Paladin_Spell = Spells.iloc[ind,68]
        if Is_Paladin_Spell != 'Paladin':
              pass
        else: 
               Class_List.append('Paladin')
        Is_Ranger_Spell = Spells.iloc[ind,69]
        if Is_Ranger_Spell != 'Ranger':
              pass
        else: 
               Class_List.append('Ranger')
        Is_Sorcerer_Spell = Spells.iloc[ind,70]
        if Is_Sorcerer_Spell != 'Sorcerer':
              pass
        else: 
               Class_List.append('Sorcerer')
        Is_Warlock_Spell = Spells.iloc[ind,71]
        if Is_Warlock_Spell != 'Warlock':
              pass
        else: 
               Class_List.append('Warlock')
        Is_Wizard_Spell = Spells.iloc[ind,72]
        if Is_Wizard_Spell != 'Wizard':
              pass
        else: 
               Class_List.append('Wizard')
        
        #print(Class_List)

        Sourcebook = Spells.iloc[ind,73]
        #print(Effect_Type)
        Method = Spells.iloc[ind,74]
        #print(Method)
        if str(Method) != 'nan':
                Method_Str = str(Spells.iloc[ind,74])
                #print('here1')
                Method_List = Method_Str.split(':')
                #print('here2')
                Method_Process = Method_List[0].split(',')
                #print('here3')
                Method_Target = Method_List[1].split(',')
                #print('here4')
        else:
               Method_Process = 'nan'
               Method_Target = 'nan'

        #if str(Effect_Type) != 'nan':
        #       Effect_List = Effect_Type.split(':')

        

        Special_Method = False



        Spells_Dict[Name] = Spell(Name,School,Base_Level,Ritual,Casting_Time,'Placeholder','Placeholder','Placeholder','Placeholder','Placeholder',Somatic_Componenet,Verbal_Component,Material_Component,'Cost Placeholder',Concentration,Duration,Roll_Type,Save_Score,Half_Dmg_on_Save,Damage_Heal_Effect,Damage_Type,Healing_Type,Gives_Options,Effect_Type,Num_Damage_Dice,Damage_Dice,Flat_Damage,First_Damage_Type,Bonus_Num_Damage_Dice,Bonus_Damage_Dice,Bonus_Damage_Type,Condition_Inflicted,Requires_Sight,Requires_Pathing,Page_Num,Cantrip_Scaling,Upcastable,Upcast_Type,Upcast_Increase_Per,Average_Damage_at_Base,Subsequent_Action,Subsequent_Action_Effect,Spell_End_Condition,Class_List,Sourcebook,Method,Method_Process,Method_Target)


Artificer_Spell_List = []
Bard_Spell_List = []    
Cleric_Spell_List = []  
Druid_Spell_List = []   
Paladin_Spell_List = [] 
Ranger_Spell_List = [] 
Sorcerer_Spell_List = []
Warlock_Spell_List = [] 
Wizard_Spell_List = []  

Class_List = {
       'Class': ['Artificer','Bard','Cleric','Druid','Paladin','Ranger','Sorcerer','Warlock','Wizard'],
       'List': [Artificer_Spell_List,Bard_Spell_List,Cleric_Spell_List,Druid_Spell_List,Paladin_Spell_List,Ranger_Spell_List,Sorcerer_Spell_List,Warlock_Spell_List,Wizard_Spell_List]
}

# Creating Spell Effects
#print('Seperator')
Spell_Effects = {}
for spell in Spells.index:
       Spell_Effects[Spells.iloc[spell,0]] = []
       #print(Spell_Effects)

       Effect_Type = Spells.iloc[spell,42]
       print(Effect_Type)

       if Effect_Type != float:
              Effect_String = str(Effect_Type)
              Effect_List = Effect_String.split(',')
       else:
              Effect_Type = 'nan'
              Effect_List = ['None']

       print(Effect_List)
       for effect in Effect_List:
              Effect_List_Types = []
              if effect == 'Buff_Circumstance':
                     pass
              elif effect == 'Light_Effect':
                     pass
              elif effect == 'Move_Effect':
                     pass
              elif effect == 'Condition_Effect':
                     pass
              elif effect == 'Illusory_Effect':
                     pass
              elif effect == 'Buff_Bonus':
                     pass
              elif effect == 'Create_Item_Effect':
                     pass
              elif effect == 'Share_Information_Effect':
                     pass
              elif effect == 'Terrain_Effect':
                     pass
              elif effect == 'Speed_Effect':
                     pass
              elif effect == 'Enchant_Item_Effect':
                     pass
              elif effect == 'Summon_Effect':
                     pass
              else: pass






#print(Spells_Dict.keys())
#print(Spells_Dict['Acid Splash'].Class_Lists)

#for Spell in Spells_Dict.keys():
#       print(Spell)
#       for Class in Class_List['Class']:
#              if Class in Spell.Class_List:
#                     Class_List['List'][Class].append(Spell)
#              else: pass

# What if instead of compiling a brand new list, I simply copy the dictionary and then cut down the spells that don't fit?
#Artificer_Spell_Dict = filter(Spells_Dict)
#Bard_Spell_Dict = filter(Spells_Dict)
#Cleric_Spell_Dict = filter(Spells_Dict)
#Druid_Spell_Dict = filter(Spells_Dict)
#Paladin_Spell_Dict = filter(Spells_Dict)
#Ranger_Spell_Dict = filter(Spells_Dict)
#Sorcerer_Spell_Dict = filter(Spells_Dict)
#Warlock_Spell_Dict = filter(Spells_Dict)
#Wizard_Spell_Dict = filter(Spells_Dict)




def Prepare_Spell(Spell,Player_Character):
        Player_Character.Spellcasting_Prepared.append(Spell)

        if Spell.Casting_Time == 'Action':
                Player_Character.Actions['Cast'][Spell.Name] = Run_Spell(Spell)

        elif Spell.Casting_Time == 'Bonus_Action':
                Player_Character.Bonus_Actions['Independent']['Cast'][Spell.Name] = Run_Spell(Spell)

        elif Spell.Casting_Time == 'Reaction':
                Player_Character.Reactions[Spell.Reaction_Stimulus][Spell.Name] = Run_Spell(Spell)

        else: pass
        # This is how the spell gets added as an option



#def Summarize_Spell(Spell): # needs to include the caster later
#
#       Average_Damage = Dice_Rolls.Average_Roll(Spell.Num_Damage_Dice,Spell.Damage_Dice,0,0)

       # I need to calculate the number of 5ft spaces that could fit in the area
       # then multiply that by the percentage chance that a creature is in the space
              # for instance, a space in the air is less likely to be filled than one on the ground
       # I could calculate it 5ft level by 5ft level  

#       if len(Spell.Method_Target) == 3:
#              if Spell.Method_Target[2] == 'Radius':
#                     Radius = Spell.Method_Target[3]

#                     Area = py.pi * py.square(Radius)
#                     Spaces_in_Area = (Area / 5)

              # the most enemy creatures in combat I can imagine is 12
              # for every additional square in the AOE, the probability that a creature is in that square goes down
 #                    Space_Probability_Modifiers = []
 #                    for i in range(Spaces_in_Area):
                            # for a cube, statistically speaking, there's less of a chance the higher up
#                            if i <= 2:
#                                   Space_Probability_Modifiers.append(1)

#                            if i > 12:
#                                   Space_Probability_Modifiers.append(Spaces_in_Area * 1/i)
                     

#              elif Spell.Method_Target[2] == 'Cube':
#                     Distance = Spell.Method_Target[3]
                     
#                     Area = Distance * Distance * Distance
#                     Height_Levels = Distance / 5
#                     Spaces_in_Area = Area / 25

#                     Space_Probability_Modifiers = []
#                     for i in range(Spaces_in_Area):
                            # for a cube, statistically speaking, there's less of a chance the higher up
#                            if i <= 2:
#                                   Space_Probability_Modifiers.append(1)

#                            if i > 12:
#                                   Space_Probability_Modifiers.append(Spaces_in_Area * 1/i)
              
#              elif Spell.Method_Target[2] == 'Cone':
#                     Length = Spell.Method_Target[3]
#                     Radius = Length * py.sin(45)
#                     Area = (1/3) * py.pi * py.square(Radius) * Length
#                     Height_Levels = (Radius * 2) / 5

#                     Spaces_in_Area = Area / 25

#                     Space_Probability_Modifiers = []
#                     for i in range(Spaces_in_Area):
                            # and I can't imagine that an AOE would be used instead of a single target spell if there were less than 2 targets
#                            if i <= 2:
#                                   Space_Probability_Modifiers.append(1)

#                            if i > 12:
#                                   Space_Probability_Modifiers.append(Spaces_in_Area * 1/i)                     # I don't know if this is the right equation to use for probability
              
#              elif Spell.Method_Target[2] == 'Sphere':
#                     Radius = Spell.Method_Target[3]
                     
#                     Area = 4 * py.pi * py.square(Radius)
#                     Num_of_Levels = Radius / 5
#                     Spaces_in_Area = ((Area / 5) / 5)
#                     Space_Probability_Modifiers = []
#                     for i in range(Spaces_in_Area):
                            # and I can't imagine that an AOE would be used instead of a single target spell if there were less than 2 targets
#                            if i <= 2:
#                                   Space_Probability_Modifiers.append(1)

#                            if i > 12:
#                                   Space_Probability_Modifiers.append(Spaces_in_Area * 1/i)                     # I don't know if this is the right equation to use for probability
              

#              else: pass


#       elif len(Spell.Method_Target) == 4:
#              if Spell.Method_Target[3] == 'Radius':
#                     Radius = Spell.Method_Target[4]

#                     Area = py.pi * py.square(Radius)
#                     Spaces_in_Area = (Area / 5)

                     # the most enemy creatures in combat I can imagine is 12
                     # for every additional square in the AOE, the probability that a creature is in that square goes down
                     
#                     Space_Probability_Modifiers = []
#                     for i in range(Spaces_in_Area):
                            # for a cube, statistically speaking, there's less of a chance the higher up
#                            if i <= 2:
#                                   Space_Probability_Modifiers.append(1)

#                            if i > 12:
#                                   Space_Probability_Modifiers.append(Spaces_in_Area * 1/i)


#              elif Spell.Method_Target[3] == 'Cone':
#                     Distance = Spell.Method_Target[4]
 


#              elif Spell.Method_Target[3] == 'Cube':
#                     Length = Spell.Method_Target[4]

#                     Area = Distance * Distance * Distance
#                     Height_Levels = Distance / 5
#                     Spaces_in_Area = Area / 25

#                     Space_Probability_Modifiers = []
#                     for i in range(Spaces_in_Area):
                            # for a cube, statistically speaking, there's less of a chance the higher up
#                            if i <= 2:
#                                   Space_Probability_Modifiers.append(1)

#                            if i > 12:
#                                   Space_Probability_Modifiers.append(Spaces_in_Area * 1/i)

#              elif Spell.Method_Target[3] == 'Sphere':
#                     Radius = Spell.Method_Target[4]

#              else: pass

#       if Spell.Method_Target == []:
#              pass

#       else: pass

#       Adjusted_Average_Damage = Average_Damage
#       for i in Space_Probability_Modifiers:
#              Adjusted_Average_Damage = Adjusted_Average_Damage + (Adjusted_Average_Damage * Space_Probability_Modifiers[i])
       
#       return Adjusted_Average_Damage



       # if 'Condition' in Spell.Method_Process:
       #       pass
       #elif 'Damage' in Spell.Method_Process:
       #       pass
       #else: pass   


def Run_Spell(Spell,Caster):           # need a way to implement the Caster, Spell Slot, Sorcery Points, and Components
        print(Spell.Name)

        if Spell.Concentration == True:
               Caster.Concentration = True
        
        #print(Spell.Method)
        #print('Beginning of Run Spell:',Spells_Dict[Spell.Name].Num_Damage_Dice)

        if Spell.Method == 'nan':
               

                if Spell.Effect_Type == 'Damage':
                        if Spell.Roll_Type == 'Save':
                               Spell.Save_Score

                        elif Spell.Roll_Type == 'Melee Spell Attack':
                               pass # going to have to deal with Targets

                        elif Spell.Roll_Type == 'Ranged Spell Attack':
                               pass # going to have to deal with Targets

                        elif Spell.Roll_Type == 'HP Affected':
                                pass
                        elif Spell.Roll_Type == 'Heal':
                               pass
                        elif Spell.Roll_Type == 'Melee Weapon Attack':
                               pass
                        elif Spell.Roll_Type == 'Weapon Attack':
                               pass

                elif Spell.Effect_Type == 'Effect':
                       pass

                elif Spell.Effect_Type == 'Healing':
                       pass

                else: 
                       pass

        else:
                if Spell.Method_Process == ['Attack Roll','Damage']:
                      #print('If Method:',Spell.Num_Damage_Dice)
                      #print('Damage Dice:',Spell.Damage_Dice)
                      
                      Damage_Roll = Dice_Rolls.Average_Roll(Spell.Num_Damage_Dice,Spell.Damage_Dice,0,0)
                      print('Damage Results:',Damage_Roll)

                elif Spell.Method_Process == ['Attack Roll','Damage','Effect']:
                      pass
               
                elif Spell.Method_Process == ['Save','Damage']:
                      pass
                      
                elif Spell.Method_Prices == ['Save','Damage','Effect']:
                       pass

                elif Spell.Method_Price == ['Save','Effect']:
                       pass

                else: 
                        pass

        def Spell_Ends(Spell,Caster):
               if Spell.Concentration == True:
                      Caster.Concentration = False
                

#Summarize_Spell(Spells_Dict['Thunderclap'])


# How am I going to handle all of the different Spell Effects?

# Buff Circumstance
        # Blade Ward
        # Chill Touch
        # Friends
        # Frostbite
        # Viscious Mockery
        # 

# Buff Bonuses

# Buff Replacement

# Light

# Move

# Share Information

# Create Item

# Terrain

# Illusory Effects

# 




#Shield
Shield_Spell_Effect = Effects.AC_Effect('Spell','Self','1 Round','Magical',5)
def Shield_Spell(Player_Character):
       Effects.Apply_AC_Effect(Shield_Spell_Effect,Player_Character)

       if 'Shield' in Player_Character.At_Will_Spells:
              pass
       else: pass


#Thunderwave
Thunderwave_Damage_Effect = Effects.Damage_Effect('AOE','Save','Thunder',True,'Instantaneous',8,2,0,False,'Con',True)
Thunderwave_Move_Effect = Effects.Move_Effect('Cast',True,True,5,'Away',False,False,False,False,False)
def Thunderwave_Spell(Player_Character):
       Effects.Apply_Damage_Effect(Thunderwave_Damage_Effect,Player_Character,True)
       Effects.Apply_Move_Effect(Thunderwave_Move_Effect)

#Scorching Ray
Scorching_Ray_Damage_Effect = Effects.Damage_Effect('Single Target','Attack','Fire',True,'Instantaneous',8,1,0,'Ranged Spell',False,False)
def Scorching_Ray_Spell(Player_Character):
       Effects.Apply_Damage_Effect(Scorching_Ray_Damage_Effect,Player_Character,True)
       Effects.Apply_Damage_Effect(Scorching_Ray_Damage_Effect,Player_Character,True)
       Effects.Apply_Damage_Effect(Scorching_Ray_Damage_Effect,Player_Character,True)

#Shatter
Shatter_Damage_Effect = Effects.Damage_Effect('AOE','Save','Thunder',True,'Instantaneous',8,2,0,False,'Con',True)
def Shatter_Spell(Player_Character):
       Effects.Apply_Damage_Effect(Shatter_Damage_Effect,Player_Character,True)

#Fireball
#Wind Wall
#Wall of Ice
#Wall of Fire
#Cone of Cold
#Wall of Force

