
class Species:
  def __init__(self,Book,Creature_Type,Species_Sizes,Species_Senses,Species_Bonuses,Movement_Speeds,Species_Circumstances,Species_Language_Prof,Species_Skill_Profs,Species_Weapon_Profs,Species_Tool_Profs,Species_Artisan_Tool_Profs,Species_Actions,Species_Bonus_Actions,Species_WRI,Species_Feat):
    self.Book = Book
    self.Creature_Type = Creature_Type    # Humanoid, Ooze, Monstrosity, etc
    self.Species_Sizes = Species_Sizes    # = ['Medium','Small']
    self.Species_Bonuses = Species_Bonuses  # = [STR:2,DEX:3] and then a function like string.split() apply bonuses...
    self.Species_Senses = Species_Senses
    self.Movement_Speeds = Movement_Speeds
    self.Species_Circumstances = Species_Circumstances
    self.Species_Language_Prof = Species_Language_Prof
    self.Species_Skill_Profs = Species_Skill_Profs
    self.Species_Weapon_Profs = Species_Weapon_Profs
    self.Species_Tool_Profs = Species_Tool_Profs
    self.Species_Artisan_Tool_Profs = Species_Artisan_Tool_Profs
    self.Species_Actions = Species_Actions
    self.Species_Bonus_Actions = Species_Bonus_Actions
    self.Species_WRI = Species_WRI
    self.Species_Feat = Species_Feat

    # what about trance, unusual nature, amorphous form, and other abnormal traits?
    # Should they all be booleans or should I use a list at a certain point?
    # and what about the "counts as" sections from MPMM???

    def Apply_Species(Player_Character):
      pass

class Subspecies(Species):
  def __init__(self,Book,Subspecies_Bonus,Subspecies_WRI,Skill_Profs,Weapon_Profs,Armor_Profs,at_Will_Spells,per_Use_Spells,Subspecies_Language_Profs,Subspecies_Actions,Subspecies_Bonus_Actions):
    self.Book = Book
    self.Subspecies_Bonus = Subspecies_Bonus
    self.Subspecies_WRI = Subspecies_WRI
    self.Skill_Profs = Skill_Profs
    self.Weapon_Profs = Weapon_Profs
    self.Armor_Profs = Armor_Profs
    self.at_Will_Spells = at_Will_Spells
    self.per_Use_Spells = per_Use_Spells
    self.Subspecies_Language_Profs = Subspecies_Language_Profs
    self.Subspecies_Actions = Subspecies_Actions
    self.Subspecies_Bonus_Actions = Subspecies_Bonus_Actions

    def Apply_Subspecies(Player_Character):
      pass



def Apply_Species(Species,Player_Character):
    # (Book: Any, Creature_Type: Any, Species_Sizes: Any, Species_Senses: Any, Species_Bonuses: Any, Movement_Speeds: Any, 
    # Species_Circumstances: Any, Species_Language_Prof: Any, Species_Skill_Profs: Any, Species_Weapon_Profs: Any, 
    # Species_Tool_Profs: Any, Species_Artisan_Tool_Profs: Any, Species_Actions: Any, Species_Bonus_Actions: Any, 
    # Species_WRI: Any, Species_Feat: Any)

    Player_Character.Size = Species.Species_Sizes[0]
    #Player_Character.Speeds['Walking'] = Species.Movement_Speed
    #Player_Character.Senses
    
    #Player_Character.Language_Profs.append(Species.Language_Profs)
    # need a function to choose a random language if there's a 1 or a 2
    #    Player_Character.Language_Profs.append(Species.Language_Profs)

    #Player_Character.Skill_Profs.append(Species.Species_Skill_Profs)
    Player_Character.Weapon_Profs.append(Species.Species_Weapon_Profs)
    Player_Character.Tool_Profs.append(Species.Species_Tool_Profs)
    Player_Character.Artisans_Tools_Prof.append(Species.Species_Artisan_Tool_Profs)

    Player_Character.WRI.append(Species.Species_WRI)

    #Player_Character.Actions
    #Player_Character.Bonus_Actions

    for i in range(0,len(Species.Species_Bonuses),1):
        x = str(Species.Species_Bonuses[i])
        if 'STR' in Species.Species_Bonuses[i]:
            Player_Character.Str_Score = Player_Character.Str_Score + int(x[4])
        else: pass

        if 'DEX' in Species.Species_Bonuses[i]:
            Player_Character.Dex_Score = Player_Character.Dex_Score + int(x[4])
        else: pass

        if 'CON' in Species.Species_Bonuses[i]:
            Player_Character.Con_Score = Player_Character.Con_Score + int(x[4])
        else: pass

        if 'INT' in Species.Species_Bonuses[i]:
            Player_Character.Int_Score = Player_Character.Int_Score + int(x[4])
        else: pass

        if 'WIS' in Species.Species_Bonuses[i]:
            Player_Character.Wis_Score = Player_Character.Wis_Score + int(x[4])
        else: pass
        
        if 'CHA' in Species.Species_Bonuses[i]:
            Player_Character.Cha_Score = Player_Character.Cha_Score + int(x[4])
        else: pass



