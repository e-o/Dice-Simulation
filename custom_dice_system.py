#https://rpg.stackexchange.com/questions/103090/how-can-i-calculate-the-probability-of-being-able-to-purchase-a-card-in-my-custo/103565#103565

import enum
import random
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


class dice(enum.IntEnum):
    def __str__(self):
        return str(self.name) # don't need to print the number
    def __repr__(self):
        return str(self.name)
    Sword_1 = 1
    Sword_2 = 2
    Sword_3 = 3
    Sword_4 = 4
    Sword_5 = 5
    Sword_6 = 6
    Sword_7 = 7
    Sword_8 = 8
    Sword_9 = 9
    Sword_10 = 10
    Sword_11 = 11
    Sword_12 = 12
    # numeric values are for matching Swords
    Political = 0
    Castle = 0
    Wizard = 0
    @classmethod
    def rollable(cls):
        "Returns a tuple of the six possible rolls"
        return (cls.Sword_1, cls.Sword_2, cls.Sword_3, cls.Political, cls.Castle, cls.Wizard)

def roll():
    return random.choice(dice.rollable())

class card():
    def __init__(self, name, *requirements):
        self.name = name
        self.reqs = requirements

def buy(card, number_of_rolls=7):
    rolls = [roll() for _ in range(number_of_rolls)]
    requirements = list(card.reqs) # create a copy
    requirements.sort(reverse=True)  # sort the requirements to ensure largest sword is first.
    penalty = 0
    all_matches = []
    while requirements and rolls: # Each iteration of this loop is one round.
        matches = []  # need to track the matches in a round for penalty determination
        logging.debug("Reqs: {}".format(requirements))
        logging.debug("Rolls: {}".format(rolls))
        if all_matches:
            logging.debug("Current Matches: {}".format(all_matches))
        for easy in (dice.Political, dice.Castle, dice.Wizard):
            while easy in requirements and easy in rolls:
                # remove all instances.
                logging.debug("Matched: {}".format(easy))
                requirements.remove(easy)
                rolls.remove(easy)
                matches.append(easy)
        #for big_sword in [dice.Sword_12]:
        for big_sword in [dice.Sword_12, dice.Sword_11, dice.Sword_10, dice.Sword_9, dice.Sword_8, dice.Sword_7, dice.Sword_6, dice.Sword_5, dice.Sword_4]:
        # for big_sword in [dice.Sword_12, dice.Sword_11, dice.Sword_10, dice.Sword_9, dice.Sword_8, dice.Sword_7, dice.Sword_6, dice.Sword_5]:
            while big_sword in requirements:
                if sum(rolls) >= big_sword:  # we can match a big_sword.
                    rolls.sort(reverse=True)
                    
                    requirements.remove(big_sword)
                    # the first approach removes the largest swords first -- this may be suboptimal if there are other requirements.
                    # 30 % versus 40% for 3xSword_4 new versus old. Now up to 36.5% and that's probably where I'll leave it.
                    # so Sword_3, Sword_3, Sword_1, Sword_1 should match 2xSword_4, but with the first approach it doesn't.
                    # also don't want to match 1,1,1,1 with Sword_4 if there is another Sword remaining. 
                    # -- although we'd need 5 dice to allow for the mismatch penalty
                    swords = 0
                    new_matches = []
                    if False:
                        for d in rolls:
                            if swords < big_sword:
                                if d > 0:  # shouldn't get here are the rolls are now sorted.
                                    new_matches.append(d)
                                    # can't remove from rolls here as we're iterating through rolls.
                                    swords += d
                        #logging.debug("Matched {} with : {}".format(big_sword, new_matches))
                        for d in new_matches:
                            rolls.remove(d)
                            matches.append(d)
                    else:
                        # This approach tries to minimise the Swords used, but will match 1,1,1,1 regardless of remaining requirements
                        matched = False
                        while sum(rolls) > 0 and not matched: # still swords available.
                            logging.debug("A match is available for {} with {} in {}".format(big_sword, swords, rolls))
                            swords += rolls[0]
                            new_matches.append(rolls[0])                
                            rolls.remove(rolls[0])
                            if swords + rolls[0] >= big_sword:  
                            # we can match with one dice, so iterate from the smallest to optimise use
                                for d in reversed(rolls):  # creates an iterator, NOT a copy            
                                    if swords + d >= big_sword:
                                        new_matches.append(d)
                                        matched = True
                                        break  # break out of the for loop
                            else:
                                # we need at least two more dice, so loop again
                                pass
                        logging.debug("Matched {} with : {}".format(big_sword, new_matches))
                        # only need to remove the last of the new_matches from rolls as they're removed to iterate
                        rolls.remove(new_matches[-1])
                        matches.extend(new_matches)
                        
                        
                else:  # check if we have enough dice to match on a re-roll.
                    if 3 * (len(rolls) - 1) < requirements.count(big_sword) * big_sword: # handle multiple big swords
                        logging.debug("Next round can't match {} with {} dice".format(big_sword, len(rolls) - 1))
                        # just set rolls to an empty list to trigger failure case
                        rolls = []
                    break
        # swords required OR re-roll for easys
        while dice.Sword_4 in requirements:
            # worst case, but if we have a Sword_4 and a Sword_2 and rolled Sword_3 and Sword_1 would we match the 4 or the 2? Maybe depends on how many other die there are and what round we're in.
            # just match this first then handle the rest of the Swords.
            if dice.Sword_3 in rolls and dice.Sword_1 in rolls:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_3, dice.Sword_1))
                logging.debug("4 matched by 3, 1")
                rolls.remove(dice.Sword_3)
                rolls.remove(dice.Sword_1)
            elif rolls.count(dice.Sword_2) >= 2:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_2, dice.Sword_2))
                logging.debug("4 matched by 2, 2")
                rolls.remove(dice.Sword_2)
                rolls.remove(dice.Sword_2)
            elif rolls.count(dice.Sword_3) >= 2:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_3, dice.Sword_3))
                logging.debug("4 matched by 3, 3")
                rolls.remove(dice.Sword_3)
                rolls.remove(dice.Sword_3)
            elif dice.Sword_3 in rolls and dice.Sword_2 in rolls:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_3, dice.Sword_2))
                logging.debug("4 matched by 3, 2")
                rolls.remove(dice.Sword_3)
                rolls.remove(dice.Sword_2)
            else: # no possible matches for Sword_4
                break
        for d in (dice.Sword_3, dice.Sword_2, dice.Sword_1):
            while d in requirements:
                if d in rolls:
                    logging.debug("{} Matched exactly".format(d))
                    rolls.remove(d)
                    requirements.remove(d)
                    matches.append(d)
                else:
                    break
        # check to match Sword 2 with Sword 3
        if dice.Sword_2 in requirements and dice.Sword_3 in rolls:
            requirements.remove(dice.Sword_2)
            matches.append(dice.Sword_3)
            logging.debug("2 matched by 3")
            rolls.remove(dice.Sword_3)
        if dice.Sword_1 in requirements and dice.Sword_3 in rolls:
            requirements.remove(dice.Sword_1)
            matches.append(dice.Sword_3)
            logging.debug("1 matched by 3")
            rolls.remove(dice.Sword_3)
        if dice.Sword_1 in requirements and dice.Sword_2 in rolls:
            requirements.remove(dice.Sword_1)
            matches.append(dice.Sword_2)
            logging.debug("1 matched by 2")
            rolls.remove(dice.Sword_2)
        if requirements:
            logging.debug("No more matches with: {}, still need {}".format(rolls, requirements))
            if matches:
                all_matches.extend(matches)
                penalty = 0
            else:
                penalty = 1
            rerolls = len(rolls) - penalty
            logging.debug("Rerolling {}".format(rerolls))
            rolls = [roll() for _ in range(rerolls)]
        else:
            logging.debug("Unneeded: {}".format(rolls))
        penalty += 1
    if requirements:
        logging.debug("Failed to acquire {} remaining:".format(card.name, requirements))
        return False
    else:
        logging.debug("Successfully acquired {}".format(card.name))
        return True


