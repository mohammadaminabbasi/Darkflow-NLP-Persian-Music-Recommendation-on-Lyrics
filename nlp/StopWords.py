import hazm


class StopWords:
    stopwords_list = []

    def __init__(self):
        stopword_file = open('../resources/stopwords_all.txt', 'r')

        for stop_word in stopword_file:
            self.stopwords_list.append(stop_word)

    def is_stop_word(self, word):
        for stop_word in self.stopwords_list:
            if stop_word.strip() == word.strip():
                return True
        return False
