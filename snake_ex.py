from tkinter import *
import tkinter as tk
import random
import os

GAME_WIDTH = 1000   #initializes the constants
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
    
    def __init__(self, snake):

        x, y = aux_random(snake)

        self.coordinates = [x, y]

        screen.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=POINT_COLOUR, tag="point") #creates a point at random x, y coordinates

def aux_forget():   #auxilary function that deletes everything from the screen
    screen.delete(ALL)
    start_btn.place_forget()
    spd_btn.place_forget()
    plusspd_button.place_forget()
    minusspd_button.place_forget()
    speedometer.place_forget()
    hiscore_btn.place_forget()
    restart_btn.place_forget()
    return_btn.place_forget()
    reset_btn.place_forget()

def aux_start_menu():   #auxilary functions that calls all the main menu elements
    start_btn.place (x= ((screen.winfo_width())/2)-80, y=1)
    spd_btn.place (x= ((screen.winfo_width())/2)-80, y=100)
    plusspd_button.place (x= ((screen.winfo_width())/2)-80+350, y=100)
    minusspd_button.place (x= ((screen.winfo_width())/2)-80-50, y=100)
    hiscore_btn.place (x= ((screen.winfo_width())/2)-80, y=200)
    speedometer.place(x=1, y=1)

def aux_random(snake):  #auxilary function that ensures the point doesn't spawn inside the snake
    global score

    x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE   #generates random coordinates for the point
    y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

    coordinates = [x, y]
    
    for i in range (0, int(score/(int(10-(speed/10))))+BODY_PARTS):
        a, b = snake.coordinates[i]

        if coordinates == [a, b]:   #if the point has the same coordinates as a body part of the snake calls the function again         
            return aux_random(snake) #and loops until the coordinates dont match
    return coordinates


def start_game():
    aux_forget()
    snake = Snake()
    point = Point(snake)
    label.config(text="Score:{}".format(score))

    next_turn(snake, point)         #starts the game proper


def next_turn(snake, point):    #this function makes the calculations for the next movement in the game and is looped until the game is over
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
        score += (int(10-(speed/10)))

        label.config(text="Score:{}".format(score))

        screen.delete("point")

        point = Point(snake)

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

def check_colision(snake):  #returns true if the snake's head collides with another part of its body
    
    x, y = snake.coordinates[0]

    for body_parts in snake.coordinates[1:]:
        if x == body_parts[0] and y == body_parts[1]:
            return True
        
    return False

def restart():
    global score
    global direction

    aux_forget()                    #resets everything necessary
    snake = Snake()
    point = Point(snake)
    score = 0
    direction = "right"
    label.config(text="Score:{}".format(score))

    next_turn(snake, point)         #starts the game again

def game_over():    #prints the necessary information forthe game over screen
    global score

    aux_forget()
    screen.create_text(screen.winfo_width()/2, (screen.winfo_height()/3 +45), font=("consolas", 70), text="GAME OVER", fill="red")
    screen.create_text(screen.winfo_width()/2, (screen.winfo_height()/2 +15), font=("consolas", 50), text="HI-SCORES:", fill="red")

    final_scores = ""

    for n in range(5):
        if score > int(hiscores[n]):
            hiscores.insert(n, score)
            screen.create_text(screen.winfo_width()/2, ((screen.winfo_height()/2)+(n+1)*50 +20), font=("consolas", 35), text="Score:{}".format(hiscores[n]), fill="red")
            hiscores.pop()
            score = 0
        else:
            screen.create_text(screen.winfo_width()/2, ((screen.winfo_height()/2)+(n+1)*50 +20), font=("consolas", 35), text="Score:{}".format(hiscores[n]), fill="red")
        
        final_scores += str(hiscores[n]) + " "

    f = open("hiscores.txt", "w")
    f.write(final_scores)
    f.close()

    restart_btn.place (x=((screen.winfo_width()/2)-120), y=1)
    return_btn.place (x= ((screen.winfo_width())/2)-90, y=100)


def change_speed(symbol):
    global speed

    if symbol == "+":
        if speed > 10:
            speed -= 10
    else:
        if speed < 100:
            speed += 10

    speedometer.config(text="Speed:{}".format(int(10-(speed/10))) )

def show_scores(hiscores):
    screen.create_text(screen.winfo_width()/2, (screen.winfo_height()/3)-50, font=("consolas", 70), text="HI-SCORES:", fill="red")

    aux_forget()
    start_btn.place (x= ((screen.winfo_width())/2)-80, y=1)
    return_btn.place (x= ((screen.winfo_width())/2)-90, y=100)
    reset_btn.place (x=1, y=1)

    for n in range(5):
        if n == 1:
            screen.create_text(screen.winfo_width()/2, (screen.winfo_height()/2), font=("consolas", 35), text="Score:{}".format(hiscores[n]), fill="red")
        else:
            screen.create_text(screen.winfo_width()/2, (screen.winfo_height()/2)+(n-1)*50, font=("consolas", 35), text="Score:{}".format(hiscores[n]), fill="red")

def return_to_menu():
    aux_forget()
    aux_start_menu()

def reset_scores():
    temp_scores = "0 0 0 0 0"
    hiscores = temp_scores.split()
    f = open("hiscores.txt", "w")
    f.write(temp_scores)
    f.close()
    show_scores(hiscores)
    

root = Tk()
root.title = "snake game"
#root.resizable(False, False)

score = 0
direction = "right"
speed = 50

if not os.path.isfile("hiscores.txt"):
    temp_scores = "0 0 0 0 0"
    hiscores = temp_scores.split()
else:
    f = open("hiscores.txt", "r")
    temp_scores = f.readline()
    hiscores = temp_scores.split()
    f.close()


label = Label(root, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

screen = Canvas(root, bg=BG_COLOUR, height = GAME_HEIGHT, width = GAME_WIDTH)
screen.pack()

speedometer = Label(screen, text="Speed:{}".format(int(speed/10)), font=("consolas", 40))

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
hiscore_btn = tk.Button(screen, font=("consolas", 35), text="HI-SCORES", bg="red", fg="black", command=lambda: show_scores(hiscores))
return_btn = tk.Button(screen, font=("consolas", 35), text="RETURN", bg="red", fg="black", command= return_to_menu)
reset_btn = tk.Button(screen, font=("consolas", 35), text="RESET", bg="red", fg="black", command= reset_scores)

aux_start_menu()

root.mainloop()