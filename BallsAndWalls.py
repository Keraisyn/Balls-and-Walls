"""
  ____        _ _              
 |  _ \      | | |       ___   
 | |_) | __ _| | |___   ( _ )  
 |  _ < / _` | | / __|  / _ \/\
 | |_) | (_| | | \__ \ | (_>  <
 |____/ \__,_|_|_|___/  \___/\/
 \ \        / /  | | |         
  \ \  /\  / /_ _| | |___      
   \ \/  \/ / _` | | / __|     
    \  /\  / (_| | | \__ \     
     \/  \/ \__,_|_|_|___/     
       by Matthews Ma

"""

from tkinter import *
from time import *
from math import *
from pickle import *
from functools import *
from winsound import *

# CONSTANTS AND GLOBALS

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
GRAVITY = 0.07
CANNON_SIZE = 50
Y_DRAG = 0.0
X_DRAG = 0.0000
ABSORPTION = 0.9
FONT = "Corbel"
mouseDown = False
objects = []

# TKINTER SETUP

root = Tk()
screen = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, background="#1A535C")
screen.pack()
root.update()


# GLOBAL VARIABLES

class Cache:
    drawMode = "none"
    gameMode = "editor"

    xPower = 0
    yPower = 0

    wallsLeft = StringVar()
    wallsLeft.set("11110")

    filled = False
    level = 0
    fired = False


# WINDOWS

class IntroScreen:
    buttonColour = "#4ECDC4"
    textColour = "#F7FFF7"

    def __init__(self, screen):
        self.screen = screen
        self.components = []  # To house all parts of the intro screen

        self.bg = "#1A535C"
        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")

        self.title = Label(root, text="balls & walls", fg=self.textColour, bg=self.bg,
                           font=(FONT, 100, "bold"))  # Create the widget
        self.title.place(x=SCREEN_WIDTH / 2, y=150, anchor="center")  # Place the widget on the screen
        self.components.append(self.title)  # Append it to the components array

        self.author = Label(root, text="by matthews ma", fg=self.textColour, bg=self.bg, font=(FONT, 20, "bold"))
        self.author.place(x=SCREEN_WIDTH / 2, y=230, anchor="center")
        self.components.append(self.author)

        self.startButton = Button(root, text="play", font=(FONT, 40, "bold"), cursor="hand2",
                                  width=10, height=1, bg=self.buttonColour, fg=self.textColour,
                                  command=self.levelSelect)
        self.startButton.place(x=SCREEN_WIDTH / 2, y=350, anchor="center")
        self.components.append(self.startButton)

        self.instructionsButton = Button(root, text="instructions", font=(FONT, 40, "bold"), cursor="hand2",
                                         width=10, height=1, fg=self.textColour, bg=self.buttonColour,
                                         command=self.instructions)
        self.instructionsButton.place(x=SCREEN_WIDTH / 2, y=500, anchor="center")
        self.components.append(self.instructionsButton)

        self.editorButton = Button(root, text="editor", font=(FONT, 40, "bold"), cursor="hand2",
                                   width=10, height=1, fg=self.textColour, bg=self.buttonColour, command=self.editor)
        self.editorButton.place(x=SCREEN_WIDTH / 2, y=650, anchor="center")
        self.components.append(self.editorButton)

    def instructions(self):
        # Show the instructions screen
        self.hide()
        instructions.show()

    def editor(self):
        # Show the editor screen
        self.hide()
        levelEditor.show()

    def levelSelect(self):
        # Show the level select screen
        self.hide()
        levelSelect.show()

    def hide(self):
        # Hide the current screen
        self.placeInfo = []  # Keep place() information so it can be brought back correctly

        for component in self.components:
            self.placeInfo.append(component.place_info())  # Save place() info
            component.place_forget()  # Remove widget from screen

        self.screen.delete(self.background)  # Also remove the background colour

    def show(self):
        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")  # Place the background colour
        for i in range(len(self.components)):
            self.components[i].place(self.placeInfo[i])  # Place the components with reference to the place() info array


# Create an instance
introScreen = IntroScreen(screen)


