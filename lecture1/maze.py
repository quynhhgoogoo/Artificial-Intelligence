import sys

# Intialize node for graph
class Node():
    def __init__(self, state, parent, action):
        self.state = state              # coordinate of the node
        self.parent = parent
        self.action = action            # moving direction 

# Initilize queue frontier for BFS
class StackFrontier():
    def __init__(self):
        # Create an empty list to store the frontier
        self.frontier = []

    # Add new node to frontier
    def add(self, node):
        self.frontier.append(node)

    # Check if frontier contains node
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
class QueueFrontier(StackFrontier):
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
    # Construct maze with maze width/height, walls, start and goal point, solution bool
    def __init__(self, filename):
        # Read file and set up the maze
        with open(filename) as f:
            contents = f.read()
        
        # Check if start point and goal point are valid
        if contents.count("A") != 1:
            raise Exception("Maze needs to have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze needs to have exactly one goal point")
        
        # Determine height and width of maze
        # Converting txt file as a list of splitted elements (maze row)
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of obstacles
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
                
                self.walls.append(row)
            # Create a list to store solution node
            self.solution = None

    # Print out solution
    def print_path(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i,j) == self.start:
                    print("A", end="")
                elif (i,j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    # Adding neighbour node to explored table
    def neighbours(self,state):
        row, col = state

        # Store the coordinate of neighbour node [actions, (row, column)]
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Store all accessible node to a neighbour table
        result = []
        for action, (row, column) in candidates:
            # If node is accessible to build a path
            if (0 <= row < self.height) and (0 <= column < self.width) and not self.walls[row][column]:
                result.append((action, (row,column)))
            return result

    # Find solution to maze
    def solve(self):
        
        # Keep track of number of states that has been explored
        self.num_explored = 0

        # Initialize frontier and add the starting/root node
        start = Node(state = self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize empty explored set
        self.explored = set()

        while True:
            # Check if frontier is empty
            if frontier.empty():
                raise Exception("No solution found")

            # Retrieve one node from frontier
            node = frontier.remove()
            self.num_explored += 1

            # Check if node is goal
            if node.state == self.goal:
                actions = []
                cells = []
                # Store all the node and its state in path solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                # Create a route from start point to goal
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return None

            # Mark node as explored
            self.explored.add(node.state)

            # Add node's neighbor to frontier
            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state = state, parent = node, action = action)
                    frontier.add(child)

    # Draw solution as an image
    # show_solution: show the path to goal after searching
    # show_explore: show all the node that the algorithm has itterated through
    def output_image(self, filename, show_solution = True, show_explore = False):
        pass

if __name__ == '__main__':
    # If the arguments is not passed correctly
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    m = Maze(sys.argv[1])
    
    print("Maze: ")
    m.print_path()
    
    print("Solving maze")
    m.solve()
    print("States Explored:", m.num_explored)
    print("Solution: ")
    m.print_path()

    m.output_image("maze.png", show_explore=True)