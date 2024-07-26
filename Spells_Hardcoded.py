# spells hardcoded
import random
import Dice_Rolls
import Establishing_Hierarchy
from Establishing_Hierarchy import GameEvent
from functools import partial

# what if there was a queue system 
# option-based spells need an argument to store the lists that represent the agents choice 
# there needs to be a main game loop that is checked every round to see if the agent has made a choice
# and some spells need to be able to add segments to that check

# how will spells be added to an entity? how will their sub-actions? 

class Spell:
    def __init__(self, name: str, level: int, school: str, func):
        self.name = name
        self.level = level
        self.school = school
        self.func = func
        self.subaction = None

        def learn_spell(self, character, source):
            if self in character.spellcasting_known:
                print(f"{character.name} already knows {self.name}")
                return
            character.spellcasting_known[self] = partial(self.func, source=source)

        def prepare_spell(self, character, source):
            if self in character.spellcasting_prepared:
                print(f"{character.name} already knows {self.name}")
                return
            else:
                character.spellcasting_prepared[self] = partial(self.func, source=source)



        def remove_spell(self, character, source):        
            if self in character.spellcasting_prepared:
                del character.spellcasting_prepared[self]
            else:
                print(f"{character.name} does not have {self.name} prepared")



## Cantrips
# Acid Splash

def cast_acid_splash(caster, target):
    caster.notify(GameEvent('Verbal Component'))
    caster.notify(GameEvent('Somatic Component'))


    # first choose a target within 60 feet of caster
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location

    targetable_locations = []
    for dx in range(-11, 12):
        for dy in range(-11, 12):
            x = agent_location[0] + dx
            y = agent_location[1] + dy


    # remove locations without creatures in them
    for location in targetable_locations:
        if locations[location[0], location[1]][3] == 0:
            targetable_locations.remove(location)
    
    targets_list = []

    # choose a random space within the targetable_locations list
    target_location = random.choice(targetable_locations)

    # what if I included an optional kwarg "target"...

    Save_DC = 8 + caster.Proficiency + caster.Spellcasting_Mod

    # identify the target creature in the world
    creatures_in_world = caster.world.Creatures
    target_creature = None
    for creature in creatures_in_world:
        if creature.Location == target_location:
            target_creature = creature
            break
    
    if target_creature == None:
        return
    
    targets_list += [target_creature]

    # if there's a creature adjacent to the target, add that creature to the targets_list
    adjacent_locations = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = target_location[0] + dx
            y = target_location[1] + dy

            if (0 <= x < rows) and (0 <= y < cols) and (dx != 0 or dy != 0):
                adjacent_locations.append([x, y])
    
    for location in adjacent_locations:
        for creature in creatures_in_world:
            if creature.Location == location:
                targets_list += [creature]
                break

    for target in targets_list:
        # make the saving throw
        Saving_Throw_Result = target.Saving_Throw('Dexterity', Save_DC)

        if Saving_Throw_Result == 'Fail':
            damage_dice = 6

            if caster.Level >= 5:
                dice_number = 2
            elif caster.Level >= 11:
                dice_number = 3
            elif caster.Level >= 18:
                dice_number = 4
            else:
                dice_number = 1
        
            damage = 0
            for i in range(dice_number):
                damage += random.randint(1, damage_dice)

                caster.notify(GameEvent('Dealing Damage', {'damage': damage, 'target': target, 'damage_type': 'Acid', 'source': 'spell'}))

        elif Saving_Throw_Result == 'Success':
            damage = 0
            return

        target.take_damage(damage, 'Acid')

acid_splash = Spell('Acid Splash', 0, 'Conjuration', cast_acid_splash())


# Blade Ward
def Blade_Ward(caster):
    caster.notify(GameEvent('Verbal Component'))
    caster.notify(GameEvent('Somatic Component'))
    
    active = True
    duration = 1

    def blade_ward_effect(event):
        nonlocal active, duration

        if not active:
            return

        if event.type == "character_taking_damage" and event.data["character"] == caster and event.data["damage_type"] in ["slashing", "piercing", "bludgeoning"] and event.data["source"] == "weapon":
            print(f"{caster.name} takes reduced damage from {event.data['source']}!")
            event.data["damage"] = event.data["damage"] // 2

        elif event.type == "turn_end" and event.data["character"] == caster:
            duration -= 1
            if duration <= 0:
                active = False
                print(f"Blade Ward on {caster.name} has ended.")

        print(f"{caster.name} casts Blade Ward!")

