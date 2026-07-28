# Step 5: Real Docking Example (Virtual Screening) 🧪

Teaching molecular docking is best done with a real-world example. In this folder, we will dock **10 real drug molecules** against a classic non-metalloprotein target: **HIV-1 Protease**. 

This simulates a "Virtual Screening" campaign, showing how computational chemistry is used to rank multiple compounds.

## 1. The Target: HIV-1 Protease (`1HSG`)
HIV-1 protease is an enzyme essential for the replication of the HIV virus. It is a textbook example for docking because:
* It is a non-metalloprotein (no metal ions to complicate the charges).
* It has a very clear, deep binding pocket.
* There are many known FDA-approved drugs designed specifically for it.

## 2. Getting the Data (`download_data.py`)
Instead of manually searching the PDB and PubChem 11 times, I have provided a Python script that automates the download of the entire dataset.

**What it downloads:**
*   **Receptor:** `1HSG` (HIV-1 Protease) raw PDB file.
*   **Ligands:** 9 FDA-approved HIV Protease Inhibitors (Indinavir, Ritonavir, Saquinavir, etc.) + 1 Negative Control (Aspirin). 

**How to run it:**
1. Open your Command Prompt / Terminal in this folder.
2. Type: `python download_data.py`
3. Watch it create a `protein` and `ligands` folder and fill them with real data!

## 3. The Homework (Preparation)
To teach the pipeline, you should now have the student apply the skills from Steps 1-3 to this dataset:
1.  **Clean `1HSG_raw.pdb`** in PyMOL (remove the co-crystallized ligand and water).
2.  **Convert to PDBQT** using AutoDock Tools.
3.  **Convert all 10 ligand `.sdf` files** to `.pdbqt` using OpenBabel or AutoDock Tools.
4.  **Find the Grid Box** coordinates for the active site of 1HSG. (Hint: Center it roughly around the middle of the protein where the two flaps open up).

*(Put all the final prepared `.pdbqt` files into a folder named `prepared_files`).*

### 🐧 Pro-Tip: Using WSL & Open Babel
If you are using a Linux terminal (like WSL or a conda environment like `mgl_env`), doing Step 3 manually for 10 files is tedious. 

I have provided a bash script: `prepare_ligands_wsl.sh`. 
If you have `obabel` installed in your terminal, just run this script! It will automatically loop through the `ligands` folder, generate 3D coordinates, add hydrogens at pH 7.4, and convert all `.sdf` files into `.pdbqt` instantly.

## 4. Automating the Docking (`run_virtual_screening.bat`)
When screening 10 compounds (or 10,000), you don't type the Vina command manually every time. You use a batch script!

Once the files are prepared:
1. Review the `config.txt` and ensure the grid box coordinates are correct for 1HSG.
2. Double-click `run_virtual_screening.bat` (Windows).
3. The script will loop through all 10 ligands, run Vina on each one, and save the results automatically into a `docking_results` folder!

This is exactly how high-throughput virtual screening works in the real world.
