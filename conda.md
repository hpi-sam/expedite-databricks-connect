# Using Conda Environments

## Installing Conda
1. **Download the latest Miniconda installation script**:
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```
2. **Run the installation script**:
   ```bash
   bash Miniconda3-latest-Linux-x86_64.sh
   ```
3. **Follow the interactive installation**:
   - The installer will ask some questions. Answer them with `yes` where appropriate.

Now, Conda is installed.

4. **Reopen your terminal** and connect to the host.

---

## Creating a New Environment

To create an environment from an existing YAML file:

```bash
conda env create -n <name> -f environment.yaml
```

To create a new Conda environment:
```bash
conda create -n <name> python=<version>
```
Replace `<name>` with your desired environment name and `<version>` with the Python version (e.g., `3.10`).

---

## Deleting an Environment
To delete a Conda environment:
```bash
conda remove -n <name> --all
```
Replace `<name>` with the name of the environment you wish to delete.

