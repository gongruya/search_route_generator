import string
import numpy

def generator(node_num=10, min_solution_path=3, max_solution_step=5, percentage=20):

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
    whole_map = whole_map < percentage

    solution_paths = []
    for solution in solution_array:
        solution_paths += [(solution[i], solution[i+1]) for i in range(len(solution) - 1)]

    for solution_path in solution_paths:
        whole_map[solution_path] = True

    return [source, solution_array[:,-1], whole_map]

def output_map(map_set, vocabulary, output_file):
    output_file.write("BFS\n")
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
                        vocabulary[j] + " " + str(1) + " " + str(0) + "\n")
    output_file.write(str(0) + "\n")


if __name__ == "__main__":
    test_case_number = 1000
    char_array = numpy.array([])
    for c in string.uppercase:
        char_array = numpy.append(char_array, [c])

    with open("./generatedInput.txt", "w") as f:
        f.write(str(test_case_number) + "\n")
        for i in range(test_case_number):
            print(i + 1)
            map_set = generator(node_num = 20, max_solution_step=10, percentage = 0)
            output_map(map_set, char_array, f)
            f.write("\n")
    pass
