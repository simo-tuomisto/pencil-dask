import os
import shutil
from glob import glob
import contextlib
import pencil as pc
    
@contextlib.contextmanager
def keep_cwd():
    cwd = os.getcwd()
    try:
        yield
    finally:
        os.chdir(cwd)

def copy_initial_simulation(source_dir, target_dir, quiet=True, overwrite=False):
    intial_simulation = pc.sim.simulation(os.path.realpath(source_dir), quiet=quiet)
    root_folder, sim_name = os.path.split(os.path.realpath(target_dir))
    start_components = intial_simulation.start_components
    if not os.path.exists(os.path.join(source_dir, 'data')):
        intial_simulation.start_components = []
    if not os.path.exists(target_dir) or overwrite:
        new_simulation = intial_simulation.copy(root_folder, sim_name, quiet=quiet, OVERWRITE=overwrite)
        for source_file in glob(os.path.join(source_dir, 'src', '*.x')):
            target_file = source_file.replace(source_dir, target_dir)
            shutil.copy(source_file, target_file)
        return isinstance(new_simulation, pc.sim.__Simulation__)
    return False