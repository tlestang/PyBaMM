# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import pybamm as pb

def prep_model():
    model = pb.lithium_ion.SPM()
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

    return model

def time_SPM(model):
    solver = pb.ScipySolver()
    solver.solve(model, [0, 3600])
time_SPM.setup_cache = prep_model
    
