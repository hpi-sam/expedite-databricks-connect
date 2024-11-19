# Using Conda Environments

## Installing Conda
1. **Download the latest Miniconda installation script**, Create first a directory for stroing the bash script:
   ```bash
   mkdir miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   ```
2. **Run the installation script**:
   ```bash
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   ```
   Remove the directory
   ```bash
   rm ~/miniconda3/miniconda.sh
   ```

Now, Conda is installed.

3. **Reopen your terminal** and connect to the host. Refresh by running
   ```bash
   source ~/miniconda3/bin/activate
   ```
   Now you should see the base environment in your terminal (base)

   The install instructions are retrieved from https://docs.anaconda.com/miniconda/install/#quick-command-line-install
---

## Creating a New Environment

To create an environment from an existing YAML file:

```bash
conda env create-f environment.yaml
```

To create a new Conda environment:
```bash
conda create -n <name> python=<version>
```
Replace `<name>` with your desired environment name and `<version>` with the Python version (e.g., `3.10`).

To activate the environment run:
```bash
conda activate <name>
```

---

## Deleting an Environment
To delete a Conda environment:
```bash
conda remove -n <name> --all
```
Replace `<name>` with the name of the environment you wish to delete.

