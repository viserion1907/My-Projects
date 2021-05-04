""" A simple Square Hunt game using Python turtle graphics"""
import random
import threading
import turtle
import sys

# Named constants for the layout
WINDOW_WIDTH = 750  # Screen width
WINDOW_HEIGHT = 800  # Screen height
GRID_SIZE = 700  # Size of the grid (700 x 700)
BTM_LEFT_X = -350  # Bottom left corner of grid (x-coordinate)
BTM_LEFT_Y = -375  # Bottom left corner of grid (y-coordinate)
TITLE_XCOR = -350  # Game title x-coordinates
TITLE_YCOR = 345  # Game title y-coordinates
START_BTN_X = 0  # Start button x-coordinate
START_BTN_Y = 345  # Start button y-coordinate
START_BTN_BORDER_X = -55  # Start button border x-coordinate
START_BTN_BORDER_Y = 340  # Start button border y-coordinate
START_BTN_BORDER_LENGTH = 114  # Start button border length
SCORE_XCOR = 350  # Score display x-coordinates
SCORE_YCOR = 345  # Score display y-coordinates
MARGIN = 10  # Margin around size of the target box in pixels
PENSIZE = 3  # Set the pen size to 3

grid_box = 0  # Variable to hold the grid box value
timer = 0  # Variable to set the difficulty level
score = 0  # Create a score global variable to keep track of the score
square_count = 0  # Create a square count global variable to keep track of the squares


def setup():
    """ Provide the config for the screen """
    turtle.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    turtle.speed(0)  # Disable all turtle animation
    turtle.hideturtle()  # Hide the turtle
    turtle.tracer(10)  # auto-refresh the screen after every 10 drawing steps
    turtle.pensize(PENSIZE)
    turtle.penup()  # Put the pen up to prevent unnecessary drawings
    turtle.goto(TITLE_XCOR, TITLE_YCOR)
    turtle.write('Square Hunt', False, align='left', font=('Arial', 20, 'normal'))  # Display the game title
    turtle.goto(START_BTN_BORDER_X, START_BTN_BORDER_Y)
    turtle.pendown()
    # Draw the start button border
    turtle.begin_fill()
    turtle.fillcolor('#06C7BA')
    for i in range(4):
        if i % 2 == 0:
            turtle.forward(START_BTN_BORDER_LENGTH)
            turtle.left(90)
        else:
            turtle.forward(40)
            turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.goto(START_BTN_X, START_BTN_Y)
    turtle.write('START', False, align='center', font=('Arial', 17, 'bold'))  # Display the start button
    turtle.goto(SCORE_XCOR, SCORE_YCOR)
    turtle.write('Score: 0', False, align='right', font=('Arial', 20, 'normal'))  # Display the initial score


def draw_grid():
    """ Function to draw the 700 x 700 grid """
    turtle.goto(BTM_LEFT_X, BTM_LEFT_Y)  # Go to the bottom-left corner of the screen
    turtle.pendown()  # Put the pen down
    turtle.pensize(PENSIZE)  # Set the pen's width to 3 pixels
    turtle.pencolor('brown')  # Set the pen colour to brown
    # Create a loop to draw a 4 x 4 grid
    for side in range(4):
        turtle.forward(GRID_SIZE)
        turtle.left(90)


def draw_x_axis(x_axis):
    """ Function to draw the x-axis grid lines """
    for line in range(x_axis):
        turtle.penup()
        turtle.goto(BTM_LEFT_X, BTM_LEFT_Y + (line * GRID_SIZE / x_axis))
        turtle.pendown()
        turtle.forward(GRID_SIZE)


def draw_y_axis(y_axis):
    """ Function to draw the y-axis grid lines """
    turtle.left(90)  # Turn the turtle to face north (the y-axis)
    for line in range(y_axis):
        turtle.penup()
        turtle.goto(BTM_LEFT_X + (line * GRID_SIZE / y_axis), BTM_LEFT_Y)
        turtle.pendown()
        turtle.forward(GRID_SIZE)


