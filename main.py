import os
from enemies import *
from items import *
from magic import *
from weapons import *
from armor import *


#generates a random list of enemies from a set of enemies the programmer chooses. Andrew Bannon
def randomEncounter(enemyList):
    encounteredEnemies = []
    enemyListMax = len(enemyList) - 1
    for num in range(3):
        enemyEncountered = enemyList[(random.randint(0, enemyListMax))]
        if enemyEncountered not in encounteredEnemies:
            print "%s ran into a %s!" % (player.Name, enemyEncountered.Name)
            encounteredEnemies.append(enemyEncountered)
    return encounteredEnemies


#The battle system, with 6 core commands. Uses elifs to check which command the player uses. Issues an invalid command message if the command is not in the elifs. Andrew Bannon
def battleSystem(enemyList):
    fullEnemyList = list(enemyList)
    encounteredMonsterNames = []
    for enemy in enemyList:
        encounteredMonsterNames.append(enemy.Name)
    while True:
        print "What would %s like to do?" % player.Name
        #asks the player for a command, like zork.
        playerAction = raw_input()
        #target selection for physical attacks. Improved version of Python Quest II's targeting.
        if playerAction == "attack":
            print "Which enemy from the list below would %s like to attack? (type 1 for the first enemy and so on)" % player.Name
            for monster in enemyList:
                print monster.Name
            try:
                attackTarget = input()
                attackTarget = int(attackTarget)
                player.attack(enemyList[attackTarget - 1])
                #checks if the player died
                if enemyTurn(enemyList, fullEnemyList) == True:
                    return True
                #checks if all enemies died.
                if enemyList == []:
                    break
            except:
                print "Invalid target!"
        #shows the player their stats and equipment
        elif playerAction == "check":
            player.status()
            if enemyList == []:
                break
        #lets the player use items.
        elif playerAction == "item":
            player.itemMenu()
            if enemyTurn(enemyList, fullEnemyList) == True:
                return True
            if enemyList == []:
                break
        #allows the player to run away
        elif playerAction == "run":
            if player.run(enemyList) == True:
                break
            else:
                print "You failed to run away!"
                if enemyTurn(enemyList, fullEnemyList) == True:
                    return True
                if enemyList == []:
                    break
        #shows the player their spell list and allows them to select one. shows spell cost, targeting type, and name
        elif playerAction == "spells":
            for spell in player.availableSpellClasses:
                print "Name: %s | MP Cost: %d | Target: %s" % (
                    spell.Name, spell.spellCost, spell.Target)
            print "Which spell from the list below would %s like to use? (type 1 for the first spell and so on)" % player.Name
            spellIndex = input()
            try:
                #target filtration for spells.
                spellIndex = int(spellIndex)
                spellSelected = player.availableSpellClasses[spellIndex - 1]
                print "You selected %s." % spellSelected.Name
                if spellSelected.Target == "Single Enemy":
                    print "Which enemy from the list below would %s like to attack? (type 1 for the first enemy and so on)" % player.Name
                    for monster in enemyList:
                        print monster.Name
                    attackTarget = input()
                    try:
                        #converts the input into an integer and uses that to get the proper spell target.
                        attackTarget = int(attackTarget)
                        #calls the spell's useSpell function.
                        spellSelected.useSpell(enemyList[attackTarget - 1])
                        if enemyTurn(enemyList, fullEnemyList) == True:
                            return True
                        if enemyList == []:
                            break
                    except:
                        print "Invalid target!"
                elif spellSelected.Target == "Player":
                    spellSelected.useSpell()
                    if enemyTurn(enemyList, fullEnemyList) == True:
                        return True
                    if enemyList == []:
                        break
                elif spellSelected.Target == "All Enemies":
                    #runs the spell's effect function on each enemy in battle once.
                    for enemy in enemyList:
                        spellSelected.useSpell(enemy)
                    #spell cost subtraction is calculated after the loop to avoid subtracting the spell's MP cost more than once
                    player.currentMP = player.currentMP - spellSelected.spellCost
                    if player.currentMP <= 0:
                        player.currentMP = 0
                    #returns true if the player dies. Used in the room scripts to load checkpoints and give specific endings.
                    if enemyTurn(enemyList, fullEnemyList) == True:
                        return True
                    if enemyList == []:
                        break
            except:
                print "Invalid spell!"
        #tells the player the command list.
        elif playerAction == "help":
            print """
      spells: casts a spell from your list of known spells
      attack: attacks a chosen enemy with your weapon
      check: full stat readout including equipped gear
      item: uses an item from your inventory
      run: tries to run away from the encounter
      clear: clears the screen
      """
        elif playerAction == "clear":
            clearScreen()
        else:
            print "Invalid command!"


