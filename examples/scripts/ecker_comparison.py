import pybamm as pybamm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# pybamm.set_logging_level("DEBUG")
# pybamm.settings.debug_mode = True
# load data
voltage_data_1C = pd.read_csv("ddliion/voltage_1C.dat", sep="\t")
voltage_data_2_5C = pd.read_csv("ddliion/voltage_2_5C.dat", sep="\t")
voltage_data_5C = pd.read_csv("ddliion/voltage_5C.dat", sep="\t")
voltage_data_7_5C = pd.read_csv("ddliion/voltage_7_5C.dat", sep="\t")

# set up models
models = {
    "SPM": pybamm.lithium_ion.BasicSPM(),
    # "SPMe": pybamm.lithium_ion.BasicSPMe(linear_diffusion=False),
    # "SPMe": pybamm.lithium_ion.BasicSPMe(linear_diffusion=True),
    "SPMe": pybamm.lithium_ion.BasicSPMe(linear_diffusion=True, wrong_av=True),
    "DFN": pybamm.lithium_ion.BasicDFN(),
}

# pick parameters, keeping C-rate as an input to be changed for each solve
chemistry = pybamm.parameter_sets.Ecker2015
parameter_values = pybamm.ParameterValues(chemistry=chemistry)
parameter_values.update({"C-rate": "[input]"})

# set up number of points for discretisation
var = pybamm.standard_spatial_vars
# var_pts = {var.x_n: 101, var.x_s: 101, var.x_p: 101, var.r_n: 101, var.r_p: 101}
var_pts = {
    var.x_n: int(parameter_values.evaluate(pybamm.geometric_parameters.L_n / 1e-6)),
    var.x_s: int(parameter_values.evaluate(pybamm.geometric_parameters.L_s / 1e-6)),
    var.x_p: int(parameter_values.evaluate(pybamm.geometric_parameters.L_p / 1e-6)),
    var.r_n: int(parameter_values.evaluate(pybamm.geometric_parameters.R_n / 1e-7)),
    var.r_p: int(parameter_values.evaluate(pybamm.geometric_parameters.R_p / 1e-7)),
}

# set up simulations
sims = {}
for name, model in models.items():
    sims[name] = pybamm.Simulation(
        model, parameter_values=parameter_values, var_pts=var_pts
    )

# pick C_rates and times to integrate over (using casasi fast mode, so want to
# stop before e.g. surface concentration goes negative)
C_rates = [1, 2.5, 5, 7.5]
t_evals = [
    np.linspace(0, 3800, 1000),
    np.linspace(0, 1510, 1000),
    np.linspace(0, 720, 1000),
    np.linspace(0, 440, 1000),
]
# t_evals = [
#    np.array(voltage_data_1C["t(s)"]),
#    np.array(voltage_data_2_5C["t(s)"]),
#    np.array(voltage_data_5C["t(s)"]),
#    np.array(voltage_data_7_5C["t(s)"]),
# ]

# loop over C-rates
solutions = {
    "SPM": [None] * len(C_rates),
    "SPMe": [None] * len(C_rates),
    "DFN": [None] * len(C_rates),
}
for i, C_rate in enumerate(C_rates):
    print("C-rate = {}".format(C_rate))

    # solve models
    t_eval = t_evals[i]

    for name, sim in sims.items():
        print("Solving {}...".format(name))
        sim.solve(
            t_eval=t_eval,
            solver=pybamm.CasadiSolver(mode="fast"),
            inputs={"C-rate": C_rate},
        )
        solutions[name][i] = sim.solution

print("Finished")

# qp = pybamm.QuickPlot(solutions["SPMe"][3])
# qp.dynamic_plot()
# qp = pybamm.QuickPlot(solutions["DFN"][3])
# qp.dynamic_plot()

# plot - could be made more efficiently, but oh well...
fig, ax = plt.subplots(2, 2, figsize=(6, 5))
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.85, wspace=0.3, hspace=0.5)
linestyles = ["solid", "dashed", "solid", "dashdot"]
colors = ["blue", "green", "black", "orange"]
V_major_ticks = np.arange(2.4, 4.2, 0.2)
V_minor_ticks = np.arange(2.5, 4.1, 0.2)

# 1C
for i, key in enumerate(solutions.keys()):
    t = solutions[key][0]["Time [s]"](solutions[key][0].t)
    V = solutions[key][0]["Terminal voltage [V]"](solutions[key][0].t)
    ax[0, 0].plot(
        t, V, label=key + "(PyBaMM)", linestyle=linestyles[i], color=colors[i]
    )
