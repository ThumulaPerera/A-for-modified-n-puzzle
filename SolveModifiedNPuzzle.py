import math
import copy
import csv
import time
import heapq

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Move:
    def __init__(self, tile, direction):
        self.tile = tile
        self.direction = direction

class Node:
    def __init__(self, config, g, heuristic = '1', parent = None, move = None):
        self.config = config
        self.parent = parent
        self.move = move
        self.g = g
        self.heuristic = heuristic
        if heuristic == '0':
            self.calc_h_misplaced_tiles()
        else:
            self.calc_h_manhatton_distance()
        self.f = self.g + self.h
        self.get_blank_positions()
        self.successor_nodes = None

    # comparison function for heap sort
    def __lt__(self, other):
        return self.f < other.f

    def calc_h_misplaced_tiles(self):
        if self.config == goal_config:
            self.h = 0
        else:
            h = 0
            for i in range(side_len):
                for j in range(side_len):
                    if (
                        self.config[i][j] != goal_config[i][j] and
                        self.config[i][j] != '-'
                        ):
                        h += 1
            self.h = h
    
    def get_goal_position(self, number):
        for i in range(side_len):
            for j in range(side_len):
                if goal_config[i][j] == number:
                    return i, j

    def calc_h_manhatton_distance(self):
        if self.config == goal_config:
            self.h = 0
        else:
            h = 0
            for i in range(side_len):
                for j in range(side_len):
                    if self.config[i][j] == '-':
                        continue
                    goal_i, goal_j = self.get_goal_position(self.config[i][j])
                    h += abs(i - goal_i) + abs(j - goal_j)
            self.h = h

    def get_blank_positions(self):
        blank_positions = []
        for i in range(side_len):
            for j in range(side_len):
                if self.config[i][j] == '-':
                    blank_positions.append(Coordinate(i,j))
        self.blank_positions = blank_positions

    def get_successor_node(self, cur_x, cur_y, new_x, new_y, move_direction):
        shuffled_config = copy.deepcopy(self.config)
        tile_number = shuffled_config[new_x][new_y]
        shuffled_config[cur_x][cur_y] = shuffled_config[new_x][new_y]
        shuffled_config[new_x][new_y] = '-'
        return Node(shuffled_config, self.g + 1, self.heuristic, self, Move(tile_number,move_direction))

    def get_successor_nodes(self):
        if self.successor_nodes == None:
            self.set_successor_nodes()
        return self.successor_nodes

    def set_successor_nodes(self):
        successor_nodes = []
        for position in self.blank_positions:
            # move blank up
            if position.x > 0 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x - 1, 
                        position.y,
                        'down'
                    )
                )
            # move blank down
            if position.x < side_len - 1 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x + 1, 
                        position.y,
                        'up'
                    )
                )
            # # move blank left
            if position.y > 0 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x, 
                        position.y - 1,
                        'right'
                    )
                )
            # move blank right
            if position.y < side_len - 1 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x, 
                        position.y + 1,
                        'left'
                    )
                )
        self.successor_nodes = successor_nodes


def print_parents(node):
    current_node = node
    while current_node != None:
        for row in current_node.config:
            print(row)
        print()
        current_node = current_node.parent

def print_moves(node, output_file):
    current_node = node
    moves = []
    while current_node != None and current_node.move != None:
        moves.append(current_node.move)
        current_node = current_node.parent
    moves.reverse()
    with open(output_file, "w") as f:
        for move in moves[:-1]:
            f.write('(' + move.tile + ', ' + move.direction + ')'  + ', ')
        f.write('(' + moves[-1].tile + ', ' + moves[-1].direction + ')')

def arr_to_tuple(arr):
    return tuple(map(tuple, arr))

def solve(start_config_file, goal_config_file, output_file, heuristic):
    start_time = time.time()

    with open(start_config_file) as f:
        reader = csv.reader(f, delimiter="\t")
        global start_config
        start_config = list(reader)

    with open(goal_config_file) as f:
        reader = csv.reader(f, delimiter="\t")
        global goal_config
        goal_config = list(reader)

    global side_len
    side_len = len(start_config)

    start_node = Node(start_config, 0, heuristic)

    open_buffer = {}
    open_buffer_pri_queue = []
    closed_buffer = {}

    open_buffer[arr_to_tuple(start_node.config)] = start_node
    heapq.heappush(open_buffer_pri_queue, start_node)

    iterations = 0
    solved = False
    while open_buffer:
        iterations += 1
        node_n = heapq.heappop(open_buffer_pri_queue)
        del open_buffer[arr_to_tuple(node_n.config)]
        closed_buffer[arr_to_tuple(node_n.config)] = node_n
        if (node_n.config == goal_config):
            solved = True
            print_moves(node_n, output_file)
            break
        for successor_node in node_n.get_successor_nodes():
            successor_key = arr_to_tuple(successor_node.config)
            if(not(successor_key in open_buffer or successor_key in closed_buffer)):
                open_buffer[successor_key] = successor_node
                heapq.heappush(open_buffer_pri_queue, successor_node)
    
            if(successor_key in open_buffer):
                if(open_buffer[successor_key].g > successor_node.g):
                    open_buffer[successor_key].parent = successor_node.parent
                    open_buffer[successor_key].g = successor_node.g
                    open_buffer[successor_key].f = successor_node.f
                    open_buffer[successor_key].move = successor_node.move
                    heapq.heapify(open_buffer_pri_queue)

            if(successor_key in closed_buffer):
                if(closed_buffer[successor_key].g > successor_node.g):
                    open_buffer[successor_key] = successor_node
                    heapq.heappush(open_buffer_pri_queue, successor_node)
                    del closed_buffer[successor_key]

    return solved, node_n.f, iterations, time.time() - start_time

### main ###

output_file = 'Output.txt'

start_config_file = input('Enter start configuration file name : ')
goal_config_file = input('Enter goal configuration file name : ')
heuristic = input('Select the heuristic number \n[0 - no of misplaced tiles] \n[1 - total manhattan distance]\n : ')

print('\ncomputing....\n')
 
if heuristic != '0':
    heuristic = '1'

start_config = []
goal_config = []
side_len = 0

solved, no_of_moves, iterations, tot_time = solve(
    start_config_file,
    goal_config_file,
    output_file,
    heuristic
)

if solved:
    print('solved in ' + str(no_of_moves) + ' moves')
    print('output saved in \'' + output_file + '\'')
else:
    print('unsolvable') 
print('terminated after ' + str(iterations) + ' iterations')
print("--- %s seconds ---" % (tot_time)) 



    