#Checks if either an enemy or the player died. If an enemy dies, it is removed from the list. Andrew Bannon
def deathCheck(enemyList, fullEnemyList):
    if player.currentHP <= 0:
        print "%s died!" % player.Name
        return True
    for monsterClass in enemyList:
        if monsterClass.currentHP <= 0:
            print "The %s died!" % monsterClass.Name
            enemyList.remove(monsterClass)
            if enemyList == []:
                deathRoutine(fullEnemyList)


#Calculates XP and resets monster current HP and MP to their maximums. Also checks if the player is eligible for leveling up. Andrew Bannon
def deathRoutine(enemyList):
    totalXP = 0
    for monsterClass in enemyList:
        totalXP = totalXP + monsterClass.XP
        monsterClass.currentHP = monsterClass.HP
        monsterClass.currentMP = monsterClass.MP
    print "All enemies died! %s gained %d XP!" % (player.Name, totalXP)
    player.currentXP = player.currentXP + totalXP
    i = 0
    while True:
        if player.currentXP >= 4 * (player.level**3) + 20:
            player.levelup()
            i = i + 1
        else:
            break
    xpNeeded = (4 * (player.level)**3 + 20) - player.currentXP
    print "%s needs %d XP to advance to the next level." % (player.Name,
                                                            xpNeeded)


#Lets enemies use their attack functions, which are sandwiched between death checks to avoid glitches where enemies would stay alive for one more turn than normal. Andrew Bannon
def enemyTurn(enemyList, fullEnemyList):
    if deathCheck(enemyList, fullEnemyList) == True:
        return True
    for enemy in enemyList:
        enemy.attack()
    if deathCheck(enemyList, fullEnemyList) == True:
        return True


#lets the player enter a name and weapon preference, then calls the difficulty selector. Weapon preferences have a major effect on HP and MP, due to HP and MP increasing more slowly than they do in Python Quest II. HP and MP increases are derived from stamina and intelligence, so sword users will have much higher average HP than magic users.
def characterCreation():
    print "Greetings, mortal. What is your name?"
    player.Name = raw_input()
    print "I see. You are %s." % player.Name
    print "I must warn you that you cannot change this next decision."
    print "%s, do you prefer magic, sword, or neither?" % player.Name
    while True:
        preference = raw_input()
        if preference == "magic":
            print "Very well, %s. You seem to prefer devastating enemies with spells." % player.Name
            player.MP = player.MP + 25
            player.HP = player.HP - 5
            player.intelligence = player.intelligence + 6
            player.stamina = player.stamina - 2
            player.agility = player.agility - 4
            player.luck = player.luck + 4
            player.currentHP = player.HP
            player.currentMP = player.MP
            player.addSpell(spark)
            break
        elif preference == "sword":
            print "Very well, %s. You seem to prefer the blade above all else." % player.Name
            player.HP = player.HP + 25
            player.MP = player.MP - 10
            player.stamina = player.stamina + 4
            player.agility = player.agility + 6
            player.intelligence = player.intelligence - 3
            player.luck = player.luck - 4
            player.currentHP = player.HP
            player.currentMP = player.MP
            break
        elif preference == "neither":
            print "Most intriguing, %s." % player.Name
            break
    difficultySelector()
    print "Take this healing spell. May it aid you on your journey, %s." % player.Name
    player.addSpell(heal)


#gives difficulty options to the player. Hard and Insane add levels to the player but don't actually increase the player's stats. A byproduct of that is that said characters take longer to level due to required XP being calculated from the player's level
def difficultySelector():
    while True:
        print """ %s, please state the difficulty of your quest. There are 4 options:
      easy
      normal
      hard
      insane
      """ % player.Name
        diff = raw_input()
        if diff == 'easy':
            player.currentXP = 100
            player.level = player.level - 1
            print "%s, it seems like you want a simpler quest. Very well." % player.Name
            break
        elif diff == 'normal':
            player.currentXP = 0
            print "A run-of-the-mill quest, %s? Most uninteresting." % player.Name
            break
        elif diff == 'hard':
            player.level = player.level + 2
            print "%s, have fun testing your skills in the fields of battle." % player.Name
            break
        elif diff == 'insane':
            player.level = player.level + 4
            print "You are truly a brave soul, %s. Good luck." % player.Name
            break
        else:
            print "%s, I did not understand your selection." % player.Name


def clearScreen():
    os.system('clear')


#defines the rooms and what happens inside of them. Andrew did most of them, josh did the last few.