ax[0, 0].plot(
    voltage_data_1C["t(s)"],
    voltage_data_1C["Voltage(V)"],
    label="DFN (Dandeliion)",
    linestyle=linestyles[3],
    color=colors[3],
)
ax[0, 0].set_xlabel("Time [s]")
ax[0, 0].set_ylabel("Voltage [V]")
ax[0, 0].set_xlim([0, 4000])
ax[0, 0].set_ylim([2.4, 4.2])
t_major_ticks = np.arange(0, 4000, 500)
t_minor_ticks = np.arange(250, 3750, 500)
ax[0, 0].set_xticks(t_major_ticks)
ax[0, 0].set_xticks(t_minor_ticks, minor=True)
ax[0, 0].set_yticks(V_major_ticks)
ax[0, 0].set_yticks(V_minor_ticks, minor=True)
ax[0, 0].grid(which="major")
ax[0, 0].legend(loc="lower left")
ax[0, 0].title.set_text("1C")

# 2.5C
for i, key in enumerate(solutions.keys()):
    t = solutions[key][1]["Time [s]"](solutions[key][1].t)
    V = solutions[key][1]["Terminal voltage [V]"](solutions[key][1].t)
    ax[0, 1].plot(
        t, V, label=key + "(PyBaMM)", linestyle=linestyles[i], color=colors[i]
    )
ax[0, 1].plot(
    voltage_data_2_5C["t(s)"],
    voltage_data_2_5C["Voltage(V)"],
    label="DFN (Dandeliion)",
    linestyle=linestyles[3],
    color=colors[3],
)
ax[0, 1].set_xlabel("Time [s]")
ax[0, 1].set_ylabel("Voltage [V]")
ax[0, 1].set_xlim([0, 1600])
ax[0, 1].set_ylim([2.4, 4.2])
t_major_ticks = np.arange(0, 1600, 200)
t_minor_ticks = np.arange(100, 1500, 200)
ax[0, 1].set_xticks(t_major_ticks)
ax[0, 1].set_xticks(t_minor_ticks, minor=True)
ax[0, 1].set_yticks(V_major_ticks)
ax[0, 1].set_yticks(V_minor_ticks, minor=True)
ax[0, 1].grid(which="major")
ax[0, 1].legend(loc="lower left")
ax[0, 1].title.set_text("2.5C")

# 5C
for i, key in enumerate(solutions.keys()):
    t = solutions[key][2]["Time [s]"](solutions[key][2].t)
    V = solutions[key][2]["Terminal voltage [V]"](solutions[key][2].t)
    ax[1, 0].plot(
        t, V, label=key + "(PyBaMM)", linestyle=linestyles[i], color=colors[i]
    )
ax[1, 0].plot(
    voltage_data_5C["t(s)"],
    voltage_data_5C["Voltage(V)"],
    label="DFN (Dandeliion)",
    linestyle=linestyles[3],
    color=colors[3],
)
ax[1, 0].set_xlabel("Time [s]")
ax[1, 0].set_ylabel("Voltage [V]")
ax[1, 0].set_xlim([0, 800])
ax[1, 0].set_ylim([2.4, 4.2])
t_major_ticks = np.arange(0, 800, 100)
t_minor_ticks = np.arange(50, 750, 100)
ax[1, 0].set_xticks(t_major_ticks)
ax[1, 0].set_xticks(t_minor_ticks, minor=True)
ax[1, 0].set_yticks(V_major_ticks)
ax[1, 0].set_yticks(V_minor_ticks, minor=True)
ax[1, 0].grid(which="major")
ax[1, 0].legend(loc="lower left")
ax[1, 0].title.set_text("5C")

# 7.5C
for i, key in enumerate(solutions.keys()):
    t = solutions[key][3]["Time [s]"](solutions[key][3].t)
    V = solutions[key][3]["Terminal voltage [V]"](solutions[key][3].t)
    ax[1, 1].plot(
        t, V, label=key + "(PyBaMM)", linestyle=linestyles[i], color=colors[i]
    )
ax[1, 1].plot(
    voltage_data_7_5C["t(s)"],
    voltage_data_7_5C["Voltage(V)"],
    label="DFN (Dandeliion)",
    linestyle=linestyles[3],
    color=colors[3],
)
ax[1, 1].set_xlabel("Time [s]")
ax[1, 1].set_ylabel("Voltage [V]")
ax[1, 1].set_xlim([0, 500])
ax[1, 1].set_ylim([2.4, 4.2])
t_major_ticks = np.arange(0, 500, 100)
t_minor_ticks = np.arange(50, 450, 100)
ax[1, 1].set_xticks(t_major_ticks)
ax[1, 1].set_xticks(t_minor_ticks, minor=True)
ax[1, 1].set_yticks(V_major_ticks)
ax[1, 1].set_yticks(V_minor_ticks, minor=True)
ax[1, 1].grid(which="major")
ax[1, 1].legend(loc="lower left")
ax[1, 1].title.set_text("7.5C")

# plt.savefig("ecker_c_rates.pdf", format="pdf", dpi=1000)
plt.show()
