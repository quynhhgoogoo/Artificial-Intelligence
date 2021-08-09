import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_list = dict()

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        file_name = file_path[-4:]

        with open(file_path, encoding="utf-8") as f:
            contents = f.read()
            file_list[file_name] = contents

    return file_list

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    contents = []

    # Convert all the words to lower case
    # For all the words which are characters
    contents.extend([
        word.lower() for word in
        nltk.word_tokenize(document)
        if any (c.isalpha() and c not in string.punctuation and  c not in nltk.corpus.stopwords.words("english") for c in word)
    ])

    return contents


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words = set()

    # Get all words inside documents
    for filename in documents:
        words.update(documents[filename])
    
    # Calculate idf value for each word
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        # idf = total documents / document contains that specific word
        idf = math.log( len(documents) / f)
        idfs[word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Calculate TF-IDFs
    tfidfs = dict()
    for filename in files:
        tfidfs[filename] = []
        for word in files[filename]:
            tf = files[filename][word]
            tfidfs[filename].append( (word, tf * idfs[word]) )
    
    # Sort and get top 5 TF-IDFs for file
    for filename in files:
        tfidfs[filename].sort(key = lambda tfdif: tfdif[1], reverse=True)
        tfidfs[filename] = tfidfs[filename][:n]
    term, score = tfidfs[filename]
    
    return term

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
