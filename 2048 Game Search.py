from copy import deepcopy
from typing import Tuple, List
from sys import maxsize as MAX_INT
from random import randint, seed
import time

weights = [
        [2**15, 2**14, 2**13, 2**12],
        [2**8, 2**9, 2**10, 2**11],
        [2**7, 2**6, 2**5, 2**4],
        [2**0, 2**1, 2**2, 2**3]
]

def placeTile(grid, row: int, col: int, tile: int):
    grid[row][col] = tile
    return grid

def heuristic(grid) -> int:
    count = 0
    sumNumbers = 0
    sumEmpty = 0

    for i in range(4):
        for j in range(4):
            sumNumbers += (grid[i][j] * weights[i][j])
            if grid[i][j] == 0:
                count += 1
                # sumEmpty += weights[1][2]
    return sumNumbers + count * weights[0][3]

def canMoveUp(grid):
    for i in range(1, 4):
        for j in range(4):
            if (grid[i][j] != 0 and grid[i-1][j] ==0) or (grid[i][j] == grid[i-1][j]):
                return True
    return False

def canMoveDown(grid):
    for i in range(3):
        for j in range(4):
            if (grid[i][j] != 0 and grid[i+1][j] ==0) or (grid[i][j] == grid[i+1][j]):
                return True
    return False

def canMoveLeft(grid):
    for i in range(4):
        for j in range(1, 4):
            if (grid[i][j] != 0 and grid[i][j-1] ==0) or (grid[i][j] == grid[i][j-1]):
                return True
    return False

def canMoveRight(grid):
    for i in range(4):
        for j in range(3):
            if (grid[i][j] != 0 and grid[i][j+1] ==0) or (grid[i][j] == grid[i][j+1]):
                return True
    return False


def getAvailableMovesForMax(grid) -> List[int]:
    availableMoves = []

    if canMoveUp(grid):
        availableMoves.append(0)
    if canMoveDown(grid):
        availableMoves.append(1)
    if canMoveLeft(grid):
        availableMoves.append(2)
    if canMoveRight(grid):
        availableMoves.append(3)

    return availableMoves

def isMaxTerminal(grid):
    if canMoveLeft(grid):
        return False
    if canMoveRight(grid):
        return False
    if canMoveUp(grid):
        return False
    if canMoveDown(grid):
        return False
    return True

def getAvailableTile(grid):
    availableTiles = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                availableTiles.append((i,j))
    return availableTiles

def isChanceTerminal(grid):
    availableTiles = getAvailableTile(grid)
    if len(availableTiles) == 0:
        return True
    return False


def right(grid):
    for i in [0,1,2,3]:
        j = 3
        while j >= 0:
            if grid[i][j] == 0:
                j -= 1
            elif j > 0 and grid[i][j] == grid[i][j-1]:
                grid[i][j] *= 2
                grid[i][j-1] = 0
                j -= 2
            elif j > 1 and grid[i][j-1] == 0 and grid[i][j] == grid[i][j-2]:
                grid[i][j] *= 2
                grid[i][j - 2] = 0
                j = -1
            elif j == 3 and grid[i][j] == grid[i][0] and grid[i][j-1] == 0 and grid[i][j-2] == 0:
                grid[i][j] *= 2
                grid[i][0] = 0
                j = -1
            else:
                j -= 1
        j = 0
        n = []
        while j <= 3:
            if grid[i][j] != 0:
                n.append(grid[i][j])
                grid[i][j] = 0
            j += 1
        m = len(n)
        for i1 in n:
            grid[i][3-m+1] = i1
            m -= 1
    return grid

def left(grid):
    for i in [0, 1, 2, 3]:
        j = 0
        while j <= 3:
            if grid[i][j] == 0:
                j += 1
            elif j < 3 and grid[i][j] == grid[i][j+1]:
                grid[i][j] *= 2
                grid[i][j+1] = 0
                j += 2
            elif j < 2 and grid[i][j+1] == 0 and grid[i][j] ==grid[i][j+2]:
                grid[i][j] *= 2
                grid[i][j + 2] = 0
                j = 4
            elif j == 0 and grid[i][j] == grid[i][3] and grid[i][j+1] == 0 and grid[i][j+2] == 0:
                grid[i][j] *= 2
                grid[i][3] =0
                j = 4
            else:
                j += 1
        j = 0
        n = []
        while j <= 3:
            if grid[i][j] != 0:
                n.append(grid[i][j])
                grid[i][j] = 0
            j += 1
        m = 0
        for i1 in n:
            grid[i][m] = i1
            m += 1
    return grid

