#!/bin/bash

echo "=================================================="
echo "  AutoDock Vina Virtual Screening Script (WSL)    "
echo "=================================================="
echo ""

# Ensure we are in the correct directory where the files are
# Assuming you run this from the 05_Real_Docking_Example folder or similar where protein/ and ligands/ are

PROTEIN="../protein/1HSG_raw_receptor.pdbqt"
CONFIG="config.txt"
LIGAND_DIR="../ligands"
OUTPUT_DIR="docking_results"

# If running inside 05_Real_Docking_Example, adjust paths if necessary
if [ -f "protein/1HSG_raw_receptor.pdbqt" ]; then
    PROTEIN="protein/1HSG_raw_receptor.pdbqt"
    LIGAND_DIR="ligands"
fi

# Note: We need a config.txt. Let's create a temporary one for 1HSG if it doesn't exist
if [ ! -f "$CONFIG" ]; then
    echo "Creating config.txt for HIV-1 Protease (1HSG)..."
    cat <<EOF > $CONFIG
# Grid Box Parameters for 1HSG (roughly centered on active site)
center_x = 16.0
center_y = 25.0
center_z = 4.0
size_x = 20
size_y = 20
size_z = 20

# Expert Parameters
exhaustiveness = 8
num_modes = 9
energy_range = 3
seed = 42
EOF
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Clear the summary log file
SUMMARY_LOG="screening_summary.txt"
echo "Docking Summary Results" > "$SUMMARY_LOG"
echo "=======================" >> "$SUMMARY_LOG"

# Count total ligands for progress tracking
ligand_files=("$LIGAND_DIR"/*.pdbqt)
total_ligands=${#ligand_files[@]}
current_ligand=1

# Loop through every PDBQT ligand file in the ligand directory
for lig_path in "${ligand_files[@]}"; do
    if [ ! -f "$lig_path" ]; then
        echo "Error: No .pdbqt files found in $LIGAND_DIR. Did you run prepare_ligands_wsl.sh?"
        exit 1
    fi
    
    # Extract filename without path and extension
    filename=$(basename -- "$lig_path")
    base_name="${filename%.pdbqt}"
    
    echo -e "\n=================================================="
    echo " [$current_ligand/$total_ligands] Docking ligand: $base_name"
    echo "=================================================="
    
    out_file="$OUTPUT_DIR/${base_name}_out.pdbqt"
    log_file="$OUTPUT_DIR/${base_name}_log.txt"
    
    # Run Vina and use 'tee' to show the progress bar on screen while saving to log file
    vina --receptor "$PROTEIN" --ligand "$lig_path" --config "$CONFIG" --out "$out_file" | tee "$log_file"
    
    # Extract the top score from the log file (usually on line 26 or after the table header)
    top_score=$(grep -A 1 "mode |   affinity" "$log_file" | tail -n 1 | awk '{print $2}')
    
    echo "Finished $base_name. Best Score: $top_score kcal/mol" >> "$SUMMARY_LOG"
    ((current_ligand++))
done

echo ""
echo "All docking runs complete!"
echo "Check '$SUMMARY_LOG' for a quick ranking, and '$OUTPUT_DIR' for 3D results."
