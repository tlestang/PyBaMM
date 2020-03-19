import pybamm

pybamm.set_logging_level("INFO")
# pybamm.settings.debug_mode = True

model = pybamm.lead_acid.Full()
# model.options_set(preset="thermal coin cell")
sim = pybamm.Simulation(model)
sim.solve()
sim.plot()
