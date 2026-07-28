# Molecular Docking Tutorial 🧬💻

Welcome to the Molecular Docking Tutorial repository! This repository is designed to teach you the entire computational docking pipeline from absolute scratch. 

By the end of this tutorial, you will know how to take a raw protein crystal structure and a small molecule (ligand), prepare them computationally, simulate their interaction, and analyze the results like a computational chemist.

## 🗺️ The Roadmap

We have divided the docking process into four distinct phases. Navigate to each folder in order to complete the tutorial:

### [Step 1: Protein Preparation](./01_Protein_Preparation)
*   **Goal:** Clean a raw protein structure from the Protein Data Bank (PDB) and make it ready for docking.
*   **Concepts:** Removing water/heteroatoms, adding polar hydrogens, assigning Kollman charges.
*   **Tools:** PyMOL, AutoDock Tools (MGLTools).

### [Step 2: Ligand Preparation](./02_Ligand_Preparation)
*   **Goal:** Process a small molecule (drug candidate) into a 3D format that Vina can use.
*   **Concepts:** 3D structure generation, energy minimization, Gasteiger charges, defining rotatable bonds (torsion tree).
*   **Tools:** PubChem, OpenBabel / AutoDock Tools.

### [Step 3: Running the Docking](./03_Running_Docking)
*   **Goal:** Define the search space and run the AutoDock Vina simulation.
*   **Concepts:** The Grid Box (coordinates and dimensions), search parameters (`exhaustiveness`, `num_modes`), running command-line tools.
*   **Tools:** AutoDock Vina, Command Prompt/Terminal.

### [Step 4: Analysis & Visualization](./04_Analysis)
*   **Goal:** Interpret the results and create publication-quality images of the interactions.
*   **Concepts:** Binding affinity scores (kcal/mol), identifying Hydrogen bonds, hydrophobic contacts, and Pi-stacking.
*   **Tools:** PyMOL, PLIP (Protein-Ligand Interaction Profiler).

### [Step 5: Real Docking Example (Virtual Screening)](./05_Real_Docking_Example)
*   **Goal:** Apply everything learned to a real dataset involving 10 drugs.
*   **Concepts:** Virtual screening, automating docking with batch scripts, identifying strong vs. weak binders.
*   **Tools:** Python, Windows Batch Scripting, AutoDock Vina.

### [Step 6: Advanced - Automated Grid Box Docking](./06_Advanced_Auto_Grid)
*   **Goal:** Learn how to mathematically calculate the perfect grid box based on a co-crystallized ligand.
*   **Concepts:** Geometric centroids, automated configuration generation, Python automation.
*   **Tools:** Python, AutoDock Vina.

### [Step 7: Redocking Validation (Self-Docking)](./07_Redocking_Validation)
*   **Goal:** Prove that the docking protocol is scientifically valid.
*   **Concepts:** Redocking, RMSD (Root-Mean-Square Deviation) calculation, protocol validation.
*   **Tools:** Python, AutoDock Vina, PyMOL.

---

## 🛠️ Prerequisites
Before you begin, please install the following free software:
1.  [PyMOL](https://pymol.org/) (for visualization)
2.  [AutoDock Tools / MGLTools](https://ccsb.scripps.edu/mgltools/) (for file preparation)
3.  [AutoDock Vina](https://vina.scripps.edu/) (the docking engine)
4.  [OpenBabel](https://openbabel.org/docs/dev/Installation/install.html) (for chemical file conversions)

Ready? Head over to **01_Protein_Preparation** to get started!
