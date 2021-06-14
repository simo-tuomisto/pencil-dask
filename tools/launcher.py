import os
from typing import Optional, Callable

from yaml import load as yaml_load, dump as yaml_dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from sh import bash
from .misc import keep_cwd
    
class PencilCodeLauncher:

    def __init__(self, simulation_dir, environment=None, verbose=False):
        self._queue_comment = None
        self._simulation_dir = os.path.realpath(simulation_dir)
        self._env = environment
        if not self._env:
            self._env = os.environ.copy()
            
        self._state_file = os.path.join(self._simulation_dir, 'pc_state.yml')
        self.load_state()
        self.update_state()
        if verbose:
            print(self)
        
    def load_state(self) -> None:       
        if not os.path.isfile(self._state_file):
            self.state = {
                'start': False,
                'run': False,
            }
        else:
            with open(self._state_file, 'r') as state_file:
                self.state = yaml_load(state_file, Loader=Loader)


            
    def update_state(self) -> None:
        with open(self._state_file, 'w') as state_file:
            state_file.write(yaml_dump(self.state, Dumper=Dumper))
    
    @keep_cwd()
    def _run_cmd(self, executable: str, output_name: str) -> bool:
        """
        This function runs a command or an executable in the simulation directory.
        Output of the command is written to the outfile.

        Parameters
        ----------
        executable : str
            Command or executable to run.
        output_name : str
            File name for the output.

        Returns
        -------
        bool
            True if run finished with exit code 0, False otherwise.

        """
        output_file = os.path.join(self._simulation_dir, output_name)
        result = os.path.isfile(output_file)
        with open(output_file, 'a') as output:
            result = bash('-c', executable, _cwd=self._simulation_dir, _env=self._env, _out=output)
        print(result)
        result = result.exit_code == 0
        return result
    
    def start(self, restart: Optional[bool] = False) -> bool:
        try:
            os.mkdir(os.path.join(self._simulation_dir, 'data'))
        except FileExistsError:
            pass
        if not self.state['start'] or restart:
            self.state['start'] = self._run_cmd('pc_start', 'launcher-start.out')
            self.update_state()
        return self.state['start']
    
    def run(self, rerun: Optional[bool] = False) -> bool:
        if not self.state['run'] or rerun:
            self.state['run'] = self._run_cmd('pc_run', 'launcher-run.out')
            self.update_state()
        return self.state['run']
    
    def has_started(self) -> bool:
        return self.state['start']
    
    def has_run(self) -> bool:
        return self.state['run']
    
    def __str__(self) -> str:
        return 'Current state:\n{0}'.format(str(self.state))    
    #def write_config(self, str: )
    
class SlurmLauncher(PencilCodeLauncher):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue_comment = 'SLURM'