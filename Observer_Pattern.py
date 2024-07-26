# creating an observer pattern for game events
import abc
from typing import List, Dict, Any


class GameEvent:
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.type = event_type
        self.data = data

class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, event: GameEvent):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: GameEvent):
        for observer in self._observers:
            observer.update(event)

class Game(Subject):
    def __init__(self):
        super().__init__()
        self.characters = []
        self.current_turn = 0
        self.round_number = 1

    def run(self):
        while True:
            self.handle_turn()

    def handle_turn(self):
        active_character = self.characters[self.current_turn]
        
        # Notify observers that a new turn is starting
        self.notify(GameEvent("turn_start", {"character": active_character}))

        # Handle character actions here...

        # End of turn
        self.notify(GameEvent("turn_end", {"character": active_character}))

        self.current_turn = (self.current_turn + 1) % len(self.characters)
        if self.current_turn == 0:
            self.round_number += 1
            self.notify(GameEvent("round_end", {"round": self.round_number}))

class Spell(Observer):
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration
        self.active = False

    def update(self, event: GameEvent):
        if event.type == "turn_start" and self.active:
            print(f"Spell {self.name} is active on {event.data['character'].name}")
            self.duration -= 1
            if self.duration <= 0:
                self.active = False
                print(f"Spell {self.name} has ended")

class ClassFeature(Observer):
    def __init__(self, name: str, character):
        self.name = name
        self.character = character

    def update(self, event: GameEvent):
        if event.type == "turn_start" and event.data['character'] == self.character:
            print(f"Class feature {self.name} is checking if it should activate for {self.character.name}")
 
class Character:
    def __init__(self, name: str):
        self.name = name

# Usage example
game = Game()

# Create characters
player1 = Character("Aragorn")
player2 = Character("Gandalf")
game.characters = [player1, player2]

# Create spells and class features
fireball = Spell("Fireball", 3)  # Lasts for 3 rounds
sneak_attack = ClassFeature("Sneak Attack", player1)

# Attach observers to the game
game.attach(fireball)
game.attach(sneak_attack)

# Start the game loop
# game.run()