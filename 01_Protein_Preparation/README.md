# Step 1: Protein Preparation 🧬

Before a protein can be used for docking, it must be properly prepared. Raw structures from the PDB (Protein Data Bank) contain artifacts from the crystallization process that will ruin a docking simulation if not removed.

## 1. Download the Structure
1. Go to [rcsb.org](https://www.rcsb.org/).
2. Search for your target protein (e.g., `6JMB` for insect chitinase, or `1IEP` for a classic kinase example).
3. Download the file in **PDB Format**.

## 2. Clean the Protein (Using PyMOL)
1. Open the downloaded `.pdb` file in PyMOL.
2. Remove all water molecules. Water is highly mobile in reality, and standard rigid docking cannot account for it properly.
   * *Command:* `remove resn HOH`
3. Remove co-crystallized ligands or unwanted ions (unless they are structural ions like Zinc that the protein needs to fold).
4. Save the cleaned molecule:
   * *File > Export Molecule > Save as > `protein_clean.pdb`*

## 3. Prepare for Vina (Using AutoDock Tools / MGLTools)
AutoDock Vina requires files in a specific format called **PDBQT** (Protein Data Bank, Partial Charge (Q), & Atom Type (T)).

1. Open **AutoDockTools (ADT)**.
2. Go to **File > Read Molecule** and load your `protein_clean.pdb`.
3. **Add Hydrogens:** X-ray crystallography rarely resolves hydrogen atoms, but they are crucial for H-bonding.
   * *Edit > Hydrogens > Add (Select Polar Only).*
4. **Assign Charges:** Vina needs electrical charges to calculate electrostatic interactions.
   * *Edit > Charges > Add Kollman Charges.*
5. **Save the File:** 
   * *Grid > Macromolecule > Choose...* 
   * Save it as `protein.pdbqt`.

You are now ready for [Step 2: Ligand Preparation](../02_Ligand_Preparation)!
