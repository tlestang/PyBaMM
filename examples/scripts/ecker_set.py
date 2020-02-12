import pybamm as pb

pb.set_logging_level("DEBUG")

model = pb.lithium_ion.DFN()
# model.convert_to_format = "python"

chemistry = pb.parameter_sets.Ecker2015
# chemistry = pb.parameter_sets.Marquis2019
parameter_values = pb.ParameterValues(chemistry=chemistry)

sim = pb.Simulation(model, parameter_values=parameter_values)

solver = pb.CasadiSolver(mode="safe")
sim.solve(solver=solver)

