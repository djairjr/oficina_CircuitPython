class Zombie:
    def __init__(self, hardware):
        # Constants for grid dimensions
        self.hardware = hardware
        self.GRID_WIDTH = self.hardware.screen.width
        self.GRID_HEIGHT = self.hardware.screen.height

        # Constants for number of zombies and quicksand
        self.ZOMBIE_COUNT = 4
        self.QUICKSAND_COUNT = 8

        # Initialize positions of zombies and quicksand
        self.zombies = [(self.get_random_coordinate(self.GRID_WIDTH), self.get_random_coordinate(self.GRID_HEIGHT)) for _ in range(self.ZOMBIE_COUNT)]
        self.quicksand = [(self.get_random_coordinate(self.GRID_WIDTH), self.get_random_coordinate(self.GRID_HEIGHT)) for _ in range(self.QUICKSAND_COUNT)]

        # Initialize position of the human
        human_x = self.get_random_coordinate(self.GRID_WIDTH-2)
        human_y = self.get_random_coordinate(self.GRID_HEIGHT-2)
        self.human = (human_x, human_y)

        # Draw the initial grid
        self.play()
    
    def play(self):
        self.hardware.screen.fill (0)
        self.hardware.marquee("ZOMBIES", loop = False)
        self.create_empty_grid()
        self.draw_grid()
        self.update()
       
    def get_random_coordinate(self, limit):
        # Generate a random coordinate within the given limit
        return random.randint(1, limit)

    def create_empty_grid(self):
        # Create an empty grid
        grid = []
        for _ in range(self.GRID_HEIGHT):
            row = []
            for _ in range(self.GRID_WIDTH):
                row.append(0x000000) # pixel color 0x000000
            grid.append(row)
        return grid

    def draw_grid(self):
        # Draw the grid with the current positions of the human, zombies, and quicksand
        grid = self.create_empty_grid()

        # Place quicksand in the grid
        for x, y in self.quicksand:
            self.hardware.screen.pixel(x, y, 0xFFEBCD)  # BlanchedAlmond

        # Place zombies in the grid
        for x, y in self.zombies:
            if x != 0 and y != 0:
                self.hardware.screen.pixel(x, y, 0x8B008B)  # Zombie is Purple color Square

        # Place human in the grid
        human_x, human_y = self.human
        self.hardware.screen.pixel(human_x, human_y, 0xFFFFFF)  # Human is bright White Pixel

        # Draw the borders
        for x in range(self.GRID_WIDTH):
            self.hardware.screen.pixel(x, 0, 0x0000FF)  # Top border in blue
            self.hardware.screen.pixel(x, self.GRID_HEIGHT - 1, 0x0000FF)  # Bottom border in blue

        for y in range(1, self.GRID_HEIGHT - 1):
            self.hardware.screen.pixel(0, y, 0x0000FF)  # Left border in blue
            self.hardware.screen.pixel(self.GRID_WIDTH - 1, y, 0x0000FF)  # Right border in blue
        
        self.hardware.screen.display()

    def update(self):
        while True:
            # Get direction from user
            direction = self.hardware.get_direction()
            human_x, human_y = self.human
            human_x += direction[0]
            human_y += direction[1]
            
            # Check if the human has escaped
            if self.zombies == [(0, 0) for _ in range(4)]: # All zombies are caught
                self.hardware.marquee("CONGRATULATIONS! YOU ESCAPED!", loop = False)
                break

            # Check if human is out of bounds
            if human_x in {1, self.GRID_WIDTH} or human_y in {1, self.GRID_HEIGHT}:
                self.hardware.marquee("YOU'RE IN THE SWAMP", loop = False)
                continue
            
            # Check if human is in quicksand
            if (human_x, human_y) in self.quicksand:
                self.hardware.marqueeprint("YOU'RE IN QUICKSAND", loop = False)
                break
            
            # Check if human is caught by a zombie
            if (human_x, human_y) in self.zombies:
                self.hardware.marquee("YOU'RE CAUGHT!", loop = False)
                return
            
            # Update human position and redraw the grid
            self.human = (human_x, human_y)
            self.draw_grid()
            time.sleep(0.01)
            
            # Move zombies towards the human
            for i, (zombie_x, zombie_y) in enumerate(self.zombies):
                if zombie_x == 0:
                    continue # Skip inactive zombies
                
                # Move zombie closer to human
                if human_x != zombie_x:
                    zombie_x += (human_x - zombie_x) // abs(human_x - zombie_x)
                if human_y != zombie_y:
                    zombie_y += (human_y - zombie_y) // abs(human_y - zombie_y)
                
                # Check if zombie falls into quicksand
                if (zombie_x, zombie_y) in self.quicksand:
                    self.zombies[i] = (0, 0)
                    self.hardware.marquee("A ZOMBIE GOT STUCK IN QUICKSAND", loop = False)
                    continue
                
                # Check if zombie catches human
                if (zombie_x, zombie_y) == (human_x, human_y):
                    self.hardware.marquee("CAUGHT!", loop = False)
                    return
                
                # Update zombie position and redraw the grid
                self.zombies[i] = (zombie_x, zombie_y)
                self.draw_grid()
                time.sleep(0.01)