class LevelSelect:
    buttonColour = "#4ECDC4"
    textColour = "#F7FFF7"

    def __init__(self, screen):
        self.screen = screen
        self.components = []

        self.bg = "#1A535C"
        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")

        self.title = Label(root, text="select level", fg=self.textColour, bg=self.bg, font=(FONT, 100, "bold"))
        self.title.place(x=SCREEN_WIDTH / 2, y=150, anchor="center")
        self.components.append(self.title)

        # Level buttons
        self.counter = 1

        for i in range(2):  # 2 Rows
            for j in range(5):  # 5 Columns

                # Divide the screen evenly
                x = SCREEN_WIDTH / 6 * (j + 1)
                y = SCREEN_HEIGHT / 3 * (i + 1) + 100

                # Create, place, and append button to components
                self.components.append(
                    Button(root, text=str(self.counter), font=("Calibri", 40, "bold"), cursor="hand2",
                           width=3, height=1, bg=self.buttonColour, fg=self.textColour,
                           command=partial(self.game, self.counter)))
                self.components[-1].place(x=x, y=y, anchor="center")

                self.counter += 1

    def introScreen(self):
        self.hide()
        screen.delete("all")
        introScreen.show()

    def game(self, level):
        # Go to game screen and load the correct level
        Cache.gameMode = "game"
        self.hide()
        loadLevel(str(level))
        gameScreen.level = level
        gameScreen.show()

    def hide(self):
        self.placeInfo = []

        for component in self.components:
            self.placeInfo.append(component.place_info())
            component.place_forget()

        self.screen.delete(self.background)

    def show(self):
        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")
        for i in range(len(self.components)):
            self.components[i].place(self.placeInfo[i])


# Create an instance and hide it because it is not the intro screen
levelSelect = LevelSelect(screen)
levelSelect.hide()


class GameScreen:
    buttonColour = "#4ECDC4"
    textColour = "#F7FFF7"

    def __init__(self, screen, level=0):
        self.bg = "#1A535C"
        self.screen = screen
        self.components = []
        self.level = level

        # Makes cannons shoot and starts the physics
        self.fireButton = Button(root, text="fire", font=(FONT, 20, "bold"), cursor="hand2",
                                 width=4, height=1, bg=self.buttonColour, fg=self.textColour, command=self.fire)
        self.fireButton.place(x=50, y=50)
        self.components.append(self.fireButton)

        self.resetButton = Button(root, text="reset", font=(FONT, 20, "bold"), cursor="hand2",
                                  width=4, height=1, bg=self.buttonColour, fg=self.textColour, command=self.reset)
        self.resetButton.place(x=150, y=50)
        self.components.append(self.resetButton)

        # Back button to return to intro screen
        self.backButton = Button(root, text="back", command=self.introScreen, width=4, height=1, bg=self.buttonColour,
                                 fg=self.textColour, font=(FONT, 20, "bold"))
        self.backButton.place(x=880, y=50)
        self.components.append(self.backButton)

        # Title that says, "walls left: "
        self.usedTitle = Label(root, text="walls left: ", font=(FONT, 20, "bold"), fg=self.textColour,
                               bg=self.bg)
        self.usedTitle.place(x=300, y=59)
        self.components.append(self.usedTitle)

        # Label that displays the number of walls left to use
        self.labelUsed = Label(root, textvariable=Cache.wallsLeft, font=("Calibri", 20, "bold"), fg=self.textColour,
                               bg=self.bg)
        self.labelUsed.place(x=450, y=59)
        self.components.append(self.labelUsed)

    def introScreen(self):
        self.hide()
        screen.delete("all")
        for obj in objects:
            del obj  # To remove cannons and their dependencies

        introScreen.show()
        Cache.gameMode = "screen"

    def fire(self):
        if Cache.fired == False:
            Cache.fired = True  # It is only possible to fire once
            start()  # Shoot from cannons and start the physics

    def reset(self):
        # Reset the level just by reloading it entirely
        loadLevel(str(Cache.level))

    def hide(self):
        self.placeInfo = []
        for component in self.components:
            self.placeInfo.append(component.place_info())
            component.place_forget()

    def show(self):
        # Draw mode is wall because that is the only thing the player should be able to draw
        Cache.drawMode = "wall"

        for i in range(len(self.components)):
            self.components[i].place(self.placeInfo[i])


gameScreen = GameScreen(screen)
gameScreen.hide()


