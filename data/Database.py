import psycopg2
from radiojavanapi.models import Song

from model.SongTokensModel import SongTokensModel
from nlp.StopWords import StopWords


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="Apple1378",
                                           host="localhost",
                                           port="5432",
                                           database="postgres")
        self.cursor = self.connection.cursor()

    def insert_song_to_database(self, song: Song, category: str):
        try:
            self.cursor.execute(
                f"""INSERT INTO song1(artist, name, duration, lyric, link, category, tokens_lemma) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (song.artist, song.name, song.duration, song.lyric, song.link, category, None))
            self.connection.commit()
            print("1 Record inserted successfully")

        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)

    def insert_praise_to_database(self, name: str, lyric: str, link: str, category: str):
        try:
            self.cursor.execute(
                f"""INSERT INTO song1(artist, name, duration, lyric, link, category, tokens_lemma) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (None, name, None, lyric, link, category, None))
            self.connection.commit()
            print("1 Record inserted successfully")

        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)

    def get_songs_id_lemma(self):
        try:
            self.cursor.execute("SELECT id,tokens_lemma from song1 ORDER BY id")
            records = self.cursor.fetchall()
            song_list = []

            for song in records:
                song_id = song[0]
                tokens = song[1]
                song_list.append(SongTokensModel(song_id, tokens, ""))

            return song_list
        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)

    def get_songs_id_lyric(self):
        try:
            self.cursor.execute("SELECT id,lyric from song1 ORDER BY id")
            records = self.cursor.fetchall()
            song_list = []

            for song in records:
                id = song[0]
                lyric = song[1]
                song_list.append(SongTokensModel(id, None, lyric))

            return song_list
        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)

    def update_lemma_tokens(self, source_word_to_swap, destination_word_to_swap):
        song_list = self.get_songs_id_lemma()
        for song in song_list:
            for token_num, token_lemma in enumerate(song.tokens):
                if str(token_lemma) == source_word_to_swap:
                    print(f"song.id -> {song.id}")
                    print(f"token_lemma -> {token_lemma}")
                    print(f"len -> {len(token_lemma)}")
                    print(f"token_num -> {token_num}")
                    print('----------------------------------')

                    self.update_tokens_database(song.id, token_num, destination_word_to_swap)

    def update_tokens_database(self, id: int, token_item: int, replace_word: str):
        token_item += 1
        print(id)
        print(token_item)
        print(replace_word)
        self.cursor.execute("update song1 set tokens_lemma[%s] = %s where id = %s", (token_item, replace_word, id,))
        self.connection.commit()

    def add_to_tokens(self, song_id: int, token: str):
        self.cursor.execute(f"""UPDATE song1 SET tokens_lemma = array_append(song1.tokens_lemma, %s) WHERE id = %s""",
                            (str(token).strip(), song_id,))
        self.connection.commit()

    def remove_lemma_tokens(self, word_to_remove):
        song_list = self.get_songs_id_lemma()
        for song in song_list:
            for token_num, token_lemma in enumerate(song.tokens):
                if str(token_lemma) == word_to_remove:
                    self.remove_token_database(song.id, token_lemma)

    def remove_token_database(self, song_id: int, word_to_remove: str):
        print(song_id)
        print(word_to_remove)
        self.cursor.execute("UPDATE song1 SET tokens_lemma = array_remove(tokens_lemma, %s) where id = %s",
                            (word_to_remove, song_id,))
        self.connection.commit()

    def delete_all_puncs_from_tokens(self):
        song_list = self.get_songs_id_lemma()
        for song in song_list:
            for token_num, token_lemma in enumerate(song.tokens):
                # if has_punctuation(token_lemma) and len(str(token_lemma).strip()) == 1:
                if len(str(token_lemma).strip()) == 0:
                    print(token_lemma)
                    self.cursor.execute("UPDATE song1 SET tokens_lemma = array_remove(tokens_lemma, %s)",
                                        (token_lemma,))
                    self.connection.commit()

    def remove_stop_words_from_tokens(self):
        stop_words = StopWords()
        song_list = self.get_songs_id_lemma()
        for song in song_list:
            if song.tokens is not None:
                for token in song.tokens:
                    if stop_words.is_stop_word(token):
                        print(song.id, token)
                        print("-------------------")
                        self.remove_token_database(song.id, token)

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
