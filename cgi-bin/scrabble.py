# coding=latin-1

import collections
import itertools
import os.path
import sqlite3
import string
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
db_path    = os.path.join(script_dir, 'dict.db')

dict_source = {'fr': 'liste.de.mots.francais.frgut.txt'}

for lang,f in dict_source.iteritems():
    dict_source[lang] = os.path.join(script_dir, f)

def lookup(letters, lang='fr'):

    # The name of the table in the database that corresponds to the choosen
    # language
    table_name = 'idx_{}'.format(lang)

    # Check if the database has already been created
    if not os.path.isfile(db_path):

        # Create translation table
        tt = string.maketrans('àâäçéèêëîïôûüù', 'aaaceeeeiiouuu')

        # Create DB
        db = sqlite3.connect(db_path)
        db.execute('''CREATE TABLE {}(
                      id      INTEGER PRIMARY KEY,
                      letters TEXT NOT NULL,
                      word    TEXT NOT NULL);'''.format(table_name))

        # Parse the dictionary file
        d = collections.defaultdict(list)
        with open(dict_source[lang]) as f:

            # We enumerate here only to provide the line number for the word
            # that would contain an unrecognized character
            for i,word in enumerate(f):
                word = word.strip().lower()

                # Only process words between 1 and 7 letters, and without '-'
                if len(word) > 0 and len(word) < 8 and not '-' in word:
                    word = word.translate(tt)

                    # This loop is only for debugging purposes
                    for c in word:
                        assert ord(c) >= ord('a') and ord(c) <= ord('z'), '{} ({}) {} {}'.format(ord(c), c, word, i)

                    # Sort letters in word, and add to dict
                    sorted_word = ''.join(sorted(word))
                    d[sorted_word].append(word)

        # Create the tuples and insert them in the DB
        tuples = []
        for let, words in d.iteritems():
            tuples.extend((let, w) for w in words)
        db.executemany("INSERT INTO {}(letters, word) VALUES(?, ?)".format(table_name), tuples)

        # Create the database index
        db.execute('CREATE INDEX letters_index ON {}(letters);'.format(table_name))
    else:
        db = sqlite3.connect(db_path)

    # Search for words
    letters = ''.join(sorted(letters))
    if len(letters) < 1: raise Exception('Too short')
    if len(letters) > 7: raise Exception('Too long')
    answers = set()
    for i in range(1, len(letters) + 1):
        for w in (''.join(c) for c in itertools.combinations(letters, i)):
            answers.update(w for (w,) in db.execute('SELECT word FROM {} WHERE letters=?'.format(table_name), (w,)))

    # Return a list of words sorted by length (largest first), then alpha)
    words = []
    for i in range(7, 1, -1):
        words.extend(sorted(w for w in answers if len(w) == i))
    return words

def main():
    for w in lookup(sys.argv[1]):
        print w

if __name__ == '__main__':
    main()