def down(grid):
    for j in [0,1,2,3]:
        i = 3
        while i>=0:
            if grid[i][j] == 0:
                i -= 1
            elif i> 0 and grid[i][j] == grid[i-1][j]:
                grid[i][j] *= 2
                grid[i-1][j] = 0
                i -= 2
            elif i>1 and grid[i-1][j] == 0 and grid[i][j] == grid[i-2][j]:
                grid[i][j] *= 2
                grid[i-2][j] = 0
                i -= 1
            elif i == 3 and grid[i][j] == grid[0][j] and grid[i-1][j] == 0 and grid[i-2][j] == 0:
                grid[i][j] *= 2
                grid[0][j] = 0
                i = -1
            else:
                i -= 1
        i = 0
        n = []
        while i <= 3:
            if grid[i][j] != 0:
                n.append(grid[i][j])
                grid[i][j] = 0
            i += 1
        m = len(n)
        for i1 in n:
            grid[3-m+1][j] = i1
            m -= 1
    return grid

def up(grid):
    for j in [0,1,2,3]:
        i = 0
        while i <= 3:
            if grid[i][j] == 0:
                i += 1
            elif i<3 and grid[i][j] == grid[i+1][j]:
                grid[i][j] *= 2
                grid[i + 1][j] = 0
                i += 2
            elif i < 2 and grid[i+1][j] == 0 and grid[i][j] == grid[i+2][j]:
                grid[i][j] *= 2
                grid[i + 2][j] = 0
                i += 1
            elif i ==0 and grid[i][j] ==grid[3][j] and grid[i+1][j] == 0 and grid[i+2][j] == 0:
                grid[i][j] *= 2
                grid[3][j] = 0
                i = 4
            else:
                i += 1
        i = 0
        n = []
        while i <= 3:
            if grid[i][j] != 0:
                n.append(grid[i][j])
                grid[i][j] = 0
            i += 1
        m = 0
        for i1 in n:
            grid[m][j] = i1
            m += 1
    return grid

def move(grid, mv: int): #-> grid:
    if mv == 0:
        grid = up(grid)
    elif mv == 1:
        grid = down(grid)
    elif mv == 2:
        grid = left(grid)
    elif mv == 3:
        grid = right(grid)
    return grid
    

def maximize1(grid, depth: int):
    moves = getAvailableMovesForMax(grid) #1,2,3
    newMoveGrids =[]
    
    maxUtility = -9999999
    bestMove = None

    for m in moves:
        Gridcopy = deepcopy(grid)
        newGrid = move(Gridcopy,m)
        newMoveGrids.append((m, newGrid))

    if depth == 0 or isMaxTerminal(grid):
        return (bestMove, heuristic(grid))
    depth -= 1
    
    for mv in newMoveGrids:
        utility = chance(mv[1],depth)
        if utility > maxUtility:
            maxUtility = utility
            bestMove = mv[0]
    return (bestMove, maxUtility)

def chance(grid, depth: int):
    availableTiles = getAvailableTile(grid)
    countAvailableTiles = len(availableTiles)
    chance2 = 0.9/countAvailableTiles
    chance4 = 0.1/countAvailableTiles
    if depth == 0 or isChanceTerminal(grid):
        return (heuristic(grid))

    MoveOptions = []

    for emptyTiles in availableTiles:
        MoveOptions.append((emptyTiles,2,chance2))
        MoveOptions.append((emptyTiles,4,chance4))
    utilityAll = 0
    for mv in MoveOptions:
        gridCopy = deepcopy(grid)
        newGrid = placeTile(gridCopy,mv[0][0],mv[0][1],mv[1])
        (moveDir,utility) = maximize1(newGrid,depth-1)
        utilityAll = utilityAll + utility * mv[2]
    return utilityAll

def NextMove(grid: list,step: int)->int:
    (bestMove, util) = maximize1(grid, 3)
    return bestMove

def NextMove111(grid: list,step: int)->int:
    (bestMove, util) = maximize1(grid,3)
    return (bestMove,util)

def insert_random_tile(grid):
    if randint(0,99) < 100 * 0.9:
        value = 2
    else:
        value = 4

    cells = getAvailableTile(grid)
    pos = cells[randint(0, len(cells) - 1)] if len(cells) > 0 else None #(2,3)
    placeTile(grid, pos[0], pos[1], value)

grid = [
    [ 2, 2, 0, 0],
    [ 0, 0, 0, 0],
    [ 0, 0, 0, 0],
    [ 0, 0, 0, 0]
]

start = time.time()
step = 1
thing = True
while thing:
    if isMaxTerminal(grid):
        print("Unfortunately, I lost the game.")
        break
    (moveCode,util) = NextMove111(grid, 1)
    print('step:',step)
    step+=1
    print('movecode:',moveCode)
    print('util:',util)
    grid = move(grid,moveCode)
    print(grid)
    print('addrandom')
    insert_random_tile(grid)
    print('newgrid',grid)
end = time.time()
print(end - start) 

