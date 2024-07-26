# Creating the Heirarchy
import numpy as np
import random
from random import randrange
import Dice_Rolls
from functools import partial
import abc
from typing import List, Dict, Any

##### Constants
Classes_Int_List = ['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard']
d6_Classes = [12,10]
d8_Classes = [0,2,3,4,6,9,11]
d10_Classes = [5,8,7]
d12_Classes = [2]

Senses = {
  'Precise': ['Sight'],       # Darkvision
  'Imprecise': ['Hearing'],   # Tremorsense
  'Vague': ['Smell'],
  'Disfunctional': []         # Perhaps for if blinded or deafened...
}   # Uncertain: Blindsight, Truesight, Lifesense, Detect Thoughts, ESP


##### Common Functions

def levelToProficiency(Player_Character):
  count = 0
  for i in Player_Character.Levels:
      if i != False:
        count = count + 1
      else:
        pass
  return np.floor(2 + (count - 1)/4)

def CRToProficiency(Monster):
  print(type(Monster.CR))
  return np.floor(2 + (Monster.CR - 1)/4)

def abilityScoreToModifier(Score):
  return int((Score-10)/2)                #there's currently an issue where it returns 9 as a 0 when it should be -1

def Predicted_Hit_Points(Player_Character):
  # the first level the character gets their full hit dice plus con modifier
  First_Level_Hitpoints = 0
  First_Level_Hitpoints = Player_Character.First_Class.Hit_Dice + abilityScoreToModifier(Player_Character.Con_Score) 
  #print(First_Level_Hitpoints)
  Total_Average_Hit_Points = First_Level_Hitpoints
  #print(Total_Average_Hit_Points)

  for i in Player_Character.Levels:
    if i != False:
      Class_Average_Hitpoints = Dice_Rolls.Average_Roll(1,i.Hit_Dice,abilityScoreToModifier(Player_Character.Con_Score),0)
      #print(Class_Average_Hitpoints)
      Total_Average_Hit_Points = Total_Average_Hit_Points + Class_Average_Hitpoints
    else:
      pass
  #print(Total_Average_Hit_Points)
  return Total_Average_Hit_Points

def Random_Hit_Points(Player_Character):         # Need to update this to match the changes to Predicted Hit Points
  i = Player_Character.Class.Hit_Dice
  for i in range(1,Player_Character.Level,1):
    roll = randrange(1,Player_Character.Class.Hit_Dice+1,1)
    i = i + roll
    print(roll)
  hit_points = i + (abilityScoreToModifier(Player_Character.Con_Score) * Player_Character.Level)
  print('Randomly Rolled Hit Points:',i)

def Spawn_Creature(Location,Creature):
  Creature.Location = Location

def Self_Preservation_Line(Creature): # Need a function that determines at what HP will the creature run away
  if Creature.Int_Score or Creature.Wis_Score:
    Self_Preservation_Line = Creature.HP * .6
  elif Creature.Int_Score or Creature.Wis_Score:
    Self_Preservation_Line = Creature.HP * .3
  else:
    Self_Preservation_Line = Creature.HP * .1
  return Self_Preservation_Line



def Count_Player_Levels(Player_Character):
  for i in Player_Character.Levels:
    if Player_Character.Levels.index(i) > 0:
      count = 0
      if Player_Character.Levels[i] != False:
        count = int(count) + 1
      else:
        pass
    elif i == False:
      pass
    else: pass
  return count

def Calc_Armor_Class(Player_Character):
  AC = 10
  if Player_Character.Armor_Equipped == []:
    AC = 10 + abilityScoreToModifier(Player_Character.Dex_Score)
    return AC
  else:
    for i in range(len(Player_Character.Armor_Equipped)):
      if i == 'Shield':
        AC = AC + 2

    #if 'Shield' in Player_Character.Armor_Equipped:

    Player_Character.Armor_Equipped[0] 

def Attack_Score(Creature): # most of my problems are coming from this bit of code right here
  #print("Attack Score Creature:",Creature)
  if len(Creature.Weapon_Equipped) > 1:
    if Creature.Weapon_Equipped[0].Finesse == True:
      return int(max(abilityScoreToModifier(Creature.Str_Score),abilityScoreToModifier(Creature.Dex_Score)))
    else:
      return int(abilityScoreToModifier(Creature.Str_Score))
  else:
    if Creature.Weapon_Equipped[0].Finesse == True:
      return int(max(abilityScoreToModifier(Creature.Str_Score),abilityScoreToModifier(Creature.Dex_Score)))
    else:
      return int(abilityScoreToModifier(Creature.Str_Score))

def Calculate_Expected_Damage_for_RTH(Target,Creature,Attack,Damage_Dice_Num,Damage_Dice_Type,Damage_Bonus,Damage_Bonus2): # RTH standing for Roll to Hit; this function is also assuming normal circumstances
  if Attack == False:
    Damage_Modifiers = []
    Weapon = Creature.Weapon_Equipped[0]
    #print('RTH Creature:',Creature)
    Prob_to_Hit = (21 + Attack_Score(Creature) + Creature.Prof_Bonus - Target.AC) / 20

    Damage = Dice_Rolls.Average_Roll(Damage_Dice_Num,Damage_Dice_Type,Damage_Bonus,Damage_Bonus2)
    Expected_Damage = Damage * Prob_to_Hit

    Crit_Damage = (Dice_Rolls.Average_Roll(Damage_Dice_Num,Damage_Dice_Type,0,0) * 2) + Damage_Bonus
    Crit_Expected_Damage = Crit_Damage * 0.05 * len(Creature.Crit)

    Expected_Damage = Expected_Damage + Crit_Expected_Damage

    if str(Weapon.Damage_Type + 'res') in Target.WRI:
      Damage_Modifiers.append(0.5)

    elif str(Weapon.Damage_Type + 'immu') in Target.WRI:
      Damage_Modifiers.append(0)
    
    elif 'nonmagicalres' in Target.WRI:
      Damage_Modifiers.append(0.5)
    
    elif 'nonmagicalimmu' in Target.WRI:
      Damage_Modifiers.append(0)
    
    else:
      pass


    #if 'critimmu' in Target.WRI:
    #  Total_Expected_Damage = Expected_Damage

    # Glancing Blows can only occur when the Attack_Bonus is less than the AC
    if Attack_Score(Creature) < Target.AC:
      Damage_Modifiers.append(0.5)
    
    
    for i in range(len(Damage_Modifiers)):
      Total_Expected_Damage = Expected_Damage * Damage_Modifiers[i]

  else:
    pass
  return Expected_Damage

