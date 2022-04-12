from typing import Tuple


def generate_maze() -> list:
    n = int(input())
    maze = []
    block_num = 0
    for i in range(n):
        line = input()
        nums = line.split(' ')
        maze.append([])
        for block in nums:
            maze[i].append(int(block))
    return maze


class MazeEncoder:
    def __init__(self, maze: list):
        self.maze = maze
        self.n = len(self.maze)
        self.actions = {}
        self.blocks = {}
        self.block_num = 1
        for i in range(self.n):
            for j in range(self.n):
                if maze[i][j] == 0:
                    self.blocks[(i, j)] = self.block_num
                    self.block_num += 1
        self.block_num -= 1
        self.k = self.block_num - 1
        self.action_begin = self.block_num * self.block_num * 3
        self.action_num = 1
        for i in range(self.n):
            for j in range(self.n):
                if 0 <= i + 1 < self.n and not self.maze[i + 1][j]:
                    self.actions[((i, j), (i + 1, j))] = self.action_num
                    self.action_num += 1
                if 0 <= i - 1 < self.n and not self.maze[i - 1][j]:
                    self.actions[((i, j), (i - 1, j))] = self.action_num
                    self.action_num += 1
                if 0 <= j + 1 < self.n and not self.maze[i][j + 1]:
                    self.actions[((i, j), (i, j + 1))] = self.action_num
                    self.action_num += 1
                if 0 <= j - 1 < self.n and not self.maze[i][j - 1]:
                    self.actions[((i, j), (i, j - 1))] = self.action_num
                    self.action_num += 1
        self.action_num -= 1

    def generate_variables(self):
        # generate states

        pass


if __name__ == '__main__':
    # maze = generate_maze()
    # print(maze)
    maze_test = [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]
    encoder = MazeEncoder(maze_test)

