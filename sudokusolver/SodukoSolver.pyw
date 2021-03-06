from tkinter import *
from datetime import datetime

root = Tk()

#still need to improve GUI -- because it's super ugly :(
#can probably break by inputting a non 1-9 number
#if I can find a way to say that if possibilities are 23 23 236 657 57 then the third cell must be 6

class Cell(object):

    def __init__(self, x, y, smatrix, filled, solved, value, entry):
        self.x = x
        self.y = y
        self.smatrix = smatrix
        self.filled = filled
        self.solved = solved
        self.value = value
        self.entry = IntVar()

cells = []

for i in range(1,10):
    for j in range(1,10):
            cell = Cell(i, j, 0, False, False, [1,2,3,4,5,6,7,8,9],[])
            cells.append(cell)

for i in range(0,81):
    cells[i].entry = Entry(root, width="3")
    cells[i].entry.grid(row=str(cells[i].x), column = str(cells[i].y))

#dictionary of three empty lists to hold different cells
row = {i: [] for i in range(1,10)}
col = {i: [] for i in range(1,10)}
smatrix = {i: [] for i in range(1,10)}

#add to appropriate column and row
for cell in cells:
    for i in range(1,10):
        if cell.x == i:
            row[i].append(cell)
        if cell.y == i:
            col[i].append(cell)

#add to appropriate smatrix
for cell in cells:
    k = 1
    for i in range(1,10,3):
        for j in range(1,10,3):
            if cell in row[i] and cell in col[j]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i] and cell in col[j+1]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i] and cell in col[j+2]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i+1] and cell in col[j]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i+1] and cell in col[j+1]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i+1] and cell in col[j+2]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i+2] and cell in col[j]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i+2] and cell in col[j+1]:
                smatrix[k].append(cell)
                cell.smatrix = k
            if cell in row[i+2] and cell in col[j+2]:
                smatrix[k].append(cell)
                cell.smatrix = k
            k+=1

def getSudoku():
    for i in range(0,81):
        if cells[i].entry.get() != "":
            value = cells[i].entry.get()
            value = int(value)
            cells[i].value = [value]

def returnSudoku():
    for i in range(0, 81):
        if cells[i].entry.get() == "" and type(cells[i].value) == int:
            cells[i].entry.insert(0, str(cells[i].value))

def printSudoku():
    for i in range(1,10):
        for cell in row[i]:
            try:
                if len(cell.value)==1:
                    print (cell.value[0], end=" ")
                else:
                    print (cell.value)
            except:
                if type(cell.value)==int:
                    print (cell.value, end= " ")
        print ()

def solveSudoku():
    overTime = False
    done = 0
    previousdone = 0
    dtstart = datetime.now()
    while done < len(cells):
        for cell in cells:
            if not cell.solved:
                if cell.filled:
                    done += 1
                    cell.solved = True

        for cell in cells:
            if type(cell.value) == list:
                if len(cell.value) == 1:
                    #this is gonna be a singlet so we can do this happily
                    cell.value = cell.value[0]
                    cell.filled = True

        # if a row, col, or matrix has a member that just one value--
        # remove that value from the other cells possible values
        for cell in cells:
            if cell.filled:
                value_to_remove = cell.value
                for othercells in row[cell.x]:
                    try:
                        othercells.value.remove(value_to_remove)
                    except:
                        pass
                for othercells in col[cell.y]:
                    try:
                        othercells.value.remove(value_to_remove)
                    except:
                        pass
                for othercells in smatrix[cell.smatrix]:
                    try:
                        othercells.value.remove(value_to_remove)
                    except:
                        pass

        # given the possible values of a single cell
        # if one of the possible values is unique among all possible values in that row, col, smatrix
        # then that cell is that value
        # this is really only worth it for sudoko that can't be solved by deduction... induction required.
        if previousdone == done:
            for i in range(1,10):
                compare = [1,2,3,4,5,6,7,8,9]
                for cell in row[i]:
                    if type(cell.value) == int:
                        compare.remove(cell.value)
                singlets = {}
                for cell in row[i]:
                    if type(cell.value) == list:
                        for number in compare:
                            if number in cell.value:
                                if number not in singlets.keys():
                                    singlets[number] = 1
                                else:
                                    singlets[number] += 1
                for number in compare:
                    if singlets[number] == 1:
                        for cell in row[i]:
                            if type(cell.value) == list and number in cell.value:
                                cell.value = number
                                cell.filled = True

                compare = [1,2,3,4,5,6,7,8,9]
                for cell in col[i]:
                    if type(cell.value) == int:
                        compare.remove(cell.value)
                singlets = {}
                for cell in col[i]:
                    if type(cell.value) == list:
                        for number in compare:
                            if number in cell.value:
                                if number not in singlets.keys():
                                    singlets[number] = 1
                                else:
                                    singlets[number] += 1
                for number in compare:
                    if singlets[number] == 1:
                        for cell in col[i]:
                            if type(cell.value) == list and number in cell.value:
                                cell.value = number
                                cell.filled = True

                compare = [1,2,3,4,5,6,7,8,9]
                for cell in smatrix[i]:
                    if type(cell.value) == int:
                        compare.remove(cell.value)
                singlets = {}
                for cell in smatrix[i]:
                    if type(cell.value) == list:
                        for number in compare:
                            if number in cell.value:
                                if number not in singlets.keys():
                                    singlets[number] = 1
                                else:
                                    singlets[number] += 1
                for number in compare:
                    if singlets[number] == 1:
                        for cell in smatrix[i]:
                            if type(cell.value) == list and number in cell.value:
                                cell.value = number
                                cell.filled = True

        previousdone = done
        dtend = datetime.now()
        dttotal = dtend - dtstart
        if dttotal.total_seconds() > 2:
            overTime = True
            return overTime
    return overTime

def solveSudoku_button(event):
    getSudoku()
    overTime = solveSudoku()
    if overTime:
        returnSudoku()
        overTimeText.grid(columnspan="9")
    else:
        returnSudoku()
    printSudoku()


overTimeText = Label(root, text="The program is confused. \nThis Sudoku is too much.")
button1 = Button(root, text="Solve Sudoku")
button1.bind("<Button-1>", solveSudoku_button)
button1.grid(columnspan="9")


root.mainloop()
