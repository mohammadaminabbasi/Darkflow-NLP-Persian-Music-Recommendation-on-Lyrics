import hazm
import stanza

from data.Database import Database
from model import SongTokensModel
from nlp.StopWords import StopWords
from utils.Utils import remove_punctuation


class NlpProcess:
    # 1.fetch_lyrics 2.normalizer 3.tokenize_lemmatizer_stanza_hazm

    fa_nlp_pipeline = stanza.Pipeline('fa', processors='tokenize,lemma,pos,depparse', verbose=False,
                                      use_gpu=False)

    def __fetch_lyrics(self):
        database = Database()
        songs = database.get_songs_id_lyric()
        return songs

    def __normalizer(self, text):
        normalizer = hazm.Normalizer()
        text = normalizer.normalize(text)
        text = remove_punctuation(text)
        return text

    def __tokenize_lemmatizer_stanza_hazm(self, text: str):
        tokens = []
        stop_word = StopWords()
        lemmatizer_hazm = hazm.Lemmatizer()
        fa_nlp_stanza = self.fa_nlp_pipeline(text)

        for i, sent in enumerate(fa_nlp_stanza.sentences):
            for word in sent.words:
                if not stop_word.is_stop_word(word.text):
                    try:
                        token = str(word.lemma)
                        if token.__contains__('#'):
                            token = token.split('#')[0]

                        token = str(lemmatizer_hazm.lemmatize(word.lemma))
                        if token.__contains__('#'):
                            token = token.split('#')[0]

                        tokens.append(token)
                    except Exception as e:
                        tokens.append(word)

            return tokens

    def __add_tokens_database(self, song: SongTokensModel):
        database = Database()
        if song.tokens is not None:
            for token in song.tokens:
                database.add_to_tokens(song.id, token)

    def start_nlp_process(self):
        songs = self.__fetch_lyrics()

        for song in songs:
            print(song.id)
            song.lyric = self.__normalizer(song.lyric)
            song.tokens = self.__tokenize_lemmatizer_stanza_hazm(song.lyric)
            self.__add_tokens_database(song)
