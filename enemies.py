#enemy classes are defined here. The function attack() under each one is their AI script. Joshua sumague made wolf pinkslime and slime and provided assistance with a few other enemies. Andrew did the rest.
from player import *
class omegaMKCL:
  Name = "Omega Mk. CL"
  HP = 15000
  currentHP = int(HP)
  MP = 1000
  currentMP = int(MP)
  strength = 25
  intelligence = 100
  stamina = 100
  luck = 55
  agility = 25
  XP = 60000
  dropsItems = False
  @staticmethod
  def attack():
    if player.currentHP < 200:
      print omegaMKCL.Name, "uses its built-in wave cannon! You take 201 damage!"
      player.currentHP = player.currentHP - 201
    else:
      attackroll = random.randint(1, 10)
      if len(player.availableSpellClasses) >= 7 and attackroll <= 2:
        attackstrength = random.randint(10, 25)
        print omegaMKCL.Name, "emits an antimagic field! %s takes %d damage for each learned spell!" % (player.Name, attackstrength)
        for spell in player.availableSpellClasses:
          player.currentHP = player.currentHP - attackstrength
      elif attackroll <= 2:
        print omegaMKCL.Name, "tries to create an antimagic field, but its systems fail!", omegaMKCL.Name, "takes 100 damage!"
        omegaMKCL.currentHP = omegaMKCL.currentHP - 100
      elif attackroll <= 6:
        attackstrength = math.ceil(random.randint(omegaMKCL.strength+omegaMKCL.intelligence, 3*omegaMKCL.strength+omegaMKCL.intelligence+50)/2)
        print omegaMKCL.Name, "shoots a missile from its back. %s is hit by the missile and takes %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
      else:
        attackstrength = 3*random.randint(50, 75)
        print omegaMKCL.Name, "launches a grenade barrage! %s is engulfed by the explosions and takes %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
    regenStrength = random.randint(omegaMKCL.stamina, omegaMKCL.stamina*2)
    print "%s activates its auto-repair systems, regenerating %d HP!" % (omegaMKCL.Name, regenStrength)

class slime:
  Name = "slime"
  HP = 30
  currentHP = int(HP)
  MP = 15
  currentMP = int(MP)
  strength = 3
  intelligence = 6
  stamina = 6
  luck = 5
  agility = 2
  XP = 10
  @staticmethod
  def attack():
    attackstrength = random.randint(1, 5)+slime.strength
    attackdamage = attackstrength - player.armorPower
    if attackdamage <= 0:
      print "The slime rushes you but fails to do any damage!"
    else:
      print "The slime tackles %s, dealing %d damage!" % (player.Name, attackdamage)
      player.currentHP = player.currentHP - attackdamage

class pinkslime:
  Name = " pink slime"
  HP = 50
  currentHP = int(HP)
  MP = 15
  currentMP = int(MP)
  strength = 7
  intelligence = 6
  stamina = 6
  luck = 5
  agility = 6
  XP = 25
  @staticmethod
  def attack():
    attackstrength = random.randint(2, 7)+pinkslime.strength
    attackdamage = attackstrength - player.armorPower
    if attackdamage <= 0:
      print "The pink slime rushes %s but fails to do any damage!" % player.Name
    else:
      print "The pink slime tackles %s, dealing %d damage!" % (player.Name, attackdamage)
      player.currentHP = player.currentHP - attackdamage

class wolf:
  Name = "wolf"
  HP = 45
  currentHP = int(HP)
  MP = 15
  currentMP = int(MP)
  strength = 4
  intelligence = 3
  stamina = 6
  luck = 5
  agility = 2
  XP = 45
  @staticmethod
  def attack():
    attackstrength = random.randint(1, 7)
    attackdamage = attackstrength - player.armorPower
    if attackdamage <= 0:
      print "The wolf lunges towards %s but fails to do any damage!" % player.Name
    else:
      print "The wolf bites at %s, dealing %d damage!" % (player.Name, attackdamage)
      player.currentHP = player.currentHP - attackdamage

