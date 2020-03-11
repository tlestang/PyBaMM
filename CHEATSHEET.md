# PyBaMM User Cheatsheet

## Running a simulation
The easiest way to use PyBaMM is to run a 1C constant-current discharge with a model of your choice with all the default settings:
```python3
import pybamm
model = pybamm.lithium_ion.DFN() # Doyle-Fuller-Newman model
sim = pybamm.Simulation(model)
sim.solve()
sim.plot()
```

## Running experiments
Experimental protocols are defined using a list of keyword strings, e.g. to simulate CCCV
```
experiment = pybamm.Experiment(
    [
        "Discharge at C/10 for 10 hours or until 3.3 V",
        "Rest for 1 hour",
        "Charge at 1 A until 4.1 V",
        "Hold at 4.1 V until 50 mA",
        "Rest for 1 hour",
    ]
    * 3,
)
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, experiment=experiment)
```
Each operating condition should be of the form "Do this for this long" or "Do this until this happens". For example, "Charge at 1 C for 1 hour", or "Charge at 1 C until 4.2 V", or "Charge at 1 C for 1 hour or until 4.2 V". The instructions can be of the form "(Dis)charge at x A/C/W", "Rest", or "Hold at x V". The running time should be a time in seconds, minutes or hours, e.g. "10 seconds", "3 minutes" or "1 hour". The stopping conditions should be a circuit state, e.g. "1 A", "C/50" or "3 V".
## Useful commands
| Syntax         | Description     | Example      |
| :------------- | :-------------- | :----------- |
|`list(dict.keys())` | Lists the keys of a dictionary | `list(model.variables.keys())` will list all model variables
|`param.update({dict})` | Updates the parameters with the new values in `dict` | `param.update({"a": 4, "b": 3})` will update the parameters "a" and "b" to have values 4 and 3.`


## Interacting with the solution
After solving a simulation (`sim.solve()`) the solution is stored in `sim.solution`. The solution times can be accessed as `sim.solution.t` and the corresponding states as `sim.solution.y`.

After solving, variables can be accessed directly from the `pybamm.Solution` object. E.g. to get the terminal voltage, type `sim.solution["Terminal voltage [V]"]`. This automatically creates a post-processed version of the variable that can be called at any time and space. Common variable names include:
- Time [s]
- Discharge capacity [A.h]
- Terminal voltage [V]
- Current [A]
- Negative particle concentration [mol.m-3]
- Electrolyte concentration [mol.m-3]
- Positive particle concentration [mol.m-3]
- Negative electrode potential [V]
- Electrolyte potential [V]
- Positive electrode potential [V]

## Useful links
- Getting started guides: [https://github.com/pybamm-team/PyBaMM/tree/master/examples/notebooks/Getting%20Started](https://github.com/pybamm-team/PyBaMM/tree/master/examples/notebooks/Getting%20Started)
- Deatiled examples: [https://github.com/pybamm-team/PyBaMM/tree/master/examples](https://github.com/pybamm-team/PyBaMM/tree/master/examples)
- API documentation: [http://pybamm.readthedocs.io/](http://pybamm.readthedocs.io/)
- Further examples: [https://github.com/pybamm-team/pybamm-example-results](https://github.com/pybamm-team/pybamm-example-results)
- Contributing guidelines: [https://github.com/pybamm-team/PyBaMM/blob/master/CONTRIBUTING.md](https://github.com/pybamm-team/PyBaMM/blob/master/CONTRIBUTING.md)
