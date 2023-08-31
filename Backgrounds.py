from random import randrange



class Background:
  def __init__(self,Name,Skill_Profs,Language_Profs,Tool_Profs,Artisans_Tools_Profs,Instrument_Profs,Vehicle_Profs,Game_Profs,Inventory_Tools,Inventory_Artisan_Tools,Inventory_Instruments,Inventory_Games,Inventory_Storage,Inventory_Currency,Inventory_Apparel,Inventory_Items_of_Identification,Inventory_Vehicles,Features):
    self.Name = Name
    self.Skill_Profs = Skill_Profs
    self.Language_Profs = Language_Profs
    self.Tool_Profs = Tool_Profs
    self.Instrument_Profs = Instrument_Profs
    self.Artisans_Tools_Profs = Artisans_Tools_Profs
    self.Instrument_Profs = Instrument_Profs
    self.Vehicle_Profs = Vehicle_Profs
    self.Game_Profs = Game_Profs
    self.Inventory_Tools = Inventory_Tools
    self.Inventory_Artisan_Tools = Inventory_Artisan_Tools
    self.Inventory_Instruments = Inventory_Instruments
    self.Inventory_Games = Inventory_Games
    self.Inventory_Storage = Inventory_Storage
    self.Inventory_Currency = Inventory_Currency
    self.Inventory_Apparel = Inventory_Apparel
    self.Inventory_Items_of_Identification = Inventory_Items_of_Identification
    self.Inventory_Vehicles = Inventory_Vehicles

    self.Features = Features

    def Apply_Background(Player_Character):
      pass



Artisans_Tools = ['Alchemist Supplies','Brewers Supplies','Calligraphers Supplies','Carpenters Tools',
'Cobblers Tools','Cooks Utensils','Glassblowers Tools','Jewelers Tools','Leatherworkers Tools','Masons Tools',
'Painters Supplies','Potters Tools','Smiths Tools','Tinkers Tools','Weavers Tools','Woodcarvers Tools']

Tools = ['Artisans Tools','Disguise Kit','Forgery Kit','Gaming Set','Herbalism Kit','Musical Instrument','Navigators Tools',
'Poisoners Kit','Thieves Tools']

Gaming_Sets = ['Dice Set','Dragonchess Set','Playing Card Set','Three Dragon Ante Set']

Musical_Instruments = ['Bagpipes','Drum','Dulcimer','Flute','Lute','Lyre','Horn','Pan Flute','Shawm','Viol']

Land_Vehicles = ['Carriage','Cart','Chariot','Sled','Wagon']
Water_Vehicles = ['Galley','Keelboat','Longship','Rowboat','Sailing Ship','Warship']
Mounts = ['Camel','Donkey','Mule','Elephant','Draft Horse','Riding Horse','Mastiff','Pony','Warhorse']

Common_Languages = ['Common','Dwarvish','Elvish','Giant','Gnomish','Goblin','Halfling','Orc']
Exotic_Languages = ['Abyssal','Celestial','Draconic','Deep Speech','Infernal','Primordial','Sylvan','Undercommon']


# Urchin
    # Sleight of Hand, Stealth
    # Disguise Kit, Thieves Tools
    # Common Clothes, Belt Pouch of 10gp
    # City Secrets Feature

Urchin = Background('Urchin',['Sleight of Hand','Stealth'],False,['Disguise Kit','Thieves Tools'],False,False,False,False,False,False,False,False,'Belt Pouch','15gp','Common Clothes',False,False,'City Secrets',)

# Soldier
    # Athletics, Intimidation
    # Gaming Set, Vehicles (land)
    # Insignia of Rank, Dice Set or Playing Cards, Common Clothes, Belt Pouch of 10gp
    # Military Rank Feature

Soldier = Background('Soldier',['Athletics','Intimidation'],False,False,False,False,['Land_Vehicles'],1,False,False,False,1,'Belt Pouch','10gp','Common Clothes','Insignia of Rank',False,'Military Rank')

# Sailor
    # Athletics, Perception
    # Navigator's Tools, Vehicles (water)
    # Club, Silk Rope (50ft), Common Clothes, Belt Pouch of 10gp
    # Ship's Passage Feature