class wizard:
  #The enemy's name, stats, and XP
  Name = "wizard"
  HP = 55
  currentHP = int(HP)
  MP = 35
  currentMP = int(MP)
  strength = 1
  intelligence = 15
  stamina = 6
  luck = 10
  agility = 2
  XP = 50
  @staticmethod
  #The AI script of the enemy in question
  def attack():
    #attackroll is a random number generated to determine which attack the enemy performs.
    attackroll = random.randint(1, 2)
    if attackroll == 1 and wizard.currentMP >= 5:
      attackstrength = random.randint (5, wizard.intelligence)
      print "The wizard fires an electric blast forward at %s, dealing %d damage!" % (player.Name, attackstrength)
      player.currentHP = player.currentHP - attackstrength
      wizard.currentMP = wizard.currentMP - 5
    elif attackroll == 2 and wizard.currentMP >= 15:
      for num in range(3):
        attackstrength = random.randint(3, 5)+math.floor(wizard.intelligence/6)
        print "The wizard lets out a magic missile, dealing %d damage to %s!" %(attackstrength, player.Name)
        player.currentHP = player.currentHP - attackstrength
        wizard.currentMP = wizard.currentMP - 5
    else:
      print "The wizard waits patiently for its magic power to regenerate. %s looks confused." % player.Name
  
class squire:
  Name = "squire"
  HP = 80
  currentHP = int(HP)
  MP = 0
  currentMP = int(MP)
  strength = 10
  intelligence = 2
  stamina = 9
  luck = 7
  agility = 6
  XP = 65
  @staticmethod
  def attack():
    attackstrength = random.randint(5, 10)+squire.strength
    attackdamage = attackstrength - player.armorPower
    if attackdamage <= 0:
      print "The squire swings his blade at %s but fails to do any damage!" % player.Name
    else:
      print "The squire makes a swing in a large arc at %s, dealing %d damage!" % (player.Name, attackdamage)
      player.currentHP = player.currentHP - attackdamage

class kingslime:
  Name = "king slime"
  HP = 250
  currentHP = int(HP)
  MP = 80
  currentMP = int(MP)
  strength = 22
  intelligence = 19
  stamina = 11
  luck = 10
  agility = 19
  XP = 350
  attacktype = "fire" #tracks what attack mode the king slime is in. changes when turnsInAttackType equals 3.
  turnsInAttackType = 0 #tracks how many turns the king slime has been in its attack mode.
  @staticmethod
  def attack():
    if kingslime.attacktype == "fire": #checks which attack mode the king slime is in.
      attackroll = random.randint(1, 2)
      if attackroll == 1:
        attackstrength = (random.randint(6, 12)+math.floor(kingslime.strength/3))*2
        print "The king slime veils itself in fire and tackles %s, dealing %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
        kingslime.turnsInAttackType = kingslime.turnsInAttackType + 1
        if kingslime.turnsInAttackType == 3:
          print "The king slime changes attack styles!"
          kingslime.attacktype = "ice"
          kingslime.turnsInAttackType = 0
      else:
        attackstrength = random.randint(20, 45)+kingslime.intelligence
        print "The king slime channels the strength of slimekind into a massive burst of energy, dealing %d damage to %s!" % (attackstrength, player.Name)
        player.currentHP = player.currentHP - attackstrength
        kingslime.turnsInAttackType = kingslime.turnsInAttackType + 1
        if kingslime.turnsInAttackType == 3:
          print "The king slime changes attack styles!"
          kingslime.attacktype = "ice"
          kingslime.turnsInAttackType = 0
    elif kingslime.attacktype == "ice":
      attackroll = random.randint(1, 2)
      if attackroll == 1:
        print "The king slime summons a storm of icicles that strike %s!" % player.Name
        for num in range (3):
          if kingslime.currentMP >= 7:
            attackstrength = random.randint(5, 10)
            print "An icicle strikes %s, dealing %d damage!" % (player.Name, attackstrength)
            player.currentHP = player.currentHP - attackstrength
            kingslime.currentMP = kingslime.currentMP - 7
          else:
            print "The king slime fails to summon an icicle."
        kingslime.turnsInAttackType = kingslime.turnsInAttackType + 1
        if kingslime.turnsInAttackType == 3:
          print "The king slime changes attack styles!"
          kingslime.attacktype = "lightning"
          kingslime.turnsInAttackType = 0
      else:
        print "The king slime hits %s with an MP-draining blast 4 times!" % player.Name
        for num in range (4):
          attackstrength = random.randint(3, 6)
          print "The king slime takes %d MP from %s!" % (attackstrength, player.Name)
          player.currentMP = player.currentMP - attackstrength
          if player.currentMP <= 0:
            player.currentMP = 0
          kingslime.currentMP = kingslime.currentMP + attackstrength
          if kingslime.currentMP >= kingslime.MP:
            kingslime.currentMP = kingslime.MP
    elif kingslime.attacktype == "lightning":
      print "The king slime sends down a flurry of lightning bolts!"
      for num in range (6):
        if kingslime.currentMP >= 4:
          attackstrength = random.randint(2, 5)
          print "A lightning bolt strikes %s, dealing %d damage!" % (player.Name, attackstrength)
          player.currentHP = player.currentHP - attackstrength
          kingslime.currentMP = kingslime.currentMP - 4
        else:
          print "The king slime fails to send a lightning bolt down."
        kingslime.turnsInAttackType = kingslime.turnsInAttackType + 1
        if kingslime.turnsInAttackType == 3:
          print "The king slime changes attack styles!"
          kingslime.attacktype = "fire"
          kingslime.turnsInAttackType = 0
    else:
      print "The king slime waits." # failsafe in case the attack mode value becomes invalid.

