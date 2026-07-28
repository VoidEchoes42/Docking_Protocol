# Step 4: Analysis & Visualization 📊

After Vina finishes running, it generates two files:
1. `log.txt`: Contains the predicted binding affinity scores.
2. `result.pdbqt`: Contains the 3D coordinates of all the predicted poses.

## 1. Understanding the Score (`log.txt`)
Open `log.txt` in a text editor. You will see a table ranking the poses from 1 to 9.
*   **Affinity (kcal/mol):** This is the estimated binding free energy ($\Delta G$). 
*   **The Rule of Thumb:** The more *negative* the number, the stronger the predicted binding. A score of -10 is theoretically a tighter binder than -7.
*   *Note:* Scoring functions are imperfect. They shouldn't be treated as absolute laboratory truths, but rather as a way to rank compounds relative to each other (Virtual Screening).

## 2. Visualizing in PyMOL
The true value of docking isn't just the score; it's understanding the atomic interactions.

1. Open **PyMOL**.
2. Drag and drop your original `protein_clean.pdb` into the window.
3. Drag and drop your `result.pdbqt` into the window.
4. You will see the ligand sitting inside the protein! In the bottom right corner, use the play buttons to cycle through the different generated poses (states).

### Making it Look Professional
By default, it looks like a mess of lines. Let's make it look like a journal figure:
```pymol
# Run these commands in the PyMOL command line

# 1. Clean the view
hide everything
show cartoon, protein_clean
set cartoon_transparency, 0.7

# 2. Show the ligand beautifully
show sticks, result
color tv_red, result
util.cnc result

# 3. Find and show the protein residues touching the ligand (within 3.5 Å)
select pocket, byres (protein_clean within 3.5 of result)
show sticks, pocket
color green, pocket
util.cnc pocket

# 4. Automatically find Hydrogen Bonds and display them as yellow dashes
distance h_bonds, protein_clean, result, 3.5, mode=2
color yellow, h_bonds
set dash_color, yellow
hide labels, h_bonds
```

## 3. Advanced Profiling (PLIP)
If you want an exhaustive list of exactly which residues are forming Hydrogen bonds, Hydrophobic contacts, or Pi-stacking, visual inspection can miss things.

Use the **Protein-Ligand Interaction Profiler (PLIP)**.
1. In PyMOL, save your best pose and the protein together as a single `.pdb` complex.
2. Go to the [PLIP Web Server](https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index).
3. Upload your complex.
4. It will generate a highly detailed, tabular report of every single molecular interaction anchoring your drug to the protein.

**🎉 Congratulations! You have successfully completed a full molecular docking pipeline! 🎉**
