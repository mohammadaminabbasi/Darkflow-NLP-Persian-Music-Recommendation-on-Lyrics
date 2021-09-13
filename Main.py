from data.Database import Database
from data.FetchSongRadioJavan import FetchSongRadioJavan
from data.WebScrappingPraise import WebScrappingPraise
from nlp.LDAModelTraining import LDAModelTraining
from nlp.NlpProcess import NlpProcess


def main():
    # fetch_song_radio_javan = FetchSongRadioJavan()
    # fetch_song_radio_javan.fetch()
    #
    # web_scrapping_praise = WebScrappingPraise()
    # web_scrapping_praise.scrap()

    # nlp_process = NlpProcess()
    # nlp_process.start_nlp_process()

    database = Database()
    database.remove_stop_words_from_tokens()

    lda_model_training = LDAModelTraining()
    lda_model_training.train()


if __name__ == '__main__':
    main()