class pyromancer:
  Name = "pyromancer"
  HP = 55
  currentHP = int(HP)
  MP = 50
  currentMP = int(MP)
  strength = 7
  intelligence = 9
  stamina = 11
  luck = 8
  agility = 4
  XP = 65
  @staticmethod
  def attack():
    attackroll = random.randint(1, 2)
    if attackroll == 1 and pyromancer.currentMP >= 5:
      attackstrength = random.randint(5, pyromancer.intelligence)*2
      print "The pyromancer lets out a flame jet, dealing %d damage to %s!" % (attackstrength, player.Name)
      player.currentHP = player.currentHP - attackstrength
      pyromancer.currentMP = pyromancer.currentMP - 5
    elif attackroll == 2 and pyromancer.currentMP >= 20:
      numberOfFireballs = random.randint(1, 4)
      for num in range (numberOfFireballs):
        attackstrength = random.randint(3, math.ceil(pyromancer.intelligence/2))
        print "The pyromancer launches a fireball at %s, dealing %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
        pyromancer.currentMP = pyromancer.currentMP - 5
    else:
      attackstrength = random.randint(3, 5) - player.armorPower
      if attackstrength <= 0:
        print "The pyromancer hits %s with its staff but fails to do any noticeable damage." % player.Name
      else:
        print "The pyromancer hits %s with its staff, dealing %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength

class slimeSwordsman:
  Name = "slime swordsman"
  HP = 90
  currentHP = int(HP)
  MP = 0
  currentMP = int(MP)
  strength = 17
  intelligence = 7
  stamina = 13
  luck = 8
  agility = 4
  XP = 120
  @staticmethod
  def attack():
    attackstrength = random.randint(5, slimeSwordsman.strength)+10 - player.armorPower
    if attackstrength <= 0:
      print "The slime swordsman's blade bounces off %s's armor" % player.Name
    else:
      print "The slime swordsman stabs %s with its shortsword, dealing %d damage!" % (player.Name, attackstrength)
      player.currentHP = player.currentHP - attackstrength

class redSlime:
  Name = "red slime"
  HP = 110
  currentHP = int(HP)
  MP = 10
  currentMP = int(MP)
  strength = 7
  intelligence = 25
  stamina = 9
  luck = 6
  agility = 5
  XP = 150
  @staticmethod
  def attack():
		attackroll = random.randint(1, 10)
		if attackroll <= 4:
			attackstrength = random.randint(10, redSlime.intelligence)
			print "The red slime spits fire at %s, dealing %d damage!" % (player.Name, attackstrength)
		elif attackroll <= 6:
			attackstrength = random.randint(18, redSlime.intelligence)
			print "The red slime breathes out a menacing blue flame, damaging %s's MP by %d points!" % (player.Name, attackstrength)
			player.currentMP = player.currentMP - attackstrength
			if player.currentMP <= 0:
				player.currentMP = 0
		elif attackroll <= 8 and redSlime.currentMP == 10:
			attackstrength = random.randint(2*redSlime.currentMP, 4*redSlime.currentMP)
			print "The red slime lets loose all its magic power at once! %s takes %d damage!" % (player.Name, attackstrength)
			player.currentHP = player.currentMP - attackstrength
			redSlime.currentMP = 0
		else:
			print "The red slime focuses itself and regenerates 2 MP!"
			redSlime.currentMP = redSlime.currentMP + 2
			if redSlime.currentMP >= redSlime.MP:
				redSlime.currentMP = redSlime.MP