class room1:
    roomNumber = 1

    @staticmethod
    def roomScript():
        print "%s walks into the center of a field of grass. The blades of grass line up perfectly with the horizon in the sky. It seems like a peaceful environment." % player.Name
        if random.randint(1, 3) == 3:
            print "%s sits down to take in the sights in front, but is assaulted by monsters!" % player.Name
            if battleSystem(randomEncounter([slime, wolf])) == True:
                print "%s is bloodied and disheveled due to the monsters' attacks, and flees to the coast." % player.Name
                player.currentHP = 1
                room3.roomScript()
            else:
                print "%s beats back the enemies and contemplates his next move. Before %s can do that, %s finds a scrawled piece of paper with a lightning bolt on it, and learned spark!" % (
                    player.Name, player.Name, player.Name)
                print "Where to, %s? The coast, the mountains, or the deep sea?" % player.Name
                choice = raw_input()
                if choice == "coast":
                    room3.roomScript()
                elif choice == "mountains":
                    room4.roomScript()
                elif choice == "deep sea":
                    room2.roomScript()
        else:
            if random.randint(1, 8) == 8:
                print "It truly is a peaceful environment. %s finds a bow laying on the dirt. Take it?" % player.Name
                if raw_input() == "yes":
                    print "%s takes the bow and puts it away." % player.Name
                    player.weaponName = bow.name
                    player.weaponPower = bow.weaponPower
                    print "Where to, %s? The coast, the mountains, or the deep sea?" % player.Name
                    choice = raw_input()
                    if choice == "coast":
                        room3.roomScript()
                    elif choice == "mountains":
                        room4.roomScript()
                    elif choice == "deep sea":
                        room2.roomScript()
                else:
                    print "%s lets the bow be. Maybe it should stay there." % player.Name
                    print "Where to, %s? The coast, the mountains, or the deep sea?" % player.Name
                    choice = raw_input()
                    if choice == "coast":
                        room3.roomScript()
                    elif choice == "mountains":
                        room4.roomScript()
                    elif choice == "deep sea":
                        room2.roomScript()
            else:
                print "Where to, %s? The coast, the mountains, or the deep sea?" % player.Name
                choice = raw_input()
                if choice == "coast":
                    room3.roomScript()
                elif choice == "mountains":
                    room4.roomScript()
                elif choice == "deep sea":
                    room2.roomScript()


class room2:
    roomNumber = 2

    @staticmethod
    def roomScript():
        print "%s takes a dive underwater and sees a robot staring menacingly. The robot's sound system begins whirring. The phrase 'Omega Mk. CL' is written on its upper right leg." % player.Name
        print """
      >> DIFFICULTY TERMINAL READY
      >> MISSILE BAY ONLINE
      >> ANTIMAGIC FIELD GENERATOR AT 100%
      >> WATERPROOF PLATING ACTIVE
      >> READY TO TERMINATE PLAYER
    """
        print "Challenge the robot?"
        if raw_input() == "yes":
            player.roomNumber = room2.roomNumber
            if battleSystem([omegaMKCL]) == True:
                print "Omega Mk. CL delays finishing %s off for a few seconds. Its sound system begins whirring again." % player.Name
                print """
        >> PLAYER INCAPACITATED
        >> READYING SHOCK BAY
        >> SHOCK BAY AT 250% POWER"""
                print "%s is electrocuted by Omega Mk. CL and does not live to tell the tale. Game over." % player.Name
                exit()
            else:
                print "Go back to the fields?" % player.Name
                choice = raw_input()
                if choice == "yes":
                    room1.roomScript()
                else:
                    print "%s decides to go to the mountains instead."
                    room4.roomScript()
        else:
            print "%s leaves the robot alone, and it seems to appreciate that. Go back to the fields?" % player.Name
            choice = raw_input()
            if choice == "yes":
                room1.roomScript()
            else:
                print "%s decides to go to the mountains instead." % player.Name
                room4.roomScript()


class room3:
    roomNumber = 3

    @staticmethod
    def roomScript():
        print "%s arrives at a stunning coastline. The water looks fantastic, and the environment is picturesque." % player.Name
        if random.randint(1, 10) <= 6:
            print "But %s gets assaulted by monsters!" % player.Name
            if battleSystem(randomEncounter([pinkslime, wolf,
                                             wizard])) == True:
                print "%s lies in a heap on the coast." % player.Name
            loadCheckpoint()
        print "%s finds an old book detailing how to channel magic into raw orbs, and learns the orb spell!" % player.Name
        if orb not in player.availableSpellClasses:
            player.addSpell(orb)
        print "%s sees two landmarks in the distance: a distant volcano and a small fortress. %s also sees the mountains nearby. Where would %s like to go?" % (
            player.Name, player.Name, player.Name)
        choice = raw_input()
        if choice == "mountains":
            room4.roomScript()
        elif choice == "fortress":
            room5.roomScript()
        elif choice == "volcano":
            room6.roomScript()