class LevelEditor:
    buttonColour = "#FFE66D"
    textColour = "#030301"

    def __init__(self, screen):
        self.bg = "#FF6B6B"
        self.screen = screen
        self.components = []

        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")

        self.fireButton = Button(root, text="fire", cursor="hand2", width=4, height=1, fg=self.textColour,
                                 bg=self.buttonColour, command=self.fire, font=("Calibri", 17, "bold"))
        self.fireButton.place(x=50, y=50)
        self.components.append(self.fireButton)

        # Saves the objects on screen to a .baw (balls and walls) file. The name of the file is from levelField
        self.saveButton = Button(root, text="save", cursor="hand2", width=4, height=1, fg=self.textColour,
                                 bg=self.buttonColour, font=("Calibri", 17, "bold"),
                                 command=lambda: saveLevel(objects, self.levelField.get()))
        self.saveButton.place(x=150, y=50)
        self.components.append(self.saveButton)

        # Loads the level from levelField
        self.loadButton = Button(root, text="load", cursor="hand2", width=4, height=1, fg=self.textColour,
                                 bg=self.buttonColour, font=("Calibri", 17, "bold"),
                                 command=lambda: loadLevel(self.levelField.get()))
        self.loadButton.place(x=250, y=50)
        self.components.append(self.loadButton)

        # An Entry() widget for saving and loading levels
        self.levelField = Entry(root)
        self.levelField.place(x=350, y=50)
        self.components.append(self.levelField)

        # Selects the cannon draw mode
        self.cannonButton = Button(root, text="cannon", cursor="hand2", width=6, height=1, fg=self.textColour,
                                   bg=self.buttonColour, font=("Calibri", 17, "bold"), command=self.cannonMode)
        self.cannonButton.place(x=50, y=125)
        self.components.append(self.cannonButton)

        # Selects the wall draw mode
        self.wallButton = Button(root, text="wall", cursor="hand2", width=4, height=1, fg=self.textColour,
                                 bg=self.buttonColour, font=("Calibri", 17, "bold"), command=self.wallMode)
        self.wallButton.place(x=150, y=125)
        self.components.append(self.wallButton)

        # Selects the cup/crate draw mode
        self.cupButton = Button(root, text="cup", cursor="hand2", width=4, height=1, fg=self.textColour,
                                bg=self.buttonColour, font=("Calibri", 17, "bold"), command=self.cupMode)
        self.cupButton.place(x=250, y=125)
        self.components.append(self.cupButton)

        # Slider that determines the x-speed and y-speed of balls leaving that cannon
        self.xPower = 0
        self.yPower = 0
        # The slider is configured from -5 to 5. When moved, it called setValue with its value
        self.xSlider = Scale(root, label="x Power", from_=-5, to=5, resolution=0.01,
                             orient=HORIZONTAL, command=lambda v: self.setValue("x", v))
        self.xSlider.place(x=500, y=50)
        self.components.append(self.xSlider)
        # The only difference with this slider is that it is vertical
        self.ySlider = Scale(root, label="y Power", from_=-5, to=5, resolution=0.01,
                             orient=VERTICAL, command=lambda v: self.setValue("y", v))
        self.ySlider.place(x=500, y=125)
        self.components.append(self.ySlider)

        # Back button returns to the intro screen
        self.backButton = Button(root, text="Back", cursor="hand2", width=4, height=1, fg=self.textColour,
                                 bg=self.buttonColour, font=("Calibri", 17, "bold"), command=self.introScreen)
        self.backButton.place(x=900, y=50)
        self.components.append(self.backButton)

        # Entry widget for the maximum amount of walls for that level
        self.wallLimit = Entry(root)
        self.wallLimit.place(x=670, y=50)
        self.components.append(self.wallLimit)

        # Sends the value from the wallLimit Entry to Cache
        self.wallLimitSend = Button(root, text="send wall limit", cursor="hand2", width=15, height=1,
                                    fg=self.textColour,
                                    bg=self.buttonColour, font=("Calibri", 17, "bold"),
                                    command=lambda: self.sendWallLimit(self.wallLimit))
        self.wallLimitSend.place(x=670, y=125)
        self.components.append(self.wallLimitSend)

    def sendWallLimit(self, variable):
        # Sends the wall limit to Cache.wallsLeft. It is a StringVar so that tkinter widgets can manipulate it easier
        Cache.wallsLeft.set(int(variable.get()))

    def introScreen(self):
        self.hide()
        screen.delete("all")
        for obj in objects:
            objects.remove(obj)

        introScreen.show()

    def setValue(self, axis, value):
        # Takes input from the sliders. It sets Cache.x/yPower to the slider value
        if axis == "x":
            Cache.xPower = float(value)
        elif axis == "y":
            Cache.yPower = float(value)

    def cannonMode(self):
        # Switch drawing modes. This one is for the cannon
        Cache.drawMode = "cannon"

    def wallMode(self):
        Cache.drawMode = "wall"

    def cupMode(self):
        Cache.drawMode = "cup"

    def fire(self):
        # Shoot balls and start physics
        start()

    def hide(self):
        self.placeInfo = []
        for component in self.components:
            self.placeInfo.append(component.place_info())
            component.place_forget()

        self.screen.delete(self.background)

    def show(self):
        Cache.wallsLeft.set("99999")  # There is (virtually) no limit for the walls in the editor
        Cache.gameMode = "editor"
        for i in range(len(self.components)):
            self.components[i].place(self.placeInfo[i])

        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")


