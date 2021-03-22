from tkinter import *
from tkinter.ttk import *
from graph import Graph
import search
import search_pruning
import heuristic


class App(Tk):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # size of square side and canvas side
        self.square_side = 25
        self.size = 700

        # creates the interface
        self.title('Path finding')
        self.geometry('700x800')
        self.resizable(False, False)
        self.canvas = Canvas(self, height=self.size, width=self.size)
        self.canvas.bind('<Button-1>', self.change_color)
        self.canvas.bind('<B1-Motion>', self.change_color)

        button_start = Button(self, text='Select start node')
        button_start.bind('<Button-1>', self.select_start)
        button_end = Button(self, text='Select end node')
        button_end.bind('<Button-1>', self.select_end)
        button_walls = Button(self, text='Select wall node')
        button_walls.bind('<Button-1>', self.select_walls)
        button_search = Button(self, text='Perform search')
        button_search.bind('<Button-1>', self.perform_search)
        button_reset = Button(self, text='reset')
        button_reset.bind('<Button-1>', self.reset)
        button_water = Button(self, text='Select water node')
        button_water.bind('<Button-1>', self.select_water)
        algos = ['naive',
                 'breadth first',
                 'depth first',
                 'iterative deepening',
                 'uniform cost',
                 'A star']
        self.algos_combo_box = Combobox(self, values=algos)
        self.algos_combo_box.current(1)

        self.canvas.place(x=0, y=0)

        offset = 10
        button_start.place(x=offset, y=710)
        button_water.place(x=offset, y=760)

        offset += button_start.winfo_reqwidth()+20
        button_end.place(x=offset, y=710)
        self.algos_combo_box.place(x=offset, y=763)

        offset += button_end.winfo_reqwidth() + 20
        button_walls.place(x=offset, y=710)

        offset += button_walls.winfo_reqwidth() + 20
        button_search.place(x=offset, y=710)

        offset += button_search.winfo_reqwidth() + 20
        button_reset.place(x=offset, y=710)

        # 0 Wall 1 Start 2 End 3 Water
        self.mode = 0
        self.color_node_mode_dict = [
            ('black', 'wall', 0), ('red', 'start', 1), ('green', 'end', 2), ('blue', 'water', 3), ('white', 'node', None)]

        # will contain the ids of the squares on the canvas
        self.matrix = []

        # used to check if a tile can change color
        self.last_x = None
        self.last_y = None
        self.can_change_color = True

        # fills the canvas
        for i in range(self.size // self.square_side):
            x = self.square_side*i
            row = []
            for j in range(self.size // self.square_side):
                y = self.square_side*j
                row.append(self.canvas.create_rectangle(
                    x, y, x+self.square_side, y+self.square_side, fill='white'))
            self.matrix.append(row)

    # clears the grey trail used to show the path
    def clear_from_route(self):
        for row in self.matrix:
            tmp_row = []
            for elem in row:
                color = self.canvas.itemcget(elem, 'fill')
                if color == 'grey':
                    self.canvas.itemconfig(elem, fill='white')

    # Performs the search
    def perform_search(self, event):
        self.clear_from_route()
        alg = self.get_alg()
        matrix = []
        for row in self.matrix:
            tmp_row = []
            for elem in row:
                color = self.canvas.itemcget(elem, 'fill')
                value = self.get_node_type(color)
                tmp_row.append(value)
            matrix.append(tmp_row)

        g = Graph(matrix)
        route = alg(
            g, [g.start_node], lambda n: n == g.end_node) if alg != search_pruning.A_star else alg(
            g, [g.start_node], lambda n: n == g.end_node, heuristic.distance)
        for node in route[1:-1]:
            i, j = node.value.split('_')[1:]
            i, j = int(i), int(j)
            self.canvas.itemconfig(self.matrix[i][j], fill='grey')

    # These function get called when a button is pressed
    def select_start(self, event):
        self.mode = 1

    def select_end(self, event):
        self.mode = 2

    def select_walls(self, event):
        self.mode = 0

    def select_water(self, event):
        self.mode = 3

    def reset(self, event):
        for row in self.matrix:
            for elem in row:
                self.canvas.itemconfig(elem, fill='white')

    def change_color(self, event):
        x = event.x
        y = event.y
        x = (x-(x % self.square_side))//self.square_side
        y = (y-(y % self.square_side))//self.square_side

        if (self.last_x == x and self.last_y == y) or not self.can_change_color:
            return

        self.last_x = x
        self.last_y = y
        self.can_change_color = False
        self.after(60, self.can_change_color_again)
        try:
            square = self.matrix[x][y]
        except IndexError:
            return
        color = self.get_color()

        if self.canvas.itemcget(square, 'fill') == 'white':
            self.canvas.itemconfig(square, fill=color)

        else:
            self.canvas.itemconfig(square, fill='white')

    def can_change_color_again(self):
        self.can_change_color = True

    # getters
    def get_color(self):
        for tuple in self.color_node_mode_dict:
            if tuple[2] == self.mode:
                return tuple[0]

    def get_node_type(self, color):
        for tuple in self.color_node_mode_dict:
            if tuple[0] == color:
                return tuple[1]

    def get_alg(self):
        value = self.algos_combo_box.get()
        alg_dict = {'naive': search_pruning.naive_search,
                    'breadth first': search_pruning.breadth_first_search,
                    'depth first': search_pruning.depth_first_search,
                    'iterative deepening': search_pruning.it_iterative_deepening,
                    'uniform cost': search_pruning.uniform_cost_search,
                    'A star': search_pruning.A_star}
        return alg_dict[value]


if __name__ == '__main__':
    app = App(None)
    app.mainloop()