# Booming Blade
def Booming_Blade(caster, target):
    melee_weapon = caster.Weapon_Equipped
    weapon_damage_dice = melee_weapon.Damage_Dice
    weapon_dice_number = melee_weapon.Dice_Number

    # first choose a target within 5 feet of caster
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location

    targetable_locations = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = agent_location[0] + dx
            y = agent_location[1] + dy

            # Check if the location is within bounds and is not the agent's location itself
            if (0 <= x < rows) and (0 <= y < cols) and (dx != 0 or dy != 0):
                targetable_locations.append([x, y])

    # remove locations without creatures in them
    for location in targetable_locations:
        if locations[location[0], location[1]][3] == 0:
            targetable_locations.remove(location)
    
    # choose a random space within the targetable_locations list
    target_location = random.choice(targetable_locations)


    # identify the target creature in the world
    creatures_in_world = caster.world.Creatures
    target_creature = None
    for creature in creatures_in_world:
        if creature.Location == target_location:
            target_creature = creature
            break
    
    if target_creature == None:
        return
    
    spell_damage_dice = 8

    if caster.Level >= 5:
        spell_melee_dice_number = 1
        spell_movement_dice_number = 2
    elif caster.Level >= 11:
        spell_melee_dice_number = 2
        spell_movement_dice_number = 3
    elif caster.Level >= 17:
        spell_melee_dice_number = 3
        spell_movement_dice_number = 4
    else:
        spell_melee_dice_number = 0
        spell_movement_dice_number = 1

    # make melee attack

    # need to create an 

    def cast_booming_blade(game, caster, target):
        active = True
        duration = 1

        def booming_blade_effect(event):
            nonlocal active, duration

            if not active:
                return

            if event.type == "character_moved" and event.data["character"] == target:
                print(f"Booming Blade triggered on {target.name}!")
                damage = random.randint(1, 8)  # 1d8 thunder damage
                target.take_damage(damage)
                active = False

            elif event.type == "turn_start" and event.data["character"] == caster:
                duration -= 1
                if duration <= 0:
                    active = False
                    print(f"Booming Blade on {target.name} has ended.")


        # Simulate the initial melee attack
        print(f"{caster.name} casts Booming Blade on {target.name}!")
        
        hit = caster.attack_roll(target)

        if hit:
            melee_weapon = caster.Weapon_Equipped
            weapon_damage_dice = melee_weapon.Damage_Dice
            weapon_dice_number = melee_weapon.Dice_Number        
            
            damage = 0
            for i in range(weapon_dice_number):
                damage += random.randint(1, weapon_damage_dice)

            target.take_damage(damage)
            print(f"Booming energy surrounds {target.name}.")
            game.attach(booming_blade_effect)
        else:
            print("The attack misses!")

        return booming_blade_effect

# Chill Touch
def Chill_Touch(caster, target):
    caster.notify(GameEvent('Verbal Component'))
    caster.notify(GameEvent('Somatic Component'))

    damage_dice = 8

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1

    damage = 0
    for i in range(dice_number):
        damage += random.randint(1, damage_dice)
    
    def cannot_heal_effect(event):
        if event.type == "character_healing" and event.data["character"] == target:
            print(f"{target.name} cannot regain hit points!")
            event.data["amount"] = 0
    
    print(f"{caster.name} casts Chill Touch on {target.name}!")

    attack_results = caster.Spell_Attack(target)
    if attack_results == 'Hit':
        target.take_damage(damage)
        target.attach(cannot_heal_effect)
    else:
        print("The spell attack misses!")



