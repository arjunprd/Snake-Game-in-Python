from secrets import randbits
from tkinter import *
import random
from turtle import fillcolor
from webbrowser import BackgroundBrowser


Game_Width = 700 #width of game screen
Game_Height = 700 #height of game screen

Speed = 80 #speed of snake ; canvas updation rate
Space_Size = 25

Body_Parts = 3 #body parts of snake

Snake_Color = "#00FF00" # green snake

Food_Color = "#FF0000" #red 

Background_Color = "#000000" #black 

#Snake class
class Snake:
    
    def __init__(self):

        self.body_size = Body_Parts
        self.coordinates = []

        self.squares = []


        #creates head of snake
        for i in range(0,Body_Parts):
            self.coordinates.append([0,0]) #start snake from top left most corner


        for x , y in self.coordinates:
            square = canvas.create_rectangle(x,y , x + Space_Size , y + Space_Size , fill = Snake_Color , tag ="snake")
            self.squares.append(square)

        
#Food class
class Food:
     
     def __init__(self):

        #random coordinates for food
        x = random.randint(0,(Game_Width/Space_Size)-1) * Space_Size
        y = random.randint(0,(Game_Width/Space_Size) - 1) * Space_Size

        self.coordinates =  [x , y]

        #creates food
        canvas.create_oval(x , y , x + Space_Size , y + Space_Size , fill = Food_Color , tag = "food")




def next_turn(snake , food):


    #coordinates of head of snake
    x,y = snake.coordinates[0]

    if direction == "up":
        y -= Space_Size
    
    elif direction == "down":
        y += Space_Size

    elif direction == "left":
        x -= Space_Size

    elif direction == "right":
        x += Space_Size

    snake.coordinates.insert(0,(x , y))

    square = canvas.create_rectangle( x , y , x + Space_Size , y + Space_Size , fill = Snake_Color)

    snake.squares.insert(0 , square)



    #if head of snake encounters food
    if x == food.coordinates[0] and y == food.coordinates[1]:

        #increment and update score
        global score

        score+=1

        label.config(text ="Score:{}".format(score))

        #delete food object
        canvas.delete("food")

        #make new food object somewhere else
        food = Food()

    else:

        #delete last body part of snake
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    
    #if snake collides with walls 
    if check_collision(snake):
        
        game_over()

    else:
        #for next turn
        window.after(Speed , next_turn , snake , food)



#to change direction of snake
def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
   
 


#if snake collides with wall or its own body part
def check_collision(snake):
    
    x  ,  y = snake.coordinates[0]

    #if head collides with window wall
    #end game
    if x < 0 or x >= Game_Width:
        return True
    elif y < 0 or y >= Game_Height:
        return True
         

    #if snake head encounters its own body part
    #end game
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Game over")
            return True 
    
    return False



def game_over():
    
    canvas.delete(ALL)

    canvas.create_text(canvas.winfo_width()/2 , canvas.winfo_height()/2 , font =('consolas',70) , text = "GAME OVER", fill = "red" , tag = "gameover") 



window = Tk()
window.title("Snake game")
window.resizable(False , False) #window cannot be resized

score = 0
direction = 'down' #initial direction

label = Label(window , text = "Score : {}".format(score) , font =('consolas',40)) #shows score
label.pack()

canvas = Canvas(window , bg  = Background_Color , height = Game_Height , width = Game_Width )
canvas.pack()

window.update() #window renders

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Bind control keys
window.bind('<Left>' , lambda event : change_direction('left'))
window.bind('<Right>' , lambda event : change_direction('right'))
window.bind('<Up>' , lambda event : change_direction('up'))
window.bind('<Down>' , lambda event : change_direction('down'))


snake = Snake() #snake object
food = Food() #food object



next_turn(snake,food)



window.mainloop()