Sailor = Background('Sailor',['Athletics','Perception'],False,['Navigators Tools'],False,False,['Water_Vehicles'],False,False,False,False,False,'Belt Pouch','10gp','Common Clothes',False,False,'Ships Passage')

# Pirate
    # Athletics, Perception
    # Navigator's Tools, Vehicles (water)
    #  Club, Silk Rope (50ft), Common Clothes, Belt Pouch of 10gp
    # Bad Reputation Feature

Pirate = Background('Pirate',['Athletics','Perception'],False,['Navigators Tools'],False,False,['Water_Vehicles'],False,False,False,False,False,'Belt Pouch','10gp','Common Clothes',False,False,'Bad Reputation')

# Sage
    # Arcana, History
    # Two Languages of your choice
    # Ink, Quill, Common Clothes, Belt Pouch of 10gp
    # Researcher Feature

Sage = Background('Sage',['Arcana','History'],2,False,False,False,False,False,False,False,False,False,'Belt Pouch',['10gp'],'Common Clothes',False,False,'Researcher')

# Outlander
    # Athletics, Survival
    # One musical instrument
    # One language of your choice
    # Staff, hunting trap, traveler's clothes, belt pouch of 10gp
    # Wanderer Feature

Outlander = Background('Outlander',['Athletics','Survival'],1,False,False,1,False,False,False,False,False,False,'Belt Pouch','10gp','Travelers Clothes',False,False,'Wanderer')

# Noble
    # History, Persuasion
    # Gaming Set
    # One language
    # Fine Clothes, Signet Ring, Scroll of Pedigree, Purse of 25gp
    # Position of Privilege Feature

Noble = Background('Noble',['History','Persuasion'],1,False,False,False,False,1,False,False,False,False,'Purse','25gp','Fine Clothes',['Signet Ring','Scroll of Pedigree'],False,'Position of Privilege')

# Knight
    # History, Persuasion
    # Gaming Set
    # One language
    # Fine Clothes, Signet Ring, Scroll of Pedigree, Purse of 25gp
    # Retainers Feature

Knight = Background('Knight',['History','Persuasion'],1,False,False,False,False,1,False,False,False,False,'Purse','25gp','Fine Clothes',['Signet Ring','Scroll of Pedigree'],False,'Retainers')

# Hermit
    # Medicine, Religion
    # Herbalism Kit
    # One language
    # Scroll Case, Winter Blanket, Common Clothes, Herbalism Kit, 5gp
    # Discovery Feature

Hermit = Background('Hermit',['Medicine','Religion'],1,['Herbalism Kit'],False,False,False,False,['Herbalism Kit'],False,False,False,False,'5gp','Common Clothes',False,False,'Discovery')

# Guild Merchant
    # Insight, Persuasion
    # Artisan's tools or Navigator's tools, or an additonal language
    # One language 
    # Artisan's tools OR mule and cart, letter of introduction, traveler's clothes, pouch of 15gp
    # Guild Membership Feature

Guild_Merchant1 = Background('Guild Merchant 1',['Insight','Persuasion'],1,['Navigators Tools'],False,False,False,False,False,1,False,False,'Belt Pouch','15gp','Travelers Clothes','Letter of Introduction',False,'Guild Membership')
Guild_Merchant2 = Background('Guild Merchant 2',['Insight','Persuasion'],1,False,1,False,False,False,False,False,False,False,'Belt Pouch','15gp','Travelers Clothes','Letter of Introduction',['Mule','Cart'],'Guild Membership')

# Guild Artisan
    # Insight, Persuasion
    # Artisan's tools
    # language
    # Artisan's tools, letter of introduction, traveler's clothes, belt pouch of 15gp
    # Guild Membership Feature

Guild_Artisan = Background('Guild Artisan',['Insight','Persuasion'],1,False,1,False,False,False,False,1,False,False,'Belt Pouch','15gp','Travelers Clothes','Letter of Introduction',False,'Guild Membership')

# Folk Hero
    # Animal Handling, Survival
    # One type of artisan's tools, vehicles (land)
    # Artisan's tools, shovel, iron pot, common clothes, belt pouch of 10gp
    # Rustic Hospitality feature

