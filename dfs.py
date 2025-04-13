from common import generate_total_binaries, binary_to_decimal, decimal_to_binary, binary_to_index
from graph import find_neighbors

def convert_to_index_representation(neighbors_dict):

    index_dict = {}
    for binary, neighbors in neighbors_dict.items():
        index_key = binary_to_index(binary)
        index_values = [binary_to_index(neighbor) for neighbor in neighbors]
        index_dict[index_key] = index_values
    
    return index_dict

def are_homogenous(a, b):
 
    a_str = str(a)
    b_str = str(b)

    diff_count = 0
    for digit_a, digit_b in zip(a_str, b_str):
        if digit_a != digit_b:
            diff_count += 1
            if diff_count > 1:
                return False

    return diff_count == 1

def common_prefix_length(a, b):

    min_len = min(len(a), len(b))
    count = 0
    for i in range(min_len):
        if a[i] == b[i]:
            count += 1
        else:
            break
    return count

def sort_neighbors_by_genlex(current, neighbors):

    last_node = current[-1]
    return sorted(
        neighbors,
        key=lambda x: (-common_prefix_length(last_node, x), x)
    )

def index_path_to_binary(index_path, s, t):

    binary_path = []
    total_length = s + t

    for index_str in index_path:
        binary = ['0'] * total_length
        for position in index_str:
            pos = int(position)
            binary[total_length - 1 - pos] = '1'
        binary_path.append(''.join(binary))
    
    return binary_path

def dfs_homogeneous_genlex(neighbors_index_dict, start_index, s, t):

    path = [start_index]
    visited = set([start_index])

    def backtrack():
        if len(visited) == len(neighbors_index_dict):
            return True

        current = path[-1]
        neighbors = neighbors_index_dict[current]

        sorted_neighbors = sort_neighbors_by_genlex(path, neighbors)

        for neighbor in sorted_neighbors:
            if neighbor not in visited and are_homogenous(current, neighbor):
                path.append(neighbor)
                visited.add(neighbor)

                if backtrack():
                    return True

                path.pop()
                visited.remove(neighbor)

        return False

    result = backtrack()
    
    if result and path:
        from common import index_to_decimal
        start_decimal = index_to_decimal(start_index, s, t)
        last_decimal = index_to_decimal(path[-1], s, t)
        
        if start_decimal < last_decimal:
            return None
        
    return path if result else None

def run_dfs(s, t, start=None):
    
    total_binaries = generate_total_binaries(s, t)
    neighbors = find_neighbors(total_binaries)
    neighbors_index = convert_to_index_representation(neighbors)
    
    paths_found = 0
    
    if start is not None:
        start_binary = decimal_to_binary(start)
        start_index = binary_to_index(start_binary)
        path_index = dfs_homogeneous_genlex(neighbors_index, start_index, s, t)
        
        if path_index is not None:
            paths_found += 1
            path_binary = index_path_to_binary(path_index, s, t)
            path_decimal = [binary_to_decimal(binary) for binary in path_binary]

            print(path_binary)
            print(path_index)
            print(path_decimal)
    else:
        for start_index in neighbors_index.keys():
            path_index = dfs_homogeneous_genlex(neighbors_index, start_index, s, t)
            
            if path_index is not None:
                paths_found += 1
                path_binary = index_path_to_binary(path_index, s, t)
                path_decimal = [binary_to_decimal(binary) for binary in path_binary]

                print(path_binary)
                print(path_index)
                print(path_decimal)
    
    return neighbors_index