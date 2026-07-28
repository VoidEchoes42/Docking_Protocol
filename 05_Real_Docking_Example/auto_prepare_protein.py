import os
import sys
import subprocess

def find_pythonsh():
    """Find the MGLTools pythonsh interpreter (needed for AutoDockTools API)."""
    candidates = []
    env = os.environ.get("PYTHONSH")
    if env: candidates.append(env)
    
    candidates.append(os.path.join(sys.prefix, "bin", "pythonsh"))
    candidates.append(os.path.join(os.path.dirname(sys.executable), "pythonsh"))
    
    for c in candidates:
        if c and os.path.exists(c): return c
        
    for path in os.environ.get("PATH", "").split(os.pathsep):
        cand = os.path.join(path, "pythonsh")
        if os.path.exists(cand): return cand
    return None

def clean_pdb(input_pdb, output_pdb):
    print("Cleaning {} (Removing water and heteroatoms)...".format(input_pdb))
    with open(input_pdb, 'r') as f_in, open(output_pdb, 'w') as f_out:
        for line in f_in:
            if line.startswith("ATOM") or line.startswith("TER") or line.startswith("END"):
                f_out.write(line)
    print("Saved cleaned protein as {}".format(output_pdb))

ADT_HELPER = r'''
import sys
from MolKit import Read
from AutoDockTools.MoleculePreparation import AD4ReceptorPreparation

infile, outfile = sys.argv[1:3]
mol = Read(infile)[0]
mol.buildBondsByDistance()
RPO = AD4ReceptorPreparation(
        mol, mode='automatic',
        repairs='bonds_hydrogens',
        charges_to_add='Kollman',
        cleanup='nphs_lps_waters_nonstdres_deleteAltB',
        outputfilename=outfile)
'''

def prepare_pdbqt_adt(clean_pdb, final_pdbqt):
    pythonsh = find_pythonsh()
    if not pythonsh:
        print("\nERROR: 'pythonsh' (MGLTools) not found.")
        print("Please activate mgl_env. Falling back to Open Babel is NOT recommended for best results.")
        return False
        
    print("Converting {} to PDBQT using AutoDockTools (Kollman Charges)...".format(clean_pdb))
    helper_path = "_receptor_prep_kollman.py"
    with open(helper_path, "w") as fh:
        fh.write(ADT_HELPER)

    cmd = [pythonsh, helper_path, clean_pdb, final_pdbqt]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0 and os.path.exists(final_pdbqt):
            print("\nSuccessfully generated ready-to-dock receptor: {}!".format(final_pdbqt))
            return True
        else:
            print("AutoDockTools failed:\n" + err)
            return False
    finally:
        if os.path.exists(helper_path):
            os.remove(helper_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_prepare_protein.py <raw_protein.pdb>")
        sys.exit(1)
        
    raw_pdb = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(raw_pdb))[0]
    
    dir_name = os.path.dirname(raw_pdb)
    if dir_name == "": dir_name = "."
        
    clean_pdb_file = os.path.join(dir_name, "{}_clean.pdb".format(base_name))
    final_pdbqt_file = os.path.join(dir_name, "{}_receptor.pdbqt".format(base_name))
    
    print("==================================================")
    print(" Automated Protein Preparation (MGLTools Version) ")
    print("==================================================")
    
    clean_pdb(raw_pdb, clean_pdb_file)
    prepare_pdbqt_adt(clean_pdb_file, final_pdbqt_file)