Folk_Hero = Background('Folk Hero',['Animal Handling','Survival'],False,False,1,False,['Water_Vehicles'],False,False,1,False,False,'Belt Pouch',['10gp'],'Common Clothes',False,False,'Rustic Hospitality')

# Gladiator
    # Acrobatics, Performance
    # Disguise Kit, one type of musical instrument
    # weapon, costume clothes, belt pouch of 15gp
    # By Popular Demand Feature

Gladiator = Background('Gladiator',['Acrobatics','Performance'],False,['Disguise Kit'],False,1,False,False,False,False,False,False,'Belt Pouch','15gp','Costume Clothes',False,False,'By Popular Demand')

# Entertainer
    # Acrobatics, Performance
    # Disguise Kit, one type of musical instrument
    # instrument, costume clothes, belt pouch of 15gp
    # By Popular Demand Feature

Entertainer = Background('Entertainer',['Acrobatics','Performance'],False,['Disguise Kit'],False,1,False,False,False,False,1,False,'Belt Pouch','15gp','Costume Clothes',False,False,'By Popular Demand')

# Criminal
    # Deception,Stealth
    # Gaming set, thieves' tools
    # Crowbar, common clothes, belt pouch of 15gp
    # Criminal Contact Feature

Criminal = Background('Criminal',['Deception','Stealth'],False,['Thieves Tools'],False,False,False,1,False,False,False,False,'Belt Pouch','15gp','Common Clothes',False,False,'Criminal Contact')

# Spy
    # Deception,Stealth
    # Gaming set, thieves' tools
    # Crowbar, common clothes, belt pouch of 15gp
    # Spy Contact Feature

Spy = Background('Spy',['Deception','Stealth'],False,['Thieves Tools'],False,False,False,1,False,False,False,False,'Belt Pouch','15gp','Common Clothes',False,False,'Spy Contact')

# Charlatan
    # Deception, Sleight of Hand
    # Disguise Kit, Forgery Kit
    # Fine clothes, disguise kit, belt pouch of 15gp
    # False Identity Feature

Charlatan = Background('Charlatan',['Deception','Sleight of Hand'],False,['Disguise Kit','Forgery Kit'],False,False,False,False,['Disguise Kit'],False,False,False,'Belt Pouch','15gp','Fine Clothes',False,False,'False Identity')

# Acolyte
    # Insight, Religion
    # Two languages
    # Holy Symbol, Book, Common Clothes, Belt pouch of 15gp
    # Shelter of the Faithful Feature

Acolyte = Background('Acolyte',['Insight','Religion'],2,False,False,False,False,False,False,False,False,False,'Belt Pouch','15gp','Common Clothes',False,False,'Shelter of the Faithful')


Background_Options = [Urchin,Soldier,Sailor,Pirate,Sage,Outlander,Noble,Knight,Hermit,Guild_Merchant1,Guild_Merchant2,Guild_Artisan,Folk_Hero,Gladiator,Entertainer,Criminal,Spy,Charlatan,Acolyte]

