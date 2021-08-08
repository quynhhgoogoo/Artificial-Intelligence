from collections import Counter
 
import math
import nltk
import os
import sys

nltk.download('punkt')

def main():
    '''Calculate top term frequencies for a corpus of documents'''
    if len(sys.argv) != 3:
        sys.exit("Usage: python ngrams.py n corpus")
    print("Loading data...")

    # Loading input
    n = int(sys.argv[1])
    corpus = load_data(sys.argv[2])

    # Compute n-grams
    ngrams = Counter(nltk.ngrams(corpus, n))

    # Print most common n-grams
    for ngram, freq in ngrams.most_common(10):
        print(f"{freq}: {ngram}")

def load_data(directory):
    contents = []

    # Read all files and extract words
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            
            # Convert all the words to lower case
            # For all the words which are characters
            contents.extend([
                word.lower() for word in
                nltk.word_tokenize(f.read())
                if any (c.isalpha() for c in word)
            ])

    return contents

if __name__ == "__main__":
    
    main()