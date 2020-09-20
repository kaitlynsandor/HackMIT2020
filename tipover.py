HEIGHT = 0
WIDTH = 0
START_POS = []
BOARD = []
ORIG_BOARD = []

VISITED_SPACES = []
POSSIBLE_MOVES = []

#what positions can we move to and out of these positions which ones are able to tip
def find_valid_positions(pos):
    valid_moves = []
    #check positions
    right = [pos[0], pos[1]+1]
    left = [pos[0], pos[1]-1]
    up = [pos[0]-1, pos[1]]
    down = [pos[0]+1, pos[1]]

    #make sure we are not going off the board or moving to an empty space
    if right[1] < WIDTH and BOARD[right[0]][right[1]] != '.':
        valid_moves.append(right)
    if left[1] > -1 and BOARD[left[0]][left[1]] != '.':
        valid_moves.append(left)
    if up[0] > -1 and BOARD[up[0]][up[1]] != '.':
        valid_moves.append(up)
    if down[0] < HEIGHT and BOARD[down[0]][down[1]] != '.':
        valid_moves.append(down)

    valid_moves.append(pos)
    for move in valid_moves:
        if move not in VISITED_SPACES:
            VISITED_SPACES.append(move)
            if BOARD[move[0]][move[1]] != '.' and(BOARD[move[0]][move[1]] == '*'or int(BOARD[move[0]][move[1]]) > 1):
                if BOARD[move[0]][move[1]] == '*':
                    POSSIBLE_MOVES.append('*')
                else:
                    POSSIBLE_MOVES.append(move)
            find_valid_positions(move)
    return POSSIBLE_MOVES

VALID_TIP_MOVES = []
TRIED_MOVES = []

#out of all  of the  possbile tips, which ones can we actually perform?
def find_valid_moves(moves):
    final_moves = []
    directions = [[1, 0], [0, 1], [0, -1],  [-1, 0]]
    for move in moves:
        cur_height = int(BOARD[move[0]][move[1]])
        for direction in directions:
            if cur_height > 1:
                broken = False
                for i in range(0, cur_height):
                    if direction[0] < 0 or direction[1] < 0:
                        i = -i
                    if direction[0] != 0:
                        row = int(move[0]+direction[0]+i)
                        col = int(move[1]+direction[1])
                    else:
                        row = int(move[0] + direction[0])
                        col = int(move[1] + direction[1]+i)
                    if row >= HEIGHT or row < 0 or col >= WIDTH or col < 0 or BOARD[row][col] != '.':
                        broken = True
                    elif abs(i) == cur_height-1 and not broken:
                        final_moves.append(move + direction)
    return final_moves


#final position of man after tips
def destination(move):
    distance = int(ORIG_BOARD[move[0]][move[1]])
    direction = move[2:]
    if direction[0] < 0 or direction[1] <0:
        distance = -distance
    if direction[0] == -1 or direction[0] == 1:
        return [move[0]+distance, move[1]]
    else:
        return [move[0], move[1]+distance]

#update board to reflect move
def update_BOARD(move):
    cur_height = int(ORIG_BOARD[move[0]][move[1]])
    direction = [move[2], move[3]]
    string = list(BOARD[move[0]])
    string[move[1]] = '.'
    new_string = ""
    for s in string:
        new_string += s
    BOARD[move[0]] = new_string
    for i in range(0, cur_height):
        if direction[0] < 0 or direction[1] < 0:
            i = -i
        if direction[0] != 0:
            row = int(move[0] + direction[0] + i)
            col = int(move[1] + direction[1])
        else:
            row = int(move[0] + direction[0])
            col = int(move[1] + direction[1] + i)
        string = list(BOARD[row])
        string[col] = '1'
        new_string = ""
        for s in string:
            new_string += s
        BOARD[row] = new_string

#undo moves on the board
def undo_move(move):
    cur_height = int(ORIG_BOARD[move[0]][move[1]])
    direction = [move[2], move[3]]
    string = list(BOARD[move[0]])
    string[move[1]] = str(cur_height)
    new_string = ""
    for s in string:
        new_string += s
    BOARD[move[0]] = new_string
    for i in range(0, cur_height):
        if direction[0] < 0 or direction[1] < 0:
            i = -i
        if direction[0] != 0:
            row = int(move[0] + direction[0] + i)
            col = int(move[1] + direction[1])
        else:
            row = int(move[0] + direction[0])
            col = int(move[1] + direction[1] + i)
        string = list(BOARD[row])
        string[col] = '.'
        new_string = ""
        for s in string:
            new_string+=s
        BOARD[row] = new_string

#solution that puts it all together
def find_solution(pos):
    POSSIBLE_MOVES.clear()
    VISITED_SPACES.clear()
    find_valid_positions(pos[:2])
    positions = POSSIBLE_MOVES
    if '*' in positions:
        return [pos]
    moves = find_valid_moves(positions)
    if moves != []:
        TRIED_MOVES.clear()
        for move in moves:
            if move not in TRIED_MOVES:
                update_BOARD(move)
                TRIED_MOVES.append(move)
                new_pos = destination(move) + [0, 0]
                solution = find_solution(new_pos)
                if solution:
                    return [move] + solution
                else:
                    undo_move(move)
import sys
if __name__ == '__main__':

    #update  recursion limit
    sys.setrecursionlimit(2500)

    # open file and extract meaningful data
    content = []
    for line in sys.stdin:
        content.append(line.strip())
    content[0] = content[0].split()
    content[1] = content[1].split()

    HEIGHT = int(content[0][0])
    WIDTH = int(content[0][1])

    START_POS = [int(content[1][0]), int(content[1][1])]

    for i in range(2, len(content)):
        BOARD.append(content[i])
        ORIG_BOARD.append(content[i])

    # start the  algorithm
    moves = find_solution(START_POS+[0, 0])
    # print out the final output, but remove the ending position because we don't care about that
    if moves:
        moves = moves[:-1]
        for move in moves:
            print(move[0], end = ' ')
            print(move[1], end=' ')
            print(move[2], end=' ')
            print(move[3], end=' ')
            print()