import pybamm as pb
import numpy as np

pb.set_logging_level("INFO")

model = pb.lithium_ion.DFN()
model.convert_to_format = "python"

chemistry = pb.parameter_sets.Ecker2015
# chemistry = pb.parameter_sets.Marquis2019
parameter_values = pb.ParameterValues(chemistry=chemistry)

sim = pb.Simulation(model, parameter_values=parameter_values)

solver = pb.IDAKLUSolver()  # mode="fast")
t_eval = np.linspace(0, 1, 100)
sim.solve(t_eval=t_eval, solver=solver)
sim.plot()
