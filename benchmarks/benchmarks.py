# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import pybamm as pb

class TimeDFN():
    def setup(self):
        model = pb.lithium_ion.DFN()
        geometry = model.default_geometry

        # load parameter values and process model and geometry
        param = model.default_parameter_values
        param.process_model(model)
        param.process_geometry(geometry)

        # set mesh
        mesh = pb.Mesh(geometry, model.default_submesh_types, model.default_var_pts)

        # discretise model
        disc = pb.Discretisation(mesh, model.default_spatial_methods)
        disc.process_model(model)

        self.model = model
        self.solver = model.default_solver()

    def time_solve(self):
        self.solver.solve(self.model, [0, 3600])

    
