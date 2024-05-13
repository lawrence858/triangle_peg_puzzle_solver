"""
    Solver for the 15 hole Triangular Peg Solitaire

    Interesting analysis of this type of puzzle:
    http://www.gibell.net/pegsolitaire/tindex.html#Triangle5
    https://arxiv.org/pdf/math/0703865
"""
import copy

# just one possible option for the initial setup
initial_board = [
    [1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
]

# possible hop directions
directions = [
    [0, -2],
    [0, 2],
    [2, 2],
    [2, 0],
    [-2, -2],
    [-2, 0],
]

# keep track of board configurations that were already traversed
visited = dict()


def is_in_bounds(row, col):
    if row < 0 or row >= 5:
        return False
    if col < 0 or col >= 5:
        return False
    if col > row:
        return False
    return True


def row_to_string(row):
    return ''.join(['X' if val else '_' for val in row])


def board_to_string(board):
    return ''.join([row_to_string(row) for row in board])


def can_hop_direction(board, row, col, dy, dx):
    if board[row][col] != 1:
        return False
    if not is_in_bounds(row + dy, col + dx):
        return False
    if board[row + dy][col + dx] == 1:
        return False
    if board[row + dy // 2][col + dx // 2] != 1:
        return False
    return True


def possible_hop_directions(board, row, col):
    possible_directions = []
    for direction in directions:
        if can_hop_direction(board, row, col, direction[0], direction[1]):
            possible_directions.append(direction)
    return possible_directions


def do_hop(board, row, col, dy, dx):
    # assuming can_hop_direction has already been checked
    board = copy.deepcopy(board)
    board[row + dy // 2][col + dx // 2] = 0
    board[row + dy][col + dx] = 1
    board[row][col] = 0
    return board


def print_board(board):
    for row in range(5):
        print(board[row])
    print('')


def sum_pegs(board):
    count = 0
    for row in range(5):
        count += sum(board[row])
    return count


def solve_board(board, moves):
    board_str = board_to_string(board)
    if board_str in visited:
        return
    visited[board_str] = True
    for j in range(5):
        for i in range(5):
            directions = possible_hop_directions(board, j, i)
            for direction in directions:
                new_board = do_hop(board, j, i, direction[0], direction[1])
                new_moves = moves.copy()
                new_moves.append({'pos': [j, i], 'dir': direction})
                solve_board(new_board, new_moves)
    count = sum_pegs(board)
    if count < 2:
        print(moves)
        print_board(board)
        print('steps:')
        for move in moves:
            print(f"{(move['pos'][0], move['pos'][1])} --> {(move['pos'][0] + move['dir'][0], move['pos'][1] + move['dir'][1])}")
        exit()


if __name__ == '__main__':
    print_board(initial_board)
    solve_board(initial_board, [])