class room4:
    roomNumber = 4

    @staticmethod
    def roomScript():
        print "%s reaches the mountaintop and sees the fields, sea, and coast laid out perfectly. %s finds a handy steel blade nearby. Take it?" % (
            player.Name, player.Name)
        choice = raw_input()
        if choice == "yes":
            print "%s picks up the steel blade and thinks it's a little heavy." % player.Name
            player.weaponPower = steelBlade.weaponPower
            player.weaponName = steelBlade.name
        else:
            print "%s leaves the blade alone and stands up to begin exiting. %s sees a volcano  behind and a small fortress to the left." % (
                player.Name, player.Name)
        if random.randint(1, 5) <= 2:
            print "%s's route is blocked by some monsters!" % player.Name
            if battleSystem(randomEncounter([squire, wizard])) == True:
                print "%s loses his balance and falls off the mountain." % player.Name
                loadCheckpoint()
            else:
                print "Would %s like to investigate the volcano, investigate the fortress, or head back to the fields?" % player.Name
                choice = raw_input()
                if choice == "fields":
                    room1.roomScript()
                elif choice == "fortress":
                    room5.roomScript()
                elif choice == "volcano":
                    room6.roomScript()
        else:
            print "Would %s like to investigate the volcano, investigate the fortress, or head back to the fields?" % player.Name
            choice = raw_input()
            if choice == "fields":
                room1.roomScript()
            elif choice == "fortress":
                room5.roomScript()
            elif choice == "volcano":
                room6.roomScript()


class room5:
    roomNumber = 5

    @staticmethod
    def roomScript():
        print "The fortress looms in front of %s, presenting a challenge. %s finds an elixir on the snowy floor nearby. %s also finds an explosion tome!" % (
            player.Name, player.Name, player.Name)
        player.addItem(elixir)
        if explosion not in player.availableSpellClasses:
            player.addSpell(explosion)
        print "A slime wearing a crown halts %s. Despite his inherently big smile, he manages to give %s the most menacing look of all time. It rushes %s before %s can react!" % (
            player.Name, player.Name, player.Name, player.Name)
        player.roomNumber = room4.roomNumber  # places the player back at the mountains if they die.
        enemyList = [slime, pinkslime, kingslime]
        if battleSystem(enemyList) == True:
            print "The king slime has slain %s." % player.Name
            loadCheckpoint()
        else:
            print "%s defeats the king slime. %s finds another elixir inside its goop, along with a soaked book. %s learns drain!" % (
                player.Name, player.Name, player.Name)
            if drain not in player.availableSpellClasses:
                player.addSpell(drain)
            player.addItem(elixir)
            print "Head deeper into the fortress or head back to the mountains?"
            if raw_input() == "head deeper":
                room7.roomScript()
            elif raw_input() == "mountains":
                room4.roomScript()


class room6:
    roomNumber = 6

    @staticmethod
    def roomScript():
        print "%s walks up to the base of the volcano and sees hardened magma all around the area. %s is then challenged by monsters!" % (
            player.Name, player.Name)
        if battleSystem(randomEncounter([pinkslime, pyromancer,
                                         wizard])) == True:
            print "%s loses to the group of monsters." % player.Name
            loadCheckpoint()
        else:
            print "The monsters were nice enough to leave behind a book detailing the procedure of manipulating fire and a nice suit of armor! %s learned flame burst and got the steel armor!" % player.Name
            if flameBurst not in player.availableSpellClasses:
                player.addSpell(flameBurst)
            player.armorPower = steelArmor.armorPower
            player.armorName = steelArmor.name
            print "%s remembers the fortress lingering in the distance, and also sees a second floor of the fortress. At the same time, %s sees the upper levels of the volcano. Head to the upper floor of the fortress, the lower floor, or go further up the volcano?" % (
                player.Name, player.Name)
            choice = raw_input()
            if choice == "upper floor":
                room7.roomScript()
            elif choice == "lower floor":
                room5.roomScript()
            elif choice == "go further up":
                room8.roomScript()