def Check_Save_Proficiencies(Creature,Save):
  Ability_Score = Dice_Rolls.Saving_Throws.loc[Save]
  #if Creature.Effects      will handle this when I do the same for ability_checks
  if Save in Creature.Saving_Throws:
    line = str(Creature,'.',Ability_Score)
    Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + Creature.Saving_Throws
  else:
    line = str(Creature,'.',Ability_Score)
    Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line))
  return Result

def Check_Skill_Proficiencies(Creature,Skill,Ability_Score):
  prof_list = [Creature.Proficiency,Creature.Half_Proficiency,Creature.Expertise]
  for i in prof_list:
    if Skill in 0:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + Creature.Prof_Bonus
    elif Skill in 1:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + (Creature.Prof_Bonus / 2)
    elif Skill in 2:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line)) + (Creature.Prof_Bonus * 2)
    else:
      line = str(Creature,'.',Ability_Score)
      Result = Dice_Rolls.Roll + abilityScoreToModifier(exec(line))
  return Result

def Ability_Check(Creature,Skill,Ability_Score):
  #if Creature.Effects[]          I want to put a line here that will check the creature for any effect that could influence the ability check

  if str('Advantage:' + Skill) in Creature.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Advantage(Creature)
  elif str('Disadvantage:' + Skill) in Creature.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Disadvantage(Creature)
  else:
    Roll = Dice_Rolls.d20(Creature)

  Result = Check_Skill_Proficiencies(Creature,Skill,Ability_Score)

  print(Roll)
  print(Result)

def Contested_Ability_Check(Creature1,Creature2,Skill,Ability_Score):
  #if Creature.Effects[]          I want to put a line here that will check the creature for any effect that could influence the ability check
  if str('Advantage:' + Skill) in Creature1.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Advantage()
  elif str('Disadvantage:' + Skill) in Creature1.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Disadvantage()
  else:
    Roll = Dice_Rolls.d20()
  Creature1_Result = Dice_Rolls.Check_Skill_Proficiencies(Creature1,Skill,Ability_Score) + Roll

  if str('Advantage:' + Skill) in Creature2.Circumstances['Ability Checks']:      #if Creature.Effects[]          I want to put a line here that will check the creature for any effect that could influence the ability check
    Roll = Dice_Rolls.d20_Advantage()
  elif str('Disadvantage:' + Skill) in Creature2.Circumstances['Ability Checks']:
    Roll = Dice_Rolls.d20_Disadvantage()
  else:
    Roll = Dice_Rolls.d20()
  Creature2_Result = Check_Skill_Proficiencies(Creature2,Skill,Ability_Score) + Roll

  if Creature1_Result > Creature2_Result:
    pass
  else:
    pass

def Saving_Throw(Creature,Save):
  if str('Advantage: ' + Save + ' Saving Throws') in Creature.Circumstances['Saving Throws']:
    Roll = Dice_Rolls.d20_Advantage(Creature)
  elif str('Disadvantage: ' + Save + ' Saving Throws') in Creature.Circumstances['Saving Throws']:
    Roll = Dice_Rolls.d20_Disadvantage(Creature)
  else:
    Roll = Dice_Rolls.d20(Creature)

  Result = Dice_Rolls.Check_Save_Proficiencies(Creature,Save)

  print(Roll)
  print(Result)


#### Observer Pattern

class GameEvent:
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.type = event_type
        self.data = data

class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, event: GameEvent):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: GameEvent):
        for observer in self._observers:
            observer.update(event)

class Character_Class(Observer):
    def __init__(self, name: str, hit_dice: int, saving_throws: List[str], starting_skill_number: int, armor_profs: List[str], weapon_profs: List[str], skill_profs: List[str], tool_profs: List[str], spellcasting_ability: str, subclasses, features, multiclassing_requirement, spell_list, caster_type, starting_equipment):
        self.name = name
        self.hit_dice = hit_dice
        self.saving_throws = saving_throws
        self.starting_skill_number = starting_skill_number
        self.armor_profs = armor_profs
        self.weapon_profs = weapon_profs
        self.tool_profs = tool_profs
        self.spellcasting_ability = spellcasting_ability
        self.subclasses = subclasses
        self.features = features
        self.multiclassing_requirement = multiclassing_requirement
        self.spell_list = spell_list
        self.caster_type = caster_type
        self.starting_equipment = starting_equipment
        
    # how should a class be added to a character?
    # how should adding a single level of a class to a character be handled?

    def begin_class(self, creature):
       creature.first_class = self
       creature.levels[0] = self

    def multiclass_into_class(self, creature):
       pass

    def add_level_in_class(self):
       pass


class Subclass(Observer):
    def __init__(self, name: str, features, spellcasting_ability, parent_class: CharacterClass):
        self.name = name
        self.features = features
        self.spellcasting_ability = spellcasting_ability
        self.parent_class = parent_class

    def update(self, event: GameEvent):
        if event.type == "turn_end":
            print(f"{self.name} subclass of {self.parent_class.name} is checking for end-of-turn effects")

class Class_Feature(Observer):
    def __init__(self, character_class, name: str, type: str):
        self.character_class = character_class
        self.name = name
        self.type = type

        # need a way to determine the root by which the feature is added to the character

    def add_class_feature(self, creature, type):
       pass

    def remove_class_feature(self, creature):
       pass


# should I make an entity class instead of a Player_Character class first?



