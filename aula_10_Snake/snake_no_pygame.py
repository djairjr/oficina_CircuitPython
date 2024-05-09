import random
import curses

# Set up the window
window = curses.initscr()
curses.curs_set(0)
window_height, window_width = window.getmaxyx()
game_window = curses.newwin(window_height, window_width, 0, 0)
game_window.keypad(1)
game_window.timeout(100)

# Set up the snake initial position and body
def resetgame():
    snake_x = window_width // 4
    snake_y = window_height // 2
    snake_body = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    # Set up the food initial position
    food = [window_height // 2, window_width // 2]
    game_window.addch(food[0], food[1], curses.ACS_PI)

    # Set up the initial direction and key bindings
    key = curses.KEY_RIGHT

directions = {
    curses.KEY_RIGHT: [0, 1],
    curses.KEY_LEFT: [0, -1],
    curses.KEY_UP: [-1, 0],
    curses.KEY_DOWN: [1, 0]
}

# Game logic
key = curses.KEY_RIGHT
resetgame()

while True:
    next_key = game_window.getch()
    key = key if next_key == -1 else next_key

    # Calculate the new head position
    new_head = [snake_body[0][0] + directions[key][0], snake_body[0][1] + directions[key][1]]

    # Check for game over conditions
    if (
        new_head[0] in [0, window_height - 1] or
        new_head[1] in [0, window_width - 1] or
        new_head in snake_body[1:]  # Check if new head position is in the snake body (excluding the head)
    ):
        resetgame()

    else:
        # Insert the new head and update the snake body
        snake_body.insert(0, new_head)

        # Check if the snake has eaten the food
        if snake_body[0] == food:
            # Generate new food position
            food = None
            while food is None:
                nf = [
                    random.randint(1, window_height - 2),
                    random.randint(1, window_width - 2)
                ]
                food = nf if nf not in snake_body else None
            game_window.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove the tail segment if snake did not eat food
            tail = snake_body.pop()
            game_window.addch(tail[0], tail[1], ' ')

    # Draw the snake at the new position
    game_window.addch(snake_body[0][0], snake_body[0][1], curses.ACS_CKBOARD)

    # Refresh the window
    game_window.refresh()
