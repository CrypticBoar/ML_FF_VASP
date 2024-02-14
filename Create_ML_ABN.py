def parse_positions_forces(outcar_content):
    start = False
    positions_forces = []
    for line in outcar_content:
        if "POSITION" in line and "TOTAL-FORCE" in line:
            start = True
            continue
        if start and "------" in line:
            continue
        if start and line.strip() == "":
            break
        if start:
            positions_forces.append(line.strip().split())
    return positions_forces

def parse_stress(outcar_content):
    for line in reversed(outcar_content):
        if "in kB" in line:
            _, xx, yy, zz, xy, yz, zx = line.strip().split()
            stress = [xx, yy, zz, xy, yz, zx]
            return stress
    return []

def read_outcar(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
    positions_forces = parse_positions_forces(content)
    stress = parse_stress(content)
    return positions_forces, stress

def write_mlabn(filename, configurations):
    with open(filename, 'w') as f:
        # Write header and metadata
        f.write("1.0 Version\n")
        f.write("**************************************************\n")
        f.write("     The number of configurations\n")
        f.write("--------------------------------------------------\n")
        f.write(f"          {len(configurations)}\n")
        f.write("**************************************************\n")
        f.write("     The maximum number of atom type\n")
        f.write("--------------------------------------------------\n")
        f.write("       4\n")  # Example for 4 atom types: Li, F, Ca, O
        f.write("**************************************************\n")
        f.write("     The atom types in the data file\n")
        f.write("--------------------------------------------------\n")
        f.write("     Li F  Ca O\n")  # Adjust based on your specific atom types
        f.write("**************************************************\n")
        # Add other headers like atomic mass, reference atomic energy here
        
        # Write configurations
        for i, (positions_forces, stress) in enumerate(configurations, start=1):
            f.write(f"     Configuration num.      {i}\n")
            f.write("==================================================\n")
            # System name, number of atom types, etc., can be added here
            f.write("     Atom types and atom numbers\n")
            f.write("--------------------------------------------------\n")
            # Example atom types and numbers
            f.write("     Li      8\n")
            f.write("     F       8\n")
            # Similarly add for Ca, O if needed
            f.write("==================================================\n")
            f.write("     Atomic positions (ang.)\n")
            f.write("--------------------------------------------------\n")
            for pos_force in positions_forces:
                f.write(f"   {'   '.join(pos_force[:3])}\n")
            f.write("==================================================\n")
            f.write("     Forces (eV ang.^-1)\n")
            f.write("--------------------------------------------------\n")
            for pos_force in positions_forces:
                f.write(f"  {'   '.join(pos_force[3:])}\n")
            f.write("**************************************************\n")
            f.write("     Stress (kbar)\n")
            f.write("--------------------------------------------------\n")
            f.write(f"     {'   '.join(stress[:3])}\n")
            f.write("--------------------------------------------------\n")
            f.write(f"     {'   '.join(stress[3:])}\n")
            f.write("**************************************************\n")

def main():
    outcar_files = ['OUTCAR1', 'OUTCAR2']  # Add your OUTCAR file names here
    configurations = [read_outcar(file) for file in outcar_files]
    
    write_mlabn('ML_ABN', configurations)

if __name__ == "__main__":
    main()