class Player_Character(Observer):
    def __init__(self, name: str, first_class, species, subspecies, background, tool_profs, instrument_profs, language_profs, weapon_profs, weapon_equipped, armor_profs, armor_equipped, str_score, dex_score, con_score, int_score, wis_score, cha_score, spellcasting_prepared, item_attunements, inventory, related_stat_blocks, alignment):
        self.name = name
        self.first_class = first_class
        self.species = species
        self.subspecies = subspecies
        self.size = 'medium'
        self.speed = {
            'walking': 6,
            'flying': 0,
            'swimming': 0,
            'burrowing': 0,
            'climbing': 0,
            'flyhover': 0
        }
        self.str_score = str_score
        self.dex_score = dex_score
        self.con_score = con_score
        self.int_score = int_score
        self.wis_score = wis_score
        self.cha_score = cha_score
        self.levels = [first_class] + [False] * 19
        self.level_count = Count_Player_Levels(self)
        self.subclasses = [False] * 9
        self.background = background
        
        ### Dealing with Hit Dice ###
        self.hit_dice = self.calc_hit_dice_types_list()[0]
        self.hit_dice_remaining = self.hit_dice

        self.hit_dice_by_type = self.calc_hit_dice_types_list()[1]
        self.hit_dice_remaining_by_type = self.hit_dice_by_type



        self.hp = self.calc_hit_points()
        self.temp_hp = 0
        self.current_hp = self.hp

        self.weapon_profs = weapon_profs
        self.armor_profs = armor_profs

        # there are several class features that determine armor class if the character is not wearing armor
        # so it may require an event to be notified when the character's armor class needs to be recalculated
        self.armor_equipped = armor_equipped
        self.weapon_equipped = weapon_equipped
        self.shield_equipped = False

        # I want it to be that the various armor equations are stored in a dictionary and then the function to calc ac goes through each and calcs the highest
        # or should choosing AC be part of the decision making of the agent?

        self.armor_class_formulas = {}
        self.armor_class = Calc_Armor_Class(self)
        self.background = background
        self.prof_bonus = levelToProficiency(self)
        
        # skill proficiencies is a concept that will need to be revisited based on the various modifiers that can affect it
        self.skill_profs = []
        self.skill_expertise = []
        self.skill_half_proficiency = []
        
        self.instrument_profs = instrument_profs
        self.tool_profs = tool_profs
        self.language_profs = language_profs
        
        self.item_attunements = item_attunements
        self.inventory = inventory
        self.related_stat_blocks = related_stat_blocks
        self.alignment = alignment

        self.movement_spend = 0
        self.initiative = 0

        self.saving_throws = []
        self.actions = {}
        self.reactions = {}
        self.bonus_actions = {}
        self.free_actions = {}
        self.movement_actions = {}
        self.effects = {}
        self.circumstances = {}

        self.conditions = []
        self.active_effects = []

        self.One_Minute_Options = {
          'Unlimited': [],
          'Charges': []
          }

        self.At_Will_Spells = []
        self.Per_Use_Spells = {
          '1/long_rest': {},
          '1/short_rest': {}}
        self.spellcasting_known = {}
        self.spellcasting_prepared = {}
        
        self.Class_Resources = {'Spell_Slots': {}}
        self.Class_Save_DCs = {}

        self.Concentrating = False
        self.Attunement_Slots = 3
        self.Item_Attunements = []
        self.Attunement_Slots_Filled = len(self.Item_Attunements)
        self.WRI = [] 
        self.Adapted_Environment = {
          'Air': 'Infinite',
          'Suffocating': .6 * abilityScoreToModifier(self.Con_Score),
          'Water': 1 + abilityScoreToModifier(self.Con_Score),
          }

        self.Attacks = 1
        self.Usable_Attack_Score = {
          'False': [str_score,dex_score], # Non-Magical
          'True': [str_score,dex_score], # Magical
        }
        self.Crit = [20]
        
        self.Location = [0,0,0,0] # last one is the material plane


        self.Inventory = {    # calculate the weight
          'Armor': [],
          'Weapons': [],
          'Treasure': [],

          'Magic Items': {
            'Armor': [],
            'Weapons': [],
            'Other': []
          },
          
          'Vehicles': [],
          'Instruments': [],
          'Tools': [],
          'Artisan_Tools': [],
          'Games': [],

          'Packs': [],
          'Apparel': [],
          'Storage': [],
          'Identifying_Items': [],
          'Currency': [],
          'Other': []
        }

        self.Jump_Height = 3 + abilityScoreToModifier(self.str_score)
        self.Jump_Distance = self.str_score
        self.Carrying_Capacity = self.str_score * 15
        self.Target_List = []

        self.Related_Stat_Blocks = {
          'Familiar': 'None',
          'Steed': 'None',
          'Homonculus': 'None',
          'Companion': 'None',
          'Summons': {},
          'Dominated_Creatures': {},
          'Other': 'None',
        }
        
        self.Passive_Investigation = 10 + abilityScoreToModifier(self.int_score)
        self.Passive_Perception = 10 + abilityScoreToModifier(self.wis_score)
        self.Active_Effects = []
        self.Senses = []
        self.Life_Status = 'Alive'




    ##### Character Creation #####
    def count_player_levels(self):
            count = 0
            for i in self.levels:
                if i != False:
                    count += 1
            return count
    
    def level_up(self, character_class: Character_Class):
       starting_level = self.count_player_levels()
       self.levels[starting_level] = character_class
       self.level_count = self.count_player_levels()

    
       # this is where several checks will need to be made 
       
    def ability_score_increase(self):
       pass
    
    ##### Health Functions #####
    def calc_hit_dice_types_list(self):
        hit_dice_types = [self.first_class.hit_dice] + [False] * 19
        for i in range(1, 20):
            if self.levels[i] != False:
                hit_dice_types[i] = self.levels[i].hit_dice
        
        hit_dice_dictionary = {
            12: 0,
            10: 0,
            8: 0,
            6: 0,
            4: 0
        }

        for hit_dice in hit_dice_types:
            if hit_dice != False:
                hit_dice_dictionary[hit_dice] += 1

        return hit_dice_types, hit_dice_dictionary
    
    def calc_hit_points(self):
        hit_points = 0
        for i in range(0, 20):
            if self.hit_dice_types[i] != False:
                hit_points += Dice_Rolls.Average_Roll(1, self.hit_dice_types[i], abilityScoreToModifier(self.con_score), 0)
        return hit_points

    def roll_hit_dice(self, hit_dice_to_roll: list):
       # the reason the hit dice to roll has to be a list is because the player can have multiple hit dice types 
       # the list go in order of d12, d10, d8, d6, d4
       for i in hit_dice_to_roll:
          if hit_dice_to_roll[i] > self.hit_dice_remaining_by_type[i]:
             print(f"Error: Not enough hit dice of type {i} to roll")
          else:
              self.hit_dice_remaining_by_type[i] -= hit_dice_to_roll[i]
              for j in range(hit_dice_to_roll[i]):
                  roll = Dice_Rolls.d12()
                  self.current_hp += roll
                  if self.current_hp > self.hp:
                      self.current_hp = self.hp

                  print(f"Rolled a {roll} on a d{i} hit die. HP: {self.hp}/{self.max_hp}")
       

    ##### Armor Functions #####
    def calc_armor_class(self):
       # this might need to be changed to reference the formula listed in the Armor Entity so that any magic item bonuses can be applied
       # this may also need to be changed so that unarmored defense can be taken into the equation

       if self.armor_equipped == []:
          AC = 10 + abilityScoreToModifier(self.dex_score)
          return AC
       elif self.armor_equipped[0] == 'hide':
          AC = 12 + abilityScoreToModifier(self.dex_score)
          return AC
       elif self.armor_equipped[0] == 'chain mail':
          AC = 16
          return AC
       elif self.armor_equipped[0] == 'scale mail':
          AC = 14 + min(2, abilityScoreToModifier(self.dex_score))
          return AC
       elif self.armor_equipped[0] == 'breastplate':
          AC = 14 + min(2, abilityScoreToModifier(self.dex_score))
          return AC
       elif self.armor_equipped[0] == 'half plate':
          AC = 15 + min(2, abilityScoreToModifier(self.dex_score))
          return AC
       elif self.armor_equipped[0] == 'ring mail':
          AC = 14
          return AC
       elif self.armor_equipped[0] == 'chain shirt':
          AC = 13 + min(2, abilityScoreToModifier(self.dex_score))
          return AC
       elif self.armor_equipped[0] == 'splint':
          AC = 17
          return AC
       elif self.armor_equipped[0] == 'plate':
          AC = 18
          return AC

    def check_armor_profs(self, event: GameEvent):
       if event.type == 'turn_start':
          if self.armor_equipped != [] and self.armor_equipped[0] not in self.armor_profs:
             self.notify(GameEvent('armor_debuff', {'armor': self.armor_equipped[0]}))

    def doff_armor(self):
       pass

    def equip_armor(self, armor: str):
       pass

    def calc_inventory_weight(self):
       pass


    ##### Combat Functions #####
    def take_damage(self,Damage_Type,Damage_Amount,*Tags):
      # tags that would be acceptable: ignore_res, ignore_immu, impose_vul

      # will need a way to ignore these if statements based on the tags
      if str(Damage_Type) + 'res' in self.WRI:
        Damage_Amount = Damage_Amount / 2
      if str(Damage_Type) + 'vul' in self.WRI:
        Damage_Amount = Damage_Amount * 2
      if str(Damage_Type) + 'immu' in self.WRI:
        Damage_Amount = 0
      
      # need to check for effects that would change the damage taken
      if self.Effects['Self_Taking_Damage'][Damage_Type] != []:
        pass
      


      # first remove Temp_HP
      if self.Temp_HP > 0:
        self.Temp_HP -= Damage_Amount
        if self.Temp_HP < 0:
          Damage_Amount = abs(self.Temp_HP)
          self.Temp_HP = 0
        else:
          return

      # then remove HP
      # if the damage would reduce the player to 0 HP, then the player is downed
      # if the damage would deal more than the player's HP, then the player is dead
      self.Current_HP -= Damage_Amount
      if self.Current_HP <= 0:
        self.Life_Status = 'Down'
        if Damage_Amount > self.HP:
          self.Life_Status = 'Dead'

    def heal(self, amount: int):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"{self.name} heals for {amount}. HP: {self.hp}/{self.max_hp}")

    def roll_initiative(self):
        return Dice_Rolls.d20() + abilityScoreToModifier(self.dex_score)


    ##### Functions in Combat #####
    

    def move(self, distance: int):
        self.position += distance
        print(f"{self.name} moves {distance} feet.")

        # for space moved, must notify any creatures in adjacent spaces that they can take an opportunity attack
        def notify_adjacent_creatures(event):
            if event.type == "move":
                if abs(self.position - event.data["position"]) == 5:
                    self.notify(GameEvent("opportunity_attack", {"creature": event.data["creature"]}))



    ##### Rest Functions #####
    def short_rest(self):
        self.roll_hit_dice()
    
    def long_rest(self):
        self.current_hp = self.hp
        self.hit_dice_remaining = self.hit_dice
        self.hit_dice_remaining_by_type = self.hit_dice_by_type
    
    def reset_round(self):
       pass
  
    ##### Other Functions #####

    def update(self, event: GameEvent):
        if event.type == "round_end":
            print(f"{self.name} is checking for end-of-round effects")
        # Let the class and subclass handle their specific effects

    def add_condition(self, condition: str):
        self.conditions.append(condition)
      
    def remove_condition(self, condition: str):
        self.conditions.remove(condition)




    def ability_check(self, Ability, DC, *tags):
      if Ability == "Strength":
        ability_bonus = abilityScoreToModifier(self.Str_Score)

      elif Ability == "Dexterity":
        ability_bonus = abilityScoreToModifier(self.Dex_Score)

      elif Ability == "Constitution":
        ability_bonus = abilityScoreToModifier(self.Con_Score)

      elif Ability == "Intelligence":
        ability_bonus = abilityScoreToModifier(self.Int_Score)

      elif Ability == "Wisdom":
        ability_bonus = abilityScoreToModifier(self.Wis_Score)

      elif Ability == "Charisma":
        ability_bonus = abilityScoreToModifier(self.Cha_Score)

      # check for any advantage or disadvantage
      # self.Circumstances['Ability Checks'][Ability]

    def attack_check(self, type, magical, *tags):
      # now to determine the choices behind making an attack check...
      # what's already determined:
      # - the target
      # - the weapon
      # what's not been determined:
      # - ability score to use  


      def attack_check_event(event):
         pass
         # what if instead, Attacks had tags...and instead of storing effects in a dictionary that would get looped through, 
         # the events would get looped through if they applied or not... 

      best_score = max(self.Usable_Attack_Score[magical])
      best_score_ability_modifier = abilityScoreToModifier(best_score)


      if type == 'Melee':

        if self.Circumstances['Attack Rolls']['Melee'] != []:
          pass
        else:
          pass 




    def skill_check(self, Ability, Skill, DC):
      pass

    def saving_throw(self, Ability, DC):
      pass

    def Choose_Target_Offense(self):
      pass


    def death_save(self):
       pass

    def take_turn(self):
       pass