Human = Species('Players Handbook','Humanoid',['Medium','Small'],False,['STR:1','DEX:1','CON:1','INT:1','WIS:1','CHA:1'],30,False,['Common',1],False,False,False,False,False,False,False,False)
Human_Variant = Species('Players Handbook','Humanoid',['Medium','Small'],False,30,False,False,1,False,False,False,False,False,False,False,True)

Elf = Species('Players Handbook','Humanoid',['Medium','Small'],['Darkvision 60'],['Dex:2'],30,['Fey Ancestry'],['Common','Elvish'],['Perception'],False,False,False,False,False,False,False)

#High_Elf = h.Subspecies()
#Wood_Elf = h.Subspecies()



Half_Elf = Species('Players Handbook','Humanoid',['Medium','Small'],['Darkvision 60'],['CHA:2','2:1'],30,['Fey Ancestry'],['Common','Elvish',1],2,False,False,False,False,False,False,False)

Dwarf = Species('Players Handbook','Humanoid',['Medium','Small'],['Darkvision 60'],['CON:2'],25,['Dwarven Resilience','Stonecunning'],['Common','Dwarvish'],False,['Battleaxe','Handaxe','Light Hammer','Warhammer'],False,1,False,False,['poisonres'],False)

#Hill_Dwarf = h.Subspecies()
#Mountain_Dwarf = h.Subspecies()
#Duergar = h.Subspecies()

def Apply_Breath_Weapon(Creature):
    pass

def Use_Breath_Weapon():
    pass

#Dragonborn = h.Species('Players Handbook','Humanoid',['Medium','Small'],['Darkvision 60'],[],[],False,['Common','Draconic'],False,False,False,False,[Apply_Breath_Weapon()],False,False,False)
#Dragonborn2 = h.Species('Mordenkainen Presents Monsters of the Multiverse','Humanoid',)

# Gem
    # Psychic
    # Radiant
    # Force
    # Thunder

# Metallic
    # Gold
    # Silver
    # Brass
    # Copper

# Chromatic
    # Red
    # Blue
    # Green
    # White
    # Black

#Tiefling = h.Species()




#Gnome = h.Species()

# Deep Gnome
# Rock Gnome
# 

#Halfling = h.Species()

# Lightfoot
# Stout

#Aasimar = h.Species()

#Aarakocra = h.Species()

#Genasi = h.Species()

# Fire
# Water
# Earth
# Air

#Warforged = h.Species()

#Kenku = h.Species()

#Yuan_Ti = h.Species()

#Satyr = h.Species()

#Kobold = h.Species()

#Orc = h.Species()

#Half_Orc = h.Species()



Species_List = [Human,Elf,Half_Elf,Dwarf]