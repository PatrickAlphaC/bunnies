import sys
import json


def get_input(input_file):
    file = open(input_file)
    return json.load(file)


def run_depth_first_search(board, closed_list, open_list):
    current = Node((0, 0))
    closed_list.append(current)
    current.explore_possible_moves(board, closed_list, open_list)
    fastest_run = None
    print("Board size is {} x {} for a total of {}".format(
        len(board), len(board[0]), fastest_run))
    while len(open_list) > 0:
        current = open_list.pop(0)
        closed_list.append(current)
        if current.is_win_state(board):
            if not fastest_run:
                fastest_run = current.move_count
            elif current.move_count < fastest_run:
                fastest_run = current.move_count
        else:
            current.explore_possible_moves(board, closed_list, open_list)
    return fastest_run


class Node:
    DOWN = [1, 0]
    UP = [-1, 0]
    RIGHT = [0, 1]
    LEFT = [0, -1]
    possible_moves = [RIGHT, DOWN, LEFT, UP]

    def __init__(self, position, bomb=True, dad=None, move_count=0):
        self.position = position
        self.dad = dad
        self.bomb = bomb
        self.move_count = move_count

    def get_new_state(self, move):
        new_position = self.position[0] + move[0], self.position[1] + move[1]
        return Node(new_position, bomb=self.bomb, dad=self, move_count=self.move_count + 1)

    def explore_possible_moves(self, board, closed_list, open_list):
        for move in self.possible_moves:
            new_state = self.get_new_state(move)
            if new_state.isvalid_andor_bomb(board, closed_list, open_list):
                open_list.append(new_state)

    def __eq__(self, other):
        return self.position == other.position and self.bomb == other.bomb and self.move_count >= other.move_count

    def isvalid_andor_bomb(self, board, closed_list, open_list):
        if self in closed_list or self in open_list:
            return False
        if self.position[0] >= len(board) or self.position[1] >= len(board[0]):
            return False
        if self.position[0] < 0 or self.position[1] < 0:
            return False
        if board[self.position[0]][self.position[1]] == 1 and self.bomb == True:
            self.bomb = False
            return True
        if board[self.position[0]][self.position[1]] != 1:
            return True
        return False

    def is_win_state(self, board):
        if self.position == (len(board) - 1, len(board[0]) - 1):
            return True
        return False


def main():
    input_file = sys.argv[1]
    list_of_boards = get_input(input_file)
    for board in list_of_boards:
        closed_list = []
        open_list = []
        fastest_run = run_depth_first_search(board, closed_list, open_list)
        print("Board {} had a fastest run of {}".format(board, fastest_run))


if __name__ == '__main__':
    main()
