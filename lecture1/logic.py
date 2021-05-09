import itertools

class Sentence():
    def evaluate(self, model):
        """
        Evaluates the logical sentence
        """
        pass

    def formula(self):
        """
        Return string formula representing logical sentence
        """
        return
    
    def symbols(self):
        """
        Return a set of all symbols in logical sentence
        """
        pass

    @classmethod
    def validate(cls, sentence):
        """
        Validate if input is a logical sentence
        """
        pass

    @classmethod
    def parenthesis(cls,s):
        """
        Parenthesizes an expression if it is not already parenthesized
        """
        pass


class Symbol(Sentence):
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def evaluate(self, model):
        pass

    def formula(self):
        pass

    def symbols(self):
        pass


class Not(Sentence):
    def __init__(self, operand):
        self.operand = operand
    
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def evaluate(self, model):
        pass

    def formula(self):
        pass

    def symbols(self):
        pass


class And(Sentence):
    def __init__(self, *conjuncts):
        self.conjuncts = list(conjuncts)
    
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def evaluate(self, model):
        pass

    def formula(self):
        pass

    def symbols(self):
        pass


class Or(Sentence):
    def __init__(self, *disjuncts):
        self.conjuncts = list(disjuncts)
    
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def evaluate(self, model):
        pass

    def formula(self):
        pass

    def symbols(self):
        pass


class Implication(Sentence):
    def __init__(self, anteceden, consequent):
        self.anteceden = anteceden
        self.consequent = consequent
    
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def evaluate(self, model):
        pass

    def formula(self):
        pass

    def symbols(self):
        pass


class Biconditional(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def evaluate(self, model):
        pass

    def formula(self):
        pass

    def symbols(self):
        pass


def model_check(knowledge, query):
    """
    Check if knowledge base entails query
    """
    pass