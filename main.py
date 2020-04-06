import opc
import random
import copy
from tkinter import *

'''
Helper function to easily 
generate tuples based on 
colour name
'''


def randomPx():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def px(color):
    if color == "red":
        return (255, 0, 0)
    elif color == "green":
        return (0, 255, 0)
    elif color == "blue":
        return (0, 0, 255)
    elif color == "black":
        return (0, 0, 0)
    elif color == "white":
        return (255, 255, 255)


'''
Window class for the
tkinter window and to 
manage the controls 
'''


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x300")
        self.root.title("Coursework")
        self.root.bind("<Key>", self.key)

        frame = Frame(self.root)
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        frame.grid(row=0, column=0, sticky=N+S+E+W)
        grid = Frame(frame)
        grid.grid(sticky=N+S+E+W, column=0, row=0, columnspan=2)

        upBtn = Button(frame, text="Up",
                       command=lambda: self.btnEvent("up"))
        upBtn.grid(column=1, row=0, sticky=N+S+E+W)

        ltBtn = Button(frame, text="Left",
                       command=lambda: self.btnEvent("left"))
        ltBtn.grid(column=0, row=1, sticky=N+S+E+W)

        rtBtn = Button(frame, text="Right",
                       command=lambda: self.btnEvent("right"))
        rtBtn.grid(column=2, row=1, sticky=N+S+E+W)

        dnBtn = Button(frame, text="Down",
                       command=lambda: self.btnEvent("down"))
        dnBtn.grid(column=1, row=2, sticky=N+S+E+W)

        for x in range(3):
            Grid.columnconfigure(frame, x, weight=1)

        for y in range(3):
            Grid.rowconfigure(frame, y, weight=1)

    def mainloop(self):
        self.root.mainloop()

    def key(self, event):
        snake.set_direction(event.keysym.lower())

    def btnEvent(self, direction):
        snake.set_direction(direction)


'''
Screen class to abstract
away the opc methods
'''


class Screen:
    def __init__(self, screen=[]):
        self.screen = screen
        self.client = opc.Client('localhost:7890')

    def render(self, screen):
        self.client.put_pixels(screen)
        self.client.put_pixels(screen)


'''
Just a simple class
for a point with an
x & y position
'''


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


'''
The class for the
player & snake
'''


class Snake:
    def __init__(self, direction='left'):
        self.body = [Point(57, 0), Point(58, 0), Point(59, 0)]
        self.direction = direction
        self.grow = False

    def show(self, screen):
        for point in self.body:
            screen[point.y][point.x] = px("red")

    def eat(self, food, screen):
        screen[food.y][food.x] = px("black")
        self.grow = True

    def set_direction(self, direction):
        if self.direction == "right" and direction == "left":
            self.direction = "right"
        elif self.direction == "left" and direction == "right":
            self.direction = "left"
        elif self.direction == "up" and direction == "down":
            self.direction = "up"
        elif self.direction == "down" and direction == "up":
            self.direction = "down"
        else:
            self.direction = direction

    def move(self, screen):
        newSnake = copy.deepcopy(self.body)
        newHead = newSnake[0]

        if self.direction == "right":
            newHead.x += 1
        elif self.direction == "left":
            newHead.x -= 1
        elif self.direction == "up":
            newHead.y -= 1
        elif self.direction == "down":
            newHead.y += 1

        if newHead.x >= 60:
            newHead.x = 0

        elif newHead.x <= -1:
            newHead.x = 59

        if newHead.y >= 6:
            newHead.y = 0
        elif newHead.y <= -1:
            newHead.y = 5

        if not self.grow:
            toClear = self.body.pop()
            screen[toClear.y][toClear.x] = px("black")

        self.body.insert(0, newHead)
        self.grow = False


window = Window()

screen = Screen()
snake = Snake()
apple = Point(0, 0)


def update():
    gameOver = False
    screen_arr = [[px("black") for i in range(60)] for j in range(6)]

    for i in range(1, len(snake.body)-1):
        if snake.body[i].x == snake.body[0].x and snake.body[i].y == snake.body[0].y:
            gameOver = True

    if gameOver:
        screen_arr = [[randomPx() for i in range(60)] for j in range(6)]
        screen.render([j for sub in screen_arr for j in sub])
        window.root.after(100, update)
    else:
        snake.show(screen_arr)
        screen_arr[apple.y][apple.x] = px("green")

        if snake.body[0].x == apple.x and snake.body[0].y == apple.y:
            snake.eat(apple, screen_arr)
            while True:
                apple.x = random.randint(0, 59)
                apple.y = random.randint(0, 5)

                inBody = False

                for piece in snake.body:
                    if piece.x == apple.x and piece.y == apple.y:
                        inBody = True

                if inBody:
                    continue
                else:
                    break

        screen.render([j for sub in screen_arr for j in sub])
        snake.move(screen_arr)
        window.root.after(100, update)


window.root.after(100, update)
window.mainloop()
