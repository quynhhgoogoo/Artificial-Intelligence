# Implement Hill Climbing algorithm
import random

class Space():

    def __init__(self, height, width, num_hospitals):
         ''' Create State Space with given dimenisons '''
         self.height = height
         self.width = width
         self.num_hospitals = num_hospitals
         self.houses = set()
         self.hospitals = set()

    def add_house(self, row, col):
        ''' Add a house at a specific location in state space '''
        self.houses.add((row, col))
    
    def available_spaces(self):
        '''Returns all available cells which is not used by a house or hospital'''
        # Consider all posible cells
        candidates = set (
            (row, col)
            for row in range (self.height)
            for col in range (self.width)
        )

        #Remove all cells used by houses and hospitals
        for house in self.houses:
            candidates.remove(house)
        for hospital in self.hospitals:
            candidates.remove(hospital)

        return candidates

    def hill_climb(self, maximum = None, image_prefix = None, log = False):
        '''Perform Hill Climbing to find solution'''
        count = 0

        # Initialize hospitals randomly
        self.hospitals = set()
        for i in range (self.num_hospitals):
            self.hospitals.add (random.choice(list(self.available_spaces())))
        if log:
            print("Initial State: cost", self.get_cost(self.hospitals))
        if image_prefix:
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

        # Continue until we reach to max number of iterations
        while maximum is None or count < maximum:
            count += 1
            best_neighbors = []
            best_neighbors_cost = None

            for hospital in self.hospitals:
                for replacement in self.get_neighbors(*hospital):
                    # Replace the old hospital placement with new one inside neigbour list
                    neighbour = self.hospitals.copy()
                    neighbour.remove(hospital)
                    neighbour.add(replacement)

                    # Check if neighbour is the best one so far
                    cost = self.get_cost(neighbour)
                    
                    if best_neighbors_cost is None or cost < best_neighbors_cost:
                        # Overwrite best neighbour list and update new cost
                        best_neighbors_cost = cost
                        best_neighbors = [neighbour]

                    elif best_neighbors_cost == cost:
                        # Add new neighbour to the list
                        best_neighbors.append(neighbour)

            # If none of the neigbours are better than current state
            if best_neighbors_cost >= self.get_cost(self.hospitals):
                return self.hospitals
            else:
                # Move to highest-valued neighbour
                if log:
                    print(f"Found better neighbor: cost {best_neighbors_cost}")
                self.hospitals = random.choice(best_neighbors)
            
            if image_prefix:
                self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")
            
    def random_restart(self, maximum, image_prefix=None, log=False):
        '''Repeats hill-climbing multiple times.'''
        best_hospitals = None
        best_cost = None

        # Repeat hill-climbing a fixed number of times
        for i in range (maximum):
            hospitals = self.hill_climb()
            cost = self.get_cost(hospitals)
            
            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_hospitals = hospitals
                if log:
                    print(f"{i}: Found new best state: cost {cost}")
            else:
                if log:
                    print(f"{i}: Found state: cost {cost}")
            
            if image_prefix:
                self.output_image(f"{image_prefix}{str(i).zfill(3)}.png")
        return best_hospitals


    def get_cost(self, hospitals):
        '''Calculates sum of distances from houses to nearest hospital'''
        cost = 0
        for house in self.houses:
            cost += min (
                abs (house[0] - hospital[0]) + abs(house[1] - hospital[1])
                for hospital in hospitals
            )
        
        return cost

    def get_neighbors(self, row, col):
        '''Returns neighbors not already containing a house or hospital'''
        # Get all the possible neighbour's placement
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col + 1),
            (row, col - 1)
        ]
        neighbours = []

        for r, c in candidates:
            # Keep looking for placement are not placed by houses and hospitals
            if (r, c) in self.houses or (r, c) in self.hospitals:
                continue
            if 0 <= r < self.height and 0 <= c <= self.width:
                neighbours.append((r, c))
        return neighbours

    def output_image(self, filename):
        '''Generates image with all houses and hospitals.'''
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10
 
        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "white"
        )
        house = Image.open("lectures/hospital/assets/images/House.png").resize(
            (cell_size, cell_size)
        )
        hospital = Image.open("lectures/hospital/assets/images/Hospital.png").resize(
            (cell_size, cell_size)
        )
        font = ImageFont.truetype("lectures/hospital/assets/fonts/OpenSans-Regular.ttf", 30)
        draw = ImageDraw.Draw(img)
 
        for i in range(self.height):
            for j in range(self.width):
 
                # Draw cell
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="black")
 
                if (i, j) in self.houses:
                    img.paste(house, rect[0], house)
                if (i, j) in self.hospitals:
                    img.paste(hospital, rect[0], hospital)
 
        # Add cost
        draw.rectangle(
            (0, self.height * cell_size, self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "black"
        )
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Cost: {self.get_cost(self.hospitals)}",
            fill="white",
            font=font
        )
 
        img.save(filename)

if __name__ == '__main__':
    # Create a space and add house randomly
    s = Space(height = 10, width = 20, num_hospitals = 3)
    for i in range (15):
        s.add_house(random.randrange(s.height), random.randrange(s.width))

    # Find hospital placement using local search
    hospitals = s.hill_climb(image_prefix = "hospitals", log = True)