import os
import glob
import subprocess

def calculate_grid_box(reference_ligand_pdb, padding=5.0):
    """
    Reads a reference ligand PDB file, calculates the geometric center, 
    and determines the minimum box size required to encompass it.
    """
    x_coords, y_coords, z_coords = [], [], []
    
    with open(reference_ligand_pdb, 'r') as f:
        for line in f:
            if line.startswith("HETATM") or line.startswith("ATOM"):
                x_coords.append(float(line[30:38].strip()))
                y_coords.append(float(line[38:46].strip()))
                z_coords.append(float(line[46:54].strip()))
                
    if not x_coords:
        print("Error: No coordinates found in reference ligand file!")
        return None, None

    # Calculate Center
    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    center_z = sum(z_coords) / len(z_coords)
    
    # Calculate Size (Max - Min + Padding on both sides)
    size_x = (max(x_coords) - min(x_coords)) + (padding * 2)
    size_y = (max(y_coords) - min(y_coords)) + (padding * 2)
    size_z = (max(z_coords) - min(z_coords)) + (padding * 2)
    
    center = (round(center_x, 3), round(center_y, 3), round(center_z, 3))
    size = (round(size_x, 3), round(size_y, 3), round(size_z, 3))
    
    return center, size

def create_config_and_run(receptor, ref_ligand, ligands_dir, output_dir="advanced_results"):
    print("--- 1. Automatically Calculating Grid Box ---")
    center, size = calculate_grid_box(ref_ligand, padding=5.0)
    
    if not center:
        return

    print(f"Calculated Center: X={center[0]}, Y={center[1]}, Z={center[2]}")
    print(f"Calculated Size: X={size[0]}, Y={size[1]}, Z={size[2]}\n")

    os.makedirs(output_dir, exist_ok=True)
    
    print("--- 2. Starting High-Throughput Docking ---")
    ligand_files = glob.glob(os.path.join(ligands_dir, "*.pdbqt"))
    
    for lig in ligand_files:
        lig_name = os.path.basename(lig).replace(".pdbqt", "")
        print(f"Docking {lig_name}...")
        
        # Write temporary config for this specific run
        config_text = f"""receptor = {receptor}
ligand = {lig}
center_x = {center[0]}
center_y = {center[1]}
center_z = {center[2]}
size_x = {size[0]}
size_y = {size[1]}
size_z = {size[2]}
exhaustiveness = 16
num_modes = 9
energy_range = 3
seed = 42
"""
        with open("temp_config.txt", "w") as f:
            f.write(config_text)
            
        out_file = os.path.join(output_dir, f"{lig_name}_out.pdbqt")
        log_file = os.path.join(output_dir, f"{lig_name}_log.txt")
        
        # Run Vina
        cmd = f"vina --config temp_config.txt --out {out_file} > {log_file}"
        subprocess.run(cmd, shell=True)
        
    print("\n--- All done! Check the results folder. ---")
    if os.path.exists("temp_config.txt"):
        os.remove("temp_config.txt")

if __name__ == "__main__":
    # USER: Change these variables to point to your prepared files!
    RECEPTOR_FILE = "protein.pdbqt"
    
    # This is the original co-crystallized ligand saved directly from PyMOL as a PDB
    REFERENCE_LIGAND = "original_co_crystallized_ligand.pdb" 
    
    LIGANDS_DIRECTORY = "ligands"
    
    print("WARNING: Make sure your files are prepared and Paths are correct in the script!")
    # create_config_and_run(RECEPTOR_FILE, REFERENCE_LIGAND, LIGANDS_DIRECTORY)