def Take_Background(Background,Player_Character):
    # Skill_Profs,Language_Profs,Tool_Profs,Artisans_Tools_Profs,Instrument_Profs,Vehicle_Profs,Game_Profs,Inventory,Features
    Player_Character.Skill_Profs.append(Background.Skill_Profs[0])
    Player_Character.Skill_Profs.append(Background.Skill_Profs[1])

    if type(Background.Language_Profs) == bool:
        pass
    elif type(Background.Language_Profs) == int:
        if Background.Language_Profs > 1:
            for i in range(Background.Language_Profs):
                Player_Character.Language_Profs.append(Common_Languages[randrange(0,len(Common_Languages),1)])
        else:
            Player_Character.Language_Profs.append('Elvish')

    elif type(Background.Language_Profs) == str:
        Player_Character.Language_Profs.append(Background.Language_Profs)

    elif type(Background.Language_Profs) == list:
        Player_Character.Language_Profs.append(Background.Language_Profs)
    else: pass

        #if len(Background.Language_Profs) > 0:               # I could make a list of properties and build a for loop that could reduce the lines of code by 4/5ths
        #    for i in range(0,Background.Language_Profs,1):
        #        if type(i) == int:
        #            for i in range(0,i,1):
        #                Player_Character.Language_Profs.append(Common_Languages[randrange(0,len(Common_Languages),1)])
        #        else:
        #            Player_Character.Language_Profs.append(Background.Language_Profs[i])
        #else: pass

    if type(Background.Tool_Profs) == bool:
        pass
    elif type(Background.Tool_Profs) == int:
        if Background.Tool_Profs > 1:
            for i in range(Background.Tool_Profs):
                Player_Character.Tool_Profs.append(Tools[randrange(0,len(Tools),1)])
        else:
            Player_Character.Tool_Profs.append('Thieves Tools')

    elif type(Background.Tool_Profs) == str:
        Player_Character.Tool_Profs.append(Background.Tool_Profs)

    elif type(Background.Tool_Profs) == list:
        Player_Character.Tool_Profs.append(Background.Tool_Profs)
    else: pass

    #if type(Background.Tool_Profs) == bool:
    #    pass
    #elif type(Background.Tool_Profs) == list:
    #    if len(Background.Tool_Profs) > 0:
    #        for i in Background.Tool_Profs:
    #            if type(i) == int:
    #                for i in range(0,i,1):
    #                    Player_Character.Tool_Profs.append(Tools[randrange(0,len(Tools),1)])
    #            else:
    #                Player_Character.Tool_Profs.append(Background.Tool_Profs[i])
    #    else: pass
    #else: pass

    if type(Background.Instrument_Profs) == bool:
        pass
    elif type(Background.Instrument_Profs) == list:
        if len(Background.Instrument_Profs) > 0:
            for i in Background.Instrument_Profs:
                if type(i) == int:
                    for i in range(0,i,1):
                        Player_Character.Instrument_Profs.append(Musical_Instruments[randrange(0,len(Musical_Instruments),1)])
                else:
                    Player_Character.Instrument_Profs.append(Background.Instrument_Profs[i])
        else: pass    
    else: pass

    if type(Background.Artisans_Tools_Profs) == bool:
        pass
    elif type(Background.Artisans_Tools_Profs) == list:
        if len(Background.Artisans_Tools_Profs) > 0:
            for i in Background.Artisans_Tools_Profs:
                if type(i) == int:
                    for i in range(0,i,1):
                        Player_Character.Artisans_Tools_Profs.append(Artisans_Tools[randrange(0,len(Artisans_Tools),1)])
                else:
                    Player_Character.Artisans_Tools_Profs.append(Background.Artisans_Tools_Profs[i])
        else: pass
    else: pass

    if type(Background.Game_Profs) == bool:
        pass
    elif type(Background.Game_Profs) == list:
        if len(Background.Game_Profs) > 0:
            for i in Background.Game_Profs:
                if type(i) == int:
                    for i in range(0,i,1):
                        Player_Character.Game_Profs.append(Gaming_Sets[randrange(0,len(Gaming_Sets),1)])
                else:
                    Player_Character.Game_Profs.append(Background.Game_Profs[i])
        else: pass
    else: pass

    if type(Background.Vehicle_Profs) == bool:
        pass
    elif type(Background.Vehicle_Profs) == list:
        if len(Background.Vehicle_Profs) > 0:
            Player_Character.Vehicle_Profs.append(Background.Vehicle_Profs)
        else: pass
    else: pass
    
    Player_Character.Inventory['Instruments'].append(Background.Inventory_Instruments)
    
    Player_Character.Inventory['Tools'].append(Background.Inventory_Tools)
    
    Player_Character.Inventory['Artisan_Tools'].append(Background.Inventory_Artisan_Tools)
    
    Player_Character.Inventory['Games'].append(Background.Inventory_Games)

    Player_Character.Inventory['Apparel'].append(Background.Inventory_Apparel)
    
    Player_Character.Inventory['Storage'].append(Background.Inventory_Storage)
    
    Player_Character.Inventory['Identifying_Items'].append(Background.Inventory_Items_of_Identification)
    
    Player_Character.Inventory['Currency'].append(Background.Inventory_Currency)


   






