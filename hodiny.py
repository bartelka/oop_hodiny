import tkinter as tk
from datetime import datetime

win = tk.Tk()

W = 1100
H = 400
canvas = tk.Canvas(win, width=W, height=H, background="white")
canvas.pack()


class Line:
    def __init__(self, point: tuple, dx: int, dy: int, colour: str, canvas):
        self.coords = point
        self.dx = dx
        self.dy = dy
        self.colour = colour
        self.canvas = canvas
        self.id_1 = None
        self.id_2 = None
        self.id_3 = None
        if dx < dy:
            self.id_1 = canvas.create_polygon(point[0], point[1], point[0] + dx // 2, point[1] - dx // 2 , point[0] + dx, point[1], point[0] + dx, point[1] + dy, point[0] + dx // 2, point[1] + dy + dx // 2, point[0], point[1] + dy,fill=colour, outline="white")
        if dx > dy:
            self.id_2 = canvas.create_polygon(point[0], point[1], point[0] + dx, point[1], point[0] + dx + dy // 2, point[1] + dy // 2, point[0] + dx, point[1] + dy, point[0], point[1] + dy, point[0] - dy // 2, point[1] + dy // 2,fill=colour, outline="white")
        if dx == dy:
            self.id_3 = canvas.create_rectangle(point[0], point[1], point[0] + dx, point[1] + dy, fill=colour, outline="")

    def on(self):
        if self.id_1:
            canvas.itemconfig(self.id_1, fill=self.colour)
        if self.id_2:
            canvas.itemconfig(self.id_2, fill=self.colour)
        if self.id_3:
            canvas.itemconfig(self.id_3, fill=self.colour)

    def off(self):
        if self.id_1:
            canvas.itemconfig(self.id_1, fill="white")
        if self.id_2:
            canvas.itemconfig(self.id_2, fill="white")


class Segment:
    def __init__(self, point: tuple, dx: int, dy: int, small: int, big: int, colour: str, canvas):
        self.parts = []
        self.coords = point
        self.colour = colour
        x = point[0]
        y = point[1]
        self.parts.append(Line((x + small, y), big, small, colour, canvas))
        self.parts.append(Line((x + small + big, y + small), small, big, colour, canvas))
        self.parts.append(Line((x + small, y + big + small), big, small, colour, canvas))
        self.parts.append(Line((x, y + small), small, big, colour, canvas))
        self.parts.append(Line((x + small + big, y + small * 2 + big), small, big, colour, canvas))
        self.parts.append(Line((x + small, y + big * 2 + small * 2), big, small, colour, canvas))
        self.parts.append(Line((x, y + small * 2 + big), small, big, colour, canvas))

    def reset(self):
        for part in self.parts:
            part.off()

    def error(self):
        for part in self.parts:
            part.on()

    def display(self, number: int):
        if number == 0:
            self.error()
            self.parts[2].off()
        elif number == 1:
            self.reset()
            self.parts[1].on()
            self.parts[4].on()
        elif number == 2:
            self.error()
            self.parts[3].off()
            self.parts[4].off()
        elif number == 3:
            self.error()
            self.parts[3].off()
            self.parts[6].off()
        elif number == 4:
            self.error()
            self.parts[0].off()
            self.parts[5].off()
            self.parts[6].off()
        elif number == 5:
            self.error()
            self.parts[1].off()
            self.parts[6].off()
        elif number == 6:
            self.error()
            self.parts[1].off()
        elif number == 7:
            self.reset()
            self.parts[0].on()
            self.parts[1].on()
            self.parts[4].on()
        elif number == 8:
            self.error()
        elif number == 9:
            self.error()
            self.parts[6].off()


class Clock:
    def __init__(self, canvas):
        self.segments = []
        self.canvas = canvas

        # Adjusted spacing factor for smaller gaps
        spacing_factor = 0.4
        # Create 6 segments
        for i in range(6):
            if i > 3:
                if i > 4:
                    spacing_factor = 0.23
                x = i * (140 + spacing_factor * 140)
                y = 200
                segment = Segment((x, y), 10, 50, 10, 50, "purple", canvas)
                self.segments.append(segment)
            else:
                if i == 0 or i == 2 or i == 4:
                    x = i * (140 + spacing_factor * 140) + 45
                else:
                    x = i * (140 + spacing_factor * 140)
                y = 100
                segment = Segment((x, y), 20, 100, 20, 100, "purple", canvas)
                self.segments.append(segment)
                if i == 3 or i == 1:
                    col_1 = Line((x + 160,y + 140), 20, 20, "purple", canvas)
                    col_2 = Line((x + 160,y + 100), 20, 20, "purple", canvas)
                    col_1.on()
                    col_2.on()

    def display_current_time(self):
        current_time = datetime.now().strftime("%H%M%S")

        # Display digits on corresponding segments
        for i in range(6):
            digit = int(current_time[i])
            self.segments[i].display(digit)

        # Reschedule the method to be called after 1000 milliseconds (1 second)
        win.after(1000, self.display_current_time)


# Usage
clock = Clock(canvas)
clock.display_current_time()
win.mainloop()
