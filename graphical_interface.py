import game as game
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox


class GraphicalInterfaces():
    def __init__(self):
        self.grid = game.createGame(12, 10, 2, False)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.grid.getWidth() *
                                38, height=self.grid.getHeight()*38)
        self.agreement = tk.StringVar()
        self.rectangles = []
        self.image_container = []
        self.casePNG = [PhotoImage(file="image/noHole.png"),
                        PhotoImage(file="image/singleHole.png"),
                        PhotoImage(file="image/twoHoles.png"),
                        PhotoImage(file="image/threeHoles.png")]

        self.root.geometry('1500x750')
        self.root.title('Expansion')
        self.canvas.pack()
        self.initializeCanvas()

        self.DimensionsFrame = tk.Frame(self.root)
        self.DimensionsFrame.pack(side="top")
        self.nbPlayersFrame = tk.Frame(self.root)
        self.nbPlayersFrame.pack(side="top")

        (self.spinboxHeightLabel, self.spinboxHeight) = self.createSpinbox(True,
                                                                           "Enter the height of the board :", 3, 10, self.DimensionsFrame, "left")
        gap = tk.Label(self.DimensionsFrame, width=10)
        gap.pack(side="left")
        (self.spinboxWidthLabel, self.spinboxWidth) = self.createSpinbox(True,
                                                                         "Enter the width of the board :", 3, 12, self.DimensionsFrame, "left")

        (self.spinboxPlayerLabel, self.spinboxPlayer) = self.createSpinbox(True,
                                                                           "Number of player :", 2, 8, self.nbPlayersFrame, "left")
        gap = tk.Label(self.nbPlayersFrame, width=10)
        gap.pack(side="left")

        style = ttk.Style()
        style.configure("MyCheckbutton.TCheckbutton", font=("Arial", 20))
        checkbox = ttk.Checkbutton(self.nbPlayersFrame,
                                   style="MyCheckbutton.TCheckbutton",
                                   text='Do you want bots ?',
                                   command=self.botornot,
                                   variable=self.agreement,
                                   onvalue='Bot added',
                                   offvalue='Bot removed'
                                   ).pack(side="top")

        (self.spinboxBotsLabel, self.spinboxBots) = self.createSpinbox(False,
                                                                       "Number of bots :", 1, 7, self.nbPlayersFrame, "left")

        self.botornot()

        self.SaveFrame = tk.Frame(self.root)
        self.SaveFrame.pack(side="bottom")
        self.saveButton = self.createButton(
            "Save game", self.saveGame, self.SaveFrame,  "left")
        self.loadGridButton = self.createButton(
            "Load game", self.loadGame, self.SaveFrame, "left")

        self.newGridButton = self.createButton(
            "New board", self.newBoard, self.root, "bottom")
        self.newGridButton.configure(width=33)

        self.canvas.bind('<Button-1>', self.placePawn)
        self.spinboxPlayer.bind("<ButtonRelease-1>",
                                lambda event: self.root.after(1, self.update_max, self.spinboxPlayer, self.spinboxBots))

    def initializeCanvas(self):
        self.canvas.configure(width=self.grid.getWidth()
                              * 38, height=self.grid.getHeight()*38)
        self.rectangles = []
        self.image_container = []
        for i in range(self.grid.getHeight()):
            self.rectangles.append([])
            self.image_container.append([])

            for j in range(self.grid.getWidth()):
                x0 = j * 38
                y0 = i * 38
                x1 = x0 + 38
                y1 = y0 + 38
                xi = (x1-x0)/2+x0
                yi = (y1-y0)/2+y0
                self.rectangles[i].append(self.canvas.create_rectangle(
                    x0, y0, x1, y1, outline=self.grid.getCurrentPlayer().getColor(), width=2))
                self.image_container[i].append(
                    self.canvas.create_image(xi, yi, image=self.casePNG[0]))

        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                self.canvas.itemconfig(
                    self.rectangles[i][j], fill=cell.getPlayer().getColor())

        self.update(True)

    def update(self, first=False):
        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                if cell.getPawnNumber() < 4:
                    score_case = cell.getPawnNumber()
                else:
                    score_case = 3
                self.canvas.itemconfig(
                    self.image_container[i][j], image=self.casePNG[score_case])
                self.canvas.itemconfig(
                    self.rectangles[i][j],
                    outline=self.grid.getNextPlayer().getColor(),
                    fill=cell.getPlayer().getColor()
                )
                if first:
                    self.canvas.itemconfig(
                        self.rectangles[i][j],
                        outline=self.grid.getCurrentPlayer().getColor(),
                    )

    def placePawn(self, event):

        x, y = event.x, event.y
        selectedRow = y // 38
        selectedCol = x // 38

        if self.grid.checkWin():
            return

        if isinstance(self.grid.getCurrentPlayer(), game.Bot):
            coordo = self.grid.getCurrentPlayer().pickCoordo(self.grid)
            while self.grid.placePawn(coordo, self.grid.getCurrentPlayer()) == False:
                coordo = self.grid.getCurrentPlayer().pickCoordo(self.grid)
            self.grid.expandPawn(coordo,
                                 self.grid.getCurrentPlayer())
        else:
            if self.grid.placePawn((selectedRow, selectedCol), self.grid.getCurrentPlayer()) == False:
                return
            self.grid.expandPawn((selectedRow, selectedCol),
                                 self.grid.getCurrentPlayer())

        # self.grid.display()
        self.update()
        self.grid.NextPlayer()

        if self.grid.checkWin():
            self.root.after(1, self.displayWinner)

    def displayWinner(self):
        winner = self.grid.getPlayerList()[0]
        messagebox.showinfo(
            "Winner", f"Player {winner.getNumber()} Won the game")

    def clear(self):
        self.grid.display()
        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                self.canvas.delete(self.rectangles[i][j])
                self.canvas.delete(self.image_container[i][j])

    def newBoard(self):
        messagebox.showinfo("Board update", "The board has been updated")
        height = int(self.spinboxHeight.get())
        width = int(self.spinboxWidth.get())
        nbPlayer = int(self.spinboxPlayer.get())
        bots = self.botornot()
        nbBots = int(self.spinboxBots.get())

        self.clear()
        self.grid = game.createGame(width, height, nbPlayer, bots, nbBots)
        self.initializeCanvas()
        self.canvas.pack()

    def createSpinbox(self, state: bool, text: str, min: int, max: int, frame, side: str = "top"):
        label = tk.Label(frame, text=text)
        label.config(font=("Arial", 20))
        label.pack(side=side)
        spinbox = tk.Spinbox(frame, from_=min, to=max, width=2)
        spinbox.config(font=("Arial", 20))
        spinbox.pack(side=side)
        if state:
            spinbox.config(validate="key", validatecommand=(
                spinbox.register(self.validation), "%P"))
        else:
            spinbox.config(state='disabled', validate="key", validatecommand=(
                spinbox.register(self.validation), "%P"))
        spinbox.bind("<Key>", self.ignore_input)
        return (label, spinbox)

    def botornot(self):
        if self.agreement.get() == 'Bot added':
            self.spinboxBots.config(state='normal')
            self.spinboxBots.pack(side="right")
            self.spinboxBotsLabel.pack()
            self.spinboxPlayer.config(from_=1)
            self.spinboxPlayer.config(to=7)
            return True
        else:
            # self.spinboxBots.config(state='disabled')
            self.spinboxBots.pack_forget()
            self.spinboxBotsLabel.pack_forget()
            self.spinboxPlayer.config(from_=2)
            self.spinboxPlayer.config(to=8)
            return False

    def validation(self, new_text):
        if new_text.isdigit():
            return True
        elif new_text == "":
            return True
        else:
            return False

    def ignore_input(self, event):
        return "break"

    def update_max(self, spinbox1, spinbox2):
        value = int(spinbox1.get())
        if value >= 8:
            return
        if 8-value == 1:
            spinbox2.config(from_=0)
        spinbox2.config(to=8-value)
        spinbox2.config(from_=1)

    def createButton(self, text: str, command, frame, direction="top"):
        button = tk.Button(
            frame, text=text, command=command)
        button.config(font=("Arial", 20), height=2, width=15)
        button.pack(side=direction)
        return button

    def saveGame(self):
        self.grid.saveGame()
        # self.grid.display()

    def loadGame(self):
        self.clear()

        if self.grid.loadGame() == False:
            messagebox.showinfo("No Savefile", "You don't have any saved game")
            self.update()
            return

        self.grid.loadGame()
        # self.grid.display()
        self.initializeCanvas()


if __name__ == "__main__":
    GI = GraphicalInterfaces()
    GI.root.mainloop()
