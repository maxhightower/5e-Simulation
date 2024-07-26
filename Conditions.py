import Effects

 
# Conditions
# blinded

Blinded_Attack_Effect = Effects.Buff_Circumstance_Effect('Attack Rolls','Self','Instantaneous','Attack Rolls','Disadvantage')
Blinded_Check_Effect = Effects.Buff_Replacement_Effect('Ability Check','Self','Instantaneous','Ability Check',2)

def Blind(Creature):
  if "Blindedimmu" in Creature.WRI:
    print('Creature Immune to Being Blinded')
  else:
    Creature.Active_Conditions.append("Blinded")
    Effects.Apply_Buff_Circumstance_Effect(Blinded_Attack_Effect,Creature)
    Effects.Apply_Buff_Circumstance_Effect(Blinded_Check_Effect,Creature)

  #A blinded creature can't see and automatically fails any ability check that requires sight.
    # so all ability checks will need a tag for if they require sight or not
  #Attack rolls against the creature have advantage, and the creature's attack rolls have disadvantage.
    # will need to wait for this until I finalize the adv and dis stuff

# deafened
def Deafen(Creature):
  if "Deafenedimmu" in Creature.WRI:
    print('Creature Immune to Being Deafened')
  else:
    Creature.Active_Conditions.append("Deafened")



# poisoned
  # A poisoned creature has disadvantage on attack rolls and ability checks.
Poisoned = Effects.Buff_Circumstance_Effect(['Attack Rolls','Ability Checks'],'Self','Instantaneous',['Attack Rolls','Ability Checks'],'Disadvantage')

def Poison(Creature):
  if "Poisonedimmu" in Creature.WRI:
    print('Creature Immune to Being Poisoned')
  else:
    Creature.Active_Conditions.append("Poisoned")
    Effects.Apply_Buff_Circumstance_Effect(Poisoned,Creature)


# incapacitated
  # loses concentration
  # no actions, bonus actions, free actions, or reactions
def Incapacitate(Creature):
  if "Incapacitatedimmu" in Creature.WRI:
    print('Creature Immune to Being Incapacitated')
  else:
    Creature.Active_Conditions.append('Incapacitated')
    Creature.Concentrating = False

# unconcious
  # incapacitated
  # prone
  # autofails strength and dexterity saves
  # attack rolls have advantage
  # any attack from within 5ft that hits is a critical
def Unconcious(Creature):
  if "Unconciousimmu" in Creature.WRI:
    print('Creature Immune to Being Unconcious')
  else:
    Creature.Active_Conditions.append('Unconcious')
    Incapacitate(Creature)
    Prone(Creature)

# stunned
  # incapacitated
  # speed = 0
  # autofails strength and dexterity saves
  # attacks against creature have advantage

Stunned_Save_Fail_Effect = Effects.Buff_Replacement_Effect('Condition','Self','Instantaneous',['Strength Saving Throw','Dexterity Saving Throw'],2)
Stunned_Speed_Effect = Effects.Speed_Effect('Condition','Self','','Any',False,0)    # Need to add a duration...

def Stun(Creature):
  if "Stunnedimmu" in Creature.WRI:
    print('Creature Immune to Being Stunned')
  else:
    Creature.Active_Conditions.append('Stunned')
    Incapacitate(Creature)
    #Effects.Apply_Speed_Effect
    Effects.Apply_Buff_Replacement_Effect(Stunned_Save_Fail_Effect,Creature)

# prone
  # A prone creature's only movement option is to crawl, unless it stands up and thereby ends the condition.
  # The creature has disadvantage on attack rolls.
  # An attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the attack roll has disadvantage.
def Prone(Creature):
  if "Proneimmu" in Creature.WRI:
    print('Creature Immune to Being Prone')
  else:
    Creature.Active_Conditions.append('Prone')


# restrained
def Restrained(Creature):
  if 'Restrainedimmu' in Creature.WRI:
    print('Creature Immune to Being Restrained')
  else:
    Creature.Active_Conditions.append('Restrained')
    
    
  # speed = 0
  # Attacks against have advantage
  # creature's attack have disadvantage
  # disadvantage on dexterity saving throws

# grappled
def Grapple(Creature):
  if "Grappleimmu" in Creature.WRI:
    print('Creature Immune to Being Grappled')
  else:
    Creature.Active_Conditions.append('Grappled')

# paralyzed
  # incapacitated
  # speed = 0
  # The creature automatically fails Strength and Dexterity saving throws.
  # Attack rolls against the creature have advantage.
  # Any attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.
def Paralyze(Creature):
  if "Paralyzedimmu" in Creature.WRI:
    print('Creature Immune to Being Paralyzed')
  else:
    Creature.Active_Conditions.append('Paralyzed')
    Incapacitate(Creature)

# invisible
  # An invisible creature is impossible to see without the aid of magic or a special sense. For the purpose of hiding, the creature is heavily obscured. The creature's location can be detected by any noise it makes or any tracks it leaves.
  # Attacks against have disadvantage
  # Creature's attacks have advantage


