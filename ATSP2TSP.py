def atsp_to_tsp(input_file, output_file):
    """    
    Args:
        input_file: Inupt file path (.atsp file)
        output_file: Ouput file path (.tsp file)
    """
    
    # Read .atsp file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Header
    header = {}
    matrix_start_idx = 0
    
    for idx, line in enumerate(lines):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            header[key.strip()] = value.strip()
        elif line == 'EDGE_WEIGHT_SECTION':
            matrix_start_idx = idx + 1
            break
    
    n = int(header.get('DIMENSION', 0))
    
    # Distence matrix
    matrix_lines = []
    for i in range(matrix_start_idx, len(lines)):
        line = lines[i].strip()
        if line == 'EOF' or line == '':
            break
        matrix_lines.append(line)
    
    atsp_matrix = []
    all_values = ' '.join(matrix_lines).split()
    
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(all_values[i * n + j]))
        atsp_matrix.append(row)
    
    # finx max value for calculating u_ij (R. JONKER and T. VOLGENANT article)
    max_val = max(max(row) for row in atsp_matrix)
    
    # new ditence matrix (2*n x 2*n)
    new_n = 2 * n
    tsp_matrix = [[max_val for _ in range(new_n)] for _ in range(new_n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                tsp_matrix[i][n + j] = 0
            else:
                tsp_matrix[i][n + j] = atsp_matrix[i][j]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                tsp_matrix[n + i][j] = 0
            else:
                tsp_matrix[n + i][j] = atsp_matrix[j][i]
    
    # Write new (.tsp) file
    with open(output_file, 'w') as f:
        f.write(f"NAME: {header.get('NAME', 'converted')}\n")
        f.write(f"TYPE: TSP\n")
        f.write(f"COMMENT: Converted from ATSP\n")
        f.write(f"DIMENSION: {new_n}\n")
        f.write(f"EDGE_WEIGHT_TYPE: EXPLICIT\n")
        f.write(f"EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        f.write(f"EDGE_WEIGHT_SECTION\n")
        
        for i in range(new_n):
            row_str = ' '.join(f"{val:5d}" for val in tsp_matrix[i])
            f.write(f"{row_str}\n")
        
        # Important : FIXED_EDGES_SECTION
        f.write("FIXED_EDGES_SECTION\n")
        for i in range(1, n + 1):
            f.write(f"{i} {i + n}\n")
        f.write("-1\n")
        
        f.write("EOF\n")
    
    print(f"Conversion complete")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        # Utilisation par défaut
        input_file = "/home/tarek-ubuntu/Tarek/Doctorat/Lin-Kernighan/LKH-2.0.10/instances/kro124/kro124.atsp"
        output_file = "/home/tarek-ubuntu/Tarek/Doctorat/Lin-Kernighan/LKH-2.0.10/instances/kro124/kro124.tsp"
    
    try:
        atsp_to_tsp(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: File {input_file} wasn't fine.")
    except Exception as e:
        print(f"Error in conversion: {e}")