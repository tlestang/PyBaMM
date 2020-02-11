#
# Test the Ecker 2015 NCO cell parameter set
#
import pybamm
import numbers
import unittest
import numpy as np


class TestEcker(unittest.TestCase):
    def test_load_params(self):
        anode = pybamm.ParameterValues({}).read_parameters_csv(
            "input/parameters/lithium-ion/anodes/graphite_Ecker2015/parameters.csv"
        )
        self.assertEqual(anode["Reference temperature [K]"], "296.15")

        cathode = pybamm.ParameterValues({}).read_parameters_csv(
            "input/parameters/lithium-ion/cathodes/LiNiCoO2_Ecker2015/parameters.csv"
        )
        self.assertEqual(cathode["Reference temperature [K]"], "296.15")

        electrolyte = pybamm.ParameterValues({}).read_parameters_csv(
            "input/parameters/lithium-ion/electrolytes/lipf6_Ecker2015/parameters.csv"
        )
        self.assertEqual(electrolyte["Reference temperature [K]"], "296.15")

        cell = pybamm.ParameterValues({}).read_parameters_csv(
            "input/parameters/lithium-ion/cells/kokam_Ecker2015/parameters.csv"
        )
        self.assertAlmostEqual(
            cell["Negative current collector thickness [m]"], 1.4 * 10 ** (-5)
        )

    def test_standard_lithium_parameters(self):

        parameter_values = pybamm.ParameterValues(
            chemistry=pybamm.parameter_sets.Ecker2015
        )
        model = pybamm.lithium_ion.DFN()
        sim = pybamm.Simulation(model, parameter_values=parameter_values)
        sim.set_parameters()

        # sim.build()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
