import pandas as pd

def to_1D(series):
  return pd.Series([x for _list in series for x in _list])

import Establishing_Hierarchy

Creatures = pd.read_excel(r'C:\Users\maxhi\OneDrive\Desktop\Python Project\Python 5e Project Data.xlsx',sheet_name='Creatures')
Actions = pd.read_excel(r'C:\Users\maxhi\OneDrive\Desktop\Python Project\Python 5e Project Data.xlsx',sheet_name='Actions')

# will need to go through for armor source and add to inventory





XP_Table = {  # this way I can track knowledge and experience via level through killing a creature
  'CR': [0,.125,.25,.5,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
  'XP': [10,25,50,100,200,450,700,1100,1800,2300,2900,3900,5000,5900,7200,8400,10000,11500,13000,15000,18000,20000,22000,25000,33000,41000,50000,62000,75000,90000,105000,120000,135000,155000]}



# Making the Table for Monster Analysis
# Saving Throws
for i in Creatures.index:
  Str_i = str(Creatures.Saves[i])
  List_i = Str_i.split(',')
  Creatures.Saves[i] = List_i

# Speeds
for i in Creatures.index:
  Str_i = str(Creatures.Speeds[i])
  List_i = Str_i.split(',')
  Creatures.Speeds[i] = List_i
#Creatures["Speeds"] = Creatures["Speeds"].apply(eval)

# Skills
for i in Creatures.index:
  Str_i = str(Creatures.Skills[i])
  List_i = Str_i.split(',')
  Creatures.Skills[i] = List_i
#Creatures["Skills"] = Creatures["Skills"].apply(eval)

# WRI
for i in Creatures.index:
  Str_i = str(Creatures.WRI[i])
  #print(Str_i)
  List_i = Str_i.split(',')
  #print(List_i)
  Creatures.WRI[i] = List_i
#Creatures["WRI"] = Creatures["WRI"].apply(eval)

# Senses
for i in Creatures.index:
  Str_i = str(Creatures.Senses[i])
  List_i = Str_i.split(',')
  Creatures.Senses[i] = List_i
#Creatures["Senses"] = Creatures["Senses"].apply(eval)

# Languages
for i in Creatures.index:
  Str_i = str(Creatures.Languages[i])
  List_i = Str_i.split(',')
  Creatures.Languages[i] = List_i
#Creatures["Languages"] = Creatures["Languages"].apply(eval)

# Features
for i in Creatures.index:
  Str_i = str(Creatures.Features[i])
  List_i = Str_i.split(',')
  Creatures.Features[i] = List_i
#Creatures["Features"] = Creatures["Features"].apply(eval)

# Actions
for i in Creatures.index:
  Str_i = str(Creatures.Actions[i])
  List_i = Str_i.split(',')
  Creatures.Actions[i] = List_i
#Creatures["Actions"] = Creatures["Actions"].apply(eval)

# Bonus Actions
for i in Creatures.index:
  Str_i = str(Creatures.Bonus_Actions[i])
  List_i = Str_i.split(',')
  Creatures.Bonus_Actions[i] = List_i
#Creatures["Bonus_Actions"] = Creatures["Bonus_Actions"].apply(eval)

# Reactions
for i in Creatures.index:
  Str_i = str(Creatures.Reactions[i])
  List_i = Str_i.split(',')
  Creatures.Reactions[i] = List_i
#Creatures["Reactions"] = Creatures["Reactions"].apply(eval)

# Multiattack
for i in Creatures.index:
  Str_i = str(Creatures.Multiattack[i])
  List_i = Str_i.split(':')
  Creatures.Multiattack[i] = List_i
#Creatures["Multiattack"] = Creatures["Multiattack"].apply(eval)

# Spells
for i in Creatures.index:
  Str_i = str(Creatures.Spells[i])
  List_i = Str_i.split(',')
  Creatures.Spells[i] = List_i
#Creatures["Spells"] = Creatures["Spells"].apply(eval)

# Spells
for i in Actions.index:
  Str_i = str(Actions.Damage_Type[i])
  List_i = Str_i.split(',')
  Actions.Damage_Type[i] = List_i
#Creatures["Spells"] = Creatures["Spells"].apply(eval)

Creatures_and_Actions = Actions.merge(Creatures,how='left',on=['Creature Name','Book'])
#print(list(Creatures_and_Actions))

def Convert(response):
    string = str(response)
    l = list(string.split(","))
    return l

monster_primes = {}
for ind in Creatures.index:
  Monster_ID = str(str(Creatures.iloc[ind,0]) + ',' + str(Creatures.iloc[ind,1]))
  Name = str(Creatures.iloc[ind,0])
  Book = str(Creatures.iloc[ind,1])
  HP = int(Creatures.iloc[ind,5])
  AC = int(Creatures.iloc[ind,4])
  Type = str(Creatures.iloc[ind,3])
  Size = str(Creatures.iloc[ind,2])
  CR = int(Creatures.iloc[ind,18])
  XP = 0
  Prof_Bonus = 1
  Saving_Throws = Convert(Creatures.iloc[ind,12])
  Skill_Profs = Convert(Creatures.iloc[ind,13])
  Str_Score = int(Creatures.iloc[ind,6])
  Dex_Score = int(Creatures.iloc[ind,7])
  Con_Score = int(Creatures.iloc[ind,8])
  Int_Score = int(Creatures.iloc[ind,9])
  Wis_Score = int(Creatures.iloc[ind,10])
  Cha_Score = int(Creatures.iloc[ind,11])
  Languages = Convert(Creatures.iloc[ind,17])
  Features = Convert(Creatures.iloc[ind,19])
  #print(Creatures.iloc[ind,15])
  WRI = Creatures.iloc[ind,15]
  Skills = Creatures.iloc[ind,14]
  Senses = Creatures.iloc[ind,16]
  Speeds = Creatures.iloc[ind,13]
  Actions = Creatures.iloc[ind,20]
  Bonus_Actions = Creatures.iloc[ind,21]
  Reactions = Creatures.iloc[ind,22]
  Spellcasting_Prepared = Creatures.iloc[ind,27]
  Spell_DC = Creatures.iloc[ind,29]
  #Creatures[ind,1] = Monster(Name,HP,AC,Type,Size,CR,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,[],[],[],[],[],True,True)
  monster_primes[Monster_ID] = Establishing_Hierarchy.Monster(Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,True,Spellcasting_Prepared,Spell_DC,True,True,True,True,True,True,Languages,Features,WRI,True)
  #Monster_ID,Name,HP,AC,Type,Size,CR,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Active_Conditions
  monster_primes[Monster_ID].Prof_Bonus = Establishing_Hierarchy.CRToProficiency(monster_primes[Monster_ID])

  for i in Actions:
    monster_primes[Monster_ID].Actions[i] = i 
  
  for i in Bonus_Actions:
    monster_primes[Monster_ID].Bonus_Actions[i] = i
  
  for i in Reactions:
    monster_primes[Monster_ID].Reactions[i] = i
  
  
  monster_primes[Monster_ID].Features += Features
  monster_primes[Monster_ID].Languages += Languages
  monster_primes[Monster_ID].Skill_Profs += Skills
  #monster_primes[Monster_ID].Senses += Senses
  #monster_primes[Monster_ID].Speeds += Speeds

#print(monster_primes)

#print(monster_primes['Fire Elemental,Monster Manual'].WRI)
#print(Creatures.WRI)

#monster_instances = {}
#for ind in Creatures.index:
#  Monster_ID = str(str(Creatures.iloc[ind,0]) + ',' + str(Creatures.iloc[ind,1]))
#  Name = str(Creatures.iloc[ind,0])
#  Book = str(Creatures.iloc[ind,1])
#  HP = int(Creatures.iloc[ind,5])
#  AC = int(Creatures.iloc[ind,4])
#  Type = str(Creatures.iloc[ind,3])
#  Size = str(Creatures.iloc[ind,2])
#  CR = int(Creatures.iloc[ind,18])
#  Prof_Bonus = 1
#  Saving_Throws = Convert(Creatures.iloc[ind,12])
#  Skill_Profs = Convert(Creatures.iloc[ind,13])
#  Str_Score = int(Creatures.iloc[ind,6])
#  Dex_Score = int(Creatures.iloc[ind,7])
#  Con_Score = int(Creatures.iloc[ind,8])
#  Int_Score = int(Creatures.iloc[ind,9])
#  Wis_Score = int(Creatures.iloc[ind,10])
#  Cha_Score = int(Creatures.iloc[ind,11])
#  Languages = Convert(Creatures.iloc[ind,17])
#  Features = Convert(Creatures.iloc[ind,19])
#  WRI = Convert(Creatures.iloc[ind,15])
#  Skills = Creatures.iloc[ind,14]
#  Senses = Creatures.iloc[ind,16]
#  Speed = Creatures.iloc[ind,13]
#  Actions = Creatures.iloc[ind,20]
#  Bonus_Actions = Creatures.iloc[ind,21]
#  Reactions = Creatures.iloc[ind,22]
#  Spells = Creatures.iloc[ind,27]
#  Spell_DC = Creatures.iloc[ind,29]
#  Instance = 1
#  Spawn_Inventory = 0
#  Monster_Instance_ID = str(Monster_ID + str(Instance))
#  Current_HP = HP
  #Creatures[ind,1] = Monster(Name,HP,AC,Type,Size,CR,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,[],[],[],[],[],True,True)
#  monster_instances[Monster_Instance_ID] = Establishing_Hierarchy.Monster_Instance(Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,True,Spells,Spell_DC,True,True,Languages,Features,WRI,Spawn_Inventory,Instance,Monster_Instance_ID,True,True,True,'Alive',True,False)
  #Monster_ID,Name,HP,AC,Type,Size,CR,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Active_Conditions
#  monster_primes[Monster_ID].Prof_Bonus = Establishing_Hierarchy.CRToProficiency(monster_primes[Monster_ID])
#  monster_primes[Monster_ID].Actions += Actions
#  monster_primes[Monster_ID].Bonus_Actions += Bonus_Actions
#  monster_primes[Monster_ID].Reactions += Reactions
#  monster_primes[Monster_ID].Features += Features
#  monster_primes[Monster_ID].Languages += Languages
#  monster_primes[Monster_ID].Skill_Profs += Skills
  #monster_primes[Monster_ID].Senses += Senses
  #monster_primes[Monster_ID].Speed += Speed

#print(Creatures_and_Actions)

#print(monster_instances)
