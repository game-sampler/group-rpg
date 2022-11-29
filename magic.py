#defines spells and what they do. spells are all written in the same format. Andrew Bannon did most spells, though Joshua Sumague helped significantly and came up with the base ideas behind the flame burst spell (originally icicle), and the spark spell (originally fireball). 
from player import *
class spark: # damages a single enemy with electricity
  #How much MP the spell costs
  spellCost = 5
  #How powerful it is (recalculated after each cast to ensure randomness)
  spellStrength = random.randint(10, 15) + math.floor(player.intelligence*2)
  #the spell's name, which is printed out when the player uses the "spells" command in battle.
  Name = "spark"
  #which character(s) the spell targets. Checked against with the spells command.
  Target = "Single Enemy"
  @staticmethod
  #The core of what the spell does. some spells can affect other things than HP, or have a chance to have an additional effect.
  def useSpell(enemyClass):
    if player.currentMP >= spark.spellCost:
      print "%s fires a small shock that hits the %s, dealing %d damage" % (player.Name, enemyClass.Name, spark.spellStrength)
      enemyClass.currentHP = enemyClass.currentHP - spark.spellStrength
      player.currentMP = player.currentMP - spark.spellCost
      if player.currentMP < 0:
        player.currentMP = 0
      spark.spellStrength = random.randint(10, 15) + math.floor(player.intelligence*2)
    else:
      print "You do not have enough MP!"

class drain:
  spellCost = 10 #damages an enemy and gives the HP to the user.
  spellStrength = random.randint(5, 10) + math.floor(player.intelligence*2.75)
  Name = "drain"
  Target = "Single Enemy"
  @staticmethod
  def useSpell(enemyClass):
		if player.currentMP >= drain.spellCost:
			print "%s leeches %d HP from the %s!" % (player.Name, drain.spellStrength, enemyClass.Name)
			enemyClass.currentHP = enemyClass.currentHP - drain.spellStrength
			player.currentHP = player.currentHP + drain.spellStrength
			if player.currentHP >= player.HP:
				player.currentHP = player.HP
			player.currentMP = player.currentMP - drain.spellCost
			if player.currentMP <= 0:
				player.MP = 0
		else:
			print "You do not have enough MP!"
		drain.spellStrength = random.randint(5, 10) + math.floor(player.intelligence*2.75)

class heal: #self-explanatory
  spellCost = 8
  spellStrength = random.randint(12, 18) + math.floor(player.intelligence*2)
  Name = "heal"
  Target = "Player"
  @staticmethod
  def useSpell():
    if player.currentMP >= heal.spellCost:
      print "%s gains %d HP!" % (player.Name, heal.spellStrength)
      player.currentHP = player.currentHP + heal.spellStrength
      player.currentMP = player.currentMP - heal.spellCost
      if player.currentHP > player.HP:
        player.currentHP = player.HP
      if player.currentMP <= 0:
        player.currentMP = 0
      heal.spellStrength = random.randint(12, 18)+math.floor(player.intelligence*2)
    else:
      print "You do not have enough MP!"

class explosion: #hits all enemies with an explosion
  spellCost = 15
  spellStrength = random.randint(10, 20)+math.floor(player.intelligence*2)
  Name = "explosion"
  Target = "All Enemies"
  @staticmethod
  def useSpell(enemyClass):
    if player.currentMP >= explosion.spellCost:
      explosion.spellStrength = random.randint(10, 20)+math.floor(player.intelligence*2)
      print "%s beckons forth a large explosion! The %s is caught in the blast and takes %d damage!" % (player.Name, enemyClass.Name, explosion.spellStrength)
      enemyClass.currentHP = enemyClass.currentHP - explosion.spellStrength
    else:
      print "You do not have enough MP!"

class orb: #hits a single target with an orb of pure magic. 30% chance to "crit" and do triple damage.
  spellCost = 20
  spellStrength = random.randint(8, 16)+math.floor(player.intelligence/2)
  Name = "orb"
  Target = "Single Enemy"
  @staticmethod
  def useSpell(enemyClass):
    if player.currentMP >= orb.spellCost:
      orb.spellStrength = random.randint(8, 16)+math.floor(player.intelligence/2)
      if random.randint(1, 10) >= 8:
        orb.spellStrength = orb.spellStrength*3
        print "%s assaults the %s with a mighty orb of magic, dealing %d damage!" % (player.Name, enemyClass.Name, orb.spellStrength)(player.Name, enemyClass.Name, orb.spellStrength)
        enemyClass.currentHP = enemyClass.currentHP - orb.spellStrength
        player.currentMP = player.currentMP - orb.spellCost
        if player.currentMP <= 0:
          player.currentMP = 0
      else:
        print "%s sends an orb of magic flying at the %s, dealing %d damage!" % (player.Name, enemyClass.Name, orb.spellStrength)
        enemyClass.currentHP = enemyClass.currentHP - orb.spellStrength
        player.currentMP = player.currentMP - orb.spellCost
        if player.currentMP <= 0:
          player.currentMP = 0
    else:
      print "You do not have enough MP!"

class flameBurst: #Hits a single target with lava. 50% chance to cause equivalent damage to the enemy's MP.
  spellCost = 30
  spellStrength = random.randint(12, 25) + math.floor(player.intelligence*3)
  Name = "flame burst"
  Target = "Single Enemy"
  @staticmethod
  def useSpell(enemyClass):
    if player.MP >= flameBurst.spellCost:
      flameBurst.spellStrength = random.randint(12, 25) + math.floor(player.intelligence*3)
      print "%s assails the %s with a burst of flame, dealing %d damage!" %  (player.Name, enemyClass.Name, flameBurst.spellStrength)
      enemyClass.currentHP = enemyClass.currentHP - flameBurst.spellStrength
      player.currentMP = player.currentMP - flameBurst.spellCost
      if player.currentMP <= 0:
        player.currentMP = 0
      if random.randint(1, 2) == 2:
        print "The flames roar into a blaze, making the enemy lose %d MP!" % flameBurst.spellStrength
        enemyClass.currentMP = enemyClass.currentMP - flameBurst.spellStrength      

class windStorm: #hits all enemies with a gust.
  spellCost = 45
  spellStrength = random.randint(9, 16)+math.floor(player.intelligence*3)
  Name = "wind storm"
  Target = "All Enemies"
  @staticmethod
  def useSpell(enemyClass):
    if player.currentMP >= windStorm.spellCost:
      windStorm.spellStrength = random.randint(9, 16)+math.floor(player.intelligence*3)
      print "%s summons a powerful gust! The %s is caught in the winds and takes %d damage!" % (player.Name, enemyClass.Name, windStorm.spellStrength)
      enemyClass.currentHP = enemyClass.currentHP - windStorm.spellStrength
    else:
      print "You do not have enough MP!"
   
