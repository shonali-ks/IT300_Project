from Generate_moves import *
import numpy as np


class State:
    cube = None
    cost = 0
    parent = None
    move = None


# checks if goal reached. 
def goal_reached(cube):
    for ref in [0, 3, 6, 9, 12, 15]:
        first = cube[ref, 0]
        for i in range(3):
            for j in range(3):
                if first != cube[ref + i, j]:
                    return False

    # goal reached
    print('Goal reached..\n')
    PrintCube(cube)
    return True


# checks if child ascendant of parent
def contains1(child, parent):
    curr = parent.parent
    while curr is not None:
        if np.array_equal(curr.cube, child): return True
        curr = curr.parent

    return False


# checks if frontier contains child
def contains2(child, frontier):
    for curr in frontier:
        if np.array_equal(curr.cube, child): return True

    return False


def idfs(start):
    cost_limit = 1
    nodes = 0
    frontier = list()
    branching_factors = list()

    while True:
        frontier.append(start)

        while len(frontier) != 0:
            curr = frontier.pop()

            if goal_reached(curr.cube):
                print('Goal Height:', curr.cost)
                print('Branching Factor:', sum(branching_factors)/len(branching_factors))
                print('Moves to solve:')
                while curr is not None:
                   if curr.move is not None:
                       print(curr.move)
                   curr = curr.parent
                print("Nodes Generated:", nodes)
                return

            if curr.cost + 1 <= cost_limit:
                child_cost = curr.cost + 1
                b = 0
                for i in range(12):
                    nodes = nodes + 1
                    new = State()
                    new.cube = np.array(curr.cube)
                    new.cost = child_cost
                    new.parent = curr
                    new.move = make_move(new.cube, i + 1, 0)
                    # if curr.parent is not None and np.array_equal(curr.parent.cube, new.cube):
                    if curr.parent is not None and (contains1(new.cube, curr) or contains2(new.cube, frontier)):
                        continue
                    frontier.append(new)
                    b = b + 1
                branching_factors.append(b)

        branching_factors.clear()
        cost_limit = cost_limit + 1


def manhattan_distance(cube, i, z, corner):
    x = i / 3
    y = i % 3
    center = None
    for c in [1, 4, 7, 10, 13, 16]:
        if cube[i, z] == cube[c, 1]:
            center = c
            break

    if corner:
        d1 = abs((center - 1) / 3 - x) + abs((center - 1) % 3 - y) + abs(z - 0)
        d2 = abs((center - 1) / 3 - x) + abs((center - 1) % 3 - y) + abs(z - 2)
        d3 = abs((center + 1) / 3 - x) + abs((center + 1) % 3 - y) + abs(z - 0)
        d4 = abs((center + 1) / 3 - x) + abs((center + 1) % 3 - y) + abs(z - 2)
        return min(d1, d2, d3, d4)
    else:
        d1 = abs((center - 1) / 3 - x) + abs((center - 1) % 3 - y) + abs(z - 1)
        d2 = abs(center / 3 - x) + abs(center % 3 - y) + abs(z - 0)
        d3 = abs(center / 3 - x) + abs(center % 3 - y) + abs(z - 2)
        d4 = abs((center + 1) / 3 - x) + abs((center + 1) % 3 - y) + abs(z - 1)
        return min(d1, d2, d3, d4)


def corner_edge_sum_max(cube):
    corners = 0
    edges = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges = edges + manhattan_distance(cube, i, 1, False)
        else:
            edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return max(corners / 4, edges / 4)


# driver
def driver_idfs(input):
    curr = State()
    curr.cube = np.array(xInitial)
    handle = open(input)
    indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
    index = 0
    for line in handle:
        line = line.replace(' ', '')
        for row in line.split('['):
            if len(row) != 0:
                i = indexes[index]
                curr.cube[i, 0] = row[1]
                curr.cube[i, 1] = row[4]
                curr.cube[i, 2] = row[7]
                index = index + 1
    idfs(curr)
    
