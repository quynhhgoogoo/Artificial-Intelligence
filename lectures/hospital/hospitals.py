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
        self.house.add((row, col))

    def available_spaces(self):
        '''Returns all available cells which is not used by a house or hospital'''
        pass

    def hill_climb(self, maximum = None, image_prefix = None, log = False):
        '''Perform Hill Climbing to find solution'''
        pass

    def random_restart(self, maximum, image_prefix=None, log=False):
        '''Repeats hill-climbing multiple times.'''
        pass

    def get_cost(self, hospitals):
        '''Calculates sum of distances from houses to nearest hospital'''
        pass

    def get_neighbors(self, row, col):
        '''Returns neighbors not already containing a house or hospital'''
        pass

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
        house = Image.open("assets/images/House.png").resize(
            (cell_size, cell_size)
        )
        hospital = Image.open("assets/images/Hospital.png").resize(
            (cell_size, cell_size)
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 30)
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