class Game(Subject):
    def __init__(self):
        super().__init__()
        self.creatures = []
        self.current_turn = 0
        self.round_number = 1

    def add_creature(self, creature):
        self.creatures.append(creature)

    def roll_initiative(self):
        for creature in self.creatures:
            creature.initiative = creature.roll_initiative()
        self.creatures.sort(key=lambda x: x.initiative, reverse=True)

    def run(self):
        while True:
            self.handle_turn()

    def take_turn(self, creature):
        print(f"\n{creature.name}'s turn:")
        self.notify(GameEvent("turn_start", {"creature": creature}))

        # Movement
        move_distance = random.randint(0, 30)
        creature.move(move_distance)

        # Action
        action = random.choice(["attack", "cast_spell", "dodge"])
        if action == "attack":
            self.perform_attack(creature)
        elif action == "cast_spell":
            self.cast_spell(creature)
        elif action == "dodge":
            print(f"{creature.name} takes the Dodge action.")

        self.notify(GameEvent("turn_end", {"character": creature}))

    def handle_turn(self):
        active_character = self.creatures[self.current_turn]
        
        # Handle character actions here...
        self.take_turn(active_character)

        self.current_turn = (self.current_turn + 1) % len(self.creatures)
        if self.current_turn == 0:
            self.round_number += 1
            self.notify(GameEvent("round_end", {"round": self.round_number}))








