import random
import csv
import copy
import os

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, config):
        self.config = config
        self.get_blank_positions()
        self.successor_nodes = None

    def get_blank_positions(self):
        blank_positions = []
        for i in range(n):
            for j in range(n):
                if self.config[i][j] == '-':
                    blank_positions.append(Coordinate(i,j))
        self.blank_positions = blank_positions

    def get_successor_node(self, cur_x, cur_y, new_x, new_y):
        shuffled_config = copy.deepcopy(self.config)
        tile_number = shuffled_config[new_x][new_y]
        shuffled_config[cur_x][cur_y] = shuffled_config[new_x][new_y]
        shuffled_config[new_x][new_y] = '-'
        return Node(shuffled_config)

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
                        position.y
                    )
                )
            # move blank down
            if position.x < n - 1 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x + 1, 
                        position.y
                    )
                )
            # # move blank left
            if position.y > 0 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x, 
                        position.y - 1
                    )
                )
            # move blank right
            if position.y < n - 1 :
                successor_nodes.append(
                    self.get_successor_node(
                        position.x, 
                        position.y, 
                        position.x, 
                        position.y + 1
                    )
                )
        self.successor_nodes = successor_nodes

### main ###

folder_name = 'RandomPuzzles30_1/'
max_moves = 30
no_of_puzzles_of_same_size = 10

if not os.path.exists(folder_name[:-1]):
    os.makedirs(folder_name[:-1])

for n in range(5, 21):
    for j in range(1, no_of_puzzles_of_same_size + 1):
        start_config_file = folder_name + 'RandStart_' + str(n) + '_' + str(j) + '.txt'
        goal_config_file = folder_name + 'RandGoal_' + str(n) + '_' + str(j) + '.txt'

        tiles = list(range(1, n**2 -1))
        tiles.append('-')
        tiles.append('-')

        random.shuffle(tiles)

        start_config = []
        for i in range(0, n**2, n):
            start_config.append(tiles[i:i+n])


        with open(start_config_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerows(start_config)


        current_node = Node(start_config)
        for i in range(max_moves):
            current_node = random.choice(current_node.get_successor_nodes())

        with open(goal_config_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerows(current_node.config)
