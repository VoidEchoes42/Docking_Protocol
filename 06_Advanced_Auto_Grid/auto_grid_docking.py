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

    print("Calculated Center: X={}, Y={}, Z={}".format(center[0], center[1], center[2]))
    print("Calculated Size: X={}, Y={}, Z={}\n".format(size[0], size[1], size[2]))

    # Python 2.7 compatible directory creation
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("--- 2. Starting High-Throughput Docking ---")
    ligand_files = glob.glob(os.path.join(ligands_dir, "*.pdbqt"))
    
    for lig in ligand_files:
        lig_name = os.path.basename(lig).replace(".pdbqt", "")
        print("Docking {}...".format(lig_name))
        
        # Write temporary config for this specific run
        config_text = "receptor = {req}\nligand = {lig}\ncenter_x = {cx}\ncenter_y = {cy}\ncenter_z = {cz}\nsize_x = {sx}\nsize_y = {sy}\nsize_z = {sz}\nexhaustiveness = 16\nnum_modes = 9\nenergy_range = 3\nseed = 42\n".format(
            req=receptor, lig=lig, cx=center[0], cy=center[1], cz=center[2], sx=size[0], sy=size[1], sz=size[2]
        )
        
        with open("temp_config.txt", "w") as f:
            f.write(config_text)
            
        out_file = os.path.join(output_dir, "{}_out.pdbqt".format(lig_name))
        log_file = os.path.join(output_dir, "{}_log.txt".format(lig_name))
        
        # Run Vina (Using check_call instead of run for Python 2.7 compatibility)
        cmd = "vina --config temp_config.txt --out {} > {}".format(out_file, log_file)
        subprocess.check_call(cmd, shell=True)
        
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