# Control Flames
def Control_Flames(caster):
    caster.notify(GameEvent('Somatic Component'))

    # find fire within 60 feet
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location

    targetable_locations = []
    for dx in range(-11, 12):
        for dy in range(-11, 12):
            x = agent_location[0] + dx
            y = agent_location[1] + dy

            # Check if the location is within bounds and is not the agent's location itself
            if (0 <= x < rows) and (0 <= y < cols) and (dx != 0 or dy != 0):
                targetable_locations.append([x, y])
    
    # remove targetable_locations that are not on fire
    for location in targetable_locations:
        if locations[location[0], location[1]][1] != 2:
            targetable_locations.remove(location)
    
    # choose a random space within the targetable_locations list
    target_location = random.choice(targetable_locations)

    # options for Control Flames
    # 1. set fire to adjacent space
    # 2. extinguish fire
    # will need to add a way to double or halve the light level from a source later

    options = [0,1] # 0 = set fire, 1 = extinguish fire
    choice = random.choice(options)

    if choice == 0:
        # choose a space adjacent to target_location
        adjacent_locations = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = target_location[0] + dx
                y = target_location[1] + dy

                # Check if the location is within bounds and is not the target_location itself
                if (0 <= x < rows) and (0 <= y < cols) and (dx != 0 or dy != 0):
                    adjacent_locations.append([x, y])

        # remove adjacent_locations that are not on the ground
        for location in adjacent_locations:
            if locations[location[0], location[1]][2] != 1:
                adjacent_locations.remove(location)

        # choose a random space within the adjacent_locations list
        new_location = random.choice(adjacent_locations)
        new_location[1] = 2 # set fire

    elif choice == 1:
        target_location[1] = 0 # set air (extinguish fire)

# Create Bonfire
def Create_Bonfire(caster):
    # should create bonfire be used as targeting the environment or creatures?
    caster.notify(GameEvent('Verbal Component'))
    caster.notify(GameEvent('Somatic Component'))


    caster.Concentrating = True

    # choose a space within 60 feet of caster
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location

    targetable_locations = []
    for dx in range(-11, 12):
        for dy in range(-11, 12):
            x = agent_location[0] + dx
            y = agent_location[1] + dy

            # Check if the location is within bounds and is not the agent's location itself
            if (0 <= x < rows) and (0 <= y < cols) and (dx != 0 or dy != 0):
                targetable_locations.append([x, y])

    # need to narrow down locations on the ground
    for location in targetable_locations:
        if locations[location[0], location[1]][2] == 0:
            targetable_locations.remove(location)

    # need to narrow down locations to those that can be seen by the caster
    if 'devilsight' not in caster.senses:
        for location in targetable_locations:
            if locations[location[0], location[1]][6] == 3:
                targetable_locations.remove(location)
    if 'darkvision' not in caster.senses:
        for location in targetable_locations:
            if locations[location[0], location[1]][6] == 2:
                targetable_locations.remove(location)

    # choose a random space within the spaces_within_movement list
    target_location = random.choice(targetable_locations)

    # create a bonfire in that location
    caster.world.Grid[target_location[0], target_location[1]][1] = 2 # fire



    damage_dice = 8

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1

    damage = 0
    for i in range(dice_number):
        damage += random.randint(1, damage_dice)
    
# Dancing Lights
def Dancing_Lights(caster):
    caster.notify(GameEvent('Verbal Component'))
    caster.notify(GameEvent('Somatic Component'))
    caster.notify(GameEvent('Material Component'))

    caster.Concentrating = True
    # choose 4 spaces within environment within 120 feet of caster
    x, y, z, d = caster.Location

    # each space must be within 20 feet of another space
    # shed Bright Light in a 10-foot radius

    # add Bonus Action to move the lights up to 60 feet to a new spot

    

# Druidcraft
def Druidcraft(caster):
    # options
    # 0 - illusory effect
    # 1 - light a light source
    # 2 - extinguish a light source

    options = [0,1,2]
    choice = random.choice(options)

    if choice == 0:
        # choose a location with 30 feet of caster
        locations = caster.world.Grid
        rows, cols = locations.shape
        agent_location = caster.Location

        targetable_locations = []
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                x = agent_location[0] + dx
                y = agent_location[1] + dy

                # Check if the location is within bounds and is not the agent's location itself
                if (0 <= x < rows) and (0 <= y < cols) and (dx != 0 or dy != 0):
                    targetable_locations.append([x, y])
        
        # choose a random space within the targetable_locations list
        target_location = random.choice(targetable_locations)

        # choose the type of illusion
        # 0 - wind
        # 1 - sound
        # 2 - odor

        illusion_options = [0,1,2]
        illusion_choice = random.choice(illusion_options)

        # need the illusion to only last a round and reset after
        if illusion_choice == 0: # wind
            locations[target_location[0], target_location[1]][12] = 1 # light wind
            locations[target_location[0], target_location[1]][11] = 1 # illusion boolean
        elif illusion_choice == 1: # sound
            locations[target_location[0], target_location[1]][8] = 1 # normal sound
            locations[target_location[0], target_location[1]][11] = 1 # illusion boolean
        elif illusion_choice == 2: # odor
            locations[target_location[0], target_location[1]][9] = 1 # light odor
            locations[target_location[0], target_location[1]][11] = 1 # illusion boolean

    elif choice == 1: # light a light source
        pass
        # this could play out in a couple ways: 
        # 1. a torch, lantern, or candle being held gets lit
        # 2. a candle or lantern within 30 feet gets lit

    elif choice == 2: # extinguish a light source
        pass