class room7:
    roomNumber = 7

    @staticmethod
    def roomScript():
        print "%s enters the second floor of the fortress. A band of slimes challenges %s to a battle!" % (
            player.Name, player.Name)
        if battleSystem(randomEncounter([redSlime, slimeSwordsman])) == True:
            print "%s is defeated by the band of slimes." % player.Name
            loadCheckpoint()
        else:
            for battleNumber in range(4):
                battleList = randomEncounter([redSlime, pinkslime, slime])
                if battleSystem(battleList) == True:
                    print "%s is defeated by slime group number %d" % (
                        player.Name, battleNumber)
                    loadCheckpoint()
                else:
                    if random.randint(1, 5) == 4:
                        print "%s finds a mana vial!" % player.Name
                        player.addItem(manaVial)
                    else:
                        print "%s finds nothing interesting here." % player.Name
            print "it seems like you've seen everything there is on this floor. There are two stairways leading up to the third floor. Take the left stairway or the right stairway?"
            choice = raw_input()
            if choice == "left stairway":
                room9.roomScript()
            else:
                room10.roomScript()


class room8:
    roomNumber = 8

    @staticmethod
    def roomScript():
        print "%s stands on a small strip of ground on the midpoint of the volcano. Monsters assault %s from all sides!" % (
            player.Name, player.Name)
        if battleSystem(randomEncounter([redSlime, pyromancer])) == True:
            print "%s gets knocked down to the mountains." % player.Name
            player.currentHP = 1
            room4.roomScript()
        print "%s finds a suspicious door on another strip of land a few feet away. However, a masked knight seems to be guarding it. Fight the knight or go back to the mountains?" % player.Name
        choice = raw_input()
        if choice == 'fight the knight':
            room11.roomScript()
        elif choice == 'mountains':
            room4.roomScript()


class room9:
    roomNumber = 9

    @staticmethod
    def roomScript():
        print "Slimes assail %s from all directions!" % player.Name
        enemyList = randomEncounter([redSlime, slimeSwordsman])
        if battleSystem(enemyList) == True:
            print "%s is taken down by the slimes." % player.Name
            loadCheckpoint()
        else:
            print "%s reaches the third floor of the fortress. There is a long hallway ahead, and a staircase to the fourth floor there. There is also a ladder that leads out of the fortress. Use the ladder or go through the hallway?" % player.Name
            choice = raw_input()
            if choice == "ladder":
                room4.roomScript()
            else:
                for battleNumber in range(5):
                    enemyList = randomEncounter([redSlime, slimeSwordsman])
                    if battleSystem(enemyList) == True:
                        print "%s is taken down by the slimes." % player.Name
                        loadCheckpoint()
                    else:
                        print "%s pushes deeper into the hallway." % player.Name
                room12.roomScript()


class room10:
    roomNumber = 10

    @staticmethod
    def roomScript():
        print "%s arrives in a round room with a table in the center. A seemingly rare suit of armor catches %s's eye. Take it?" % (
            player.Name, player.Name)
        choice = raw_input()
        if choice == "yes":
            print "%s got the regal armor!" % player.Name
            player.armorPower = regalArmor.armorPower
            player.armorName = regalArmor.name
        print "%s takes a look around and sees a slime bursting with electricity, and another slime with the power of fire guarding a staircase. They would like to battle. Do battle with them?" % player.Name
        choice = raw_input()
        if choice == "yes":
            enemyList = [redSlime, shockingSlime]
            if battleSystem(enemyList) == True:
                print "%s loses to the pair." % player.Name
                loadCheckpoint()
            elif battleSystem != True and enemyList != []:
                print "The slimes laugh in their language at %s's cowardice." % player.Name
                print "Should %s go downstairs or use the ladder leading out?" % player.Name
                choice = raw_input()
                if choice == "go downstairs":
                    room7.roomScript()
                elif choice == "use the ladder":
                    room4.roomScript()
            else:
                print "Should %s go downstairs, use the ladder leading out, or go upstairs?" % player.Name
                choice = raw_input()
                if choice == "go downstairs":
                    room7.roomScript()
                elif choice == "use the ladder":
                    room4.roomScript()
                else:
                    room13.roomScript()
        print "%s chooses not to battle the slimes." % player.Name
        print "Should %s go downstairs or use the ladder leading out?" % player.Name
        choice = raw_input()
        if choice == "go downstairs":
            room7.roomScript()
        elif choice == "use the ladder":
            room4.roomScript()


