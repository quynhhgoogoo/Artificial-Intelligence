import sys

# Intialize node for graph
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Initilize queue frontier for BFS
class QueueFrontier():
    def __init__(self):
        # Create an empty list to store the frontier
        self.frontier = []

    # Add new node to frontier
    def add(self, node):
        self.frontier.append(node)

    # Check if node inside frontier contains state
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    # Check if frontier list is empty
    def empty(self):
        return len(self.frontier) == 0

    # Remove a node from frontier list
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            # Retrieve last node in frontier list
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# Initialize stack frontier for DFS
class StackFrontier(QueueFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            # Retrieve first node in frontier list
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# Initialize class for maze
class Maze():
    def __init__(self, filename):
        pass

    # Print out solution
    def print_path(self):
        pass

    # Adding neighbour node to explored table
    def neighbours(self,state):
        pass

    # Find solution to maze
    def solve(self):
        pass

    # Draw solution as an image
    # show_solution: show the path to goal after searching
    # show_explore: show all the node that the algorithm has itterated through
    def output_image(self, filename, show_solution = True, show_explore = False):
        pass

if __name__ == '__main__':
    # If the arguments is not passed correctly
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    m = Maze(sys.arg[1])
    
    print("Maze: ")
    m.print_path()
    
    print("Solving maze")
    m.solve()
    print("Solution: ")
    m.print_path()

    m.output_image("maze.png", show_explore=True)