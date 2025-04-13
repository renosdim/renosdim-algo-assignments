from common import generate_total_binaries, binary_to_decimal

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

def run_graph(s, t):
    total_binaries = generate_total_binaries(s, t)
    neighbors = find_neighbors(total_binaries)
    
    for binary, neighbors_list in neighbors.items():
        decimal_bin = binary_to_decimal(binary)
        decimal_neighbors = [binary_to_decimal(n) for n in neighbors_list]
        print(f"{decimal_bin} -> {decimal_neighbors}")
    
    return neighbors