levelEditor = LevelEditor(screen)
levelEditor.hide()


class Instructions:
    buttonColour = "#4ECDC4"
    textColour = "#F7FFF7"

    instructions = """welcome to balls and walls. 
    in this game there are cannons which shoot balls, 
    walls for them to bounce off of, 
    and crates that must be hit. 
    your goal is to draw in walls within the amount 
    allowed for that level so that the balls hit the crates. 
    
    drag with the left mouse button to draw walls.
    click fire to shoot the ball from the cannon.
    click reset to start over."""

    def __init__(self, screen):
        self.screen = screen
        self.components = []

        self.bg = "#1A535C"
        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")

        # Title
        self.title = Label(root, text="instructions", fg=self.textColour, bg=self.bg, font=(FONT, 100, "bold"))
        self.title.place(x=SCREEN_WIDTH / 2, y=150, anchor="center")
        self.components.append(self.title)

        self.text = Label(root, text=self.instructions, fg=self.textColour, bg=self.bg,
                          font=(FONT, 25, "bold"), width=50)
        self.text.place(x=SCREEN_WIDTH / 2, y=450, anchor="center")
        self.components.append(self.text)

        self.introButton = Button(root, text="back", font=(FONT, 20, "bold"), cursor="hand2",
                                  width=4, height=1, bg=self.buttonColour, fg=self.textColour, command=self.introScreen)
        self.introButton.place(x=750, y=650)
        self.components.append(self.introButton)

    def introScreen(self):
        self.hide()
        screen.delete("all")
        introScreen.show()

    def game(self, level):
        # A function not in use now, but may be in the future
        Cache.gameMode = "game"
        self.hide()
        loadLevel(str(level))
        gameScreen.level = level
        gameScreen.show()

    def hide(self):
        self.placeInfo = []
        for component in self.components:
            self.placeInfo.append(component.place_info())
            component.place_forget()

        self.screen.delete(self.background)

    def show(self):
        self.background = self.screen.create_rectangle(0, 0, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, fill=self.bg,
                                                       outline="")
        for i in range(len(self.components)):
            self.components[i].place(self.placeInfo[i])


instructions = Instructions(screen)
instructions.hide()


# GAME OBJECTS

class Ball:
    # The ball bounces around and interacts with cups/crates
    name = "ball"

    def __init__(self, screen, x, y, r, xSpeed, ySpeed, colour="white"):
        self.screen = screen  # Tkinter screen
        self.x = x  # Centre x coordinate
        self.y = y  # Centre y coordinate
        self.r = r  # Radius
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.colour = colour

        # Draw the ball and save it to self.id
        self.id = self.screen.create_oval(self.x - self.r, self.y - self.r,
                                          self.x + self.r, self.y + self.r,
                                          fill=self.colour, outline=None)

    def update(self):
        # Move object to new coordinates.
        # screen.coords moves the object. It would not make sense to delete it in this object-orientated style
        self.screen.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

        # Update coordinates every frame
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.ySpeed += GRAVITY