def test_buy(target, number_of_tests=10000, print_last=False):
    count = 0
    logger = logging.getLogger()
    log_level = logger.level
    for i in range(number_of_tests):
        # only print the last round
        if i == number_of_tests - 1 and print_last:
            logger.setLevel(logging.DEBUG)  # note this will permanently
        if buy(target):
            count += 1
    logger.info("Chance to buy card {} is about {:.2%} after {:,} iterations".format(target.name, count/number_of_tests, number_of_tests))
    logger.setLevel(log_level)
      
# Priest: 4 Swords, 1 Sword, 1 Political, and 1 Castle
priest = card("Priest", dice.Sword_4, dice.Sword_1, dice.Political, dice.Castle)
warrior = card("Warrior", dice.Sword_4, dice.Sword_4, dice.Sword_4)
# warrior = card("Warrior", dice.Sword_4, dice.Sword_4)
blade_master = card("Blademaster", dice.Sword_12)
blade_apprentice = card("Blade", dice.Sword_8)


for target in [priest, warrior, blade_master, blade_apprentice]:
    # test_buy(target)
    test_buy(target, number_of_tests=10_000)
"""Chance to buy card Priest is about 96.25% after 100,000 iterations
Chance to buy card Warrior is about 36.38% after 100,000 iterations
Chance to buy card Blademaster is about 11.52% after 100,000 iterations
Chance to buy card Blade is about 69.21% after 100,000 iterations"""

