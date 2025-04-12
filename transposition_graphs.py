import argparse
import sys

def binary_to_index(binary_str):
    indices = []
    reversed_str = binary_str[::-1]

    for i, bit in enumerate(reversed_str):
        if bit == '1':
            indices.append(str(i))

    return ''.join(sorted(indices, reverse=True))

def decimal_to_binary(decimal, length):
    binary = bin(decimal)[2:]
    return binary.zfill(length)

def generate_total_binaries(s, t):
    result = []

    def backtrack(current, zeros_left, ones_left):
        if zeros_left == 0 and ones_left == 0:
            result.append(''.join(current))
            return

        if zeros_left > 0:
            current.append('0')
            backtrack(current, zeros_left - 1, ones_left)
            current.pop()

        if ones_left > 0:
            current.append('1')
            backtrack(current, zeros_left, ones_left - 1)
            current.pop()

    backtrack([], s, t)
    return result

def binary_to_decimal(binary_str):
    return int(binary_str, 2)

def find_neighbors(binary_list):
    neighbors_dict = {}

    def is_one_transposition(bin1, bin2):
        diff_indices = []
        for i in range(len(bin1)):
            if bin1[i] != bin2[i]:
                diff_indices.append(i)
        if len(diff_indices) == 2:
            i, j = diff_indices
            return bin1[i] == bin2[j] and bin1[j] == bin2[i]
        return False

    for bin1 in binary_list:
        neighbors_dict[bin1] = []
        for bin2 in binary_list:
            if bin1 != bin2 and is_one_transposition(bin1, bin2):
                neighbors_dict[bin1].append(bin2)

    return neighbors_dict

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

def index_to_decimal(index_str, s, t):
    """Convert an index string to its decimal representation"""
    total_length = s + t
    binary = ['0'] * total_length
    
    for position in index_str:
        pos = int(position)
        binary[total_length - 1 - pos] = '1'
        
    return int(''.join(binary), 2)

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
    
    # Check if path was found and if the start index is smaller than the last index when expressed as decimals
    if result and path:
        start_decimal = index_to_decimal(start_index, s, t)
        last_decimal = index_to_decimal(path[-1], s, t)
        
        if start_decimal < last_decimal:
            return None  # Don't return a path if start element is smaller than last element
        
    return path if result else None

def binary_path_to_decimal(binary_path):
    return [binary_to_decimal(binary) for binary in binary_path]

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

def main():
    parser = argparse.ArgumentParser(description="Process binary strings with optional modes.")
    parser.add_argument("s", type=int, help="Number of zeros")
    parser.add_argument("t", type=int, help="Number of ones")
    parser.add_argument("mode", choices=["graph", "bts", "dfs"], help="Mode of operation")
    parser.add_argument("start", nargs="?", type=int, help="Starting node for DFS (decimal)")

    args = parser.parse_args()

    total_binaries = generate_total_binaries(args.s, args.t)
    neighbors = find_neighbors(total_binaries)

    if args.mode == "graph":
        for binary, neighbors_list in neighbors.items():
            decimal_bin = binary_to_decimal(binary)
            decimal_neighbors = [binary_to_decimal(n) for n in neighbors_list]
            print(f"{decimal_bin} -> {decimal_neighbors}")

    elif args.mode == "dfs":
        neighbors_index = convert_to_index_representation(neighbors)

        if args.start is not None:
            start_binary = decimal_to_binary(args.start, args.s + args.t)
            start_index = binary_to_index(start_binary)
            path_index = dfs_homogeneous_genlex(neighbors_index, start_index, args.s, args.t)
            
            if path_index is not None:
                path_binary = index_path_to_binary(path_index, args.s, args.t)
                path_decimal = [binary_to_decimal(binary) for binary in path_binary]

                print(f"{path_binary}")
                print(f"{path_index}")
                print(f"{path_decimal}")
        else:
             for start_index in neighbors_index.keys():
                path_index = dfs_homogeneous_genlex(neighbors_index, start_index, args.s, args.t)
                
                if path_index is not None:
                    path_binary = index_path_to_binary(path_index, args.s, args.t)
                    path_decimal = [binary_to_decimal(binary) for binary in path_binary]

                    print(f"{path_binary}")
                    print(f"{path_index}")
                    print(f"{path_decimal}")

if __name__ == "__main__":
    main()
