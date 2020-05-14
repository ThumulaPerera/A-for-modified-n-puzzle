from csv import DictWriter
import os

from SolveModifiedNPuzzle import solve

### field names in results file ###

result_fields = ['puzzle_size',
            'iters_with_nmp',
            'iters_with_mhd', 
            'iter_diff', 
            'moves_with_nmp',
            'moves_with_mhd',              
            'move_diff']

### helpers ###

def append_dict_as_row(file_name, dict_of_elem, field_names):
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        if not file_exists:
            dict_writer.writeheader()  
        dict_writer.writerow(dict_of_elem)


### main ###

folder_name = 'RandomPuzzles30_1/'

results_file = folder_name + 'Results.txt'
no_of_puzzles_of_same_size = 10

file_exists = os.path.isfile(results_file)
if file_exists:
    os.remove(results_file)

for n in range(5, 21):
    for j in range(1, no_of_puzzles_of_same_size + 1):
        iterations_tracker = []
        no_of_moves_tracker = []
        for k in range(2):
            heuristic = str(k)

            start_config_file = folder_name + 'RandStart_' + str(n) + '_' + str(j) + '.txt'
            goal_config_file = folder_name + 'RandGoal_' + str(n) + '_' + str(j) + '.txt'
            output_file = folder_name + 'OP_' + str(n) + '_' + str(j) + '_' + str(k) + '.txt'

            solved, no_of_moves, iterations, tot_time = solve(
                start_config_file,
                goal_config_file,
                output_file,
                heuristic
            )

            iterations_tracker.append(iterations)
            no_of_moves_tracker.append(no_of_moves)

            print(str(n) + ',' + str(j) + ',' + str(k))    
            print("--- %s seconds ---" % (tot_time))  
        
        result = {
            'puzzle_size': n,
            'iters_with_nmp': iterations_tracker[0],
            'iters_with_mhd': iterations_tracker[1], 
            'iter_diff': iterations_tracker[0] - iterations_tracker[1], 
            'moves_with_nmp': no_of_moves_tracker[0],
            'moves_with_mhd': no_of_moves_tracker[1],              
            'move_diff': no_of_moves_tracker[0] - no_of_moves_tracker[1]
        }
        append_dict_as_row(results_file, result, result_fields)

    


    
