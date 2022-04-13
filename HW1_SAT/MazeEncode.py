from enum import Enum


class Variable(Enum):
    current = 0
    arrived = 1
    empty = 2


def generate_maze() -> list:
    n = int(input())
    maze = []
    for i in range(n):
        line = input()
        maze.append([])
        for block in line:
            maze[i].append(int(block))
    return maze


def package_clause(variables: list) -> str:
    clause = str(variables[0])
    for i in range(1, len(variables)):
        clause += ' ' + str(variables[i])
    clause += ' ' + str(0)
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
    def __init__(self, maze: list, file: str):
        self.file = file
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
                if self.maze[i][j]:
                    continue
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
        self.variable_num = self.action_begin + self.action_num * self.k
        self.clauses = []

    def encode(self):
        self.generate_clauses()
        self.generate_cnf()

    def generate_clauses(self):
        # generate states
        self.clause_1()
        self.clause_2()
        self.clause_3_4()
        self.clause_5_6()
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

    def clause_3_4(self):
        for t in range(self.block_num):
            for i in range(self.block_num):
                start = self.block_num * 3 * t + i * 3
                # 每个state变量至少有一个value
                self.clauses.append(package_clause([start + 1, start + 2, start + 3]))
                # 每个state变量最多有一个value
                self.clauses.append(package_clause([-(start + 1), -(start + 2)]))
                self.clauses.append(package_clause([-(start + 2), -(start + 3)]))
                self.clauses.append(package_clause([-(start + 1), -(start + 3)]))

    def clause_5_6(self):
        # 每个action都满足pre
        for t in range(self.k):
            for key, value in self.actions.items():
                a = self.action_begin + t * self.action_num + value
                # 每个action都满足pre
                pre_block_1 = self.block_num * 3 * t + self.blocks[key[0]] * 3 - 2
                pre_block_2 = self.block_num * 3 * t + self.blocks[key[1]] * 3 - 2
                c1 = set_block(pre_block_1, Variable.current) + set_block(pre_block_2, Variable.empty)
                # 每个action都实现eff
                eff_block_1 = self.block_num * 3 * (t + 1) + self.blocks[key[0]] * 3 - 2
                eff_block_2 = self.block_num * 3 * (t + 1) + self.blocks[key[1]] * 3 - 2
                c2 = set_block(eff_block_1, Variable.arrived) + set_block(eff_block_2, Variable.current)
                for i in c1 + c2:
                    self.clauses.append(package_clause([-a, i]))

    def clause_7(self):
        # state变量不经过action不可改变
        for t in range(self.k):
            for key, value in self.blocks.items():
                block_1 = self.block_num * 3 * t + (value - 1) * 3
                block_2 = self.block_num * 3 * (t + 1) + (value - 1) * 3
                first_match = []
                second_match = []
                for a_key, a_value in self.actions.items():
                    if a_key[0] == key:
                        first_match.append(self.action_begin + t * self.action_num + a_value)
                    if a_key[1] == key:
                        second_match.append(self.action_begin + t * self.action_num + a_value)
                # current
                self.clauses.append(package_clause([block_1 + 1, -(block_2 + 1)] + second_match))
                # arrived
                self.clauses.append(package_clause([block_1 + 2, -(block_2 + 2)] + first_match))
                # empty
                self.clauses.append(package_clause([block_1 + 3, -(block_2 + 3)]))

    def clause_8(self):
        # 每一步最多只能使用一个action
        for t in range(self.k):
            for a1 in self.actions.values():
                a1 += self.action_begin + t * self.action_num
                for a2 in self.actions.values():
                    a2 += self.action_begin + t * self.action_num
                    if a1 == a2:
                        continue
                    self.clauses.append(package_clause([-a1, -a2]))

    def generate_cnf(self):
        with open(self.file, 'w') as f:
            f.write('p cnf ' + str(self.variable_num) + ' ' + str(len(self.clauses)) + '\n')
            for c in self.clauses:
                f.write(c + '\n')

    def decode(self):
        with open(self.file, 'r') as f:
            for line in f.readlines():
                if line.strip() == 'SAT':
                    continue
                variables = line.split(' ')
        variables.remove('0\n')
        path = []
        for t in range(self.block_num):
            for key, value in self.blocks.items():
                block = self.block_num * 3 * t + (value - 1) * 3 + 1
                if int(variables[block - 1]) > 0:
                    path.append(key)
                    break
        for i, j in path:
            self.maze[i][j] = 2
        print('PATH')
        for i in range(self.n):
            line = ''
            for j in range(self.n):
                line += str(maze[i][j])
            print(line)


if __name__ == '__main__':
    maze = generate_maze()

    # encoder = MazeEncoder(maze, 'encoding/sample0.cnf')
    # encoder.encode()

    encoder = MazeEncoder(maze, 'encoding/output_sample2.log')
    encoder.decode()
