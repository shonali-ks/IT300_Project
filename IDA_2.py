from Generate_moves import *
import numpy as np
import sqlite3


db = dict()


def get_corner_string(cube):
    string = ''
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            string = string + cube[i, 0] + cube[i, 2]
    return string


class State:
    cube = None
    g = 0
    h = 0
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


def get_db():
    conn = sqlite3.connect('corners.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM CornerValue")
    rows = cur.fetchall()
    for x, y in rows:
        db[x] = y


def ida(start):
    start.h = heuristic(start.cube)
    cost_limit = start.h
    nodes = 0
    frontier = list()
    branching_factors = list()

    while True:
        minimum = None
        frontier.append(start)

        while len(frontier) != 0:
            curr = frontier.pop()

            if goal_reached(curr.cube):
                print('Goal Height:', curr.g)
                print('Branching Factor:', sum(branching_factors)/len(branching_factors))
                print('Moves to solve:')
                while curr is not None:
                   if curr.move is not None:
                       print(curr.move)
                   curr = curr.parent
                print("Nodes Generated:", nodes)
                return

            b = 0
            nodes = nodes + 12
            for i in range(12):
                new = State()
                new.cube = np.array(curr.cube)
                new.g = curr.g + 1
                new.parent = curr
                new.move = make_move(new.cube, i + 1, 0)
                new.h = heuristic(new.cube)

                if new.g + new.h > cost_limit:
                    if minimum is None or new.g + new.h < minimum:
                        minimum = new.g + new.h
                    continue
                if curr.parent is not None and (contains1(new.cube, curr) or contains2(new.cube, frontier)):
                    continue
                frontier.append(new)
                b = b + 1
            if b != 0:
                branching_factors.append(b)

        cost_limit = minimum


def heuristic(cube):
    a = db[get_corner_string(cube)]
    return a

# driver
def driver_ida_pattern(input):
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
    get_db()
    ida(curr)