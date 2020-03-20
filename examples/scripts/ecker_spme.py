import numpy as np
import pybamm
import pandas as pd
import matplotlib.pyplot as plt

pybamm.set_logging_level("INFO")

# load models
models = [
    # pybamm.lithium_ion.BasicSPM(name="BasicSPM"),
    # pybamm.lithium_ion.SPM(name="SPM"),
    pybamm.lithium_ion.BasicSPMe(name="SPMe (linear)", linear_diffusion=True),
    pybamm.lithium_ion.BasicSPMe(
        name="SPMe (linear, wrong j0.)", linear_diffusion=True, wrong_j0=True
    ),
    pybamm.lithium_ion.SPMe(name="SPMe (nonlinear)"),
    # pybamm.lithium_ion.BasicDFN(name="BasicDFN"),
    pybamm.lithium_ion.DFN(name="DFN"),
]


# load parameter values and process models and geometry
chemistry = pybamm.parameter_sets.Ecker2015
param = pybamm.ParameterValues(chemistry=chemistry)
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
t_eval = np.linspace(0, 440, 1000)
for i, model in enumerate(models):
    solutions[i] = pybamm.CasadiSolver(mode="fast").solve(model, t_eval)

# plot
c_e_dict = {}
v_dict = {}
for i, model in enumerate(models):
    c_e_dict[model.name] = solutions[i]["Electrolyte concentration [mol.m-3]"]
    v_dict[model.name] = solutions[i]["Terminal voltage [V]"]

times = [0, 40, 50, 440]
timescale = model.timescale.evaluate()
L_x = param.evaluate(pybamm.geometric_parameters.L_x)
x = np.linspace(0, 1, 100)

linestyles = ["solid", "dashdot", "dashed", "solid"]
colors = ["green", "red", "blue", "black"]

# c_e
plt.figure()
for i, time in enumerate(times):
    for j, model in enumerate(models):
        plt.plot(
            x * L_x,
            c_e_dict[model.name](x=x, t=time / timescale),
            label="{}".format(model.name) if i == 0 else "",
            linestyle=linestyles[j],
            color=colors[j],
        )

plt.xlabel("x [m]")
plt.ylabel("Electrolyte concentration [mol.m-3]")
plt.legend()

# V
plt.figure()
for j, model in enumerate(models):
    plt.plot(
        t_eval,
        v_dict[model.name](t=t_eval / timescale),
        label="{}".format(model.name),
        linestyle=linestyles[j],
        color=colors[j],
    )

plt.xlabel("Time [s]")
plt.ylabel("Terminal voltage [V]")
plt.legend()

plt.show()
