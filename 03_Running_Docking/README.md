# Step 3: Running the Docking 🚀

Now we have `protein.pdbqt` and `ligand.pdbqt`. We need to tell AutoDock Vina *where* to look on the protein to find the best binding site. We do this by defining a Grid Box.

## 1. Defining the Grid Box
Vina requires 6 numbers to define the 3D search space: Center (X, Y, Z) and Size (X, Y, Z).

1. Open AutoDockTools (ADT).
2. Load your `protein.pdbqt`.
3. Go to **Grid > Macromolecule > Choose** and select your protein.
4. Go to **Grid > Grid Box**. A 3D box will appear.
5. Adjust the dials for Center and Size so that the box completely encompasses the active site you want to target.
   * *Tip:* The size is in Angstroms. Make sure it's big enough for the ligand to rotate freely inside it, plus a few Angstroms of padding.
6. Write down the 6 numbers from the Grid Box panel.

## 2. Setting up the Configuration File (`config.txt`)
Instead of typing a massive command every time, it's standard practice to create a text file named `config.txt` containing all your parameters.

Create a text file called `config.txt` and put it in the same folder as your PDBQT files:

```text
receptor = protein.pdbqt
ligand = ligand.pdbqt

# Grid Box Parameters
center_x = 52.736
center_y = 51.641
center_z = 28.209

size_x = 25
size_y = 25
size_z = 25

# Expert Parameters
exhaustiveness = 16
num_modes = 9
energy_range = 3
seed = 42
```

### Understanding the Expert Parameters:
*   **`exhaustiveness`**: Determines how long Vina spends searching for the best pose. Default is 8. Setting it to 16 or 24 takes longer but gives more accurate/consistent results, especially for large, flexible ligands.
*   **`num_modes`**: How many different binding poses to output in the final file (default 9).
*   **`energy_range`**: Vina will only output poses that are within this many kcal/mol of the very best score (default 3).
*   **`seed`**: Vina uses a random number generator. By specifying a seed (e.g., `42`), you ensure that if you run the exact same job twice, you get the exact same results. This is crucial for scientific reproducibility.

## 3. Running Vina
1. Open your Command Prompt (Windows) or Terminal (Mac/Linux).
2. Navigate (`cd`) to the folder containing your files.
3. Run the following command:
   ```bash
   vina --config config.txt --out result.pdbqt --log log.txt
   ```
4. Wait for the progress bar to finish!

You are now ready for [Step 4: Analysis & Visualization](../04_Analysis)!
