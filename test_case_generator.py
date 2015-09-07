import string
import numpy

def fs_generator(node_num=10, min_solution_path=3, max_solution_step=5, percentage=20, start_time=0, return_type=0):

    solution_array = numpy.array([])
    source = numpy.random.randint(node_num)
    tmp_array = numpy.delete(numpy.arange(node_num), source)
    solution_array = []
    for i in range(min_solution_path):
        numpy.random.shuffle(tmp_array)
        tmp_solution_list = tmp_array.tolist()[0:max_solution_step]
        tmp_solution_list.insert(0, source)
        solution_array.append(tmp_solution_list)
    solution_array = numpy.array(solution_array)

    whole_map = numpy.random.randint(100, size=(node_num, node_num))
    whole_map = (whole_map < percentage) * numpy.logical_not(numpy.eye(node_num, node_num))

    solution_paths = []
    for solution in solution_array:
        solution_paths += [(solution[i], solution[i+1]) for i in range(len(solution) - 1)]

    for solution_path in solution_paths:
        whole_map[solution_path] = True

    cost_map = numpy.ones((node_num, node_num))
    time_map = [numpy.ones((node_num, node_num)) for x in range(24)]


    if return_type is 0:
        return [source, solution_array[:,-1], whole_map, start_time, cost_map, time_map]
    else:
        return [source, solution_array[:,-1], whole_map, start_time, solution_array]

def ucs_generator(node_num=10, min_solution_path=3, max_solution_step=5, percentage=20, max_path_cost=10, start_time=0):
    [source, dests, whole_map, start_time, solution_array] = fs_generator(node_num=node_num,
            min_solution_path=min_solution_path, max_solution_step=max_solution_step, percentage=percentage,
            start_time=start_time, return_type=1)

    cost_map = (numpy.random.randint(max_path_cost, size=(node_num, node_num)) + 1) * whole_map
    time_map = [numpy.random.randint(2, size=(node_num, node_num)) for x in range(node_num)]

    for solution in solution_array:
        solution_paths = [(solution[x], solution[x+1]) for x in range(len(solution) - 1)]
        available_time = (start_time % node_num)
        for path in solution_paths:
            for i in range(cost_map[path[0], path[1]]):
                print(node_num)
                print(available_time)
                print(path[0])
                print(path[1])
                print("===-=-=")
                time_map[available_time][path[0], path[1]] = 1
                available_time = ((available_time + 1) % node_num)

    return [source, dests, whole_map, start_time, cost_map, time_map]

def output_map(map_set, vocabulary, output_file):
    output_file.write(map_set[-1] + "\n")
    output_file.write(vocabulary[map_set[0]] + "\n")

    dests = list(set(map_set[1]))
    for dest in dests:
        output_file.write(vocabulary[dest])
        if dest != dests[-1]:
            output_file.write(" ")
    output_file.write("\n")

    nodes_num = numpy.size(map_set[2], 0)
    middles = [x for x in range(nodes_num) if x not in ([map_set[0]] + map_set[1].tolist())]

    for middle in middles:
        output_file.write(vocabulary[middle])
        if middle != middles[-1]:
            output_file.write(" ")
    output_file.write("\n")

    output_file.write(str(numpy.sum(map_set[2])))

    output_file.write("\n")
    for i in range(nodes_num):
        for j in range(nodes_num):
            if map_set[2][i,j] == True:
                output_file.write(vocabulary[i] + " " + \
                        vocabulary[j] + " " + str(int(map_set[4][i,j])) + " ")
                time_range = [numpy.logical_not(x[i,j]) for x in map_set[5]]
                time_range = [x for x in range(len(time_range)) if time_range[x] == True]
                time_range = [(time_range[x], time_range[x+1]) for x in range(len(time_range) - 1)]
                tr_string = []
                if time_range:
                    begin = -1
                    for time_split in time_range:
                        if(time_split[1] - time_split[0]) != 1 or time_split is time_range[-1]:
                            end = time_split[0]
                            if begin == -1:
                                tr_string.append(str(end) + "-" + str(end))
                            else:
                                tr_string.append(str(begin) + "-" + str(end))
                                begin = -1
                            if(time_split[1] - time_split[0]) != 1 and time_split is time_range[-1]:
                                tr_string.append(str(time_split[1]) + "-" + str(time_split[1]))
                        else:
                            if(begin == -1):
                                begin = time_split[0]
                                end = time_split[1]
                            else:
                                end = time_split[1]
                output_file.write(str(int(len(tr_string))))
                for tr_str in tr_string:
                    output_file.write(" " + tr_str)
                output_file.write("\n")
    output_file.write(str(map_set[3]) + "\n")


if __name__ == "__main__":
    test_case_number = 1000
    char_array = numpy.array([])
    case_types = ["DFS", "BFS", "UCS"]
    for c in string.uppercase:
        char_array = numpy.append(char_array, [c])

    with open("./generatedInput.txt", "w") as f:
        f.write(str(test_case_number) + "\n")
        for i in range(test_case_number):
            print(i + 1)
            node_num = numpy.random.randint(16) + 10
            min_solution_path = numpy.random.randint(2) + 2
            max_solution_step = numpy.random.randint(4) + 3
            percentage = numpy.random.randint(25)
            max_path_cost = numpy.random.randint(10) + 5
            case_type = case_types[numpy.random.randint(3)]
            start_time = numpy.random.randint(40)
            if case_type == "DFS":
                map_set = fs_generator(node_num = node_num, max_solution_step=max_solution_step,
                        min_solution_path=min_solution_path, percentage=percentage, start_time=start_time)
            elif case_type == "BFS":
                map_set = fs_generator(node_num = node_num, max_solution_step=max_solution_step,
                        min_solution_path=min_solution_path, percentage=percentage, start_time=start_time)
            else:
                map_set = ucs_generator(node_num = node_num, max_solution_step=max_solution_step,
                        min_solution_path=min_solution_path, percentage=percentage,
                        max_path_cost=max_path_cost, start_time=start_time)
            map_set.append(case_type)
            output_map(map_set, char_array, f)

            f.write("\n")
    pass