class room11:
    roomNumber = 11

    @staticmethod
    def roomScript():
        player.roomNumber = 8  # places the player back at the room before the masked knight battle if they die.
        print "%s makes the leap over to the door. The masked knight challenges %s to a battle!" % (
            player.Name, player.Name)
        enemyList = [maskedKnight]
        if battleSystem(enemyList) == True:
            print "The masked knight takes a long look at %s. He decides that keeping his target alive isn't worth it and rolls you down the volcano. Game over." % player.Name
            exit()  #terminates the program, or in this case ends the game.
        elif battleSystem != True and enemyList != []:  #!= is "not equal to." Checks if the player didn't kill every enemy in battle and did not die, which means the player ran away.
            print "The masked knight is not impressed at that act of cowardice but lets %s go anyway." % player.Name
        else:
            print "The masked knight lies helpless on the floor. His polearm lies on the ground next to him. Take it?"
            choice = raw_input()
            if choice == "yes":
                print "%s picks up the polearm from the floor." % player.Name
                player.weaponName = polearm.name
                player.weaponPower = polearm.weaponPower
        print "Enter the door, go to the fortress, or go down the volcano?"
        choice = raw_input()
        if choice == "enter the door":
            room14.roomScript()
        elif choice == "fortress":
            room5.roomScript()
        else:
            room8.roomScript()


class room12:
    roomNumber = 12

    @staticmethod
    def roomScript():
        print "%s reaches a door and opens it to reveal a mana vial inside!" % player.Name
        player.addItem(manaVial)
        print "%s looks around the rest of the room. A shocking slime pops out of a drawer and challenges %s!" % (
            player.Name, player.Name)
        enemyList = [shockingSlime]
        if battleSystem(enemyList) == True:
            print "%s is beaten by the shocking slime." % player.Name
            loadCheckpoint()
        else:
            print "%s successfully deals with the shocking slime. Its red slime brother tries to get revenge!" % player.Name
            enemyList = [redSlime]
            if battleSystem(enemyList) == True:
                print "The red slime decimates %s." % player.Name
                loadCheckpoint()
            else:
                if windStorm.Name not in player.availableSpells:
                    player.addSpell(windStorm)
                print "%s finds a manuscript left behind in a basket. %s learned wind storm!" % (
                    player.Name, player.Name)
                print "%s sees a ladder leading to a fourth floor, a door to the other end of the floor, and a torch-lit entrance to what seems to be a throne room." % player.Name
                print "Should %s go to the other end of the floor, go to the throne room, or use the ladder?" % player.Name
                choice = raw_input()
                if choice == "go to the other end":
                    room13.roomScript()
                elif choice == "throne room":
                    room15.roomScript()
                else:
                    room16.roomScript()


class room13:
    roomNumber = 13

    @staticmethod
    def roomScript():
        print "%s arrives at the fourth floor of the fortress, and sees a king slime wishing to do battle. However, his companions have gotten stronger. Challenge them?" % player.Name
        choice = raw_input()
        if choice == "yes":
            enemyList = [kingslime, slimeSwordsman, shockingSlime]
            if battleSystem(enemyList) == True:
                print "%s loses to the royal squad." % player.Name
                loadCheckpoint()
            elif battleSystem != True and enemyList != []:
                print "The slimes are unimpressed at that act of cowardice. They block the way to the throne room."
                print "Use the portal or go downstairs?"
                choice = raw_input()
                if choice == "use the portal":
                    room1.roomScript()
                else:
                    room10.roomScript()
            else:
                print "After a grueling battle, %s seems interested in the throne room, but also sees a kind of portal leading to a field. Use the portal ,go to the throne room, or go downstairs?" % player.Name
                choice = raw_input()
                if choice == "use the portal":
                    room1.roomScript()
                elif choice == "throne room":
                    room15.roomScript()
                else:
                    room10.roomScript()
            print "The slimes laugh and refuse entry to the throne room."
            print "Use the portal or go downstairs?"
            choice = raw_input()
            if choice == "use the portal":
                room1.roomScript()
            else:
                room10.roomScript()


class room14:
    roomNumber = 14

    @staticmethod
    def roomScript():
        print "%s enters the door and sees molten rock flowing along the walls, and a fountain full of crystal-clear water. %s steps in, and HP and MP are fully restored!" % (
            player.Name, player.Name)
        player.currentHP = player.HP
        player.currentMP = player.MP
        print "A large group of monsters assaults %s!" % player.Name
        enemyList = randomEncounter(
            [redSlime, slimeSwordsman, pyromancer, wizard, pinkslime])
        if battleSystem(enemyList) == True:
            print "%s loses to the monsters!" % player.Name
            loadCheckpoint()
        elif battleSystem(enemyList) != True and enemyList != []:
            print "The monsters are mad at %s's cowardice and kick you out!" % player.Name
            room8.roomScript()
        else:
            print "The monsters lie defeated around %s. There is a ladder down to a deeper level of the volcano. There is also a door to another room on the same level, and an exit leading to the mountains. Use the door, take the exit, or use the ladder?" % player.Name
            choice = raw_input()
            if choice == "door":
                room17.roomScript()
            elif choice == "ladder":
                room18.roomScript()
            else:
                room4.roomScript()


