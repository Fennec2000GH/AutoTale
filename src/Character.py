import enum


class Relationship:
    # What type of relationship this is can be categorized
    class Type(enum.Enum):
        Friendly = 1
        Romantic = 2
        Ally = 3

    def __init__(self, with_, type_, strength: int):
        self.with_ = with_
        # type is a keyword so add an underline
        self.type = type_
        # I was thinking we could score relationships from -10 to 10
        # A strength of 0 means the relationship is completely neutral.
        # A strength of 10 means the relationship is positive and very strong
        # A strength of -10 means the relationship is negative and very strong
        self.strength = strength


class Character:
    # default location is UNKNOWN if not provided
    def __init__(self, name, location, relationships={}, visited_locations=set()):
        self.name = name
        self.location = location,
        # relationships will be a dictionary with the key being the name of another
        #   character and the value being a Relationship object
        self.relationships = relationships
        self.visited_location = visited_locations
        self.visited_location.add(location)

    def add_relationship(self, with_, type_, strength):
        relationship = Relationship(type_, strength)
        # the key for the relationship dictionary is the name of the other person
        #   but the Relationship has a reference to the whole Character object
        self.relationships[with_.name] = relationship
