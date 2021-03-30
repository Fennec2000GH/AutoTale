# These methods are just for testing and provide no functionality
def test_relationships():
    my_house = Location("Eric's house")
    eric = Character("Eric", my_house)
    print(eric.name)
    jake = Character("Jake", my_house)
    eric.add_relationship(jake, Relationship.Type.Friendly, 10)
    print(eric.relationships['Jake'].strength)
    print(jake.relationships['Eric'].strength)


def test_sample_story():
    starting_location = Location('Turlington Hall Room L007')
    player_name = input('Your name: ')
    game_state = GameState(player_name, starting_location)
    print("Jake joins the party!")
    jake = Character("Jake", starting_location)
    game_state.add_to_party(jake)
    print("Eric and Jake go to Little Hall")
    new_location = Location('Little Hall')
    game_state.go_to_location(new_location)
    print("Jake is at ", jake.location.name)