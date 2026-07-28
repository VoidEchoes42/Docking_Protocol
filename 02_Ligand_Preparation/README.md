# Step 2: Ligand Preparation 💊

Just like the protein, the small molecule (drug/ligand) must be converted into a PDBQT format with electrical charges and flexible bonds defined.

## 1. Get the Structure
1. Go to [PubChem](https://pubchem.ncbi.nlm.nih.gov/).
2. Search for your ligand (e.g., `Bisdemethoxycurcumin`).
3. Download the **3D SDF** file. If only 2D is available, you will need to generate 3D coordinates using software like OpenBabel (`obabel -i sdf input.sdf -o sdf -O output_3d.sdf --gen3d`).

## 2. Energy Minimization
The downloaded structure might not be in its most stable, relaxed physical state.
* *Note: OpenBabel can do this via command line, but many prefer GUI tools like Avogadro for beginners.*
* In Avogadro, open the file, click the 'E' (Extensions > Optimize Geometry), use the **MMFF94 forcefield**, and run it until the energy stops decreasing. Save the file.

## 3. Prepare for Vina (Using AutoDock Tools)
1. Open AutoDockTools (ADT).
2. Go to **Ligand > Input > Open...** and select your optimized ligand file (if it asks to add Gasteiger charges, say yes).
3. **Check the Torsion Tree:** This is the most critical step for ligands. It defines which single bonds are allowed to rotate freely during the docking simulation.
   * *Ligand > Torsion Tree > Choose Torsions.*
   * You will see the molecule colored: Green (rotatable), Red (non-rotatable, usually double bonds or rings). Make sure it looks chemically accurate.
4. **Save the File:**
   * *Ligand > Output > Save as PDBQT.*
   * Save it as `ligand.pdbqt`.

You are now ready for [Step 3: Running the Docking](../03_Running_Docking)!
