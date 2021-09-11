from radiojavanapi import Client
import psycopg2

from data.Database import Database
from model.SongCategory import SongCategory


class FetchSongRadioJavan:
    # Dep Love playlists id
    playlist_yadete = "0acc4ffba36b"
    playlist_dislove = "58ea0e1e4ff2"
    playlist_broken_heart = "b27131390e03"
    playlist_breakup = "604c599a9433"

    # Happy Romantic playlists id
    playlist_2nafare = "19054aeaf694"
    playlist_love_songs = "5b37b9739b73"
    playlist_fall_in_love = "0cc48c1c5eba"

    # Hip Hop playlists id
    playlist_hiphop_party = "673c1d3da026"
    playlist_hiphop_workout = "0fa40da912e4"
    playlist_gang = "8ce83b27ddfc"
    playlist_diss = "f2fb8dd6aed8"

    list_happy_love = [playlist_2nafare, playlist_love_songs, playlist_fall_in_love]
    list_dep_love = [playlist_yadete, playlist_dislove, playlist_broken_heart, playlist_breakup]
    list_hip_hop = [playlist_hiphop_party, playlist_hiphop_workout, playlist_gang, playlist_diss]

    def fetch(self):

        client = Client()
        self.__insert_song_of_playlist_deteils(client, self.list_happy_love,
                                             SongCategory.happyLove.value)
        self.__insert_song_of_playlist_deteils(client, self.list_dep_love,
                                             SongCategory.depLove.value)
        self.__insert_song_of_playlist_deteils(client, self.list_hip_hop,
                                             SongCategory.hipHop.value)

    def __insert_song_of_playlist_deteils(self, client: Client, list_of_playlist: [], category: str):
        database = Database()

        for playlist_id in list_of_playlist:
            playlist = client.get_music_playlist_by_id(playlist_id)
            for meta_song in playlist.songs:
                song = client.get_song_by_id(meta_song.id)
                print(meta_song.name + " inserting...")
                if song.lyric is not None:
                    try:
                        database.insert_song_to_database(meta_song, category)
                    except (Exception, psycopg2.Error) as error:
                        print("Error db: ", error)
