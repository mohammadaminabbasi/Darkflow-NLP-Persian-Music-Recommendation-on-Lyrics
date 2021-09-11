import psycopg2
import hazm

from nlp.StopWords import StopWords

connection = psycopg2.connect(user="postgres",
                              password="Apple1378",
                              host="localhost",
                              port="5432",
                              database="postgres")


def update_lyric():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from song")
        records = cursor.fetchall()
        for song in records:
            id = song[6]
            lyric = song[3]
            link = song[4]
            # Executing a SQL query to update table
            # cursor.execute(f"""UPDATE song SET lyric = %s WHERE id = %s""", (str(lyric).strip(), id,))
            # cursor.execute(f"""UPDATE song SET lyric = %s WHERE id = %s""", (lemmatizer.normalize(lyric), id,))
            # cursor.execute(f"""UPDATE song SET lyric = %s WHERE id = %s""",
            #                (re.sub("[\*\(\[].*?[\*\)\]]", "", lyric), id,))
            connection.commit()
            # print(f"{song[2]} updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)


def tokenize_remove_stopwords():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from song")
        records = cursor.fetchall()

        stopwords = StopWords()

        for song in records:
            id = song[6]
            lyric = song[3]
            link = song[4]

            tokens = stopwords.is_stopword(lyric)
            print(tokens)

            for token in tokens:
                cursor.execute(f"""UPDATE song SET tokens = array_append(song.tokens, %s) WHERE id = %s""",
                               (str(token).strip(), id,))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)


def main():
    lemma = hazm.Lemmatizer()
    print(lemma.lemmatize("بری"))
    # tokenize_remove_stopwords()


if __name__ == '__main__':
    main()