class Cannon:
    # Shoots balls
    name = "cannon"

    def __init__(self, screen, x, y, r, angle=0, colour="white", xSpeed=3, ySpeed=3):
        self.screen = screen  # Tkinter screen
        self.x = x  # Wheel centre x coordinate
        self.y = y  # Wheel centre y coordinate
        self.r = r  # Radius of the wheel
        self.colour = colour
        self.xSpeed = xSpeed  # x-speed for balls shot from this cannon
        self.ySpeed = ySpeed  # y-speed for balls shot from this cannon

        if self.xSpeed == 0:
            # A quick trick to remove division by zero errors and not affect the values (too much)
            self.xSpeed = 0.001

        self.angle = degrees(atan(-self.ySpeed / self.xSpeed))  # The angle of the barrel
        self.balls = []  # Balls fired from the cannon
        self.components = []  # Parts of the cannon drawing

        self.draw()  # The drawing is more complicated so a separate function is more clean

    def __del__(self):
        # To delete the balls and components of each cannon
        for component in self.components:
            self.screen.delete(component)

    def draw(self):
        # Draws the cannon centered on the middle of the wheel

        # Barrel
        # barrelPoints is the points required to draw the barrel facing one way.
        # flippedBarrelPoints is the points in the opposite way.
        self.barrelPoints = [[self.x, self.y],  # Axel
                             [self.x + self.r, self.y],  # Right of wheel
                             [self.x + self.r * 2, self.y - self.r],  # Butt end
                             [self.x + self.r, self.y - self.r * 2],  # Fuse area
                             [self.x, self.y - self.r * 2],  # Start of barrel
                             [self.x - self.r * 2, self.y - self.r * 1.5],  # Dipped top
                             [self.x - self.r * 3, self.y - self.r * 2],  # Top tip
                             [self.x - self.r * 3, self.y],  # Bottom tip
                             [self.x - self.r * 2, self.y - self.r * 0.5],  # Dipped bottom
                             ]

        self.flippedBarrelPoints = [[self.x, self.y],  # Axel
                                    [self.x - self.r, self.y],  # Right of wheel
                                    [self.x - self.r * 2, self.y - self.r],  # Butt end
                                    [self.x - self.r, self.y - self.r * 2],  # Fuse area
                                    [self.x, self.y - self.r * 2],  # Start of barrel
                                    [self.x + self.r * 2, self.y - self.r * 1.5],  # Dipped top
                                    [self.x + self.r * 3, self.y - self.r * 2],  # Top tip
                                    [self.x + self.r * 3, self.y],  # Bottom tip
                                    [self.x + self.r * 2, self.y - self.r * 0.5],  # Dipped bottom
                                    ]

        self.newPoints = []

        # Depending on the x-speed, draw the barrel facing the right way and with the right angle
        if self.xSpeed <= 0:
            for point in rotate(self.barrelPoints, radians(360 - self.angle), [self.x, self.y]):
                self.newPoints.append(point[0])
                self.newPoints.append(point[1])
        else:
            for point in rotate(self.flippedBarrelPoints, radians(360 - self.angle), [self.x, self.y]):
                self.newPoints.append(point[0])
                self.newPoints.append(point[1])

        # Draw the barrel and append it to components
        self.components.append(self.screen.create_polygon(*self.newPoints,
                                                          fill="black", smooth=True))

        # Wheel
        # Outer circle
        self.components.append(self.screen.create_oval(self.x - self.r, self.y - self.r,
                                                       self.x + self.r, self.y + self.r,
                                                       fill=None, outline="gray",
                                                       width=15))
        # Crosses
        self.components.append(self.screen.create_line(self.x - self.r * 0.75,
                                                       self.y - self.r * 0.75,
                                                       self.x + self.r * 0.75,
                                                       self.y + self.r * 0.75,
                                                       width=15, fill="gray"))

        self.components.append(self.screen.create_line(self.x + self.r * 0.75,
                                                       self.y - self.r * 0.75,
                                                       self.x - self.r * 0.75,
                                                       self.y + self.r * 0.75,
                                                       width=15, fill="gray"))

        self.components.append(self.screen.create_line(self.x,
                                                       self.y - self.r * 0.95,
                                                       self.x,
                                                       self.y + self.r * 0.95,
                                                       width=15, fill="gray"))

        self.components.append(self.screen.create_line(self.x - self.r * 0.95,
                                                       self.y,
                                                       self.x + self.r * 0.95,
                                                       self.y,
                                                       width=15, fill="gray"))

    def fireCannon(self):
        # Shoots a ball out of the cannon
        # Depending on x-speed, adjust where the ball spawns and then rotate it by the angle to line up with the barrel
        if self.xSpeed <= 0:
            self.firePoints = rotate([[self.x - self.r * 2, self.y - self.r]], radians(360 - self.angle),
                                     [self.x, self.y])
        else:
            self.firePoints = rotate([[self.x + self.r * 2, self.y - self.r]], radians(360 - self.angle),
                                     [self.x, self.y])

        # Create the ball with the right coordinates and velocity
        self.balls.append(Ball(self.screen, self.firePoints[0][0], self.firePoints[0][1], 30, self.xSpeed, self.ySpeed,
                               colour="black"))

        # The ball is added to the global objects so collision can be done
        global objects
        objects.append(self.balls[-1])

    def update(self):
        # Updates positions and velocities for each child ball
        for ball in self.balls:
            ball.update()


