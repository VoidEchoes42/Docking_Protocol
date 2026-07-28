import os
import time

try:
    # Python 3
    from urllib.request import urlretrieve
except ImportError:
    # Python 2 (mgl_env compatibility)
    from urllib import urlretrieve

def download_file(url, filename):
    print("Downloading {}...".format(filename))
    try:
        urlretrieve(url, filename)
        print("Successfully downloaded {}\n".format(filename))
    except Exception as e:
        print("Error downloading {}: {}\n".format(filename, e))
    time.sleep(1)  # Be nice to the servers

# Create directories (Python 2.7 compatible)
if not os.path.exists("protein"):
    os.makedirs("protein")
if not os.path.exists("ligands"):
    os.makedirs("ligands")

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
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/SDF".format(cid)
    filename = "ligands/{}.sdf".format(name)
    download_file(url, filename)

print("All downloads complete! You now have a real dataset to practice with.")
