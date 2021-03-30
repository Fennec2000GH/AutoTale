from Character import *
from CorpusParser import *
from Location import *
from GameState import *
from nltk.corpus import brown

# Gets a genre from the brown corpus
def get_user_selected_topic():
    print("Welcome to Autotale!")
    print()
    print("Which genre would you like to generate a story for?")
    for i, genre in enumerate(brown.categories()):
        print("{}: {}".format(i, genre))
    max_index = len(brown.categories()) - 1
    genre_index = -1
    while genre_index < 0 or genre_index > max_index:
        print("Enter a number between 0 and {}.".format(max_index))
        genre_index = int(input())
        if 0 <= genre_index <= max_index:
            break
        else:
            print("Invalid option")
    genre = brown.categories()[genre_index]
    print("selected input:", genre)
    return genre