class Wall:
    # Walls are bounced off by balls
    name = "wall"

    def __init__(self, screen, x1, y1, x2, y2, colour, width):
        self.screen = screen  # Tkinter screen
        self.x1 = x1  # Top left corner x and y values
        self.y1 = y1
        self.x2 = x2  # Bottom right corner x and y values
        self.y2 = y2
        self.colour = colour
        self.width = width  # Thickness of the wall

        # Draw the wall
        self.id = self.screen.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.colour, width=self.width,
                                          outline=None)

    def changePosition(self, x, y):
        # Change the second coordinate for the drawing animation of walls
        self.x2 = x
        self.y2 = y
        self.screen.coords(self.id, self.x1, self.y1, self.x2, self.y2)

    def update(self):
        # Update is called on all objects so this function must exist to prevent errors
        pass


class Cup:
    # If the cup/crate is touched by the ball, the level is cleared
    name = "cup"

    def __init__(self, screen, x, y, size, colour):
        self.screen = screen
        self.x = x  # Center x-coordinate
        self.y = y  # Center y-coordinate
        self.size = size  # Half of the length of a side. Acts more like a radius
        self.colour = colour
        self.components = []
        self.draw()  # Drawing is better suited to a separate function
        self.filled = False  # Whether the ball has touched it or not

    def draw(self):
        # Outside box
        self.components.append(screen.create_rectangle(self.x - self.size, self.y - self.size,
                                                       self.x + self.size, self.y + self.size,
                                                       fill="#b2854b"))

        self.components.append(screen.create_rectangle(self.x - self.size * 0.7, self.y - self.size * 0.7,
                                                       self.x + self.size * 0.7, self.y + self.size * 0.7,
                                                       fill="#c19a6b"))

        self.components.append(screen.create_line(self.x - self.size * 0.8, self.y - self.size * 0.8,
                                                  self.x + self.size * 0.8, self.y + self.size * 0.8,
                                                  fill="#786550", width=20))

        self.components.append(screen.create_line(self.x + self.size * 0.8, self.y - self.size * 0.8,
                                                  self.x - self.size * 0.8, self.y + self.size * 0.8,
                                                  fill="#786550", width=20))

    def update(self):
        pass


# ROTATION

def rotate(points, angle, center):
    # Rotates points by an angle around the center point
    cosValue = cos(angle)
    sinValue = sin(angle)
    cx, cy = center

    new_points = []

    for xOld, yOld in points:
        xOld -= cx
        yOld -= cy
        xNew = xOld * cosValue - yOld * sinValue
        yNew = xOld * sinValue + yOld * cosValue
        new_points.append([xNew + cx, yNew + cy])

    return new_points


# COLLISION DETECTION

def formatVector(x, y):
    """Formats a vector nicely given x and y values."""
    return "<" + str(x) + ", " + str(y) + ">"


def vectors(x1, y1, x2, y2, v1, v2):
    """Calculates a return vector given a wall and incoming vector."""
    if x1 == x2:
        return [-v1, v2]

    # Wall vector
    w1 = x2 - x1
    w2 = y2 - y1

    # Normal vector
    n1 = -w2
    n2 = w1

    # Angle between incoming and normal
    theta = acos((n1 * v1 + n2 * v2) / (sqrt(n1 ** 2 + n2 ** 2) * sqrt(v1 ** 2 + v2 ** 2)))

    if v1 > 0:
        # Angle of rotation
        r = pi - theta * 2
    else:
        r = pi + 2 * theta

    # New vector
    a1 = v1 * cos(r) + v2 * sin(r)
    a2 = -v1 * sin(r) + v2 * cos(r)

    return [a1, a2]


def standardForm(x1, y1, x2, y2):
    """Return the values of a line in standard form given its coodinates."""
    # Slope
    if x2 == x1:
        return ["undefined", 0, 0]
    else:
        m = (y2 - y1) / (x2 - x1)

    # y intercept
    b = y1 - (m * x1)

    # Standard form
    A = m
    B = -1
    C = b

    return [A, B, C]


def getDistance(x1, y1, x2, y2):
    """Finds the distance between two points."""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def getIntersection(m1, m2, b1, b2):
    """Finds the intersection point between two lines."""
    a = m1
    b = m2
    c = b1
    d = b2

    return [(d - c) / (a - b), (a * d - b * c) / (a - b)]


