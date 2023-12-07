from tkinter import *
from tkinter import ttk

UNFILLED = '#fff'
COLOR = ( 'black', 'blue', 'red', 'magenta', 'green', 'cyan', 'yellow', 'white')

# class SemiGraphicCharacter():
    
#     HEIGTH_SEMIGRAPHIC = 30
#     WIDTH_SEMIGRAPHIC = 10
#     PIXEL_SIZE = 5

#     def __init__(self, grid_layout, r: int, c: int) -> None:

#         self.canvas = Frame(grid_layout)
#         self.canvas.grid(0, 0)

#         self.r = r
#         self.c = c

#         self.color = 'white'

#         self.pixels = []
#         for i in range(3):
#             for j in range(2):
#                 rect = self.canvas.create_rectangle(
#                                             i * self.PIXEL_SIZE, j * self.PIXEL_SIZE, 
#                                             i * self.PIXEL_SIZE + self.PIXEL_SIZE, j * self.PIXEL_SIZE + self.PIXEL_SIZE , 
#                                             fill=UNFILLED)
                
#         self.
        
#         self.pixels.append(rect)


#     def setColor(self, color):
#         self.color = color
#         for element in self.pixels:
#             self.canvas.itemconfig(element, fill=self.color)


# class Palette():
    
#     HEIGHT_PALETTE = 20
#     WIDTH_PALETTE = 100

#     def __init__(self, root, pos_x, pos_y) -> None:
#         self.canvas = Canvas(root, height=self.HEIGHT_PALETTE, width=self.WIDTH_PALETTE, background='white')



root = Tk()
root.geometry("1000x900")

toolbar = Frame(root, background="#d5e8d4", height=40)
statusbar = Frame(root, background="#e3e3e3", height=20)
main = PanedWindow(root, background="#99fb99")

toolbar.pack(side='top', fill='x')
statusbar.pack(side='bottom', fill='x')
main.pack(side='top', fill='both', expand=True)

paletteframe = Frame(toolbar, height=20)

screenframe = Frame(main, background='#ffe6cd', height=30)
main.add(screenframe)

selected_color = 'black'
mouse_pressed = False

def clickColor(event):
    global selected_color 
    selected_color = event.widget['background']

def OnMouseUp(event):
    global mouse_pressed
    mouse_pressed = False
    print('button released')

def OnMouseDown(event):
    global mouse_pressed
    mouse_pressed = True
    print('button held')
    poll(root)

def poll(root):
    if not mouse_pressed:
        return
    x,y = root.winfo_pointerxy()
    widget = root.winfo_containing(x,y)
    
    try:
        widget = root.nametowidget(widget)
        if widget.master.master == screenframe:
            widget.config(bg=selected_color)
            if selected_color != 'black':
                for child in widget.master.winfo_children():
                    if child['background'] != 'black':
                        child.config(background=selected_color)
    except:
        print("Exception occured")

    root.after(1, poll, root)    

iter = 0
for color in COLOR:
    print(color)
    f = Frame(toolbar, height=20, width=20, background=color, bd=2, relief='flat')
    f.grid(row=0, column=iter)
    iter+=1
    f.bind('<Button-1>', clickColor)

for row in range(23):
    for column in range(40):
        semigraphframe = Frame(screenframe, width=20, height=30,relief='sunken', bd=1)
        semigraphframe.grid(row=row, column=column)

        for row2 in range(3):
            for column2 in range(2):
                f = Frame(semigraphframe, background='black', bd=1, relief='ridge', width=10, height=10)
                f.grid(row=row2, column=column2)

root.bind("<ButtonPress-1>", OnMouseDown)
root.bind("<ButtonRelease-1>", OnMouseUp)

# palette = Palette(root, 1, 1)
# char = SemiGraphicCharacter(root, 0, 0)
# char.setColor('white')

root.mainloop()