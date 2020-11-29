import time
from PatternsDB import *
from IDA_1 import *
from IDA_2 import *
from IDFS import *

input='input1.txt'

print('IDFS Algorithm\n')
start = time.time()
driver_idfs(input)
end = time.time()
print("Time taken(sec):", end - start)

print('\nIDA* with maximum of the sum of manhattan distance of cube corners and of edges as heuristics\n')
start = time.time()
driver_ida(input)
end = time.time()
print("Time taken(sec):", end - start)

print('\nIDA* which uses depth of corners configuration of cube as heuristic\n')
print('Creating DB for patterns..')
creat_db()
print('\n DB created..\nRunning algo..')
start = time.time()
driver_ida_pattern(input)
end = time.time()
print("Time taken(sec):", end - start)