def checkCollision(objects):
    doCollide = False
    ballInCup = False

    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):  # Start from i to avoid double counting object pairs

            # Wall-Ball collision pairs
            if objects[i].name == "wall" and objects[j].name == "ball":
                wall = objects[i]
                ball = objects[j]
                doCollide = True
            elif objects[i].name == "ball" and objects[j].name == "wall":
                wall = objects[j]
                ball = objects[i]
                doCollide = True

            # Cup-Ball collision pairs
            if objects[i].name == "cup" and objects[j].name == "ball":
                ball = objects[j]
                cup = objects[i]
                ballInCup = True
            elif objects[i].name == "ball" and objects[j].name == "cup":
                ball = objects[i]
                cup = objects[j]
                ballInCup = True

            # Handles Cup-Ball collisions
            if ballInCup:
                if getDistance(ball.x, ball.y, cup.x, cup.y) < cup.size:
                    # If the ball is within a circle of the cup
                    if Cache.gameMode == "game":
                        # Do not go on to the next level if the game mode is "editor" or anything other than "game"
                        cup.filled = True
                        Cache.filled = True

            # Handles Ball-Ball collisions
            if doCollide:
                doCollide = False

                xBall = ball.x  # Center point of the ball
                yBall = ball.y
                xSpeed = ball.xSpeed  # Ball velocity
                ySpeed = ball.ySpeed

                # Wall coordinates
                x1Wall = wall.x1
                y1Wall = wall.y1
                x2Wall = wall.x2
                y2Wall = wall.y2

                # Wall in standard form
                standard = standardForm(x1Wall, y1Wall, x2Wall, y2Wall)

                # Wall values
                A = standard[0]
                B = standard[1]
                C = standard[2]

                # Find the shortest distanced point from the ball to the wall's line equation
                if A == "undefined":
                    # It is a vertical line
                    d = abs(x1Wall - xBall)
                    intersection = [x1Wall, yBall]
                else:
                    # Perpendicular line
                    perpendicularSlope = -(1 / A) if A != 0 else 1
                    perpendicularInt = yBall - perpendicularSlope * xBall

                    intersection = getIntersection(A, perpendicularSlope, C, perpendicularInt)

                    # Perpendicular distance
                    d = abs((A * xBall + B * yBall + C)) / sqrt(A ** 2 + B ** 2)

                # Check if that point is on the line segment.
                # If the distance from intersection to both walls points is equal to the length of the wall
                if abs((getDistance(intersection[0], intersection[1], x1Wall, y1Wall) +
                        getDistance(intersection[0], intersection[1], x2Wall, y2Wall)
                       ) - getDistance(x1Wall, y1Wall, x2Wall, y2Wall)) < 0.001:
                    onLine = True
                else:
                    onLine = False

                # If the ball and wall are colliding, calculate the ball's new velocity
                if d <= ball.r and onLine == True:
                    onLine = False

                    # Place the ball right on the wall, not any further
                    ratio = getDistance(intersection[0], intersection[1], xBall, yBall) / ball.r
                    ball.x = intersection[0] - (ball.xSpeed * ratio) - (intersection[0] - ball.x)
                    ball.y = intersection[1] - (ball.ySpeed * ratio) - (intersection[1] - ball.y)

                    # Calculate the new vector and apply it to the ball
                    newVector = vectors(x1Wall, y1Wall, x2Wall, y2Wall, xSpeed, ySpeed)
                    ball.xSpeed = newVector[0]
                    ball.ySpeed = newVector[1]

                    # Take away some velocity on each collision so balls do not bounce forever
                    if ball.xSpeed != 0:
                        ball.xSpeed *= ABSORPTION

                    if ball.ySpeed != 0:
                        ball.ySpeed *= ABSORPTION


# EVENT HANDLERS

def mouseClickHandler(event):
    global mouseDown, xStart, yStart, objects

    xMouse = event.x
    yMouse = event.y

    if Cache.drawMode == "wall":
        if Cache.gameMode == "screen":
            # Do not draw anything if it is an intro, instruction screen, etc.
            return

        if Cache.gameMode == "game":
            if int(Cache.wallsLeft.get()) > 0:
                # If there are enough walls left, draw the wall
                objects.append(Wall(screen, xMouse, yMouse, xMouse + 1, yMouse + 1, "#66D7D1", 5))

        else:
            # Otherwise it is the editor mode, so draw a wall
            objects.append(Wall(screen, xMouse, yMouse, xMouse + 1, yMouse + 1, "#66D7D1", 5))

    elif Cache.drawMode == "cannon" and mouseDown == False:
        # Draw a cannon with xPower and yPower from the level editor sliders
        objects.append(Cannon(screen, xMouse, yMouse, 40, xSpeed=Cache.xPower, ySpeed=Cache.yPower))

    elif Cache.drawMode == "cup" and mouseDown == False:
        # Draw in a cup/crate
        objects.append(Cup(screen, xMouse, yMouse, 80, "green"))

    mouseDown = True  # So the mouseMotionHandler can take over


