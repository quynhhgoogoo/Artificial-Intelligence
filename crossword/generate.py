import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword

        # Adding all available words inside word list to domain
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print_crossword(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            for word in self.crossword.words:
                # If length of word is not consistent
                if len(word) != variable.length:
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        overlap = self.crossword.overlaps[x, y]
        domains_copy = copy.deepcopy(self.domains)

        if overlap:
            # Get the coordinate of overlapping position 
            i, j = overlap

            for val_x in domains_copy[x]:
                word_matched = False
                
                for val_y in self.domains[y]:
                    # If x and y have same word in overlapping position
                    if val_x[i] == val_y[j]:
                        word_matched = True
                        break

                # Remove words from domain if overlapping position is not matching
                if word_matched:
                    continue 
                else:
                    self.domains[x].remove(val_x)
                    revision = True

        return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Get the initial list of arcs
        if arcs is None:
            # Stare with initial queue of all of the arcs in the problem
            queue = []
            for word in self.crossword.variables:
                for neighbors_word in self.crossword.neighbors(word):
                    queue.append((word, neighbors_word))
        else:
            queue = list(arcs)

        # Revise each arc in the queue
        while queue:
            x, y = queue.pop(0)
            list_y = set()
            list_y.add(y)

            # If there is revision made for domain x
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                
                for neighbor in self.crossword.neighbors(x) - list_y:
                    queue.append((x, neighbor))
        return True                


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = True
        for var in self.domains:
            if var not in assignment:
                complete = False
        return complete


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for variable1 in assignment:
            word1 = assignment[variable1]

            # Check if word has correct length
            if len(word1) != variable1.length:
                return False

            for variable2 in assignment:
                word2 = assignment[variable2]

                # Check if word is distinct
                if  variable1 != variable2:
                    if word1 == word2:
                        return False 

                    # Check if there is any conflicts between words
                    overlap = self.crossword.overlaps[variable1, variable2]
                    if overlap is not None:
                        i, j = overlap
                        if word1[i] != word2[j]:
                            return False
                
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        var_domain = dict()

        for i in assignment:
            if i in neighbors:
                neighbors.remove(i)

        for word in self.domains[var]:
            removed_element = 0

            # Rules out neighbor's words which does not belong to the domain
            for neighbor in neighbors:
                i, j = self.crossword.overlaps[var, neighbor]
                
                for neighbor_word in self.domains[neighbor]:
                    # Check if overlap word is consistent
                    if word[i] != neighbor_word[j]:
                        removed_element += 1

            # map each word and its number of eliminated neighbour values
            var_domain[word] = removed_element

        # sort words by number of eliminated neighbour values
        sorted_domain = sorted(var_domain.items(), key=lambda item: item[1])
        for w, n in sorted_domain:
            return w, n


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return variable


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assignment is completed
        if self.assignment_complete(assignment):
            return assignment

        # Get one of the unassigned element
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            
            # If value is consistent with assignment
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print_crossword(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
