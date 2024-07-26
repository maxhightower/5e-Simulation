# barbarian class
import Establishing_Hierarchy
import numpy as np
import random
import Dice_Rolls

class Barbarian(Establishing_Hierarchy.Character_Class):
    def __init__(self):
        super().__init__()
        self.name = 'Barbarian'
        self.hit_dice = 12
        self.saving_throws = ["Strength", "Constitution"]
        self.starting_skill_number = 2
        self.starting_skill_list = ['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']
        self.armor_proficiencies = ["Light Armor", "Medium Armor", "Shields"]
        self.weapon_proficiencies = ["Simple Weapons", "Martial Weapons"]
        self.spellcasting_ability = None

        self.starting_equipment = {} 

    def give_starting_equipment(self, character):
        for item in self.starting_equipment:
            character.inventory.append(item)
    
    def first_level_barbarian(self, character):
        character.first_class = self
        character.saving_throws.append("Strength")
        character.saving_throws.append("Constitution")

        # need one last thing for hit dice

    def give_rage_feature(self, character):
        
        def end_rage(self, character):
            character.rage = False

            character.WRI.remove('piercingres')
            character.WRI.remove('bludgres')
            character.WRI.remove('slashingres')
            
            def begin_rage(self, character):
                character.rage = True

                character.Effects['Attack Damage']['Melee']['Strength']['rage_damage'] = 2
                # need to calc the damage bonus for the character based on level eventually...


                character.Circumstances['Ability Checks']['Strength']['rage'] = 'ADV'
                character.Circumstances['Saving Throws']['Strength']['rage'] = 'ADV'

                effects_removed = []
                actions_removed = []
                bonus_actions_removed = []
                # I need to remove the ability to spellcast
                # could I use tags to determine what needs to be removed somehow?


                character.WRI.append('piercingres')
                character.WRI.append('bludgres')
                character.WRI.append('slashingres')


                character.rage_rounds_remaining = 10
                character.rage_persists = False
                # need to check if the character has taken damage this round or has attacked a hostile creature
                def check_rage_effect(event):
                    if event == 'round_end' or event == 'damage' or event == 'attack':
                        character.rage_persists = True
                    # I also need to check if they aren't wearing heavy armor...
                    # and if they get knocked unconscious 
                
                character.bonus_actions['End Rage'] = end_rage()

            character.bonus_actions['Rage'] = self.begin_rage()

        character.bonus_actions['Rage'] = self.begin_rage()

    def give_unarmored_defense(self, character):
        #character.AC = 10 + character.ability_scores['Dexterity'] + character.ability_scores['Constitution']
        character.armor_class_formulas['Barbarian Unarmored Defense'] = 10 + character.dex_score + character.con_score

    def give_danger_sense(self, character):
        
        # need a check to see if the character is surprised, blinded, deafened, or incapacitated
        def danger_sense_effect(event):
            if event == 'dexterity saving_throw':
                if 'surprised' in character.conditions or 'blinded' in character.conditions or 'deafened' in character.conditions or 'incapacitated' in character.conditions:
                    character.Circumstances['Saving Throws']['Dexterity']['danger_sense'] = None
                else:
                    character.Circumstances['Saving Throws']['Dexterity']['danger_sense'] = 'ADV'

    def give_reckless_attack(self, character):
        
        character.Circumstances['Attack Rolls']['Melee']['Strength']['reckless_attack'] = 'ADV'

    def give_fast_movement(self, character):

        def fast_movement_effect(event):
            if event == 'round_start' and character.armor_equipped not in ['Heavy Armor']:
                for speed_type in character.speed:
                    if character.speed[speed_type] > 10: # because it's not giving new speed types, simply increasing those that already exist
                        character.speed[speed_type] += 10
            if event == 'round_end':
                for speed_type in character.speed:
                    if character.speed[speed_type] > 10:
                        character.speed[speed_type] -= 10

    def give_feral_instinct(self, character):
        character.Circumstances['Initiative']['feral_instinct'] = 'ADV'

        def feral_instinct_effect(observer):
            if event == 'round_start' and 'surprised' in character.conditions:
                character.conditions.remove('surprised')
                # have to set rage as the first action...

    def give_instinctive_pounce(self, character):
        pass
        # just redo the rage bonus action but give it movement as well

    def give_brutal_critical(self, character):
        # what if instead, Attacks had tags...and instead of storing effects in a dictionary that would get looped through, 
        # the events would get looped through if they applied or not... 

        character.Effects['Attack Damage']['Melee']['Crit'] = 1
