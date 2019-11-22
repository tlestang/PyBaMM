import pybamm
import numpy as np
import matplotlib.pyplot as plt

import models
import plots

pybamm.set_logging_level("INFO")


solve_spmecc = False
solve_reduced_2p1 = True
solve_full_2p1 = True

plot_voltage = False
plot_potentials = True
reduced_and_full_potential_errors = True

t_eval = np.linspace(0, 0.17, 100)

C_rate = 0.5

var_pts = {
    pybamm.standard_spatial_vars.x_n: 5,
    pybamm.standard_spatial_vars.x_s: 5,
    pybamm.standard_spatial_vars.x_p: 5,
    pybamm.standard_spatial_vars.y: 5,
    pybamm.standard_spatial_vars.z: 5,
    pybamm.standard_spatial_vars.r_n: 5,
    pybamm.standard_spatial_vars.r_p: 5,
}

params = {
    # "Heat transfer coefficient [W.m-2.K-1]": 0.1,
    # "Negative current collector conductivity [S.m-1]": 5.96e6,
    # "Positive current collector conductivity [S.m-1]": 3.55e6,
    # "Negative current collector conductivity [S.m-1]": 5.96,
    # "Positive current collector conductivity [S.m-1]": 3.55,
}


if solve_spmecc:
    spmecc = models.solve_spmecc(
        t_eval=t_eval, var_pts=var_pts, params=params, C_rate=C_rate
    )
else:
    spmecc = None

if solve_reduced_2p1:
    reduced = models.solve_reduced_2p1(
        t_eval=t_eval, var_pts=var_pts, params=params, C_rate=C_rate
    )
else:
    reduced = None

if solve_full_2p1:
    full = models.solve_full_2p1(t_eval=t_eval, C_rate=C_rate, var_pts=var_pts)
else:
    full = None

if plot_voltage:
    fig, ax = plt.subplots()
    plots.plot_voltage(ax, spmecc=spmecc, reduced=reduced, full=full)

if plot_potentials:
    times = [0, t_eval[30], t_eval[50], t_eval[70]]
    for t in times:
        plots.plot_yz_potential(t, spmecc=spmecc, reduced=reduced, full=full)

if reduced_and_full_potential_errors:
    times = [0, t_eval[30], t_eval[50], t_eval[70]]
    for t in times:
        plots.plot_potential_errors(t, reduced=reduced, full=full)


plt.show()