class shockingSlime:
  Name = "shocking slime"
  HP = 200
  currentHP = int(HP)
  MP = 35
  currentMP = int(MP)
  strength = 9
  intelligence = 33
  stamina = 11
  luck = 12
  agility = 18
  XP = 330
  @staticmethod
  def attack():
    attackroll = random.randint(1, 10)
    if attackroll <= 4:
      attackstrength = random.randint(15, shockingSlime.intelligence)+5
      print "The shocking slime zaps %s, dealing %d damage!" % (player.Name, attackstrength)
    elif attackroll <= 6:
			attackstrength = random.randint(2, 6)+math.floor(shockingSlime.intelligence/2)
			print "The shocking slime produces a dark lightning bolt, damaging %s's MP by %d points!" % (player.Name, attackstrength)
			player.currentMP = player.currentMP - attackstrength
			if player.currentMP <= 0:
				player.currentMP = 0
    elif attackroll <= 8 and shockingSlime.currentMP == 35:
      attackstrength = random.randint(2*shockingSlime.currentMP, 4*shockingSlime.currentMP)
      print "The shocking slime lets loose all its electric power at once! %s takes %d damage!" % (player.Name, attackstrength)
      player.currentHP = player.currentMP - attackstrength
      shockingSlime.currentMP = 0
    else:
      print "The shocking slime absorbs some electricity from the enivronment!"
      shockingSlime.currentMP = shockingSlime.currentMP + 8
      if shockingSlime.currentMP >= shockingSlime.MP:
        shockingSlime.currentMP = shockingSlime.MP

class maskedKnight:
  Name = "masked knight"
  HP = 575
  currentHP = int(HP)
  MP = 0
  currentMP = int(MP)
  strength = 33
  intelligence = 5
  stamina = 27
  luck = 11
  agility = 16
  XP = 1200
  @staticmethod
  def attack():
    attackroll = random.randint(1, 5)
    if attackroll <= 2:
      attackstrength = (random.randint(5, maskedKnight.strength)+10) - player.armorPower
      if attackstrength <= 0:
        print "The masked knight's blade bounces off %s's armor" % player.Name
      else:
        print "The masked knight cleaves %s with his polearm, dealing %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
    elif attackroll <= 4:
      attackstrength = random.randint(math.floor(maskedKnight.stamina/3), math.ceil(maskedKnight.stamina/2))
      print "The masked knight absorbs %d HP from %s!" % (attackstrength, player.Name)
      player.currentHP = player.currentHP - attackstrength
      if maskedKnight.currentHP >= maskedKnight.HP:
        maskedKnight.currentHP = maskedKnight.HP
    else:
      print "The masked knight laughs confidently."

class rainbowSlime:
  Name = "rainbow slime"
  HP = 900
  currentHP = int(HP)
  MP = 100
  currentMP = int(MP)
  strength = 46
  intelligence = 33
  stamina = 45
  luck = 19
  agility = 255 #makes encounters this monster is in impossible to run away from due to how the math behind the player's run command works
  XP = 3500
  @staticmethod
  def attack():
    attackroll = random.randint(1, 10)
    if attackroll <= 2 and rainbowSlime.currentMP >= 80:
      print "The rainbow slime sends down a flurry of fireballs!"
      for fireball in range (random.randint(10, 16)):
        attackstrength = random.randint(5, math.floor(rainbowSlime.intelligence/4))
        print "A fireball burns %s for %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
        rainbowSlime.currentMP = rainbowSlime.currentMP - 5
    elif attackroll <= 4 and rainbowSlime.currentMP >= 30:
      attackstrength = random.randint(57, rainbowSlime.intelligence*3)
      print "The rainbow slime summons a meteor from the sky! %s is caught in the cataclysmic explosion and takes %d damage!" % (player.Name, attackstrength)
      player.currentHP = player.currentHP - attackstrength
      rainbowSlime.currentMP = rainbowSlime.currentMP - 30
    elif attackroll <= 6 and rainbowSlime.currentMP == 100:
      attackstrength = random.randint(2*rainbowSlime.currentMP, 4*rainbowSlime.currentMP)
      print "The rainbow slime lets loose all its magic power at once! %s takes %d damage from the blast!" % (player.Name, attackstrength)
      player.currentHP = player.currentHP - attackstrength
      rainbowSlime.currentMP = 0
    elif attackroll <= 8:
      print "The rainbow slime calls on the powers of its brothers!" #lets the rainbow slime "transform" into other enemies and use their powers.
      redSlime.attack()
      shockingSlime.attack()
    else:
      print "The rainbow slime puts on a cocky smirk."
    print "The rainbow slime regenerates 2 MP!"
    rainbowSlime.currentMP = rainbowSlime.currentMP + 2

