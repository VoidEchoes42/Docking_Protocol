import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

RAW_PROTEIN = os.path.join(REPO_ROOT, "protein", "1HSG_raw.pdb")
RECEPTOR_PDBQT = os.path.join(REPO_ROOT, "protein", "1HSG_raw_receptor.pdbqt")

NATIVE_LIGAND_PDB = os.path.join(SCRIPT_DIR, "MK1_native.pdb")
NATIVE_LIGAND_PDBQT = os.path.join(SCRIPT_DIR, "MK1_native.pdbqt")
OUTPUT_PDBQT = os.path.join(SCRIPT_DIR, "MK1_redocked_out.pdbqt")
LOG_FILE = os.path.join(SCRIPT_DIR, "MK1_redocked_log.txt")
TEMP_CONFIG = os.path.join(SCRIPT_DIR, "temp_config.txt")

def find_pythonsh():
    candidates = [os.environ.get("PYTHONSH"),
                  os.path.join(sys.prefix, "bin", "pythonsh"),
                  os.path.join(os.path.dirname(sys.executable), "pythonsh")]
    for c in candidates:
        if c and os.path.exists(c): return c
    for path in os.environ.get("PATH", "").split(os.pathsep):
        cand = os.path.join(path, "pythonsh")
        if os.path.exists(cand): return cand
    return None

def extract_native_ligand():
    print("--- 1. Extracting native ligand (MK1) from raw PDB ---")
    if not os.path.exists(RAW_PROTEIN):
        print("Error: {} not found!".format(RAW_PROTEIN))
        return False
        
    with open(RAW_PROTEIN, 'r') as fin, open(NATIVE_LIGAND_PDB, 'w') as fout:
        for line in fin:
            if line.startswith("HETATM") and "MK1" in line:
                fout.write(line)
    print("Saved as {}\n".format(NATIVE_LIGAND_PDB))
    return True

ADT_LIGAND_HELPER = r'''
import sys
from MolKit import Read
from AutoDockTools.MoleculePreparation import AD4LigandPreparation

infile, outfile = sys.argv[1:3]
mol = Read(infile)[0]
mol.buildBondsByDistance()
LPO = AD4LigandPreparation(
    mol, mode='automatic',
    repairs='bonds_hydrogens',
    charges_to_add='gasteiger',
    cleanup='nphs_lps',
    allowed_bonds='backbone',
    root='auto',
    outputfilename=outfile)
'''

def prepare_ligand():
    print("--- 2. Converting native ligand to PDBQT using AutoDockTools ---")
    pythonsh = find_pythonsh()
    if not pythonsh:
        print("ERROR: 'pythonsh' not found. Please activate mgl_env.")
        return False
        
    helper_path = "_ligand_prep.py"
    with open(helper_path, "w") as fh:
        fh.write(ADT_LIGAND_HELPER)

    cmd = [pythonsh, helper_path, NATIVE_LIGAND_PDB, NATIVE_LIGAND_PDBQT]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0 and os.path.exists(NATIVE_LIGAND_PDBQT):
            print("Successfully generated {}\n".format(NATIVE_LIGAND_PDBQT))
            return True
        else:
            print("AutoDockTools failed:\n" + err)
            return False
    finally:
        if os.path.exists(helper_path):
            os.remove(helper_path)

def calculate_grid_box(padding=5.0):
    print("--- 3. Calculating exact Grid Box based on native ligand ---")
    x_coords, y_coords, z_coords = [], [], []
    
    with open(NATIVE_LIGAND_PDB, 'r') as f:
        for line in f:
            if line.startswith("HETATM") or line.startswith("ATOM"):
                x_coords.append(float(line[30:38].strip()))
                y_coords.append(float(line[38:46].strip()))
                z_coords.append(float(line[46:54].strip()))

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    center_z = sum(z_coords) / len(z_coords)
    
    size_x = (max(x_coords) - min(x_coords)) + (padding * 2)
    size_y = (max(y_coords) - min(y_coords)) + (padding * 2)
    size_z = (max(z_coords) - min(z_coords)) + (padding * 2)
    
    center = (round(center_x, 3), round(center_y, 3), round(center_z, 3))
    size = (round(size_x, 3), round(size_y, 3), round(size_z, 3))
    
    print("Calculated Center: X={}, Y={}, Z={}".format(center[0], center[1], center[2]))
    print("Calculated Size:   X={}, Y={}, Z={}\n".format(size[0], size[1], size[2]))
    return center, size

def run_docking(center, size):
    print("--- 4. Running Vina Redocking ---")
    config_text = "receptor = {req}\nligand = {lig}\ncenter_x = {cx}\ncenter_y = {cy}\ncenter_z = {cz}\nsize_x = {sx}\nsize_y = {sy}\nsize_z = {sz}\nexhaustiveness = 16\nnum_modes = 9\nenergy_range = 3\nseed = 42\n".format(
        req=RECEPTOR_PDBQT, lig=NATIVE_LIGAND_PDBQT, 
        cx=center[0], cy=center[1], cz=center[2], 
        sx=size[0], sy=size[1], sz=size[2]
    )
    
    with open(TEMP_CONFIG, "w") as f:
        f.write(config_text)
        
    cmd = "vina --config {} --out {} | tee {}".format(TEMP_CONFIG, OUTPUT_PDBQT, LOG_FILE)
    subprocess.check_call(cmd, shell=True)
    os.remove(TEMP_CONFIG)
    print("\nRedocking Complete! Open PyMOL to compare {} and {}".format(NATIVE_LIGAND_PDB, OUTPUT_PDBQT))

if __name__ == "__main__":
    if extract_native_ligand():
        if prepare_ligand():
            center, size = calculate_grid_box()
            run_docking(center, size)
