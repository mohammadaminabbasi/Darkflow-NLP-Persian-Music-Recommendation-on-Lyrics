import re
import string


def has_numbers(input_string):
    return bool(re.search(r'\d', input_string))


def remove_punctuation(text):
    punctuations = string.punctuation.replace("*", '')
    translator = str.maketrans(punctuations, ' ' * len(punctuations))
    return text.translate(translator)
