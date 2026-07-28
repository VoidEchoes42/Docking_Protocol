#!/bin/bash

echo "=================================================="
echo "  Open Babel Automated Ligand Preparation (WSL)   "
echo "=================================================="
echo ""

# Ensure we are in the correct directory
cd ligands || { echo "Error: 'ligands' directory not found!"; exit 1; }

echo "Converting all .sdf files to .pdbqt..."

# Loop through all SDF files in the ligands directory
for sdf_file in *.sdf; do
    # Extract filename without extension
    base_name="${sdf_file%.sdf}"
    
    echo "Processing $base_name..."
    
    # Run OpenBabel:
    # -isdf : input is SDF
    # -opdbqt : output is PDBQT
    # --gen3d : generate 3D coordinates (PubChem gives 2D by default)
    # -p 7.4 : add hydrogens at physiological pH
    obabel -isdf "$sdf_file" -opdbqt -O "${base_name}.pdbqt" --gen3d -p 7.4
    
    echo "Done with $base_name"
    echo "-----------------------------------"
done

echo ""
echo "All ligands have been prepared and converted to PDBQT format!"
echo "You can now run the Vina screening script."