# Potential Options from Pathfinder
  # Seek Action
    # You scan an area for signs of creatures or objects. 
    # If you're looking for creatures, choose an area you're scanning. 
    # If precision is necessary, the GM can have you select a 30-foot cone or a 15-foot burst within line of sight. 
    # You might take a penalty if you choose an area that's far away.

    # If you're using Seek to search for objects (including secret doors and hazards), you search up to a 10-foot square adjacent to you. 
    # The GM might determine you need to Seek as an activity, 
    # taking more actions or even minutes or hours if you're searching a particularly cluttered area.

    # The GM attempts a single secret Perception check for you and compares the result to the Stealth DCs of any undetected 
    # or hidden creatures in the area or the DC to detect each object in the area (as determined by the GM or by someone Concealing the Object). 
    # A creature you detect might remain hidden, rather than becoming observed, 
    # if you're using an imprecise sense or if an effect (such as invisibility) prevents the subject from being observed.
  
    # Critical Success If you were searching for creatures, any undetected or hidden creature you critically succeeded against becomes observed by you. 
    # If you were searching for an object, you learn its location.
    # Success If you were searching for creatures, any undetected creature you succeeded against becomes hidden from you instead of undetected, 
    # and any hidden creature you succeeded against becomes observed by you. 
    # If you were searching for an object, you learn its location or get a clue to its whereabouts, as determined by the GM.


  # Observed 
    # Anything in plain view is observed by you. 
    # If a creature takes measures to avoid detection, such as by using Stealth to Hide, it can become hidden or undetected instead of observed. 
    # If you have another precise sense instead of or in addition to sight, you might be able to observe a creature or object using that sense instead. 
    # You can observe a creature only with precise senses. 
    # When Seeking a creature using only imprecise senses, it remains hidden, rather than observed.
  
  # Concealed   
    # While you are concealed from a creature, such as in a thick fog, you are difficult for that creature to see. 
    # You can still be observed, but you're tougher to target. 
    # A creature that you're concealed from must succeed at a DC 5 flat check when targeting you with an attack, spell, or other effect. 
    # Area effects aren't subject to this flat check. If the check fails, the attack, spell, or effect doesn't affect you.

  # Hidden 
    # While you're hidden from a creature, that creature knows the space you're in but can't tell precisely where you are. 
    # You typically become hidden by using Stealth to Hide. When Seeking a creature using only imprecise senses, it remains hidden, rather than observed. 
    # A creature you're hidden from is flat-footed to you, 
    #   and it must succeed at a DC 11 flat check when targeting you with an attack, spell, or other effect or it fails to affect you. 
    # Area effects aren't subject to this flat check.
    # A creature might be able to use the Seek action to try to observe you.

  # Invisible
    # While invisible, you can't be seen. 
    # You're undetected to everyone. 
    # Creatures can Seek to attempt to detect you; 
    # if a creature succeeds at its Perception check against your Stealth DC, 
    # you become hidden to that creature until you Sneak to become undetected again. 
    # If you become invisible while someone can already see you, 
    # you start out hidden to the observer (instead of undetected) until you successfully Sneak. 
    # You can't become observed while invisible except via special abilities or magic.

  # Undetected
    # When you are undetected by a creature, that creature cannot see you at all, has no idea what space you occupy, and can't target you, 
    # though you still can be affected by abilities that target an area. When you're undetected by a creature, that creature is flat-footed to you.
    # A creature you're undetected by can guess which square you're in to try targeting you. It must pick a square and attempt an attack. 
    # This works like targeting a hidden creature (requiring a DC 11 flat check), but the flat check and attack roll are rolled in secret by the GM, 
    # who doesn't reveal whether the attack missed due to failing the flat check, failing the attack roll, or choosing the wrong square.
    # A creature can use the Seek action to try to find you.

  # Unnoticed
    # If you are unnoticed by a creature, that creature has no idea you are present at all. 
    # When you're unnoticed, you're also undetected by the creature. 
    # This condition matters for abilities that can be used only against targets totally unaware of your presence.

  # Precise Sense
    # Average vision is a precise sense—a sense that can be used to perceive the world in nuanced detail. 
    # The only way to target a creature without having drawbacks is to use a precise sense. 
    # You can usually detect a creature automatically with a precise sense unless that creature is hiding or obscured by the environment, 
    # in which case you can use the Seek basic action to better detect the creature.

  # Imprecise Senses
    # Hearing is an imprecise sense—it cannot detect the full range of detail that a precise sense can. 
    # You can usually sense a creature automatically with an imprecise sense, but it has the hidden condition instead of the observed condition. 
    # It might be undetected by you if it’s using Stealth or is in an environment that distorts the sense, such as a noisy room in the case of hearing. 
    # In those cases, you have to use the Seek basic action to detect the creature. 
    # At best, an imprecise sense can be used to make an undetected creature (or one you didn’t even know was there) 
    # merely hidden—it can’t make the creature observed.

  # Vague Senses
    # A character also has many vague senses—ones that can alert you that something is there but aren’t useful for zeroing in on it to determine exactly what it is. 
    # The most useful of these for a typical character is the sense of smell. 
    # At best, a vague sense can be used to detect the presence of an unnoticed creature, making it undetected.
    # Even then, the vague sense isn’t sufficient to make the creature hidden or observed.
    # When one creature might detect another, the GM almost always uses the most precise sense available.
    # Pathfinder’s rules assume that a given creature has vision as its only precise sense and hearing as its only imprecise sense. 
    # Some characters and creatures, however, have precise or imprecise senses that don’t match this assumption. 
    # For instance, a character with poor vision might treat that sense as imprecise, 
    # an animal with the scent ability can use its sense of smell as an imprecise sense, 
    # and a creature with echolocation or a similar ability can use hearing as a precise sense. 
    # Such senses are often given special names and appear as “echolocation (precise),” “scent (imprecise) 30 feet,” or the like.


  # Detecting with Other Senses
    # Most abilities that designate “a creature you can see” or the like function just as well if the user can precisely sense the subject with 
    # a different sense. 
    # If a monster uses a sense other than vision, the GM can adapt ways of avoiding detection that work with the monster's senses. 
    # For example, a creature that has echolocation might use hearing as a primary sense. 
    # This could mean its quarry is concealed in a noisy chamber, hidden in a great enough din, or invisible under a silence spell.


  # Using Stealth With Other Senses
    # The Stealth skill is designed to use Hide for avoiding visual detection and Avoid Notice and Sneak to avoid being both seen and heard. 
    # For many special senses, a player can describe how they're avoiding detection by that special sense and use the most applicable Stealth action. 
    # For instance, a creature stepping lightly to avoid being detected via tremorsense would be using Sneak.
    # In some cases, rolling a Dexterity-based Stealth skill check to Sneak doesn't make the most sense. 
    # For example, a PC trying to avoid being detected by a creature that senses heartbeats might meditate to slow their heart rate, 
    # using Wisdom instead of Dexterity for their Stealth check. 
    # When a creature could detect you using multiple different senses, use your lowest applicable ability modifier.

  # Tremorsense
    # Tremorsense allows a creature to feel the vibrations through a solid surface caused by movement. 
    # It is usually an imprecise sense with a limited range (listed in the ability). 
    # Tremorsense functions only if the detecting creature is on the same surface as the subject, 
    # and only if the subject is moving along (or burrowing through) the surface.

  # Dim Light
    # Areas in shadow or lit by weak light sources are in dim light. 
    # Creatures and objects in dim light have the concealed condition, 
    # unless the seeker has darkvision or low-light vision (see Special Senses on page 465), or a precise sense other than vision.

  # Darkness
    # A creature or object within darkness is hidden or undetected unless the seeker has darkvision or a precise sense other than vision 
    # (Special Senses are on page 465). 
    # A creature without darkvision or another means of perceiving in darkness has the blinded condition while in darkness, 
    # though it might be able to see illuminated areas beyond the darkness. 
    # If a creature can see into an illuminated area, it can observe creatures within that illuminated area normally. 
    # After being in darkness, sudden exposure to bright light might make you dazzled for a short time, as determined by the GM.



  # Shocked

  # Turned / Fleeing
    # Needs a target to be turned by 
  
  # Hostile
  # Unfriendly
  # Indifferent
  # Friendly
  # Helpful

  # Enfeebled
  # Stupefied

  # Encumbered
  # Fascinated (for stuff like Entralled)
  # Persistent Damage

  # Quickened
  # Slowed




