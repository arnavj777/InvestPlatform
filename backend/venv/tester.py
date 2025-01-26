import os

# ---------- Getting Directory String ----------
root_dir = os.getcwd()
backend_dir = os.path.join(root_dir, "backend\\venv\\Datasets")
sims_dir = os.path.join(root_dir, "backend\\venv\\Simulations")

filenames = os.listdir(sims_dir)

print(filenames)