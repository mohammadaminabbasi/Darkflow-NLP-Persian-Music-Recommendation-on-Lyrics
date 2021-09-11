from data.FetchSongRadioJavan import FetchSongRadioJavan
from data.WebScrappingPraise import WebScrappingPraise
from nlp.NlpProcess import NlpProcess


def main():
    # fetch_song_radio_javan = FetchSongRadioJavan()
    # fetch_song_radio_javan.fetch()
    #
    # web_scrapping_praise = WebScrappingPraise()
    # web_scrapping_praise.scrap()

    nlp_process = NlpProcess()
    nlp_process.start_nlp_process()


if __name__ == '__main__':
    main()
