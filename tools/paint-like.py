from tkinter import Tk, Canvas, NW, NE, N

fen = Tk()
fen.geometry("1380x740")
fen.title("Dessine moi un mouton !")

c_width = 2*10*40
c_height = 6*10*23
couleur = "red"
epaisseur= 10

sdessin = Canvas(width = c_width, height = c_height, bg ='white')

rows, cols = c_height//10, c_width//10
# create the board
board = [['white' for _ in range(cols)] for _ in range(rows)]
# draw the board
for row in range(rows):
    for col in range(cols):
        x, y = col*10, row*10
        sdessin.create_rectangle(x, y, x+10, y+10, fill=board[row][col], outline='',
                                 tag='%d:%d'%(row,col))  # tag used for updating color later

def pix_to_units(x, y):
    return y//10, x//10   # row, col

def interaction(event):
    row, col = pix_to_units(event.x, event.y)
    board[row][col] = couleur
    tag = '%d:%d' % (row, col)
    sdessin.itemconfig(tag, fill=couleur)

sdessin.bind("<B1-Motion>", interaction)
sdessin.grid(row=2, column=2, sticky=N)

fen.mainloop()