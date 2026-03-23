import tkinter as tk
from gridspace import *

class GridBlob:
    def __init__(self,root) -> None:
        self.grid_size = 20
        self.element_id = 0
        self.root = root
        self.root.title("Grid Space")
        self.tooltip = tk.Menu(
            self.root,
            tearoff = 0
        )
        self.tooltip.add_command(
            label = "Cut"
        )
        self.tooltip.add_command(
            label = "Copy"
        )
        self.tooltip.add_separator()
        self.tooltip.add_command(
            label = "Paste"
        )
        self.canvas = tk.Canvas(
            root,
            width = self.root.winfo_screenwidth(),
            height = self.root.winfo_screenheight(),
            scrollregion = (
                0,
                0,
                self.root.winfo_screenwidth(),
                self.root.winfo_screenheight()
            ),
            bg = "#c7c7c7"
        )
        self.canvas.pack()

        for x in range(0, self.root.winfo_screenwidth(), self.grid_size):
            self.canvas.create_line(
                x,
                0,
                x,
                self.root.winfo_screenheight(),
                fill = "#ddd"
            )

        for y in range(0, self.root.winfo_screenheight(), self.grid_size):
            self.canvas.create_line(
                0,
                y,
                self.root.winfo_screenwidth(),
                y,
                fill = "#ddd"
            )
        self.elements = {}

        # Create highlight square (initially hidden)
        self.canvas.bind(
            '<ButtonRelease-1>',
            self.select_element
        )
        self.canvas.bind(
            '<ButtonRelease-3>',
            self.show_tooltip
        )
        self.canvas.bind(
            '<Motion>',
            self.move_mouse
        )
        self.current_element_id = None
        self.highlight_square = None
    def create_element(self,x : int,y : int,**attributes : dict) -> int:
        element_id = self.element_id
        self.element_id += 1
        self.elements[element_id] = {
            'coords' : (x,y),
            'element' : self.canvas.create_rectangle(
                x,
                y,
                x + self.grid_size,
                y + self.grid_size,
                **attributes
            )
        }
        return element_id
    def show_tooltip(self,event):
        self.tooltip.tk_popup(
            event.x_root - 10,
            event.y_root - 10
        )
        self.tooltip.focus_set()
    def get_grid_cell(self,event) -> tuple[int,int]:
        return (
            (event.x // self.grid_size) * self.grid_size,
            (event.y // self.grid_size) * self.grid_size
        )
    def select_element(self,event):
        (x,y) = self.get_grid_cell(event)

        if self.current_element_id is None:
            element_ids = [i for i,v in self.elements.items() if v['coords'] == (x,y)]
            if len(element_ids) > 0:
                self.current_element_id = element_ids[0]
        else:
            self.canvas.coords(
                self.elements[self.current_element_id],
                x,
                y,
                x + self.grid_size,
                y + self.grid_size
            )
            self.elements[self.current_element_id]['coords'] = (x,y)
            self.canvas.itemconfigure(
                self.elements[self.current_element_id],
                state = "normal"
            )
            self.canvas.unbind('<Motion>')
            self.current_element_id = None
    def move_mouse(self,event):
        (x,y) = self.get_grid_cell(event)

        element_ids = [i for i,v in self.elements.items() if v['coords'] == (x,y)]
        if len(element_ids) == 0:
            if self.highlight_square is None:
                self.highlight_square = self.canvas.create_rectangle(
                    x,
                    y,
                    x + self.grid_size,
                    y + self.grid_size,
                    fill = '#8b8b8b',
                    outline = ''
                )
            else:
                self.canvas.coords(
                    self.highlight_square,
                    x,
                    y,
                    x + self.grid_size,
                    y + self.grid_size
                )
    def try_create_square(self,event):
        (x,y) = self.get_grid_cell(event)

        if (x,y) not in self.elements:
            self.elements[x,y] = self.canvas.create_rectangle(
                x,
                y,
                x + self.grid_size,
                y + self.grid_size,
                fill = "white",
                outline = "black"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = GridSpace(root,20)
    root.mainloop()