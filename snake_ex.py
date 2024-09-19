from tkinter import *
import tkinter as tk
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 5
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

def start_game():
    snake = Snake()
    point = Point()
    label.config(text="Score:{}".format(score))
    start_btn.place_forget()
    spd_btn.place_forget()
    plusspd_button.place_forget()
    minusspd_button.place_forget()
    speedometer.place_forget()

    next_turn(snake, point)         #starts the game again


def next_turn(snake, point):
    global speed

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
        root.after(speed, next_turn, snake, point)  

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

def restart():
    global score
    global direction

    screen.delete(ALL)              #resets everything to initial values
    restart_btn.place_forget()
    snake = Snake()
    point = Point()
    score = 0
    direction = "right"
    label.config(text="Score:{}".format(score))

    next_turn(snake, point)         #starts the game again

def game_over():
    
    screen.delete(ALL)
    screen.create_text(screen.winfo_width()/2, screen.winfo_height()/2, font=("consolas", 70), text="GAME OVER", fill="red")

    restart_btn.place (x=1, y=1)

def change_speed(symbol):
    global speed

    if symbol == "+":
        speed -= 10
    else:
        speed += 10

    speedometer.config(text="Speed:{}".format(int(10-(speed/10))) )
    

root = Tk()
root.title = "snake game"
#root.resizable(False, False)

score = 0
direction = "right"
speed = 50

label = Label(root, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

screen = Canvas(root, bg=BG_COLOUR, height = GAME_HEIGHT, width = GAME_WIDTH)
screen.pack()

speedometer = Label(screen, text="Speed:{}".format(int(speed/10)), font=("consolas", 40))
speedometer.place (x= ((GAME_WIDTH - SPACE_SIZE)/2), y=200)

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

start_btn = tk.Button(screen, font=("consolas", 35), text="START", bg="red", fg="black", command= start_game) 
restart_btn = tk.Button(screen, font=("consolas", 35), text="RESTART", bg="red", fg="black", command= restart)
spd_btn = tk.Button(screen, font=("consolas", 35), text="change speed", bg="red", fg="black", state= "disabled")
plusspd_button = tk.Button(screen, font=("consolas", 35), text=">", bg="red", fg="black", command=lambda: change_speed("+"))
minusspd_button = tk.Button(screen, font=("consolas", 35), text="<", bg="red", fg="black", command=lambda: change_speed("-"))

start_btn.place (x= ((GAME_WIDTH - SPACE_SIZE)/2), y=1)
spd_btn.place (x= ((GAME_WIDTH - SPACE_SIZE)/2), y=100)
plusspd_button.place (x= ((GAME_WIDTH - SPACE_SIZE)/2)+350, y=100)
minusspd_button.place (x= ((GAME_WIDTH - SPACE_SIZE)/2)-50, y=100)



root.mainloop()
