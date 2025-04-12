import argparse

def binary_to_index(binary_str):
    indices = []
    reversed_str = binary_str[::-1]

    for i, bit in enumerate(reversed_str):
        if bit == '1':
            indices.append(str(i))

    return ''.join(sorted(indices, reverse=True))

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

def main():
    parser = argparse.ArgumentParser(description="Convert binary string to ace index representation.")
    parser.add_argument("s", type=int, help="Number of zeros")
    parser.add_argument("t", type=int, help="Number of ones")
    args = parser.parse_args()

    total_binaries = generate_total_binaries(args.s, args.t)
    neighbors = find_neighbors(total_binaries)

    print("Generated Binaries:")
    for binary in total_binaries:
        print(binary)
    
    print("\nNeighbors:")
    for binary, neighbors_list in neighbors.items():
        print(f"{binary}: {neighbors_list}")

if __name__ == "__main__":
    main()