############################################### Pre-Observer Pattern Plan ####################################################

class Entity:
  def __init__(self,AC,HP):
    self.AC = AC
    self.HP = HP
    # Damage Immunities
    # Damage Resistances
    # Damage Vulnerabilities
    # Condition Immunities

class Object(Entity):
  def __init__(self, #Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed
               
               # standard identifiers
                    # perhaps I'll need a Object ID
               Name, # the common item name or magic item name example: greatsword
               Type, # the standard types examples: weapon, armor, potion, trade good, vehicle, 
               Size, # if it's a weapon, the size creature intended for, otherwise, how much space the item fills examples: large, medium, etc
               Classification, # the way that 5e tools separates objects examples: mundane, magic, variant
               Rarity,

               # further identifiers, not every object has these so some will be homebrewed
               Material, # examples: steel, adamantine, mithral
               Weight,   # measured in lbs
               GP_Value, # for magical items I'll round 

               AC,
               HP,
               WRI,

               Magical,
               Magical_Bonus,
               Item_Passive_Effects,
               Requires_Attunement,
               No_Attunement_Effects,
               Attunement_Effects,
               
               Consumable, # does the item destroy itself upon use?
               Consumable_Effects,
               Results_When_Consumed, # example: produces a glass flask
               
               Charges,
               Recharge_Type,
               Upon_0_Charges,

               Sentient,
               Intelligence,
               Wisdom,
               Charisma,
               Senses,
               Languages,
               Spells, 
               Spell_DC,

               Bestowed_Actions,

               Spellcasting_Focus,
               Cursed
               ):


    self.Name = Name
    self.Type = Type    # Object Types = [Weapon,Armor,Trade_Good,Vehicle,]
    self.Size = Size    # Sizes =  Miniscule = 
                        #          Tiny = 1.25ft x 1.25ft
                        #          Small = 2.5ft x 2.5ft
                        #          Medium = 5ft x 5ft
                        #          Large = 10ft x 10ft
                        #          Huge = 15ft x 15ft
                        #          Gargantuan = 20ft x 20ft
                        #          Colossal = 25+ x 25+
    self.Classification = Classification
    self.Rarity = Rarity        # Rarity Types = [Common,Uncommon,Rare,Very Rare,Legendary,Artifact]

    self.Material = Material
    self.Weight = Weight
    self.GP_Value = GP_Value

    self.AC = AC 
    self.HP = HP 
    self.WRI = WRI 

    self.Magical = Magical
    self.Magical_Bonus = Magical_Bonus
    self.Item_Passive_Effects = Item_Passive_Effects
    self.Requires_Attunement = Requires_Attunement
    self.No_Attunement_Effects = No_Attunement_Effects
    self.Attunement_Effects = Attunement_Effects

    self.Consumable = Consumable
    self.Consumable_Effects = Consumable_Effects
    self.Results_When_Consumed = Results_When_Consumed

    self.Charges = Charges
    self.Recharge_Type = Recharge_Type
    self.Upon_0_Charges = Upon_0_Charges

    self.Sentient = Sentient
    self.Intelligence = Intelligence
    self.Wisdom = Wisdom
    self.Charisma = Charisma
    self.Senses = Senses
    self.Languages = Languages
    self.Spells = Spells
    self.Spell_DC = Spell_DC

    self.Bestowed_Actions = Bestowed_Actions

    self.Cursed = Cursed
    self.Spellcasting_Focus = Spellcasting_Focus
    

  def Add_Item_to_Inventory(Object,Player_Character):
    if Object.Magical == True:
      Player_Character.Inventory[Object.Type].append(Object)
    else:
      Player_Character.Inventory[Object.Type].append(Object)

    Player_Character.Effects['Object_Effects'] = Object.No_Attunement_Effects
    if Object in Player_Character.Item_Attunements and Object.Requires_Attunement != False:
      Player_Character.Effects['Object_Effects'] = Object.Attunement_Effects


  def Attune_to_Item(Object,Player_Character):
    if Object in Player_Character.Inventory and Object.Requires_Attunement == True and len(Player_Character.Item_Attunements) < Player_Character.Attunement_Slots:
      Player_Character.Item_Attunements.append(Object)
    else:
      print('Error in Attuning')


    #self.Sentient = bool()      # if this is the case, shouldn't it then be a Creature???
      # an object can have many of the same features as a creature (statistics, actions, etc)
      # the way I'm going to solve this issue is by having an attribute for each of these features in the object class

class Weapon(Object):
  def __init__(self,Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed,Weapon_Properties,Weapon_Type):
    super().__init__(Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed)
    self.Weapon_Properties = Weapon_Properties
    self.Weapon_Type = Weapon_Type

class Armor(Object):
  def __init__(self,Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed):
    super().__init__(Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed)
    
class Trade_Good(Object):
  def __init__(self,Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed):
    super().__init__(Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed)
    
class Vehicle(Object):
  def __init__(self,Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed):
    super().__init__(Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed)
    
class Object_Instance(Object):
  def __init__(self,Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed):
    super().__init__(Name,Type,Size,Classification,Rarity,Material,Weight,GP_Value,Magical,Magical_Bonus,Item_Passive_Effects,Requires_Attunement,No_Attunement_Effects,Attunement_Effects,Consumable,Consumable_Effects,Results_When_Consumed,Charges,Recharge_Type,Upon_0_Charges,Sentient,Intelligence,Wisdom,Charisma,Senses,Languages,Spells,Spell_DC,Bestowed_Actions,Spellcasting_Focus,Cursed)
    
    #self.Status = Status        # broken, disenchanted, 
    #self.Location = Location    # if not in inventory
    #self.Carrier = Carrier      # who's inventory is it in




## Object Rules
Object_Armor_Class = {
    'Material': ['Cloth','Paper','Rope','Crystal','Glass','Ice','Wood','Bone','Stone','Iron','Steel','Mithral','Adamantine'],
    'AC': [11,11,11,13,13,13,15,15,17,19,19,21,23]}
Object_Hit_Points = {
    'Size': ['Tiny','Tiny','Small','Small','Medium','Medium','Large','Large'],
    'Durability': ['Fragile','Resilient','Fragile','Resilient','Fragile','Resilient','Fragile','Resilient'],
    'Hit Dice': ['1d4','2d4','1d6','3d6','1d8','4d8','1d10','5d10']}


