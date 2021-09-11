create table song1
(
    artist       text,
    name         text,
    duration     double precision,
    lyric        text,
    link         text,
    category     text,
    id           serial not null primary key,
    tokens_lemma text[]
);

INSERT INTO song1(artist, name, duration, lyric, link, category, tokens_lemma)

UPDATE song1
SET tokens_lemma= Null;

Select count(*)
FROM song
WHERE category = 'dep_love'
   or category = 'happy_love'

UPDATE song
SET lyric = regexp_replace(lyric, '[A-Z]', ' ', 'g')
where category = 'praise';

UPDATE song
SET lyric = regexp_replace(lyric, '[a-z]', ' ', 'g')
where category = 'praise';

ALTER TABLE song
    ADD COLUMN tokens_lemma TEXT[];

UPDATE song
SET tokens = array_append(tokens, '...')
WHERE id = 1;

UPDATE song SET tokens_lemma = array_remove(tokens, '!');


SELECT array_remove(tokens, '۲۰۱۲')
from song
WHERE id = 49;

SELECT id
FROM song
WHERE song.tokens LIKE '%...%';

SELECT tokens_lemma[35]
from song
WHERE id = 15;

SELECT sum(cardinality(tokens_lemma))
from song;

