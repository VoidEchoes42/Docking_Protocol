# Step 7: Redocking Validation (Self-Docking) ✅

"How do we know if our docking protocol actually works?"

In computational chemistry, the gold standard for validating a docking methodology is **Redocking** (also known as Self-Docking). 

If a crystal structure (like `1HSG`) comes with a drug already bound to it (the co-crystallized native ligand), we should be able to mathematically pull the drug out, run it through our docking protocol blind, and have the software predict a binding pose that is nearly identical to reality.

## The Redocking Metric: RMSD
We measure success using **Root-Mean-Square Deviation (RMSD)**.
*   **< 2.0 Å:** Excellent docking protocol. The prediction perfectly matches reality.
*   **2.0 - 3.0 Å:** Acceptable, but might have slight shifts in side chains.
*   **> 3.0 Å:** Failed docking. The software placed the drug backwards or in the wrong pocket.

## The Automated Redocking Script
I have provided a Python script (`redocking_validation.py`) that performs this entire validation automatically!

### What it does:
1. Opens your raw protein (`1HSG_raw.pdb`) and mathematically extracts just the `MK1` native drug molecule into its own file (`MK1_native.pdb`).
2. Converts it to `.pdbqt` **without** altering its 3D conformation.
3. Automatically calculates the perfect grid box based on where the drug was originally sitting.
4. Runs Vina to dock the drug back into the protein.

### How to run it:
1. Open your terminal in the `07_Redocking_Validation` folder.
2. Run the script:
   ```bash
   python redocking_validation.py
   ```
3. Wait for it to finish!

## Validating the Results in PyMOL
Once the script is done, it's time to visually and mathematically prove your protocol works.

1. Open **PyMOL**.
2. Load the original experimental drug: `MK1_native.pdb` (Color it **Green**).
3. Load Vina's prediction: `MK1_redocked_out.pdbqt` (Color it **Magenta**).
4. Cycle to the first (best) pose of the prediction. 
5. In the PyMOL command line, calculate the RMSD to prove it works:
   ```pymol
   align MK1_redocked_out, MK1_native
   ```
Look at the output in the PyMOL console. If the RMSD is less than 2.0, your docking protocol is scientifically validated!