class room15:
    roomNumber = 15

    @staticmethod
    def roomScript():
        player.roomNumber = 13
        print "%s enters a throne room and sees a large throne ahead. The room seems completely empty. As %s walks out, a rainbow slime attacks from behind!" % (
            player.Name, player.Name)
        if battleSystem([rainbowSlime]) == True:
            print "The rainbow slime uses its ooze to throw %s into a trash can." % player.Name
            loadCheckpoint()
        else:
            print "The rainbow slime lies defeated in front of %s. A sword of destruction lies inside its goop. Take it?" % player.Name
            choice = raw_input()
            if raw_input() == "yes":
                print "%s took the sword of destruction!" % player.Name
                player.weaponName = swordOfDestruction.name
                player.weaponPower = swordOfDestruction.weaponPower
            print "%s sees the ladder from before, along with an entrance to what seems to be a volcano. Go to the volcano or use the ladder?"
            choice = raw_input()
            if choice == "use the ladder":
                room16.roomScript()
            else:
                room14.roomScript()


class room16:
    roomNumber = 16

    @staticmethod
    def roomScript():
        print "%s reaches what seems to be the top floor of the fortress. The fortress has a nice view of the world below. A red slime attacks %s!" % (
            player.Name, player.Name)
        enemyList = [redSlime]
        if battleSystem(enemyList) == True:
            print "%s loses to the red slime." % player.Name
            loadCheckpoint()
        else:
            print "%s beats the red slime. %s sees the ladder back down, as well as what seems to be an elevator leading to the second floor. Use the ladder or use the elevator?"
            choice = raw_input()
            if choice == "elevator":
                room7.roomScript()
            else:
                room12.roomScript()


class room17:
    roomNumber = 17

    @staticmethod
    def roomScript():
        lost = False  #sets the variable that checks if the player lost the battle to false. This battle is refightable.
        print "%s walks into a wide chamber made of volcanic rock. %s is assaulted by a group of red slimes!" % (
            player.Name, player.Name)
        for battleNumber in range(5):
            enemyList = [
                redSlime
            ]  #regenerates the red slime after each fight, because the battle system edits the list directly when it eliminates the red slime on death.
            if battleSystem(enemyList) == True:
                lost = True  # lets the game know that the player lost and exits the battle loop.
                break
        if lost == True:
            print "The red slimes descend on %s, leaving a badly burnt human in their wake. Game over." % player.Name  #gives a bad ending then kills the game.
            exit()
        else:
            print "%s solved the red slime problem. Go back to the previous room or use the ladder nearby?" % player.Name
            choice = raw_input()
            if choice == "use the ladder":
                room18.roomScript()
            else:
                room14.roomScript()


class room18:
    roomNumber = 18

    @staticmethod
    def roomScript():
        print "%s enters a deeper level of the volcano. Monsters descend from the ladder and battle %s!" % (
            player.Name, player.Name)
        if battleSystem([direWolf, pyromancer, shockingSlime]) == True:
            print "%s gets knocked back into a wall of volcanic rock!" % player.Name
            loadCheckpoint()
        else:
            print "%s looks at the walls and finds 3 doors, one red, one blue, and one yellow. Which one would %s like to go through?"
            choice = raw_input()
            if choice == "yellow door":
                room19.roomScript()
            elif choice == "red door":
                room20.roomScript()
            else:
                room21.roomScript()


class room19:
    roomNumber = 19
    levelBookUsed = False

    @staticmethod
    def roomScript():
        if room19.levelBookUsed == False:
            print "%s enters the yellow door and sees a desert, devoid of all life except the occasional cactus. Something catches %s's eye: A book detaling how to gain 2 levels!" % (
                player.Name, player.Name)
            player.levelup()
            player.levelup()
            room19.levelBookUsed = True
        else:
            print "%s enters the yellow door and sees a desert, devoid of all life except the occasional cactus."
        print "There is a cave to the east and what seems to be an ice plain to the north. Enter the cave, go to the ice plain, or go back through the door?"
        choice = raw_input()
        if choice == "cave":
            room22.roomScript()
        elif choice == "ice plain":
            room23.roomScript()
        else:
            room18.roomScript()


