# CH4114 Lammps Results Project

This repository contains the results of Lammps simulations for the CH4114 project.

## Getting the data

The data for this project is stored using Git LFS (Large File Storage) due to the large size of the simulation output files. To get the data locally, you will need to have `git` and `git-lfs` installed.

### 1. Install Git LFS

If you don't have Git LFS installed, you can download and install it from the official website: [https://git-lfs.github.com/](https://git-lfs.github.com/)

Once installed, you need to set it up for your user account by running the following command once:

```bash
git lfs install
```

### 2. Clone the repository

Clone this repository to your local machine using the following command:

```bash
git clone git@github.com:Shuvam-Banerji-Seal/CH4114_Lammps_results_project.git
```

### 3. Pull the LFS files

After cloning the repository, navigate to the project directory:

```bash
cd CH4114_Lammps_results_project
```

Then, run the following command to download the large files from the Git LFS storage:

```bash
git lfs pull
```

This will download all the large simulation files. You should now have all the data on your local machine.
