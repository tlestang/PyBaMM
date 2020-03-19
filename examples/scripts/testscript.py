import pybamm

model = pybamm.lithium_ion.SPMe()

model.options_set(preset="thermal coin cell")

sim = pybamm.Simulation(model)

sim.solve()
sim.plot()
