from game import location
from game import config
from game.display import announce
from game import ship
from game.events import sickness
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
        self.locations["oasis"] = self.starting_location
        self.locations["Seamps"] = self.starting_location
        self.locations["Wondering Woods"] =self.starting_location
        
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
        self.verbs['keep'] = self
            
        elf.event_chance = 50

    def enter (self):
        announce ("coconuts and fruit trees")
        
    def process_verb (self, verb, cmd_list, nouns):
        if(verb == "take"):
            food = input("You have found food! Do you want to keep it")
            
            if food == "keep":
                config.the_player.ship.add_food (20)
                
        #elif len(cmd_list) > 1:

        
            
class Swamp (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Swamps"
        self.verbs['explore'] = self
        self.verbs['leave'] = self
        self.ship = None
        self.symbol = "^"
        
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "explore"):
            config.the_player.gameInProgress = False
            config.the_player.kill_all_pirates("Drowned in the Swamp")
            print ("The pirates drowned in the Swamp")

        elif (verb == "leave"):
            sickness.Sickness().process(config.the_player.world)
           