# Frightened
  # Needs a target to be frightened of

def Frighten(Target):
  Target.Active_Conditions.append('frightened')


# Charmed
  # Needs a target to be charmed by 

def Charm(Target):
  pass


# Exhaustion
# Exhausted (are these two mechanically different?)

# Aflame
# Weakened
# Slowed
# Confused

# Infested

# petrified


# Death

# Memory Drained 
  # we can now reduce the accessible dictionary that is stored in the entity


# Controlled (taking this one out of the pathfinder book)
  # Needs to be a Controlling creature
    # or does there? What about spells like geas? or mind flayer thralls?

# Controlling 
  # Needs to be a target
  # perhaps a range that it can be effective in
  # Concentration
  # Two Types of Control:
    # Is an Action from the Controlling Creature needed to Direct the Controlled Creature?
      # If an action is needed, then every action the Controlled Creature has, now gets exported into the Controlling Creature's action list
    # Or can it occur via verbal commands? Issuing a thought?
  # 
  
  
  # this may be how controlled mounts work mechanically actually...


# Diseased
# Disease: Spores of Zuggtmoy
# Disease: Influence of Zuggtmoy,Charmed
  # should diseases be conditions or effects?


# Confused

# Mummy Rot

# Ability Score Penalty

# Infernal Wound

# Wakeful Rest
  # Trance, Warforged Rest, etc


# Would cover be considered a condition??? I think it would have to be 
# Half Cover
# Three Quarters Cover
# Full Cover
