from sklearn.feature_extraction.text import CountVectorizer
from data.Database import *
import numpy as np


class CountVector:

    def count(self):
        database = Database()

        sent_list = []
        songs = database.get_songs_id_lemma()
        for song in songs:
            sent = " ".join(song.tokens)
            sent_list.append(sent)

        print(len(sent_list))

        vectorizer = CountVectorizer()
        # tokenize and build vocab
        vectorizer.fit(sent_list)

        vocabularies = vectorizer.vocabulary_

        # encode document
        vectors = vectorizer.transform(sent_list)
        # summarize encoded vectors
        print(vectors.shape)

        np_array = np.array(vectors.toarray())
        count_per_word = np.sum(np_array, axis=0)
        # print(count_per_word)

        count_map = {}
        for vocabulary in vocabularies:
            count_map[vocabulary] = count_per_word[vocabularies[vocabulary]]
            # print(f"{vocabulary} :: {count_per_word[vocabularies[vocabulary]]}")

        top_repeated_words = dict(sorted(count_map.items(), key=lambda item: item[1], reverse=True)[:20])
        for hash_map in top_repeated_words:
            print(f"{hash_map} :: {top_repeated_words[hash_map]}")


CountVector().count()