def draw_target(grid_box_size):
    """ Function to draw the target squares """
    actual_grid_size = GRID_SIZE // grid_box_size  # Get the dimensions of each grid box
    target_size = actual_grid_size - 2 * MARGIN  # Get the dimensions of the target square
    # Create a random (x,y) coordinate to start the drawing
    target_x = random.randrange(BTM_LEFT_X + MARGIN, BTM_LEFT_X + GRID_SIZE - MARGIN, actual_grid_size)
    target_y = random.randrange(BTM_LEFT_Y + MARGIN, BTM_LEFT_Y + GRID_SIZE - MARGIN, actual_grid_size)
    turtle.penup()
    turtle.setheading(0)  # Make the turtle face east (0 degrees)
    turtle.goto(target_x, target_y)
    turtle.pendown()  # Put the pen down
    turtle.pensize(PENSIZE)  # Set the pen's width to 3 pixels
    turtle.pencolor('green')  # Set the pen colour to green
    turtle.fillcolor('green')  # Set the fill colour to green
    turtle.begin_fill()
    for side in range(4):
        turtle.forward(target_size)
        turtle.left(90)
    turtle.end_fill()


def clear_target(grid_box_size):
    """ Function to clear the target squares """
    actual_grid_size = GRID_SIZE // grid_box_size  # Get the dimensions of each grid box
    target_size = actual_grid_size - 2 * MARGIN  # Get the dimensions of the target square
    turtle.penup()
    turtle.setheading(0)
    turtle.goto(turtle.xcor(), turtle.ycor())  # Go to drawing's current location
    turtle.pendown()
    turtle.pensize(PENSIZE)  # Set the pen's width to 3 pixels
    turtle.pencolor('white')  # Set the pen colour to white
    turtle.fillcolor('white')  # Fill the square with white
    turtle.begin_fill()
    for side in range(4):
        turtle.forward(target_size)
        turtle.left(90)
    turtle.end_fill()


def handle_click(x, y):
    """ Click handler function which receives (x,y) location of a click point. This function is called automatically
    when a left click is detected anywhere in the window """
    # Check that clicks are registered within the game boundary
    if ((BTM_LEFT_X + MARGIN) <= x <= (BTM_LEFT_X - MARGIN + GRID_SIZE)) and \
            ((BTM_LEFT_Y + MARGIN) <= y <= (BTM_LEFT_Y - MARGIN + GRID_SIZE)):
        print('Detected a click at', x, y)
    else:
        print('Out of grid boundary')

    # This initiates the start of the game after the user clicks on the start button
    if START_BTN_BORDER_X <= x <= (START_BTN_BORDER_X + START_BTN_BORDER_LENGTH) and \
            START_BTN_BORDER_Y <= y <= (START_BTN_BORDER_Y + START_BTN_BORDER_LENGTH):
        print('GAME STARTED')
        update_start_text()
        start_string = '[' + str(square_count) + ']'  # Display the initial score value at start game
        turtle.write(start_string, False, align='center', font=('Arial', 20, 'normal'))
        turtle.setheading(0)
        next_square(grid_box, timer)  # Call the next_square function to kickstart the loop
    else:
        print('GAME NOT STARTED!')

    update_score(x, y)  # Call the update_score function to start updating the score


def update_score(target_x, target_y):
    """ This function updates the score after a successful hit or decrement after a miss """
    global score  # score to update
    actual_grid_size = GRID_SIZE // grid_box  # Get the dimensions of each grid box
    target_size = actual_grid_size - 2 * MARGIN  # Get the dimensions of the target square

    # Register a successful hit, change the cell colour and increment the score by one
    if turtle.xcor() <= target_x <= (turtle.xcor() + target_size) and turtle.ycor() <= target_y <= (turtle.ycor() + target_size) and turtle.fillcolor() == 'green':
        score += 1  # Increment score on a successful hit
        turtle.pencolor('#33DDFF')  # Set the pen colour to bright blue
        turtle.fillcolor('#33DDFF')  # Fill the square with bright blue
        turtle.begin_fill()
        for side in range(4):
            turtle.forward(target_size)
            turtle.left(90)
        turtle.end_fill()
        print('Hit', score)
    else:
        score -= 1  # Subtract one from score if hit is missed
        if score < 0:  # If score is decremented to below zero, initialize it to zero
            score = 0
        print('Miss', score)