def mouseMotionHandler(event):
    global xStart, yStart, objects
    xMouse = event.x
    yMouse = event.y

    try:
        if Cache.gameMode != "game" and mouseDown == True:
            # If it is not the "game" mode, and the clickHandler already started the wall, draw the next point
            objects[-1].changePosition(xMouse, yMouse)

        elif mouseDown == True and Cache.drawMode == "wall" and int(Cache.wallsLeft.get()) > 0:
            # If it is the "game" mode, check that there are sufficient walls remain to draw
            objects[-1].changePosition(xMouse, yMouse)
    except:
        # The Cache.wallsLeft StringVar likes to throw errors. This try-except just silences those errors
        pass


def mouseReleaseHandler(event):
    global mouseDown

    mouseDown = False
    if Cache.wallsLeft.get() != "0":
        # Remove one from wallsLeft, but do not let wallsLeft become negative
        Cache.wallsLeft.set(str(int(Cache.wallsLeft.get()) - 1))


# SAVING AND LOADING LEVELS

def loadLevel(level):
    """Load a level."""
    global objects
    screen.delete("all")  # When loading in a new level, clear everything prior

    objects = []

    try:
        Cache.fired = False  # Allow the cannon to be fired again

        # Load, using pickle the desired level (and .ballsandwalls file extension)
        levelData = load(open("levels/" + level + ".baw", "rb"))

        # Extract the data from the file
        cannons = levelData["cannons"]
        walls = levelData["walls"]
        cups = levelData["cups"]
        wallLimit = levelData["wallLimit"]

        # Append objects from the level into the game
        for cannon in cannons:
            objects.append(Cannon(screen, *cannon))

        for wall in walls:
            objects.append(Wall(screen, *wall))

        for cup in cups:
            objects.append(Cup(screen, *cup))

        Cache.wallsLeft.set(str(wallLimit))  # Set the wall limit

        Cache.level = int(level)

        print("Level", level, "loaded.")
    except:
        # If there is no such level, catch the error
        print("Level", level, "not found.")
        levelSelect.show()
        gameScreen.hide()


def saveLevel(objects, level):
    """Save a level."""
    cannons = []
    walls = []
    cups = []
    balls = []
    levelData = []

    # Go through each object and add its data to an array. pickle does not support direct pickling of tkinter objects
    for object in objects:
        if object.name == "ball":
            pass
        elif object.name == "cannon":
            cannons.append([object.x, object.y, object.r, object.angle, object.colour, object.xSpeed, object.ySpeed])
        elif object.name == "wall":
            walls.append([object.x1, object.y1, object.x2, object.y2, object.colour, object.width])
        elif object.name == "cup":
            cups.append([object.x, object.y, object.size, object.colour])

    levelData = {
        "cannons": cannons,
        "walls": walls,
        "cups": cups,
        "wallLimit": Cache.wallsLeft.get()
    }

    # Pickle the data into the desired level name
    dump(levelData, open("levels/" + level + ".baw", "wb+"))
    print("Level", level, "saved.")


def nextLevel():
    """Advance to the next level"""
    # Load the next level after beating one
    loadLevel(str(Cache.level + 1))
    Cache.filled = False


started = False


def start():
    """Fires cannons and stars physics."""
    global started, objects
    started = True
    for i in objects:
        if i.name == "cannon":
            i.fireCannon()


def runGame():
    global start

    # Bind buttons
    screen.bind("<Button-1>", mouseClickHandler)
    screen.bind("<Motion>", mouseMotionHandler)
    screen.bind("<ButtonRelease-1>", mouseReleaseHandler)
    root.bind("q", lambda x: root.destroy())

    # Background music
    PlaySound("audio/thecoolfool.wav", SND_ASYNC + SND_LOOP)

    while True:
        if Cache.filled:
            # Once the ball touches the cup/crate, advance to the next level
            nextLevel()

        checkCollision(objects)  # Goes though objects and checks for collisions

        # Update Ball objects only
        for i in objects:
            if i.name == "ball" and started == False:
                pass
            else:
                i.update()

        screen.update()
        root.update()
        sleep(0.01)  # 0.01 because it is smoother and causes less bugs for collision


if __name__ == "__main__":
    runGame()
