# AutoTale  
Autotale is an automatic story generator using NLP (natural language processing). The project utilizes Python and the NLTK package.

## Contributing
The project right now is in its early stages. We've mostly done brainstorming we're also open to new contributors.

If you're interested, join the SSD Discord and post in the #autotale channel: https://discord.gg/5SyB3yx

## Files
- GameControl
    - Controls the flow of the game. Prompts the user to pick a genre
- GameState
    - Used to initialize an instance of the game and maintain state.
    - Player
    - Party (the player and any of his allies)
    - Current location
    - Set of possible locations
- Location
    - Creates the structure for locations. The map will be represented by a graph.
    - The player can travel along edges and arrive at locations represented by nodes.
    - The map in this game will be static but has not been designed yet
- Character
    - Character class keeps track of:
        - name
        - location
        - relationships
    - Relationship class is used to describe a relationship that a character percieves with another character. 
        - A relationship is not mutual, meaning that a character
          could like another character and the other won't procate.
        - 3 types of relationships: Romantic, Friendly, Ally
- CorpusParser
    - This file contains functions that will aid in parsing corpus and extracting features.
      The features will help in generating text.
- Tests
    - Contains some methods to test out portions of the game, but provides no functionality.