def update_score_text():
    """ This function updates the score text to reflect the current results """
    global score
    turtle.setheading(0)
    turtle.penup()
    # Draw a white rectangle to clear the score each time it is updated
    turtle.goto(SCORE_XCOR, SCORE_YCOR)
    turtle.pendown()
    turtle.pencolor('white')
    turtle.fillcolor('white')
    turtle.begin_fill()
    for i in range(4):
        if i % 2 == 0:
            turtle.backward(START_BTN_BORDER_LENGTH)
            turtle.left(90)
        else:
            turtle.forward(40)
            turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.pencolor('black')
    score_string = 'Score: %s' % score
    turtle.write(score_string, False, align='right', font=('Arial', 20, 'normal'))


def next_square(grid_box_size, seconds):
    """ This function handles the displaying of target squares, erasing them and keeping a count of the number of
    squares while updating the thread """
    global square_count
    square_count += 1  # Increment square_count by 1
    if square_count <= 20:  # Set square count to 20 as it iterates between drawing and clearing a cell, 10 times each
        if square_count % 2 != 0:
            print('Draw cell', square_count)
            draw_target(grid_box_size)  # Function draws the target square on the main grid
        else:
            print('Clear cell', square_count)
            clear_target(grid_box_size)  # Clear the target square function
            update_start_text()
            turtle.write('[' + str(square_count // 2) + ']', False, align='center', font=('Arial', 20, 'normal'))
            update_score_text()
        th = threading.Timer(interval=seconds, function=next_square, args=(grid_box_size, seconds))
        th.start()
    else:
        update_start_text()
        turtle.write('FINISHED', False, align='center', font=('Arial', 20, 'italic'))


def update_start_text():
    """ This function clears the start button and  updates the square counter on the turtle window """
    turtle.setheading(0)
    turtle.penup()
    # Draw a white rectangle to clear the square each time it is updated
    turtle.goto(START_BTN_BORDER_X, START_BTN_BORDER_Y)
    turtle.pendown()
    turtle.begin_fill()
    turtle.pencolor('white')
    turtle.fillcolor('white')
    for i in range(4):
        if i % 2 == 0:
            turtle.forward(START_BTN_BORDER_LENGTH)
            turtle.left(90)
        else:
            turtle.forward(40)
            turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.pencolor('black')
    turtle.goto(START_BTN_X, START_BTN_Y)


def main():
    """ Main function """
    global grid_box, timer
    # Get user input via dialogue box
    grid_box = int(turtle.textinput('Grid Size (N)', 'Provide the grid size (3-8):'))
    difficulty = int(turtle.textinput('Difficulty Level', 'Choose a difficulty level (1-3):'))

    # Ensure user enters correct dimensions and data
    if (grid_box < 3 or grid_box > 8) or (difficulty < 1 or difficulty > 3):
        sys.exit('Please enter a valid grid size (3-8) and/or difficulty level (1-3)')
    else:
        if difficulty == 1:
            timer = 2
        elif difficulty == 2:
            timer = 1.5
        else:
            timer = 1

        setup()  # Call the screen setup function
        draw_grid()  # Call the function to draw the grid
        draw_x_axis(grid_box)  # Call the function to draw the horizontal lines (x-axis)
        draw_y_axis(grid_box)  # Call the function to draw the vertical lines (y-axis)

        turtle.listen()  # Register handle_click as the listener function
        turtle.onscreenclick(handle_click)  # pass the function name as argument
        turtle.done()  # Prevent the graphics window from automatically closing


main()  # Call the main function
