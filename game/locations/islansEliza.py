from game import location
from game import config
from game.display import announce
from game.events import *
from game.items import Cutlass
from game.items import Flintlock
from game import event
import random
import game.config as config


class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["trees"] = Trees(self)
        self.locations["oasis"] = Oasis(self)

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        elif (verb == "east" or verb == "west"):
            announce ("You walk all the way around the island on the beach. It's not very interesting.")


class Trees (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = Cutlass()
        self.item_in_clothes = Flintlock()

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the small forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."
        
        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor."
        announce (description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")

class Oasis (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "oasis"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
class Sickness(event.Event):

    def __init__ (self):
        self.name = " a random crew member gets sick "

    def process (self, world):
        c = random.choice(config.the_player.get_pirates())
        result = {}
        if (c.sick == True):
            c.set_sickness (True)
            if (c.lucky == True):
                damage = 1
                deathcause = "died of their illness"
            else:
                damage = 10
                deathcause = "died of their worsening illness"
            died = c.inflict_damage (damage, deathcause)
            if(died == True):
                result["message"] = c.get_name() + " took a turn for the worse and has died of their illness"
                result["newevents"] = [ self, self, self ]
            else:
                result["message"] = c.get_name() + " has taken a turn for the worse"
                result["newevents"] = [ self, self ]
        elif (c.lucky == False):
            c.set_sickness (True)
            result["message"] = c.get_name() + " has gotten sick"
            result["newevents"] = [ self, self ]
        else:
            result["message"] = c.get_name() + " felt a bit sick"
            result["newevents"] = [ self ]
        return result

        