class Memory_Fragment:
  def __init__(self,Type,Holder):
    self.Type = Type # Combat, Social, or Exploration
    self.Holder = Holder # Who has the memories
    
    # Combat Attributes
    self.Fight_Description = {
      'Creatures_Involved': {
        # Example Monster: {
        #   Actions Taken: {
        #     Type: Damage/Condition/Effect,
        #     Number of times used: X, 
        #     
        #   }
        # }
      },
      'Character_Level': [],
      'Party_Level': [],
      'Initiative': []
    }


    # Social Attributes
    self.Social = {

    }

    # Exploration Attributes
    self.Exploration = {

    }



class Player_Character:
  def __init__(self,Name,First_Class,Species,Subspecies,Levels,Background,Skill_Profs,Skill_Expertise,Tool_Profs,Weapon_Equipped,Armor_Equipped,Senses,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Spellcasting_Prepared,Item_Attunements,Inventory,Related_Stat_Blocks,Alignment):
    self.Name = Name
    self.First_Class = First_Class
    
    self.Species = Species
    self.Subspecies = Subspecies

    self.Size = 'Medium'
    self.Speed = {
        'Walking': 30,
        'Flying': 0,
        'Swimming': 0,
        'Burrowing': 0,
        'Climbing': 0,
        'Flyhover': 0}
    
    self.Str_Score = Str_Score
    self.Dex_Score = Dex_Score
    self.Con_Score = Con_Score
    self.Int_Score = Int_Score
    self.Wis_Score = Wis_Score
    self.Cha_Score = Cha_Score
    
    self.Levels = [
      First_Class,    # Barbarian
      False,
      False,            # I could do a level up function and in it would be an if statement for selecting a subclass
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ]                    # an option that I have for multiclassing is to have an attribute for each level that gets assigned to a class
                                          # and then the total class and subclass allocation is determined based on the summation of the attributes

    self.Level_Count = sum(1 for n in self.Levels if n != False)

    self.Subclasses = [ # the most subclasses a character could have in theory is 9 
                        # Cleric, Warlock, and Sorcerer at level 1; Druid and Wizard at level 2; means 5 subclasses by level 7, 
                        # that leaves 4 additional since 13 (levels remaining) / 3 = 4          5 + 4 = 9
                        # so I only need 9 items in the list
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ]

    self.Hit_Dice_Types = [
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ]
    self.Hit_Dice_Number = len(self.Hit_Dice_Types)
    self.HP = 0
    self.Temp_HP = 0
    self.Current_HP = self.HP
    self.Allow_for_More_than_Max_HP = False

    self.AC = 10 + abilityScoreToModifier(Dex_Score)              # This one needs to be corrected eventually
    self.Background = Background

    self.Prof_Bonus = levelToProficiency(self)        # This function is going to need an update based on the new level system
  
    self.Skill_Half_Prof = []                     
    self.Skill_Profs = []
    self.Skill_Expertise = []
    
    self.Tool_Profs = []
    self.Artisans_Tools_Prof = []
    self.Instrument_Profs = []
    
    self.Vehicle_Profs = []
    self.Game_Profs = []

    self.Weapon_Profs = []
    self.Weapon_Equipped = []
    
    self.Armor_Profs = []
    self.Armor_Equipped = []
    #self.Apperal_Adorned = []
    
    self.Language_Profs = []
    #self.Senses = {
    #  'Precise': {
    #    'Sight': 2000,
    #  },
    #  'Imprecise': {
    #    'Hearing': 70,
    #  },
    #  'Vague': {
    #    'Smell': 20,
    #  }
    #}         
    
    

    self.Saving_Throws = []

    self.Actions = {}
    
    #{

    #}
                    #   'Character_Actions.Cast_Action()' the Cast Action needs to be added via the spellcasting feature
                    
                    # Dice_Rolls.Hide_Action(),         # Not important for Simple Probability Assistant
                    # Dice_Rolls.Dash_Action(),         # Not important for Simple Probability Assistant
                    # Dice_Rolls.Help_Action(),         # Not important for Simple Probability Assistant
                    # Dice_Rolls.Search_Action(),       # Not important for Simple Probability Assistant
                    #Dice_Rolls.Disengage(),
                    #'Improvise',
                    #'Ready an Action',
                    #'Activate an Item',
                    #'Disarm',
                    #'Shove',
                    #'Shove Aside',
                    #'Use an Object',
                    #'Investigate for Illusion',
                    #'Influence'

    self.Reactions = {
                      'Enemy_Leaves_Melee_Range': {},
                      'Enemy_Casts_Spell': {},
                      'Ready_Action': {},

                      'Allied_Ability_Check': {},
                      'Allied_Attack_Roll': {},
                      'Allied_Taking_Damage': {},
                      'Allied_Saving_Throw': {},
                      
                      'Enemy_Attack_Roll': {},
                      'Enemy_Ability_Check': {},
                      'Enemy_Taking_Damage': {},
                      'Enemy_Saving_Throw': {}

    }
  
    self.Bonus_Actions = []
    #{
      #'Independent': {
      
      #},
      #'Character_Actions.Cast_Bonus_Action()'],
      #'Dependent': {
      #  'Attack_Action': {
      
      #  }
        #'Cast_Action': []
        #'Dash_Action': [],
      #}     # eventually I could use a for loop, for each Action that the player_character has and then use something to find the action's location in a list
    #}

    self.Free_Actions = {
      'Dependent': {},
      'Independent': {}
    }
                                  # Free Actions vs Effects
    self.Move_Actions = {
      'Go Prone': 0,
      'Stand Up': 0,
      'Crawl': 0,
      'Jump': 0,

    }
    self.Movement_Spent = 0
    self.Initiative = 0

    self.Effects = {            
        #'Self_Attacking': {
          #'Rolling': {
            #'Archery': []
            #'Great Weapon Fighting': []
            #'Dueling': []
            # },
          #'Hit': {
            # 
          #},
          #'Miss': []
        #},
        #'Self_Being_Attacked': {
          #'Crit': [],
          # 'Hit': [], 
        # },
    

        #'Self_Imposing_Save': [],
        #'Self_Making_Save': {
        #  'Any': [],
        #  'Strength': [],
        #  'Dexterity': [],
        #  'Constitution': [],
        #  'Intelligence': [],
        #  'Wisdom': [],
        #  'Charisma': [],
        #  'Death': []
        #},

        #'Ally_Attacking': {'Hit': [],'Miss': []},

        #'Ally_Being_Attacked': [],
        
        #'Ally_Imposing_Save': [],
        #'Ally_Making_Save': [],

        #'Self_Ability_Check': [],
        #'Ally_Ability_Check': [],
        #'Enemy_Ability_Check': [],

        #'Self_Dealing_Damage': {
        #  'Piercing': [],
        #  'Bludgeoning': [],
        #  'Slashing': [],
        #  'Fire': [],
        #  'Cold': [],
        #  'Lightning': [],
        #  'Thunder': [],
        #  'Poison': [],
        #  'Acid': [],
        #  'Necrotic': [],
        #  'Radiant': [],
        #  'Force': [],
        #  'Psychic': []
        #},
        #'Self_Taking_Damage': {
        #  'piercing': [],
        #  'bludgeoning': [],
        #  'slashing': [],
        #  'fire': [],
        #  'cold': [],
        #  'lightning': [],
        #  'thunder': [],
        #  'poison': [],
        #  'acid': [],
        #  'necrotic': [],
        #  'radiant': [],
        #  'force': [],
        #  'psychic': [],
        #},
        
        #'Ally_Dealing_Damage': [],
        #'Ally_Taking_Damage': [],

        #'Self_Drops_to_Zero': [],
        #'Ally_Drops_to_Zero': [],

        # Self_Social_Conversation
    }

      # There could be effects that are mandatory to apply, such as those based on conditions...
      # There could be effects that are one-time use charges, and thus resource management is needed, such as bardic inspiration

    self.Long_Rest_Options = {
      
    }
    self.Short_Rest_Options = {
      'Unlimited': [Roll_Hit_Dice],
      'Charges': {}
    }

    self.One_Minute_Options = {
      'Unlimited': [],
      'Charges': []
    }
    self.Round_Reset_Options = {
      
    }
    self.Level_Up_Checks = {
      
    }

    self.Active_Conditions = {
      'Self': [],
    }         # should be a dictionary for conditions on self and on certain creatures however I'm unsure how to make that work without a relevant environment 

    self.Circumstances = {
      'Attack Rolls': {},
      'Ability Checks': {},
      'Saving Throws': {},
    }
    '''
        'Next': {
          'Attack Rolls': {
            
          },
          'Ability Checks': {},
          'Saving Throws': {
            'Strength': [],
            'Dexterity': [],
            'Constitutions': [],
            'Intelligence': [],
            'Wisdom': {
              'Frightened': [],
              'Charmed': []},
            'Charisma': [],
            'Death': []}
        },
        'Any': {
          'Attack Rolls': {},
          'Ability Checks': {},
          'Saving Throws': {
            'Strength': [],
            'Dexterity': [],
            'Constitutions': [],
            'Intelligence': [],
            'Wisdom': {
              'Frightened': [],
              'Charmed': []},
            'Charisma': [],
            'Death': []}
        },
        'All': {
          'Attack Rolls': {},
          'Ability Checks': {},
          'Saving Throws': {
            'Strength': [],
            'Dexterity': [],
            'Constitutions': [],
            'Intelligence': [],
            'Wisdom': {
              'Frightened': [],
              'Charmed': []},
            'Charisma': [],
            'Death': []}
        },

    }
  '''

    self.At_Will_Spells = []
    self.Per_Use_Spells = {
      '1/long_rest': {},
      '1/short_rest': {}}
    self.Spellcasting_Known = {}
    self.Spellcasting_Prepared = {}
    # why isn't there a spell slots attribute?
      # because it will go under class resources to separate pact slots from spell slots
      
    self.Class_Resources = {
      'Spell_Slots': {}
      # 'Barbarian': {
      #    ['Rage_Charges']: 
      # }
    }
    self.Class_Save_DCs = {
      # 'Barbarian': {
      #   'Relentless_Rage': 10
      # }
    }


    self.Concentrating = False
    self.Attunement_Slots = 3
    self.Item_Attunements = []
    self.Attunement_Slots_Filled = len(self.Item_Attunements)
    self.WRI = [] # should this be a dictionary so I can identify the source of a WRI so it can be removed if needed?
    self.Adapted_Environment = {
      'Air': 'Infinite',
      'Suffocating': .6 * abilityScoreToModifier(self.Con_Score),
      'Water': 1 + abilityScoreToModifier(self.Con_Score),
    }

    self.Attacks = 1
    self.Usable_Attack_Score = {
      'False': [Str_Score,Dex_Score], # Non-Magical
      'True': [Str_Score,Dex_Score], # Magical
    }
    self.Crit = [20]
    
    self.Location = [0,0,0,0] # last one is the material plane


    self.Inventory = {    # calculate the weight
      'Armor': [],
      'Weapons': [],
      'Treasure': [],

      'Magic Items': {
        'Armor': [],
        'Weapons': [],
        'Other': []
      },
      
      'Vehicles': [],
      'Instruments': [],
      'Tools': [],
      'Artisan_Tools': [],
      'Games': [],

      'Packs': [],
      'Apparel': [],
      'Storage': [],
      'Identifying_Items': [],
      'Currency': [],
      'Other': []
    }

    self.Jump_Height = 3 + abilityScoreToModifier(self.Str_Score)
    self.Jump_Distance = self.Str_Score
    self.Carrying_Capacity = self.Str_Score * 15
    self.Target_List = []
    self.Memory = {   # perhaps I could use the pickle module
      # thinking about how this should be organized...
      # perhaps it could be a dataframe of creatures encountered in order
      # except that Joey said it may be best to be unstructured
      # so perhaps a very long string could be constructed of things that has been encountered
      # What gets recorded in memory?
        # Combat
          # Creatures?
        # Adventure
        # Social
        # Current Situation: the spell that made me think of this was Detect Good and Evil
        # perhaps what I could do is have a list of things that happen in an encounter. 
        # or it could be a dictionary that goes 

        # creatures that have been seen, creatures that have not been seen

        # index is considered the order of events
        'Combat_Encounters': {
          ''
          'Damage Dealt':       [],
          'Damage Type':        [],
          'Damage Healed':      [],
          'Effect Dealt':       [],
          'Effect Used':        [],
          'Effect Removed':     [],
          'Condition Dealt':    [],
          'Condition Removed':  [],
          'Creature Causing':   [],
          'Creature Receiving': []
        },

        'Social_Encounters': {
      
        },

        'Exploration': {
          # perhaps travel and exploration could be stored as vectors
        }
    }
    self.Related_Stat_Blocks = {
      'Familiar': 'None',
      'Steed': 'None',
      'Homonculus': 'None',
      'Companion': 'None',
      'Summons': {},
      'Dominated_Creatures': {},
      'Other': 'None',
    }
    
    self.Alignment = Alignment
    self.Passive_Investigation = 10 + abilityScoreToModifier(self.Int_Score)
    self.Passive_Perception = 10 + abilityScoreToModifier(self.Wis_Score)
    self.Active_Effects = []
    self.Senses = []
    self.Life_Status = 'Alive'

  def Take_Attack(self):
    pass

  def Take_Damage(self,Damage_Type,Damage_Amount,*Tags):
    
    # will need a way to ignore these if statements based on the tags
    if str(Damage_Type) + 'res' in self.WRI:
      Damage_Amount = Damage_Amount / 2
    if str(Damage_Type) + 'vul' in self.WRI:
      Damage_Amount = Damage_Amount * 2
    if str(Damage_Type) + 'immu' in self.WRI:
      Damage_Amount = 0
    
    # need to check for effects that would change the damage taken
    if self.Effects['Self_Taking_Damage'][Damage_Type] != []:
      pass
    


    # first remove Temp_HP
    if self.Temp_HP > 0:
      self.Temp_HP -= Damage_Amount
      if self.Temp_HP < 0:
        Damage_Amount = abs(self.Temp_HP)
        self.Temp_HP = 0
      else:
        return

    # then remove HP
    # if the damage would reduce the player to 0 HP, then the player is downed
    # if the damage would deal more than the player's HP, then the player is dead
    self.Current_HP -= Damage_Amount
    if self.Current_HP <= 0:
      self.Life_Status = 'Down'
      if Damage_Amount > self.HP:
        self.Life_Status = 'Dead'

  def Attack_Check(self, type, magical):
    best_score = max(self.Usable_Attack_Score[magical])
    best_score_ability_modifier = abilityScoreToModifier(best_score)


    if type == 'Melee':

      if self.Circumstances['Attack Rolls']['Melee'] != []:
        pass
      else:
        pass 


  def Spell_Attack(self, target):
    attack_result = 0
    return attack_result

  def Ability_Check(self, Ability, DC):
    if Ability == "Strength":
      ability_bonus = abilityScoreToModifier(self.Str_Score)

    elif Ability == "Dexterity":
      ability_bonus = abilityScoreToModifier(self.Dex_Score)

    elif Ability == "Constitution":
      ability_bonus = abilityScoreToModifier(self.Con_Score)

    elif Ability == "Intelligence":
      ability_bonus = abilityScoreToModifier(self.Int_Score)

    elif Ability == "Wisdom":
      ability_bonus = abilityScoreToModifier(self.Wis_Score)

    elif Ability == "Charisma":
      ability_bonus = abilityScoreToModifier(self.Cha_Score)

    # check for any advantage or disadvantage
    # self.Circumstances['Ability Checks'][Ability]


  def Skill_Check(self, Ability, Skill, DC):
    pass

  def Saving_Throw(self, Ability, DC):
    pass

  def Reset_Round(self):
    pass

  def Long_Rest(self):
    pass

  def Choose_Target_Offense(self):
    pass




