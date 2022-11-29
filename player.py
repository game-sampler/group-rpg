import random
import math


class player:  #Defining player attributes and actions (including leveling). Andrew Bannon did this module.
    #character statlines and equipped gear
    Name = "Mike"
    roomNumber = 1
    level = 1
    HP = 40
    currentHP = int(HP)
    MP = 40
    currentMP = int(MP)
    strength = 6
    agility = 6
    intelligence = 6
    stamina = 6
    luck = 6
    armorName = "simple armor"
    armorPower = 6
    weaponName = "iron sword"
    weaponPower = 4
    currentXP = 0
    #containers for player spells and what they do
    availableSpells = []
    availableSpellClasses = []
    #list of useable items (because we needed it) and their names (important for actually using them)
    items = []
    itemNames = []
    #allows the class functions to run without an implicit first argument (the class itself most of the time). An overview of what this does will be included in references
    @staticmethod
    #determines attack damage and inflicts it on the targeted enemy.
    def attack(enemyClass):
        attackstrength = random.randint(
            player.weaponPower + math.floor(player.strength / 6),
            math.floor(player.strength / 4) + player.weaponPower) * (
                math.floor(player.agility / 5) + 1)
        print "You attacked the %s with your %s, dealing %d damage!" % (
            enemyClass.Name, player.weaponName, attackstrength)
        enemyClass.currentHP = enemyClass.currentHP - attackstrength
        attackstrength = random.randint(
            player.weaponPower + math.floor(player.strength / 6),
            math.floor(player.strength / 4) + player.weaponPower) + math.floor(
                player.agility)

    @staticmethod
    #stat printouts plus current HP, MP, and equipped gear
    def status():
        print "Current level:", player.level
        print "Strength:", player.strength
        print "Agility:", player.agility
        print "Intelligence:", player.intelligence
        print "Stamina:", player.stamina
        print "Luck:", player.luck
        print "Max HP:", player.HP
        print "Max MP:", player.MP
        print "Current HP:", player.currentHP
        print "Current MP:", player.currentMP
        print "Equipped Weapon:", player.weaponName
        print "Equipped Armor:", player.armorName

    @staticmethod
    #levels the player up. Player xp is a function of the player's level, which is expressed in the monster death routine. Stat caps have been substantially reduced from python quest II due to being a shorter game, but HP and MP caps remain the same. HP and MP increase by less of the player's stamina and intelligence, respectively.
    def levelup():
        print "%s has advanced to level %d" % (player.Name, player.level + 1)
        player.level = player.level + 1
        if player.HP < 9999:
            print "%s's HP has increased by %d!" % (
                player.Name, math.floor(player.stamina * 0.8))
            player.HP = player.HP + math.floor(player.stamina * 0.8)
        else:
            print "%s's HP cannot go any higher!"
            player.HP = 999
        if player.MP < 999:
            print "%s's MP has increased by %d!" % (
                player.Name, math.floor(player.intelligence * .4))
            player.MP = player.MP + math.floor(player.intelligence * .4)
        else:
            print "%s's MP cannot go any higher!" % player.Name
            player.MP = 999
        statincrease = random.randint(1, 3)
        if player.stamina < 100:
            print "%s's Stamina increased by %d!" % (player.Name, statincrease)
            player.stamina = player.stamina + statincrease
        else:
            print "%s's stamina cannot go any higher!" % player.Name
            player.stamina = 100
        statincrease = random.randint(1, 3)
        if player.intelligence < 100:
            print "%s's Intelligence increased by %d!" % (player.Name,
                                                          statincrease)
            player.intelligence = player.intelligence + statincrease
        else:
            print "%s's intelligence cannot go any higher!" % player.Name
            player.intelligence = 100
        statincrease = random.randint(1, 3)
        if player.agility < 100:
            print "%s's Agility increased by %d" % (player.Name, statincrease)
            player.agility = player.agility + statincrease
        else:
            print "%s's agility cannot go any higher!" % player.Name
            player.agility = 100
        statincrease = random.randint(1, 3)
        if player.strength < 100:
            print "%s's Strength increased by %d!" % (player.Name,
                                                      statincrease)
            player.strength = player.strength + statincrease
        else:
            print "%s's strength cannot go any higher!" % player.Name
            player.strength = 100
        statincrease = random.randint(1, 3)
        if player.luck < 100:
            print "%s's Luck increased by %d!" % (player.Name, statincrease)
            player.luck = player.luck + statincrease
        else:
            print "%s's luck cannot go any higher!" % player.Name
            player.luck = 100
        player.currentHP = player.HP
        player.currentMP = player.MP

    @staticmethod
    #Adds a spell to the player (test it out with spark)
    def addSpell(spellClass):
        player.availableSpellClasses.append(spellClass)
        player.availableSpells.append(spellClass.Name)

    #Places an item into the player's inventory (items list)
    @staticmethod
    def addItem(itemClass):
        player.items.append(itemClass)
        player.itemNames.append(itemClass.name)

    #Removes an item from the player's inventory
    @staticmethod
    def removeItem(itemClass):
        player.items.remove(itemClass)
        player.itemNames.remove(itemClass.name)

    @staticmethod
    #Does the math behind running away. The implementation of it is in the main battle system.
    def run(monsterGrouping):
        totalAgility = 0
        for x in monsterGrouping:
            monsterClass = x
            totalAgility = totalAgility + monsterClass.agility
        if random.randint(-30, 50) + player.agility > 2 * totalAgility:
            print "You ran away"
            ranAway = True
            return ranAway
        else:
            ranAway = False
            return ranAway

    @staticmethod
    #Shows the player a list of their possessed items and asks them which one they would use. Calls the item's useItem function to get its effect, and then calls removeItem to take it out of the player's inventory
    def itemMenu():
        for item in player.items:
            print item.name
        print "Type 1 to use the first item in the list, and so on"
        try:
            itemIndice = int(input())
            if itemIndice > len(player.items):
                print "Invalid item index!"
            else:
                itemUsed = player.items[itemIndice - 1]
                itemUsed.useItem()
                player.removeItem(itemUsed)
        except:
            print "Invalid item index!"
