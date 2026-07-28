import sys
import subprocess
import os

def clean_pdb(input_pdb, output_pdb):
    print("Cleaning {} (Removing water and heteroatoms)...".format(input_pdb))
    with open(input_pdb, 'r') as f_in, open(output_pdb, 'w') as f_out:
        for line in f_in:
            # We ONLY keep standard ATOM records (amino acids).
            # This automatically strips HOH (water) and ligands (HETATM).
            if line.startswith("ATOM") or line.startswith("TER") or line.startswith("END"):
                f_out.write(line)
    print("Saved cleaned protein as {}".format(output_pdb))

def prepare_pdbqt(clean_pdb, final_pdbqt):
    print("Converting {} to PDBQT using Open Babel...".format(clean_pdb))
    # -xr means rigid (treat as receptor, no flexible torsions)
    # -p 7.4 adds polar hydrogens at physiological pH
    # -c adds partial charges
    cmd = "obabel -ipdb {} -opdbqt -O {} -xr -p 7.4 -c".format(clean_pdb, final_pdbqt)
    try:
        # Using check_call instead of run for Python 2.7 compatibility
        subprocess.check_call(cmd, shell=True)
        print("\nSuccessfully generated ready-to-dock receptor: {}!".format(final_pdbqt))
    except subprocess.CalledProcessError:
        print("\nError running Open Babel. Make sure 'obabel' is working in your environment.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_prepare_protein.py <raw_protein.pdb>")
        print("Example: python auto_prepare_protein.py protein/1HSG_raw.pdb")
        sys.exit(1)
        
    raw_pdb = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(raw_pdb))[0]
    
    # Put output in the same directory as the input
    dir_name = os.path.dirname(raw_pdb)
    if dir_name == "":
        dir_name = "."
        
    clean_pdb_file = os.path.join(dir_name, "{}_clean.pdb".format(base_name))
    final_pdbqt_file = os.path.join(dir_name, "{}_receptor.pdbqt".format(base_name))
    
    print("==================================================")
    print("      Automated Protein Preparation Script        ")
    print("==================================================")
    
    clean_pdb(raw_pdb, clean_pdb_file)
    prepare_pdbqt(clean_pdb_file, final_pdbqt_file)
