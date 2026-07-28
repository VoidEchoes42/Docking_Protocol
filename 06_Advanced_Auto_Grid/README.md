# Step 6: Advanced - Automated Grid Box Docking 🤖

In standard docking, you manually adjust the Grid Box dials in AutoDock Tools to cover the active site. While great for learning, this is slow and prone to human error when processing dozens of proteins.

If you have a **co-crystallized ligand** (a drug already bound to the protein in the PDB file), you can write a script to mathematically calculate the perfect grid box based on the ligand's coordinates!

## How it works

1. **Extract the Reference Ligand:** You open the original PDB file, select only the co-crystallized drug, and save it as a separate `reference_ligand.pdb`.
2. **Calculate the Centroid:** A Python script reads the X, Y, and Z coordinates of every atom in that drug and averages them. This becomes the exact `center_x`, `center_y`, `center_z` of your grid box.
3. **Calculate the Size:** The script finds the maximum distance between the atoms, adds a "padding" of 5 Angstroms on all sides to allow movement, and calculates `size_x`, `size_y`, `size_z`.
4. **Automated Docking:** The script dynamically generates the `config.txt` and runs Vina automatically.

## The Script: `auto_grid_docking.py`

I have provided a professional Python script (`auto_grid_docking.py`) in this folder that does exactly this.

### How to use it:
1. Make sure you have your prepared `protein.pdbqt`.
2. Ensure you saved the original co-crystallized drug as `reference_ligand.pdb`.
3. Put all your prepared drug `.pdbqt` files in a folder called `ligands`.
4. Open the `auto_grid_docking.py` script in a text editor and update the file paths at the bottom of the script.
5. Run the script from your terminal:
   ```bash
   python auto_grid_docking.py
   ```

The script will instantly calculate the perfect binding pocket coordinates, build the configuration files, and dock every ligand in your folder! This ensures the highest accuracy by locking the search space exactly where the native ligand bound.
