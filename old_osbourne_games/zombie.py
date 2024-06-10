'''
 Zombie Game - from https://github.com/kevinmcaleer/retro_fun
'''
import random
import time

# Constants for grid dimensions
GRID_WIDTH = 16
GRID_HEIGHT = 32

# Constants for number of zombies and quicksand
ZOMBIE_COUNT = 4
QUICKSAND_COUNT = 8

def initialize_screen():
    # Display the game title
    print("......ZOMBIES")
    print()

def get_random_coordinate(limit):
    # Generate a random coordinate within the given limit
    return random.randint(1, limit)

def create_empty_grid(width, height):
    # Create an empty grid with the given width and height
    grid = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(' ')
        grid.append(row)
    return grid

def draw_grid(human, zombies, quicksand):
    # Draw the grid with the current positions of the human, zombies, and quicksand
    
    # Create an empty grid
    grid = create_empty_grid(GRID_WIDTH, GRID_HEIGHT)
   
    # Place quicksand in the grid
    for x, y in quicksand:
        grid[y-1][x-1] = '*'
    
    # Place zombies in the grid
    for x, y in zombies:
        if x != 0 and y != 0:
            grid[y-1][x-1] = 'Z'
    
    # Place human in the grid
    human_x, human_y = human
    grid[human_y-1][human_x-1] = 'H'
    
    # Draw the grid with borders
    print("*"*(GRID_WIDTH+2))
    for row in grid:
        print("*" + ''.join(row) + "*")
    print("*"*(GRID_WIDTH+2))

def delay(seconds):
    # Delay for the given number of seconds
    time.sleep(seconds)

def get_keypress():
    # Get direction input from the user
    direction = input("Enter direction (w=up, x=down, s=stay, a=left, d=right, q=up-left, e=up-right, z=down-left, c=down-right): ").strip().lower()
    if direction == 'w': 
        return (0, -1) # Up
    elif direction == 'x': 
        return (0, 1)  # Down
    elif direction == 's':
        return (0, 0)  # Stay
    elif direction == 'a':
        return (-1, 0) # Left
    elif direction == 'd':
        return (1, 0)  # Right
    elif direction == 'q':
        return (-1, -1) # Up-left
    elif direction == 'e':
        return (1, -1) # Up-right
    elif direction == 'z':
        return (-1, 1) # Down-left
    elif direction == 'c':
        return (1, 1)  # Down-right
    else:
        print("Invalid input. Please use 'w', 's', 'a', 'd', 'q', 'e', 'z', or 'c'.")
        return get_keypress() # Keep calling until valid input

def main():
    initialize_screen()

    # Initialize positions of zombies and quicksand
    zombies = [(get_random_coordinate(GRID_WIDTH), get_random_coordinate(GRID_HEIGHT)) for _ in range(ZOMBIE_COUNT)]
    quicksand = [(get_random_coordinate(GRID_WIDTH), get_random_coordinate(GRID_HEIGHT)) for _ in range(QUICKSAND_COUNT)]
    
    # Initialize position of the human
    human_x = get_random_coordinate(GRID_WIDTH-2)
    human_y = get_random_coordinate(GRID_HEIGHT-2)
    human = (human_x, human_y)
    
     # Draw the initial grid
    draw_grid(human, zombies, quicksand)
    
    while True:
        # Get direction from user
        direction = get_keypress()
        human_x += direction[0]
        human_y += direction[1]
        
        # Check if the human has escaped
        if zombies == [(0, 0) for _ in range(4)]: # All zombies are caught
            print("CONGRATULATIONS! YOU ESCAPED!")
            break

        # Check if human is out of bounds
        if human_x in {1, GRID_WIDTH} or human_y in {1, GRID_HEIGHT}:
            print("YOU'RE IN THE SWAMP")
            continue
        
        # Check if human is in quicksand
        if (human_x, human_y) in quicksand:
            print("YOU'RE IN QUICKSAND")
            break
        
        # Check if human is caught by a zombie
        if (human_x, human_y) in zombies:
            print("YOU'RE CAUGHT!")
            break
        
        # Update human position and redraw the grid
        human = (human_x, human_y)
        draw_grid(human, zombies, quicksand)
        delay(0.5)
        
         # Move zombies towards the human
        for i, (zombie_x, zombie_y) in enumerate(zombies):
            if zombie_x == 0:
                continue # Skip inactive zombies
            
            # Move zombie closer to human
            if human_x != zombie_x:
                zombie_x += (human_x - zombie_x) // abs(human_x - zombie_x)
            if human_y != zombie_y:
                zombie_y += (human_y - zombie_y) // abs(human_y - zombie_y)
            
            # Check if zombie falls into quicksand
            if (zombie_x, zombie_y) in quicksand:
                zombies[i] = (0, 0)
                print("A ZOMBIE GOT STUCK IN QUICKSAND")
                continue
            
            # Check if zombie catches human
            if (zombie_x, zombie_y) == (human_x, human_y):
                print("CAUGHT!")
                return
            
            # Update zombie position and redraw the grid
            zombies[i] = (zombie_x, zombie_y)
            draw_grid(human, zombies, quicksand)
            delay(0.5)

if __name__ == "__main__":
    main()

