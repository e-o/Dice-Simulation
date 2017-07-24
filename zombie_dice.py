# simulation of the Zombie Dice game from Steve Jackson Games.
from enum import Enum
import random
import os
import datetime
import time

class z_side(Enum):
    """ Each side of a Zombie Dice"""
    def __repr__(self):
        return str(self.name)
    Shotgun = 0
    Brains = 1
    Runner = 2

class zombie_dice():
    def __init__(self, colour="green"):
        self.colour = colour
        if colour == "green":
            brains, shotguns, runners = 3, 1, 2
        elif colour == "yellow":
            brains, shotguns, runners = 2, 2, 2
        else: # red
            brains, shotguns, runners = 1, 3, 2
        self.sides = [z_side.Brains] * brains + [z_side.Shotgun] * shotguns + [z_side.Runner] * runners
        # ^this uses duplicates of each side object, but that no longer has any impact
    def roll(self):
        return random.choice(self.sides)
    def __repr__(self):
        return "ZD_" + self.colour
    def __eq__(self, other):
        return self.colour == other.colour

class zombie():
    """Track the player state"""
    def __init__(self, brains=0):
        self.brains = brains
        self.wounds = 0
        self.exhausted = []
        self.hand = []
        self._initialise_pool()

    def _initialise_pool(self):
        """initialise pool 6 green, 4 yellow, 3 red"""
        self.pool = [zombie_dice("green")]* 6 + [zombie_dice("yellow")]*4 + [zombie_dice("red")]*2  # note copies!
        for d in self.hand:
            self.pool.remove(d) # remove dice that are still in hand from the pool
        random.shuffle(self.pool)

    def finished(self):
        return (self.wounds >=3) or (self.brains >= 13)

    def turn(self):
        """Select some dice from the pool and roll them"""
        # how many dice do we need?
        for _ in range(3 - len(self.hand)):
            try:
                # try to select a dice from the cup
                self.hand.append(self.pool.pop())
            except IndexError:  # pool is empty
                self._initialise_pool()
                self.hand.append(self.pool.pop())
        # alea iacta est
        for d in self.hand:
            result = d.roll()
            if result == z_side.Shotgun:
                self.wounds += 1
                self.exhausted.append(d)
                self.hand.remove(d)
            elif result == z_side.Brains:
                self.brains += 1
                self.exhausted.append(d)
                self.hand.remove(d)
            else:  # Runner
                # leave it in the hand
                pass

    def __str__(self):
        return "Brains {}, wounds {}, hand {}, pool {}, exhausted {}".format(self.brains, self.wounds, self.hand, self.pool, self.exhausted)

for initial in range(13): # starting health
    start = time.time()
    rounds = 100000
    victories = 0
    for i in range(rounds):
        b = zombie(initial)
        while not b.finished():
            b.turn()
        if b.brains >= 13 and b.wounds < 3:
                victories += 1

    print("Starting with {:2} ".format(initial), end="")
    print("Success rate {:6.2%} over {:,} rounds in {:6.3} seconds".format(victories/rounds, rounds, time.time() - start))