# Eldritch Blast
def Eldritch_Blast(caster, target):
    # this one may be tricky
    # this spell can choose multiple targets with multiple attacks...


    damage_dice = 10

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1

    
    

# Encode Thoughts - not to be implemented
def Encode_Thoughts(caster):
    pass

# Fire Bolt
def Fire_Bolt(caster, target):
    damage_dice = 10

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1

    damage = 0
    for i in range(dice_number):
        damage += random.randint(1, damage_dice)

    # make the spell check


    target.Take_Damage(damage, 'fire')

# Friends
def Friends(caster, target):
    pass

# Frostbite
def Frostbite(caster, target):
    pass

# Green-Flame Blade
def Green_Flame_Blade(caster, target):
    pass

# Guidance
def Guidance(caster, target):
    pass

# Gust
def Gust(caster, option, *tags):

    # 1. Push Creature
    target = tags[0]

    # 2. Move Object
    # need a way to represent objects within the environment

    # 3. Sensory Effect

    pass

# Infestation
def Infestation(caster):
    pass

# Light
def Light(caster):
    pass

# Lightning Lure
def Lightning_Lure(caster, target):
    pass

# Mage Hand
def Mage_Hand(caster):
    pass

# Magic Stone
# Mending
# Message
# Mind Sliver
def Mind_Sliver(caster):
    pass

# Minor Illusion
def Minor_Illusion(caster):
    pass

# Mold Earth
def Mold_Earth(caster):
    pass

# Poison Spray
def Poison_Spray(caster):
    pass

# Prestidigitation
# Primal Savagery
def Primal_Savagery(caster, target):
    pass

# Produce Flame
def Produce_Flame(caster):
    caster.Active_Effect += 'Produce Flame'

# Ray of Frost
def Ray_of_Frost(caster, target):


    damage_dice = 8

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1

    damage = 0
    for i in range(dice_number):
        damage += random.randint(1, damage_dice)

    # make the spell check
    attack_result = caster.Spell_Attack(target)


    target.Movement_Spent += 10
    target.Take_Damage(damage, 'cold')

# Resistance
def Resistance(caster):
    pass

# Sacred Flame
def Sacred_Flame(caster):
    pass

# Shape Water
def Shape_Water(caster):
    pass

# Shillelagh
# Shocking Grasp
def Shocking_Grasp(caster):
    damage_dice = 8

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1
    
    damage = 0
    for i in range(dice_number):
        damage += random.randint(1, damage_dice)
    
    # make the spell check

    # remove the target's reaction

# Spare the Dying
def Spare_the_Dying(target):
    if target.Life_Status == 'Down':
        target.Life_Status = 'Stable'

# Sword Burst
def Sword_Burst(caster):
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location

    # need all the spaces around the caster
    adjacent_spaces = []

# Thaumaturgy
def Thaumaturgy(caster):
    pass

# Thorn Whip
def Thorn_Whip(caster, target):
    pass

# Thunderclap
def Thunderclap(caster):
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location

    # need all the spaces around the caster
    adjacent_spaces = []

# Toll the Dead
def Toll_The_Dead(caster):
    pass

# True Strike
def True_Strike(caster):
    pass

# Vicious Mockery
def Vicious_Mockery(caster, target):
    damage_dice = 4

    if caster.Level >= 5:
        dice_number = 2
    elif caster.Level >= 11:
        dice_number = 3
    elif caster.Level >= 17:
        dice_number = 4
    else:
        dice_number = 1
    
    damage = 0
    for i in range(dice_number):
        damage += random.randint(1, damage_dice)
    
# Word of Radiance
def Word_of_Radiance(caster):
    locations = caster.world.Grid
    rows, cols = locations.shape
    agent_location = caster.Location


## 1st Level
# Absorb Elements
def Absorb_Elements(caster):
    pass

# Alarm
# Animal Friendship
def Animal_Friendship(caster, target):
    pass

