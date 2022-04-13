from enum import Enum
from typing import Tuple


class Variable(Enum):
    current = 0
    arrived = 1
    empty = 2


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


def package_clause(variables: list) -> str:
    clause = str(variables[0])
    for i in range(1, len(variables)):
        clause += ' ' + str(variables[i])
    return clause


def set_block(start: int, choice: Variable) -> list:
    block = [start, start + 1, start + 2]
    for i in range(3):
        if i == choice.value:
            pass
        else:
            block[i] = -block[i]
    return block


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
        self.variable_num = self.action_begin + self.action_num * self.k * 12
        self.clauses = []
        self.generate_clauses()

    def generate_clauses(self):
        # generate states
        self.clause_1()
        self.clause_2()
        self.clause_3()
        self.clause_4()
        self.clause_5()
        self.clause_6()
        self.clause_7()
        self.clause_8()
        pass

    def clause_1(self):
        # 第一个state是初始状态
        c = set_block(self.blocks[(0, 0)], Variable.current)
        for i in range(1, self.block_num):
            c += set_block(i * 3 + 1, Variable.empty)
        for i in c:
            self.clauses.append(package_clause([i]))

    def clause_2(self):
        # goal condition最终被满足
        goal = set_block(self.block_num * 3 * self.k + self.blocks[(self.n - 1, self.n - 1)] * 3 - 2, Variable.current)
        for i in goal:
            self.clauses.append(package_clause([i]))

    def clause_3(self):
        # 每个state变量至少有一个value
        for t in range(self.block_num):
            for i in range(self.block_num):
                start = self.block_num * 3 * t + i * 3
                self.clauses.append(package_clause([start + 1, start + 2, start + 3]))

    def clause_4(self):
        # 每个state变量最多有一个value
        for t in range(self.block_num):
            for i in range(self.block_num):
                start = self.block_num * 3 * t + i * 3
                self.clauses.append(package_clause([-(start + 1), -(start + 2)]))
                self.clauses.append(package_clause([-(start + 2), -(start + 3)]))
                self.clauses.append(package_clause([-(start + 1), -(start + 3)]))

    def clause_5(self):
        # 每个action都满足pre
        pass

    def clause_6(self):
        # 每个action都实现eff
        pass

    def clause_7(self):
        # state变量不经过action不可改变
        pass

    def clause_8(self):
        # 每一步最多只能使用一个action
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