class room20:
    roomNumber = 20
    powerBookUsed = False  #tells the game if this room's special book has been used.

    @staticmethod
    def roomScript():
        if room20.powerBookUsed == False:
            print "%s enters the red door and sees a large field of red grass. The field is devoid of monsters, but something catches %s's eye: A book detaling how to make strikes stronger and faster." % (
                player.Name, player.Name)
            # gives the player some stat bonuses then sets the powerBookUsed variable to True.
            player.agility = player.agility + 10
            player.strength = player.strength + 10
            room20.powerBookUsed = True
        else:
            print "%s enters the red door and sees a large field of red grass devoid of monsters." % player.Name
        print "There is a hill to the north and a forest to the west. Enter the forest, go on the hill, or go back through the door?"
        choice = raw_input()
        if choice == "hill":
            room24.roomScript()
        elif choice == "forest":
            room25.roomScript()
        else:
            room18.roomScript()


class room21:
    roomNumber = 21
    chestsOpened = False

    @staticmethod
    def roomScript():
        if room21.chestsOpened == False:
            print "%s enters through the blue door, and finds a few chests in the area. Would %s like to open them?" % (
                player.Name, player.Name)
            choice = raw_input()
            if choice == "yes":
                print "%s finds a mana shot and the maximillian!" % player.Name
                player.addItem(manaShot)
                player.armorPower = maximillian.armorPower
                player.armorName = maximillian.name
                room21.chestsOpened = True
                print "%s sees nothing else here and goes back through the door." % player.Name
                room18.roomScript()
            else:
                print "%s leaves the chests alone." % player.Name
                print "%s sees nothing else here and goes back through the door." % player.Name
                room18.roomScript()
        else:
            print "%s finds that the chests have been looted already." % player.Name
            room18.roomScript()


class room22:
    roomNumber = 22

    @staticmethod
    def roomScript():
        player.roomNumber = 18
        print "%s enters a cave. The cave is dark, grimy, and unpleasant. A knight wearing a bloodied suit of armor challenges %s to a battle." % (
            player.Name, player.Name)
        enemyList = [grimKnight]
        if battleSystem(enemyList) == True:
            print "%s has lost." % player.Name
            loadCheckpoint()
        else:
            print "%s destroys the grim knight as the cave inside crumbles to dust, and escapes to the desert above. %s has saved the land from the power of darkness, but another holier threat looms in another room..." % (
                player.Name, player.Name)
            exit()


class room23:
    roomNumber = 23

    @staticmethod
    def roomScript():
        player.roomNumber = 18
        print "%s enters the ice plain. A bright light shines in the distance. %s goes towards the light, and is challenged by the holy slime." % (
            player.Name, player.Name)
        enemyList = [holySlime]
        if battleSystem(enemyList) == True:
            print "%s has lost" % player.Name
            loadCheckpoint()
        else:
            print "%s destroys the holy slime as its divine radiance covers the ice plain in light. %s has saved the land from the evil light threatening it, but another, darker threat looms in another room..." % (
                player.Name, player.Name)
            exit()


class room24:
    roomNumber = 24
    chestsOpened = False

    @staticmethod
    def roomScript():
        if room24.chestsOpened == False:
            print "%s climbs to the top of the hill and finds a chest. Open it?" % player.Name
            choice = raw_input()
            if choice == "yes":
                print "%s finds an elixir!" % player.Name
                player.addItem(elixir)
                room24.chestsOpened = True
            else:
                print "%s leaves the chest alone" % player.Name
        else:
            print "%s sees that the chest has been looted already. Maybe it was the slimes?" % player.Name
        room20.roomScript()


class room25:
    roomNumber = 21
    intelligenceBookUsed = False

    @staticmethod
    def roomScript():
        if room25.intelligenceBookUsed == False:
            print "%s heads into a thick forest and finds a single book. It lists the details of casting more powerful spells!" % player.Name
            player.intelligence = player.intelligence + 20
            player.MP = player.MP + 20
            player.currentMP = player.MP
        else:
            print "%s has read this book already." % player.Name
        room18.roomScript()


def loadCheckpoint():  # andrew did this one
    enemyList = [
        slime, pinkslime, redSlime, shockingSlime, holySlime, rainbowSlime,
        kingslime, direWolf, grimKnight, maskedKnight, wolf, wizard,
        pyromancer, squire, slimeSwordsman, omegaMKCL
    ]
    for enemy in enemyList:
        enemy.currentHP = enemy.HP
        enemy.currentMP = enemy.MP
    roomList = [
        room1, room2, room3, room4, room5, room6, room7, room8, room9, room10,
        room11, room12, room13, room14, room15, room16, room17, room18, room19,
        room20, room21, room22, room23, room24, room25
    ]
    checkpoint = roomList[player.roomNumber - 1]
    player.currentHP = player.HP
    player.currentMP = player.MP
    checkpoint.roomScript()


characterCreation()
room1.roomScript()
