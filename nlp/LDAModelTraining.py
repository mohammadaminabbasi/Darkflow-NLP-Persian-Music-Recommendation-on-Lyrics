import hazm
import tomotopy as tp
from radiojavanapi.models import Song
from radiojavanapi import Client

from data.Database import Database


class LDAModelTraining:
    topic_counts = 3
    word_topic_show = 15

    topic_map = {0: "عاشقانه",
                 1: "گنگ و دیس",
                 2: "مذهبی"}

    def __init__(self):
        self.mdl = tp.LDAModel.load("./training_model/lda_model.bin")

    def train(self):
        mdl = tp.LDAModel(k=self.topic_counts)

        database = Database()
        songs = database.get_songs_id_lemma()
        for song in songs:
            mdl.add_doc(song.tokens)

        for i in range(0, 100000, 10):
            mdl.train(10)
            print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

        print()
        print("-------------------------------------------")
        print()

        for k in range(mdl.k):
            print('Top 10 words of topic #{}'.format(k))
            print(self.get_words_of_topic(mdl.get_topic_words(k, top_n=self.word_topic_show)))

        mdl.summary()

        self.save_model(mdl)

    def save_model(self, mdl):
        mdl.save('lda_model.bin')

    def test(self, title: str, lyric: str):
        doc = []
        lyric = lyric.split("\n")
        for line in lyric:
            for word in line.strip().split():
                doc.append(word)

        doc_inst = self.mdl.make_doc(doc)
        topic_dist, ll = self.mdl.infer(doc_inst)
        best_topic_index = list(topic_dist).index(max(topic_dist))
        best_topic_word_list = self.mdl.get_topic_words(best_topic_index, top_n=self.word_topic_show)
        print(title)
        print(f"Best Topic: {self.get_words_of_topic(best_topic_word_list)}")
        print(f"topic: {self.topic_map[best_topic_index]}")
        print(f"percentage: {round(max(topic_dist), 2)}")
        print("---------------------------------------------------------------------------------")

    def get_words_of_topic(self, topic_words):
        words = []
        for map in topic_words:
            words.append(map[0])

        return words

    def fetch_data_test(self):
        urls = ["https://www.radiojavan.com/mp3s/mp3/Gdaal-Ebi?playlist=5f22145e31d8&index=49",
                "https://www.radiojavan.com/mp3s/mp3/Sepehr-Khalse-Gole-Man-(Ft-Behzad-Leito-Siavash-Rad)#lyricsTabNew",
                "https://www.radiojavan.com/mp3s/mp3/Behnam-Bani-Toyi-Entekhabam#lyricsTabNew",
                "https://www.radiojavan.com/mp3s/mp3/Alireza-JJ-Balance-(Ft-Mehrad-Hidden-Sohrab-MJ-Sepehr-Khalse)"
                ]

        client = Client()
        normalizer = hazm.Normalizer()

        # for url in urls:
        #     song = client.get_song_by_url(url)
        #     self.test(song.title, song.lyric)

        title = "test lyric"
        lyric = normalizer.normalize(open("./resources/test_data.txt").read())
        self.test(title, lyric)

    def print_topics(self):
        for i in range(0, 3):
            print(i, LDAModelTraining().get_words_of_topic(self.mdl.get_topic_words(i, top_n=self.word_topic_show)))


LDAModelTraining().print_topics()