# Armor of Agathys
def Armor_of_Agathys(caster, spell_level):
    # 1 hour 
    temp_hp = 5 * spell_level
    caster.temp_hp += temp_hp
    
    # need to add to the main loop that temp_hp is removed after 1 hour
    # need to add something that checks which creature removes the temp_hp and to deal damage to that creature
    caster.active_effects += ['Armor of Agathys']


# Arms of Hadar
# Bane
# Beast Bond
# Bless
# Burning Hands
# Catapult
# Cause Fear
# Ceremony
# Chaos Bolt
# Charm Person
# Chromatic Orb
# Color Spray
# Command
# Compelled Duel
# Comprehend Languages
# Create or Destroy Water
# Cure Wounds
# Detect Evil and Good
# Detect Magic
# Detect Poison and Disease
# Disguise Self
# Dissonant Whispers
# Divine Favor
# Earth Tremor
# Ensnaring Strike
# Entangle
# Expeditious Retreat
# Faerie Fire
# False Life
# Feather Fall
# Find Familiar
# Fog Cloud
# Goodberry
# Grease
# Guiding Bolt
# Hail of Thorns
# Healing Word
# Hellish Rebuke
# Heroism
# Hex
# Hunter's Mark
# Ice Knife
# Identify
# Illusory Script
# Inflict Wounds
# Jump
# Longstrider
# Mage Armor
# Magic Missile
# Protection from Evil and Good
# Purify Food and Drink
# Ray of Sickness
# Sanctuary
# Searing Smite
# Shield
# Shield of Faith
# Silent Image
# Sleep
# Snare
# Speak with Animals
# Tasha's Hideous Laughter
# Tenser's Floating Disk
# Thunderous Smite
# Thunderwave
# Unseen Servant
# Witch Bolt
# Wrathful Smite
# Zephyr Strike


## 2nd Level
# Aid
# Alter Self
# Animal Messenger
# Arcane Lock
# Augury
# Barkskin
# Beast Sense
# Blindness/Deafness
# Blur
# Borrowed Knowledge
# Branding Smite
# Calm Emotions
# Cloud of Daggers
# Continual Flame
# Cordon of Arrows
# Crown of Madness
# Darkness
# Darkvision
# Detect Thoughts
# Dragon's Breath
# Dust Devil
# Earthbind
# Enhance Ability
# Enlarge/Reduce
# Enthrall
# Find Steed
# Find Traps
# Flame Blade
# Flaming Sphere
# Gentle Repose
# Gift of Gab
# Gust of Wind
# Healing Spirit
# Heat Metal
# Hold Person
# Invisibility
# Knock
# Lesser Restoration
# Levitate
# Locate Animals or Plants
# Locate Object
# Magic Mouth
# Magic Weapon
# Maximilian's Earthen Grasp
# Melf's Acid Arrow
# Mind Spike
# Mirror Image
# Misty Step
# Moonbeam
# Nystul's Magic Aura
# Pass without Trace
# Phantasmal Force
# Prayer of Healing
# Protection from Poison
# Pyrotechnics
# Ray of Enfeeblement
# Rope Trick
# Scorching Ray
# See Invisibility
# Shadow Blade
# Shatter
# Silence
# Skywrite
# Snilloc's Snowball Swarm
# Spider Climb
# Spiritual Weapon
# Suggestion
# Summon Beast
# Tasha's Mind Whip
# Tasha's Caustic Brew
# Warding Wind
# Web
# Zone of Truth


## 3rd Level
'''
Animate Dead
Aura of Vitality
Beacon of Hope
Bestow Curse
Blink
Catnap
Clairvoyance
Counterspell
Create Food and Water
Crusader's Mantle
Daylight
Dispel Magic
Elemental Weapon
Enemies Abound
Erupting Earth
Fast Friends
Fear
Feign Death
Fireball
Flame Arrows
Fly
Gaseous Form
Glyph of Warding
Haste
Hypnotic Pattern
Leomund's Tiny Hut
Life Transference
Lightning Arrow
Lightning Bolt
Magic Circle
Major Image
Mass Healing Word
Meld into Stone
Melf's Minute Meteors
Nondetection
Phantom Steed
Plant Growth
Protection from Energy
Remove Curse
Revivify
Sending
Sleet Storm
Slow
Spirit Guardians
Stinking Cloud
Summon Lesser Demons
Summon Fey
Summon Undead
Thunder Step
Tidal Wave
Tiny Servant
Tongues
Vampiric Touch
Wall of Sand
Wall of Water
Water Breathing
Water Walk
Wind Wall
'''

