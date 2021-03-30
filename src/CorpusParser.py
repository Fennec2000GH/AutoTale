import nltk
from nltk.corpus import brown
import math
import pickle


# Each DocumentFeatures object will hold the 1000 most common words and the word importance of them
class DocumentFeatures:
    def __init__(self, file_id):
        self.file_id = file_id
        # A dictionary where each key is the word and the value is the calculated importance
        self.words = {}

    def add_word(self, word, importance):
        self.words[word] = importance

# Gets the word importance for the 1000 most common words of each document of the selected genre
# Return a list of DocumentFeatures for each document with data of the 1000 most common words
def analyze_word_importance(genre: str):
    # for better results, read most 1000 common instead of just 200
    WORDS_TO_PARSE = 200
    file_ids = brown.fileids(categories=genre)
    # Make a frequency distribution for each document
    fds = nltk.FreqDist()
    for file_id in file_ids:
        fds[file_id] = nltk.FreqDist(brown.words(file_id))
    n = len(file_ids)
    # the features for each document of the given genre
    genre_document_features = []
    for file_id in file_ids:
        current_document_features = DocumentFeatures(file_id)
        fd = fds[file_id]
        print("reading document features of document", file_id)
        for tuple_ in fd.most_common(WORDS_TO_PARSE):
            word = tuple_[0]
            # df is number of documents the word is in
            df = len([1 for f in fds if word in fds[f]])
            importance = tuple_[1] * math.log(n/df)
            current_document_features.add_word(word, importance)
        genre_document_features.append(current_document_features)
    # Save the features in a file so that they can be loaded in a
    #   later run and they don't have to be generated every time
    file_name = "{}_features_{}_most_common.p".format(genre, WORDS_TO_PARSE)
    pickle.dump(genre_document_features, open(file_name, "wb"))
    return genre_document_features