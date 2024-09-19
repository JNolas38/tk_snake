from tkinter import *
import random

#window = root
#canvas = screen

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
BODY_COLOUR = "green"
POINT_COLOUR = "red"
BG_COLOUR = "black"

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square=screen.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BODY_COLOUR, tag="snake")
            self.squares.append(square)

class Point:
    
    def __init__(self):
        
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        screen.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=POINT_COLOUR, tag="point") #creates a point at random x, y coordinates

def next_turn(snake, point):

    x, y = snake.coordinates[0] #select snakes head

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    if x >= GAME_WIDTH:  #loop on x axis
        x = 0
    elif x < 0:
        x = GAME_WIDTH

    if y >= GAME_HEIGHT:  #loop on y axis
        y = 0
    elif y < 0:
        y = GAME_HEIGHT

    snake.coordinates.insert(0, (x, y))

    square = screen.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BODY_COLOUR)
    
    snake.squares.insert(0, square)


    if x == point.coordinates[0] and y == point.coordinates[1]: #if a point is taken create a new body part
        global score
        score += 1

        label.config(text="Score:{}".format(score))

        screen.delete("point")

        point = Point()

    else:                                                       #deletes last body part to simulate movement
        del snake.coordinates[-1]
        screen.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_colision(snake):                           #if colision is detected trigger game over
        game_over()

    else:                                               #otherwise loop the next_turn function
        root.after(SPEED, next_turn, snake, point)  

def change_direction(new_direction):
    
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction

def check_colision(snake):
    
    x, y = snake.coordinates[0]

    for body_parts in snake.coordinates[1:]:
        if x == body_parts[0] and y == body_parts[1]:
            return True
        
    return False

def game_over():
    
    screen.delete(ALL)
    screen.create_text(screen.winfo_width()/2, screen.winfo_height()/2, font=("consolas", 70), text="GAME OVER", fill="red")

root = Tk()
root.title = "snake game"
root.resizable(False, False)

score = 0
direction = "right"

label = Label(root, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

screen = Canvas(root, bg=BG_COLOUR, height = GAME_HEIGHT, width = GAME_WIDTH)
screen.pack()

root.update()

root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()

x = int((screen_width / 2) - (root_width / 2))
y = int((screen_height / 2) - (root_height / 2))
root.geometry(f"{root_width}x{screen_height}+{x}+{y}")

root.bind('<a>', lambda event: change_direction("left"))
root.bind('<d>', lambda event: change_direction("right"))
root.bind('<s>', lambda event: change_direction("down"))
root.bind('<w>', lambda event: change_direction("up"))

snake = Snake()
point = Point()
next_turn(snake, point) #start game by calling the next_turn function

root.mainloop()
