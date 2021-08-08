import nltk
import os
import sys

def main():
    # Read data from files
    if len(sys.argv) != 2:
        sys.exit("Usage: python sentiment.py corpus")
    negatives, positives = load_data(sys.argv[1])

    # Create a set of all words
    words = set()
    for document in positives:
        words.update(document)
    for document in negatives:
        words.update(document)

    # Extract features from text
    training = []
    training.extend(generate_feature(positives, words, "positive"))
    training.extend(generate_feature(negatives, words, "negative"))

    # Classify a new sample
    classifier = nltk.NaiveBayesClassifier.train(training)
    s = input("Sentence: ")
    result = (classify(classifier, s, words))
    for key in result.samples():
        print(f"{key}: {result.prob(key):.4f}")


def extract_word(document):
    return set(
        word.lower() for word in nltk.word_tokenize(document)
        if any (c.isalpha() for c in word)
    )

def load_data(directory):
    result = []
    for filename in os.listdir(directory) :
        with open(os.path.join(directory, filename)) as f:
            result.append([
                extract_word(line)
                for line in f.read().splitlines()
            ])
    return result

def generate_feature(documents, words, label):
    features = []
    for document in documents:
        features.append(({
            word: (word in document)
            for word in words
        }, label))
    return features

def classify(classifier, document, words):
    document_words = extract_word(document)
    features = {
        word: (word in document)
        for word in words
    }
    print("Classifying: ", features)
    return classifier.prob_classify(features)

if __name__ == "__main__":
    main()