import urllib.request
import os
import time

def download_file(url, filename):
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}\n")
    except Exception as e:
        print(f"Error downloading {filename}: {e}\n")
    time.sleep(1)  # Be nice to the servers

# Create directories
os.makedirs("protein", exist_ok=True)
os.makedirs("ligands", exist_ok=True)

# 1. Download HIV-1 Protease (1HSG) - A classic non-metalloprotein target
print("--- Fetching Target Protein (HIV-1 Protease) ---")
download_file("https://files.rcsb.org/download/1HSG.pdb", "protein/1HSG_raw.pdb")

# 2. Download 10 Ligands from PubChem (9 known inhibitors + 1 negative control)
print("--- Fetching Ligands ---")
ligands = {
    "Indinavir": "5362440",
    "Ritonavir": "392622",
    "Saquinavir": "441243",
    "Lopinavir": "92727",
    "Nelfinavir": "64143",
    "Amprenavir": "65008",
    "Darunavir": "213039",
    "Atazanavir": "148192",
    "Tipranavir": "5468494",
    "Aspirin_Control": "2244"
}

for name, cid in ligands.items():
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF"
    filename = f"ligands/{name}.sdf"
    download_file(url, filename)

print("All downloads complete! You now have a real dataset to practice with.")
