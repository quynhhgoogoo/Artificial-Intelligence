import nltk

def grammar1():
    grammar = nltk.CFG.fromstring("""
        S -> NP VP

        NP -> D N | N
        VP -> V | V NP

        D -> "the" | "a"
        N -> "she" | "city" | "car"
        V -> "saw" | "walked"
    """)

    parser = nltk.ChartParser(grammar)

    sentence = input("Sentence: ").split()

    try:
        for tree in parser.parse(sentence):
            tree.pretty_print()
            tree.draw()
    except ValueError:
        print ("No parse tree possible")

def grammar2():
    grammar = nltk.CFG.fromstring("""
    S -> NP VP

    AP -> A | A AP
    NP -> N | D NP | AP NP | N PP
    PP -> P NP
    VP -> V | V NP | V NP PP
 
    A -> "big" | "blue" | "small" | "dry" | "wide"
    D -> "the" | "a" | "an"
    N -> "she" | "city" | "car" | "street" | "dog" | "binoculars"
    P -> "on" | "over" | "before" | "below" | "with"
    V -> "saw" | "walked"
    """)

    parser = nltk.ChartParser(grammar)

    sentence = input("Sentence: ").split()

    try:
        for tree in parser.parse(sentence):
            tree.pretty_print()
            tree.draw()
    except ValueError:
        print ("No parse tree possible")


if __name__ == '__main__':
    grammar2()