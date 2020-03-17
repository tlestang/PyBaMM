import numpy as np
import pybamm
import pandas as pd
import matplotlib.pyplot as plt

pybamm.set_logging_level("INFO")

# load models
models = [
    # pybamm.lithium_ion.BasicSPM(name="BasicSPM"),
    # pybamm.lithium_ion.SPM(name="SPM"),
    pybamm.lithium_ion.BasicSPMe(name="Basic SPMe"),
    # pybamm.lithium_ion.SPMe(name="SPMe"),
    # pybamm.lithium_ion.BasicDFN(name="BasicDFN"),
    # pybamm.lithium_ion.DFN(name="DFN"),
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
ddliion = pd.read_csv("ddliion/concentration_liquid.dat", sep="\t").to_numpy()
x_ddlion = ddliion[:, 0]
c_e_ddliion = ddliion[:, 1:]

c_e_dict = {}
for i, model in enumerate(models):
    c_e_dict[model.name] = solutions[i]["Electrolyte concentration [mol.m-3]"]

times = [0, 50, 100, 150, 200, 250, 300, 350, 400, 438.4]
L_x = param.evaluate(pybamm.geometric_parameters.L_x)
timescale = model.timescale.evaluate()

linestyles = ["solid", "dashed", "solid", "dashdot"]
colors = ["blue", "green", "black", "orange"]
plt.figure()
for i, time in enumerate(times):
    plt.plot(
        x_ddlion,
        c_e_ddliion[:, i],
        label="Dandeliion" if i == 0 else "",
        linestyle=linestyles[-1],
        color=colors[-1],
    )
    for j, model in enumerate(models):
        plt.plot(
            x_ddlion,
            c_e_dict[model.name](x=x_ddlion * 1e-6 / L_x, t=time / timescale),
            label="{}".format(model.name) if i == 0 else "",
            linestyle=linestyles[j],
            color=colors[j],
        )

plt.xlabel("x [m]")
plt.ylabel("c [mol.m-3]")
plt.legend()
plt.show()
