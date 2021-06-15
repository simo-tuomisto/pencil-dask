# Pencil-Dask

This is a test repository for a possible framework of running
[Pencil Code](https://github.com/pencil-code/pencil-code):
simulations and data analysis with Dask.

## Installation

The installaion is done in two steps:

1. Pencil Code installation. This is left for the user. Code assumes
   that `pc_X`-functions are available in path

### Environment installation

There's a minimal conda environment that you can use to test the framework.

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) or
   [anaconda](https://www.anaconda.com/products/individual)
2. Install minimal environment that has
   [mamba](https://github.com/mamba-org/mamba)
   (otherwise installation of the actual environment takes a long time):
   ```sh
   conda create -n pencil-dask -c conda-forge python=3.9.* mamba
   ```
3. Activate the minimal environment:
   ```sh
   conda activate pencil-dask
   ```
4. Add rest of the packages using mamba
   ```sh
   mamba env update -f environment.yml -n base
   ```

Alternative, slow method:

1. Install miniconda or anaconda.
2. Create environment using conda:
   ```sh
   conda env create -f environment.yml
   ```

## Minimal working example

### Building the example

Pencil code needs to be enabled before running the example

1. Activate the environment.
   ```sh
   conda activate pencil-dask
   ```
2. Start a jupyterlab:
   ```sh
   jupyter-lab
   ```

3. Open `build-test.ipynb` and execute cells one at a time.

### Running the example

1. Activate the environment.
   ```sh
   conda activate pencil-dask
   ```
2. Start a jupyterlab:
   ```sh
   jupyter-lab
   ```
3. Open `launcher-test.ipynb` and execute cells one at a time.