class Monster:
  def __init__(self,Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spellcasting_Prepared,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Long_Rest_Options,Short_Rest_Options,Resources,Speeds,Languages,Features,WRI,Spawn_Inventory):
    self.Monster_ID = Monster_ID
    self.Name = Name
    self.Book = Book
    self.HP = HP
    self.AC = AC
    self.Type = Type
    self.Size = Size
    self.CR = CR
    self.XP = XP
    self.Prof_Bonus = Prof_Bonus
    self.Saving_Throws = []
    self.Skill_Profs = []
    self.Str_Score = Str_Score
    self.Dex_Score = Dex_Score
    self.Con_Score = Con_Score
    self.Int_Score = Int_Score
    self.Wis_Score = Wis_Score
    self.Cha_Score = Cha_Score
    self.Actions = {}
    self.Reactions = {}
    self.Bonus_Actions = {}
    self.Free_Actions = {}
    self.Effects = {}


    self.At_Will_Spells = {}
    self.Per_Use_Spells = {
      '1/long_rest': {},
      '2/long_rest': {},
      '3/long_rest': {}
    }
    self.Spellcasting_Known = {}
    self.Spellcasting_Prepared = {}
    
    
    self.Spell_Save_DC = Spell_Save_DC
    self.Attunement_Slots = 3
    self.Attunement_Slots_Filled = 0

    self.Long_Rest_Options = {
      
    }
    self.Short_Rest_Options = {
      'Unlimited': [Roll_Hit_Dice],
      'Charges': {}
    }
    self.Resources = {}
    self.Speed = {
        'Walking': 30,
        'Flying': 0,
        'Swimming': 0,
        'Burrowing': 0,
        'Climbing': 0,
        'Flyhover': 0
    }

    self.Languages = []
    self.Features = []
    self.WRI = WRI
    self.Circumstances = {
        'Attack Rolls': False,
        'Ability Checks': False,
        'Saving Throws': False
    }
    self.Senses = []
    self.Spawn_Inventory = Spawn_Inventory
    #{
    #  'Magic Items': [],
    #  'Armor': [],
    #  'Weapons': []
    #}

