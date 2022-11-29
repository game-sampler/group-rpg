#defines items and what they do. player.removeItem is called after each use to remove the item from the player's inventory if the item's reusable flag is false.
#import with an asterisk after it from a module moves every class and function from the target module into the module it is placed in. Andrew Bannon did this module.
from player import *
class elixir:
  name = "elixir"
  Type = "Item"
  dealsDamage = False
  reusable = False
  target = "Player"
  @staticmethod
  def useItem():
    print "You drink the elixir. Your HP and MP are fully restored!"
    player.currentMP = player.MP
    player.currentHP = player.HP
class manaVial:
  name = "mana vial"
  Type = "Item"
  dealsDamage = False
  reusable = False
  target = "Player"
  @staticmethod
  def useItem():
    print "You drink the mana vial. You gain 30 MP!"
    player.currentMP = player.currentMP + 30
    if player.currentMP > player.MP:
      player.currentMP = player.MP
class potion:
  name = "potion"
  Type = "Item"
  dealsDamage = False
  reusable = False
  target = "Player"
  @staticmethod
  def useItem():
    print "You drink the potion, and you gain 30 HP!"
    player.currentHP = player.currentHP + 30
    if player.currentHP > player.HP:
      player.currentHP = player.HP
class manaShot:
  name = "mana shot"
  Type = "Item"
  dealsDamage = False
  reusable = False
  target = "Player"
  @staticmethod
  def useItem():
    print "You drink the mana vial. You gain 60 MP!"
    player.currentMP = player.currentMP + 60
    if player.currentMP > player.MP:
      player.currentMP = player.MP