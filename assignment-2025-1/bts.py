from common import balanced_ternary_to_binary, binary_to_index, binary_to_decimal, generate_total_binaries

def identify_blocks(s):
    blocks = []
    i = len(s) - 1
    processed_indices = set()
    
    while i >= 0:
        if i in processed_indices:
            i -= 1
            continue
            
        if s[i] == '0':
            if i < len(s) - 1:
                r_start = i + 1
                r_end = r_start
                while r_end < len(s) and s[r_end] == '-':
                    processed_indices.add(r_end)
                    r_end += 1
                if r_end > r_start:
                    r_end -= 1
                    blocks.append(('R', r_start, r_end, r_end - r_start + 1))
            
            j = i - 1
            while j >= 0 and s[j] != '+':
                j -= 1
            if j >= 0:
                l_start = j
                l_end = l_start
                k = l_start + 1
                while k < i and s[k] == '-':
                    l_end = k
                    k += 1
                blocks.append(('L', l_start, l_end, l_end - l_start + 1))
                for idx in range(l_start, l_end + 1):
                    processed_indices.add(idx)
            processed_indices.add(i)
        i -= 1
    
    unique_blocks = []
    seen = set()
    for block in blocks:
        if block not in seen:
            seen.add(block)
            unique_blocks.append(block)
    unique_blocks.sort(key=lambda x: x[2], reverse=True)
    
    return unique_blocks

def process_blocks(s):
    blocks = identify_blocks(s)
    if not blocks:
        return s
    block = blocks[0]
    block_type, start_idx, end_idx, length = block
    s_list = list(s)
    replacement_end_idx = 0
    if block_type == 'R':
        zero_idx = start_idx - 1 
        replacement = ['-'] + ['+'] * (length - 1) + ['0']
        s_list[zero_idx:end_idx+1] = replacement
        replacement_end_idx = zero_idx + len(replacement) - 1
    elif block_type == 'L':
        zero_idx = end_idx + 1
        replacement = ['0'] + ['+'] * length
        s_list[start_idx:zero_idx+1] = replacement
        replacement_end_idx = start_idx + len(replacement) - 1
    for i in range(replacement_end_idx + 1, len(s_list)):
        if s_list[i] in ['+', '-']:
            s_list[i] = '+' if s_list[i] == '-' else '-'
            break
    return ''.join(s_list)

def find_starting_ternary_nodes(s, t):
    result = []
    num_strings = 2**(s-1)
    for j in range(num_strings):
        sigma_j = '0' * t + '-'
        bin_rep = bin(j)[2:]
        tau_j = ''
        tau_length = s - 1
        for i in range(tau_length):
            bin_index = len(bin_rep) - 1 - i
            if bin_index >= 0:
                if bin_rep[bin_index] == '0':
                    tau_j += '+'
                else:
                    tau_j += '-'
            else:
                if len(bin_rep) > 0:
                    if bin_rep[0] == '0':
                        tau_j += '+'
                    else:
                        tau_j += '-'
                else:
                    tau_j += '+'
        sigma_j += tau_j
        result.append(sigma_j)
    return result

def generate_graph(s, t):
    starting_nodes = find_starting_ternary_nodes(s, t)
    total_binaries = generate_total_binaries(s, t)
    graph_length = len(total_binaries)
    all_paths = []
    for node in starting_nodes:
        path = [node]
        current_node = node
        for _ in range(graph_length - 1):
            next_node = process_blocks(current_node)
            path.append(next_node)
            current_node = next_node
        all_paths.append(path)
        print( node)
        print(path)
        binary_path = [balanced_ternary_to_binary(node) for node in path]
        print(binary_path)
        index_rep_path = [binary_to_index(binary) for binary in binary_path]
        print(index_rep_path)
        decimal_rep_path = [binary_to_decimal(binary) for binary in binary_path]
        print(decimal_rep_path)
    return all_paths

def run_bts(s, t):
    all_paths = generate_graph(s, t)
    return all_paths