class direWolf:
  Name = "dire wolf"
  HP = 110
  currentHP = int(HP)
  MP = 0
  currentMP = int(MP)
  strength = 10
  intelligence = 6
  stamina = 9
  luck = 6
  agility = 10
  XP = 135
  @staticmethod
  def attack():
    attackstrength = random.randint(8, 11)*(math.ceil(direWolf.agility/2))
    attackdamage = attackstrength - player.armorPower
    if attackdamage <= 0:
      print "The dire wolf lunges towards %s but fails to do any damage!" % player.Name
    else:
      print "The dire wolf bites at %s, dealing %d damage!" % (player.Name, attackdamage)
      player.currentHP = player.currentHP - attackdamage

class grimKnight:
  Name = "grim knight"
  HP = 666
  currentHP = int(HP)
  MP = 0
  currentMP = int(MP)
  strength = 45
  intelligence = 10
  stamina = 32
  luck = 19
  agility = 22
  XP = 2200
  @staticmethod
  def attack():
    attackroll = random.randint(1, 5)
    if attackroll <= 2:
      attackstrength = (random.randint(5, grimKnight.strength)+10) - player.armorPower
      if attackstrength <= 0:
        print "The masked knight's blade bounces off %s's armor" % player.Name
      else:
        print "The masked knight cleaves %s with his polearm, dealing %d damage!" % (player.Name, attackstrength)
        player.currentHP = player.currentHP - attackstrength
    elif attackroll <= 4:
      attackstrength = random.randint(math.floor(grimKnight.stamina*2), math.ceil(grimKnight.stamina*3))
      print "The masked knight absorbs %d HP from %s!" % (attackstrength, player.Name)
      player.currentHP = player.currentHP - attackstrength
      if grimKnight.currentHP >= grimKnight.HP:
        grimKnight.currentHP = grimKnight.HP
    else:
      print "The masked knight laughs confidently."

class holySlime:
  Name = "holy slime"
  HP = 1000
  currentHP = int(HP)
  MP = 200
  currentMP = int(MP)
  strength = 19
  intelligence = 52
  stamina = 22
  luck = 10
  agility = 17
  XP = 2600
  @staticmethod
  def attack():
    attackroll = random.randint(1, 6)
    if attackroll <= 2 and holySlime.currentMP == 200: #and checks for two conditions to be true. in this case, it checks that both attackroll is less than or equal to 2 and that the holy slime's MP is 200.
			attackstrength = random.randint(holySlime.currentMP, 3*holySlime.currentMP)
			print "The holy slime lets loose its full power of light! %s takes %d damage !" % (player.Name, attackstrength)
			player.currentHP = player.currentHP - attackstrength
			holySlime.currentMP = 0
    elif attackroll <= 4:
      attackstrength = random.randint(12, 22)
      print "The holy slime spits a ray of light at %s, dealing %d damage!" % (player.Name, attackstrength)
      player.currentHP = player.currentHP - attackstrength
    elif attackroll <= 6 and holySlime.currentMP >= 15:
      attackstrength = random.randint(math.floor(holySlime.strength/2), holySlime.strength)+11
      print "The holy slime slices %s with a beam of pure light, deling %d damage to both HP and MP!" (player.Name, attackstrength)
      player.currentHP = player.currentHP - attackstrength
      player.currentMP = player.currentMP - attackstrength
      if player.currentMP <= 0:
        player.currentMP = 0
      holySlime.currentMP = holySlime.currentMP - 15
      if holySlime.currentMP <= 0:
        holySlime.currentMP = 0