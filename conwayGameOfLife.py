from tkinter import *
from random import randint
# CONSTANTS NEEDED IN THE PROGRAM
SIZE = 740
NUM = 50
a = int(NUM / 2)
UNIT = SIZE / NUM
THICKNESS = 2
DEATH = "white"
LIFE = "green"
ALIVE = 1
DEAD = 0
REVIVE = 1
KILL = 0
TICK = 150
INDICES = set()  # a set with all the tuples i'll need
for i in range(NUM):  # so i never have to do 2-for loops again
    for j in range(NUM):
        INDICES.add((i, j))

# Defining the Life Canvas


class Life(Canvas):
    """creates a canvas and keeps track of who is alive"""

    def __init__(self, boss=None):
        """a canvas object, with a grid, a click bind, and dead rectangles"""
        Canvas.__init__(self, boss, width=SIZE, height=SIZE, bg=DEATH)
        self.make_grid()
        self.bind("<Button-1>", self.draw)
        self.flag = 0
        # chart keeps track of deaths/births
        self.chart = {}
        for coord in INDICES:
            self.chart[coord] = DEAD
        self.state = StringVar()  # these two variables are just for display
        self.state.set("AT REST")  # purposes later

    def make_grid(self):
        """I use a variable for the width, so it can be the same for the lines,
        and the rectangles. Otherwise, you get weird contrast"""
        for k in range(0, NUM + 1):
            self.create_line(k * UNIT, 0, k * UNIT, SIZE, width=THICKNESS)
            self.create_line(0, k * UNIT, SIZE, k * UNIT, width=THICKNESS)

    def draw(self, event):
        """revives/kills the block CLICKED ON by the user depending on its previous state"""
        if self.flag == 0:
            xn = int(event.x / UNIT)
            yn = int(event.y / UNIT)
            if self.chart[xn, yn]:
                self.kill((xn, yn))
            else:
                self.givebirth((xn, yn))

    def update(self):
        """goes one generation ahead, you can click a button to update even during
        simulation, as it only accelerates the process when you press it.
        Not worth adding another indentation block"""
        changes = {}
        for coord in INDICES:  # the need for two for loops is necessary
            if self.chart[coord] == ALIVE and (
                    self.number_of_neighbors(coord) < 2 or self.number_of_neighbors(coord) > 3):
                changes[coord] = KILL
            elif self.number_of_neighbors(coord) == 3:
                changes[coord] = REVIVE
        for coord in changes.keys():  # because the evolution is discrete
            if changes[coord] == KILL:
                self.kill(coord)
            elif changes[coord] == REVIVE:
                self.givebirth(coord)

    def react(self):
        """when the user presses the start/stop button"""
        if self.flag == 0:
            self.state.set("SIMULATING")
            self.flag = 1
            self.simulate()
        else:
            self.state.set("AT REST")
            self.flag = 0

    def simulate(self):
        """simulating indefinitely"""
        if self.flag == 1:
            self.update()
            self.after(TICK, self.simulate)

    def clear(self):
        """cleans the canvas and restarts"""
        if self.flag == 0:
            for coord in INDICES:
                self.kill(coord)
                self.chart[coord] = DEAD

    def givebirth(self, coord):
        """I create a rectangle at each turn, the color is the life indicator"""
        if self.chart[coord] == DEAD:
            self.create_rectangle((coord[0] + 1) * UNIT, coord[1] * UNIT,
                                  coord[0] * UNIT, (coord[1] + 1) * UNIT,
                                  fill=LIFE, width=THICKNESS, outline='black')
            self.chart[coord] = ALIVE

    def kill(self, coord):
        """same as givebirth with another color"""
        if self.chart[coord] == ALIVE:
            self.create_rectangle((coord[0] + 1) * UNIT, coord[1] * UNIT,
                                  coord[0] * UNIT, (coord[1] + 1) * UNIT,
                                  fill=DEATH, width=THICKNESS, outline='black')
            self.chart[coord] = DEAD

    def number_of_neighbors(self, coord):
        counter = 0
        for [x_increment, y_increment] in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0],
                                           [1, 1]]:  # neighbor vector translation
            xn = coord[0] + x_increment
            yn = coord[1] + y_increment
            if (xn, yn) in INDICES and self.chart[xn, yn] == 1:
                counter += 1
        return counter

    def implement_shape(self, shape):
        """draw a previously defined shape"""
        if self.flag == 0:
            for coord in INDICES:
                self.kill(coord)
            for coord in shape:
                self.givebirth(coord)

    def implement_random(self):
        """a random sample for visual tests"""
        shape = set()
        for coord in INDICES:
            if randint(0, 1):
                shape.add(coord)
        self.implement_shape(shape)


if __name__ == "__main__":
    # Common Shapes in GOL
    BLINKER = {(a, a), (a + 1, a), (a + 2, a)}
    TOAD = {(a, a), (a + 1, a), (a + 2, a), (a + 1, a + 1), (a + 2, a + 1), (a + 3, a + 1)}
    BEACON = {(a, a), (a + 1, a + 1), (a + 1, a), (a, a + 1), (a - 2, a - 2), (a - 2, a - 1), (a - 1, a - 1),
              (a - 1, a - 2)}
    GLIDER = {(a, a), (a + 1, a), (a + 1, a - 1), (a + 1, a - 2), (a - 1, a - 1)}
    LIGHT_WEIGHT_SPACESHIP = {(a, a), (a + 1, a), (a + 2, a), (a + 3, a), (a + 3, a - 1), (a + 3, a - 2),
                              (a + 2, a - 3), (a - 1, a - 3), (a - 1, a - 1)}
    USUAL = {'BLINKER': BLINKER, 'TOAD': TOAD,
             'BEACON': BEACON, 'GLIDER': GLIDER,
             'LWSS': LIGHT_WEIGHT_SPACESHIP}
    ############################################################################
    root = Tk()
    root.configure(background='white')
    root.title("CONWAY's GAME OF LIFE (KILL AND REVIVE BY LEFT CLICK)")
    game_of_life = Life(root)
    game_of_life.pack(side=RIGHT)
    Button(root, text='NEXT', relief=GROOVE, height=2, width=10, bg='ivory',
           font='Helvetica', command=game_of_life.update).pack()
    Button(root, text='START/STOP', relief=GROOVE, height=2, width=10,
           bg='ivory', font='Helvetica', command=game_of_life.react).pack()
    Button(root, text='RESET', relief=GROOVE, height=2, width=10, bg='ivory',
           font='Helvetica', command=game_of_life.clear).pack()
    for key in USUAL.keys():
        Button(root, text=key, relief=GROOVE, height=2, width=10, bg='ivory',
               font='Helvetica',
               command=lambda arg=USUAL[key]: game_of_life.implement_shape(arg)).pack()
    Button(root, text='RANDOM', height=2, width=10, bg='ivory', relief=GROOVE,
           font='Helvetica', command=game_of_life.implement_random).pack()
    Button(root, text='QUIT', font='Helvetica', height=2, width=10,
           command=root.destroy, bg='ivory', relief=GROOVE).pack(side=BOTTOM)
    Label(root, textvariable=game_of_life.state, font='Helvetica',
          relief=GROOVE, height=4, width=10, bg='red').pack(side=BOTTOM)
    root.mainloop()
