import os
import numpy as np

def split_parsec_isochrones(input_file):
    """
    Splits a PARSEC isochrone file into separate files based on age.
    
    Args:
        input_file (str): Path to the downloaded isochrone file.
    
    Outputs:
        Creates separate files for each age in the 'isochrones_by_age' directory.
    """
    
    output_folder = "isochrones_by_age"
    os.makedirs(output_folder, exist_ok=True)
    
    with open(input_file, "r") as file:
        lines = file.readlines()
    
    current_age = None
    current_lines = []
    ##
    selected_col_indices = []
    header_processed = False
    ##


    for i, line in enumerate(lines):
        if line.startswith("#") and "logAge" in line:  # Detect age header
            if current_age and current_lines:  # Save previous age block
                output_file = os.path.join(output_folder, f"isochrone_logAge_{float(current_age):.4f}_AV_{float(current_av):.2f}.dat")
                with open(output_file, "w") as out:
                    out.write("# logAge Mass LogL LogTe mbolmag Gmag G_Bpmag G_RPmag\n")
                    out.writelines(current_lines[1:])
            

            # Extract age value from the next non-comment line
            j = i + 1
            while j < len(lines) and lines[j].startswith("#"):  
                j += 1  # Skip additional comment lines
            
            if j < len(lines):  # Ensure we're within bounds
                current_age = lines[j].split()[2]  # Age value is the second column
            
            current_lines = [line]  # Reset block with new header
            ##
            header_processed = False  # Reset header flag
            ##
        
        #else:
        #    current_lines.append(line)  # Add data to the current block
        ####
        elif not header_processed and not line.startswith("#"):
            # Process header (column names)
            columns = line.strip().split()
            # Select desired columns (adjusting for 0-based index)
            # Columns 2, 5, 6, 7, 8, 27, 28, 29, 30 → indices: 1, 4, 5, 6, 7, 26, 27, 28, 29
            selected_col_indices = [2, 5, 6, 7, 27, 28, 29, 30]
            
            # Build new header line
            selected_header = " ".join([columns[idx] for idx in selected_col_indices]) + "\n"
            current_lines.append(selected_header)
            header_processed = True
        
        elif header_processed:
            # Process data lines: select only desired columns
            parts = line.strip().split()
            if len(parts) >= max(selected_col_indices) + 1:  # Ensure enough columns
                selected_parts = [parts[idx] for idx in selected_col_indices]
                current_lines.append(" ".join(selected_parts) + "\n")
        ####
    
    # Save the last age block
    if current_age and current_lines:
        output_file = os.path.join(output_folder, f"isochrone_logAge_{float(current_age):.4f}_AV_{float(current_av):.2f}.dat")
        with open(output_file, "w") as out:
            out.write("# logAge Mass LogL LogTe mbolmag Gmag G_Bpmag G_RPmag\n")
            out.writelines(current_lines[1:])
    
    print(f"Isochrones split and saved in '{output_folder}' folder.")

# Run the function (update filename if necessary)
current_av = 3.00
split_parsec_isochrones(f"Iso_250.5_450_{current_av:.2f}Av.dat.txt")
