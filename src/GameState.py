from Character import Character


class GameState:
    def __init__(self, player_name, location):
        self.player = Character(player_name, location)
        # set of characters in the player's party
        self.party = {self.player}
        # current location
        self.location = location
        # set of possible locations
        self.possible_locations = set()

    def add_to_party(self, partner):
        self.party.add(partner)

    def go_to_location(self, location):
        self.possible_locations.add(location)
        self.location = location
        for character in self.party:
            character.location = location
