#
# Compare lithium-ion battery models
#
import argparse
import numpy as np
import pybamm

parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug", action="store_true", help="Set logging level to 'DEBUG'."
)
args = parser.parse_args()
if args.debug:
    pybamm.set_logging_level("DEBUG")
else:
    pybamm.set_logging_level("INFO")

# load models
models = [
    # pybamm.lithium_ion.BasicSPM(name="BasicSPM"),
    # pybamm.lithium_ion.SPM(name="SPM"),
    pybamm.lithium_ion.BasicSPMe(name="Basic SPMe"),
    pybamm.lithium_ion.SPMe(name="SPMe"),
    # pybamm.lithium_ion.BasicDFN(name="BasicDFN"),
    pybamm.lithium_ion.DFN(name="DFN"),
]


# load parameter values and process models and geometry
# param = models[0].default_parameter_values
chemistry = pybamm.parameter_sets.Ecker2015
param = pybamm.ParameterValues(chemistry=chemistry)
# param["Current function [A]"] = 1
param.update({"C-rate": 7.5})
for model in models:
    param.process_model(model)

# set mesh
var = pybamm.standard_spatial_vars
var_pts = {
    var.x_n: int(param.evaluate(pybamm.geometric_parameters.L_n / 1e-6)),
    var.x_s: int(param.evaluate(pybamm.geometric_parameters.L_s / 1e-6)),
    var.x_p: int(param.evaluate(pybamm.geometric_parameters.L_p / 1e-6)),
    var.r_n: int(param.evaluate(pybamm.geometric_parameters.R_n / 1e-7)),
    var.r_p: int(param.evaluate(pybamm.geometric_parameters.R_p / 1e-7)),
}

# discretise models
for model in models:
    # create geometry
    geometry = model.default_geometry
    param.process_geometry(geometry)
    mesh = pybamm.Mesh(geometry, models[-1].default_submesh_types, var_pts)
    disc = pybamm.Discretisation(mesh, model.default_spatial_methods)
    disc.process_model(model)

# solve model
solutions = [None] * len(models)
t_eval = np.linspace(0, 3600 / param["C-rate"], 100)
for i, model in enumerate(models):
    solutions[i] = pybamm.CasadiSolver().solve(model, t_eval)

# plot
quick_plot_vars = ["Electrolyte concentration", "Terminal voltage [V]"]
# quick_plot_vars = list(models[0].variables.keys())
plot = pybamm.QuickPlot(solutions, output_variables=quick_plot_vars)
plot.dynamic_plot()
