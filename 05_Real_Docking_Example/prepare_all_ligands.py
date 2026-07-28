import os
import sys
import glob
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
LIGANDS_DIR = os.path.join(REPO_ROOT, "ligands")

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

def prepare_ligands():
    pythonsh = find_pythonsh()
    if not pythonsh:
        print("ERROR: 'pythonsh' not found. Please activate mgl_env.")
        return False
        
    print("==================================================")
    print("  Ultimate Ligand Prep (OpenBabel 3D + MGLTools)  ")
    print("==================================================")

    sdf_files = glob.glob(os.path.join(LIGANDS_DIR, "*.sdf"))
    if not sdf_files:
        print("No .sdf files found in {}!".format(LIGANDS_DIR))
        return False
        
    helper_path = os.path.join(SCRIPT_DIR, "_ligand_prep.py")
    with open(helper_path, "w") as fh:
        fh.write(ADT_LIGAND_HELPER)

    for sdf_file in sdf_files:
        base_name = os.path.splitext(os.path.basename(sdf_file))[0]
        temp_pdb = os.path.join(LIGANDS_DIR, "{}_temp.pdb".format(base_name))
        final_pdbqt = os.path.join(LIGANDS_DIR, "{}.pdbqt".format(base_name))
        
        print("\nProcessing {}...".format(base_name))
        
        # Step 1: OpenBabel to generate 3D coordinates and minimize
        print("  1. Generating 3D structure & minimizing (OpenBabel)...")
        obabel_cmd = "obabel -isdf {} -opdb -O {} --gen3d -h --minimize --ff MMFF94 --steps 2500".format(sdf_file, temp_pdb)
        try:
            subprocess.check_call(obabel_cmd, shell=True)
        except subprocess.CalledProcessError:
            print("  [ERROR] OpenBabel failed on {}".format(base_name))
            continue
            
        # Step 2: AutoDockTools to assign torsions and charges
        print("  2. Assigning Gasteiger charges & Torsion Tree (MGLTools)...")
        adt_cmd = [pythonsh, helper_path, temp_pdb, final_pdbqt]
        try:
            p = subprocess.Popen(adt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode == 0 and os.path.exists(final_pdbqt):
                print("  [SUCCESS] -> {}".format(final_pdbqt))
            else:
                print("  [ERROR] MGLTools failed on {}:\n{}".format(base_name, err))
        finally:
            if os.path.exists(temp_pdb):
                os.remove(temp_pdb)
                
    if os.path.exists(helper_path):
        os.remove(helper_path)
    
    print("\nAll ligands prepared successfully using the advanced MGLTools pipeline!")
    return True

if __name__ == "__main__":
    prepare_ligands()
