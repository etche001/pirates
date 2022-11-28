from game import location
from game import config
from game.display import announce
from game.events import *
from game.items import Cutlass
from game.items import Flintlock
from game import event
import random
import game.config as config
from game.events import Death


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

        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Wondering Woods"]
            announce ("You have arrived at the Wondering Woods")

class WonderingWoods (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Wondering Woods"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        pass

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your beach.")
            config.the_player.next_loc = config.the_player.beach
            config.the_player.visiting = False
        elif (verb == "north"):
            announce ("Ocean north")
            config.the_player.next_loc = self.main_location.locations["Wondering Woods"]
        elif (verb == "east"):
            announce ("You have enterd at the Oasis")
            config.the_player.next_loc = self.main_location.locations["Oasis"]

        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Swamp"]
            announce ("You have gotten to the Swamps")

class Oasis (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "oasis"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['take'] = self

        elf.event_chance = 50

    def enter (self):
        announce ("coconuts and fruit trees")
        
    def process_verb (self, verb, cmd_list, nouns):
         if verb == "take":
             #take food
             #take coconuts
             #take fruit
             #take all
        elif len(cmd_list) > 1:ß
            
class Swamp (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Swamps"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 50
        self.events.append(Death())
        self.events.append(drowned_pirates.DrownedPirates())
        
