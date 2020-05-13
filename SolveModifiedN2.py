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
    def __init__(self, config, g, parent = None, move = None):
        self.config = config
        self.parent = parent
        self.move = move
        self.g = g
        self.calc_h_misplaced_tiles()
        # self.calc_h_manhatton_distance()
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
        return Node(shuffled_config, self.g + 1, self, Move(tile_number,move_direction))

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

def print_moves(node):
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

# start_config_file = input('Enter start configuration file name : ')
# goal_config_file = input('Enter goal configuration file name : ')
# start_config_file = 'Sample_Start_Configuration.txt'
# goal_config_file = 'Sample_Goal_Configuration.txt'
start_config_file = 'SS.txt'
goal_config_file = 'SG.txt'
output_file = 'Output4.txt'

start_time = time.time()

with open(start_config_file) as f:
    reader = csv.reader(f, delimiter="\t")
    start_config = list(reader)

with open(goal_config_file) as f:
    reader = csv.reader(f, delimiter="\t")
    goal_config = list(reader)

side_len = len(start_config)

start_node = Node(start_config, 0)
print(arr_to_tuple(start_node.config))

open_buffer = {}
closed_buffer = {}

open_buffer[arr_to_tuple(start_node.config)] = start_node

while open_buffer:
    node_n = None
    for key in open_buffer.keys():
        if node_n == None:
            node_n = open_buffer[key]
        else:
            if open_buffer[key].f < node_n.f:
                node_n = open_buffer[key]

    del open_buffer[arr_to_tuple(node_n.config)]
    closed_buffer[arr_to_tuple(node_n.config)] = node_n
    if (node_n.config == goal_config):
        print('done')
        print(node_n.f)
        # print_parents(node_n)
        print_moves(node_n)
        break
    for successor_node in node_n.get_successor_nodes():
        successor_key = arr_to_tuple(successor_node.config)
        if(not(successor_key in open_buffer or successor_key in closed_buffer)):
            open_buffer[successor_key] = successor_node
        if(successor_key in open_buffer):
            if(open_buffer[successor_key].g > successor_node.g):
                open_buffer[successor_key] = successor_node
        if(successor_key in closed_buffer):
            if(closed_buffer[successor_key].g > successor_node.g):
                open_buffer[successor_key] = successor_node
                del closed_buffer[successor_key]



        # in_open_union_close = False
        # better_node_exists = False
        # for node_m in open_buffer:
        #     if node_m.config == successor_node.config:
        #         in_open_union_close = True
        #         if node_m.g <= (node_n.g + 1):
        #             better_node_exists = True
        #             break
        # if not better_node_exists:
        #     heapq.heappush(open_buffer, successor_node)
        # for node_m in closed_buffer:
        #     if node_m.config == successor_node.config:
        #         in_open_union_close = True
        #         already_appended = False
        #         if node_m.g > (node_n.g + 1):
        #             closed_buffer.pop(closed_buffer.index(node_m))
        #             if not already_appended:
        #                 heapq.heappush(open_buffer, successor_node)
        #                 already_appended = True
        #         break
        # if not in_open_union_close:
        #     heapq.heappush(open_buffer, successor_node)

print('terminated')
print("--- %s seconds ---" % (time.time() - start_time))

    


    