## 4th Level
'''
Arcane Eye
Aura of Life
Aura of Purity
Banishment
Blight
Charm Monster
Compulsion
Confusion
Conjure Minor Elementals
Conjure Woodland Beings
Control Water
Death Ward
Dimension Door
Divination
Dominate Beast
Elemental Bane
Evard's Black Tentacles
Fabricate
Faithful Hound
Find Greater Steed
Fire Shield
Freedom of Movement
Giant Insect
Greater Invisibility
Guardian of Faith
Hallucinatory Terrain
Ice Storm
Leomund's Secret Chest
Locate Creature
Mordenkainen's Faithful Hound
Mordenkainen's Private Sanctum
Otiluke's Resilient Sphere
Phantasmal Killer
Polymorph
Shadow of Moil
Sickening Radiance
Stone Shape
Stoneskin
Storm Sphere
Summon Construct
Summon Elemental
Vitriolic Sphere
Wall of Fire
Watery Sphere
'''

## 5th Level
'''
Animate Objects
Antilife Shell
Awaken
Banishing Smite
Bigby's Hand
Circle of Power
Cloudkill
Commune
Commune with Nature
Cone of Cold
Conjure Elemental
Conjure Volley
Contagion
Control Winds
Creation
Dawn
Destructive Wave
Dispel Evil and Good
Dominate Person
Dream
Enervation
Far Step
Flame Strike
Geas
Greater Restoration
Hallow
Hold Monster
Holy Weapon
Immolation
Infernal Calling
Legend Lore
Mass Cure Wounds
Mislead
Modify Memory
Negative Energy Flood
Passwall
Planar Binding
Rary's Telepathic Bond
Raise Dead
Reincarnate
Scrying
Seeming
Skill Empowerment
Steel Wind Strike
Swift Quiver
Synaptic Static
Telekinesis
Telepathic Bond
Teleportation Circle
Tree Stride
Wall of Force
Wall of Light
Wall of Stone
Wrath of Nature
'''

## 6th Level
'''
Arcane Gate
Blade Barrier
Bones of the Earth
Chain Lightning
Circle of Death
Conjure Fey
Contingency
Create Homunculus
Create Undead
Disintegrate
Drawmij's Instant Summons
Druid Grove
Eyebite
Find the Path
Flesh to Stone
Forbiddance
Globe of Invulnerability
Guards and Wards
Harm
Heal
Heroes' Feast
Investiture of Flame
Investiture of Ice
Investiture of Stone
Investiture of Wind
Magic Jar
Mass Suggestion
Mental Prison
Move Earth
Otiluke's Freezing Sphere
Otto's Irresistible Dance
Planar Ally
Primordial Ward
Programmed Illusion
Scatter
Soul Cage
Summon Fiend
Sunbeam
Tenser's Transformation
Transport via Plants
True Seeing
Wall of Ice
Wind Walk
Word of Recall
'''

## 7th Level
'''
Conjure Celestial
Crown of Stars
Delayed Blast Fireball
Divine Word
Etherealness
Finger of Death
Fire Storm
Forcecage
Mirage Arcane
Mordenkainen's Magnificent Mansion
Mordenkainen's Sword
Plane Shift
Power Word Pain
Prismatic Spray
Project Image
Regenerate
Resurrection
Reverse Gravity
Sequester
Simulacrum
Symbol
Teleport
Temple of the Gods
Tether Essence
Whirlwind
'''

## 8th Level
'''
Abi-Dalzim's Horrid Wilting
Animal Shapes
Antimagic Field
Antipathy/Sympathy
Clone
Control Weather
Dark Star
Demiplane
Dominate Monster
Earthquake
Feeblemind
Glibness
Holy Aura
Incendiary Cloud
Maddening Darkness
Maze
Mind Blank
Power Word Stun
Sunburst
Telepathy
Tsunami
'''

## 9th Level
'''
Astral Projection
Foresight
Gate
Imprisonment
Invulnerability
Mass Heal
Meteor Swarm
Power Word Heal
Power Word Kill
Prismatic Wall
Psychic Scream
Ravenous Void
Shapechange
Storm of Vengeance
Time Ravage
Time Stop
True Polymorph
True Resurrection
Weird
Wish
'''