class Monster_Instance(Monster):
  #Monster_ID,Name,HP,AC,Type,Size,CR,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Active_Conditions
  def __init__(self,Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Spawn_Inventory,Instance,Monster_Instance_ID,Current_HP,Location,Active_Conditions,Life_Status,Inventory,Concentrating):
    super().__init__(Monster_ID,Name,Book,HP,AC,Type,Size,CR,XP,Prof_Bonus,Saving_Throws,Skill_Profs,Str_Score,Dex_Score,Con_Score,Int_Score,Wis_Score,Cha_Score,Effects,Spells_Known,Spell_Save_DC,Attunement_Slots,Attunement_Slots_Filled,Languages,Features,WRI,Spawn_Inventory)
    self.Instance = Instance
    self.Monster_Instance_ID = Monster_Instance_ID
    self.Current_HP = Current_HP
    self.Temp_HP = 0
    self.Location = () 
    self.Active_Conditions = {

    }
    self.Life_Status = 'Alive'        #Life status can be either Alive, Stable, Down, or Dead
    self.Memory = {}
    self.Inventory = {}
    self.Concentrating = False

  #def Get_Environmental_Circumstances(self,World):
  #  self.Circumstances = {}
  #  for World.Creature in World:
      

# Only Monster_Instances and Sentient_Objects can learn and remember things, while all Player_Characters can
  # although this does bring up the concept of sentient object instances
  # and the concept of knowledge and experience being associated with a player_characters level

# How do I want memory to work???
# Should a creature remember every time it gets hit? every action that a creature can take?
# Or should the amount of data that is stored be proportional to the creature's intelligence?




