#
# Tests for the lithium-ion SPM model
#
import pybamm
import unittest


class TestSPM(unittest.TestCase):
    def test_well_posed(self):
        model = pybamm.lithium_ion.SPM()
        model.check_well_posedness()

    def test_default_geometry(self):
        model = pybamm.lithium_ion.SPM()
        self.assertIsInstance(model.default_geometry, pybamm.Geometry)
        self.assertIn("negative particle", model.default_geometry)

        model = pybamm.lithium_ion.SPM()
        model.options_set("1+1D isothermal pouch cell")
        self.assertIn("current collector", model.default_geometry)

        model = pybamm.lithium_ion.SPM()
        model.options_set("2+1D isothermal pouch cell")
        self.assertIn("current collector", model.default_geometry)

    def test_well_posed_x_plus1D(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set("1+1D isothermal pouch cell")
        model.check_well_posedness()

        model = pybamm.lithium_ion.SPM()
        model.options_set("2+1D isothermal pouch cell")
        model.check_well_posedness()

    def test_x_full_thermal_model_no_current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(thermal="x-full")
        model.check_well_posedness()

        # Not implemented with current collectors
        model = pybamm.lithium_ion.SPM()
        with self.assertRaises(pybamm.OptionWarning):
            model.options_set(thermal="x-full", thermal_current_collector=True)

    def test_x_full_Nplus1D_not_implemented(self):
        # 1plus1D
        model = pybamm.lithium_ion.SPM()
        with self.assertRaises(pybamm.OptionWarning):
            model.options_set(
                current_collector="potential pair", dimensionality=1, thermal="x-full"
            )

        # 2plus1D
        model = pybamm.lithium_ion.SPM()
        with self.assertRaises(pybamm.OptionWarning):
            model.options_set(
                current_collector="potential pair", dimensionality=2, thermal="x-full"
            )

    def test_x_lumped_thermal_model_no_Current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(thermal="x-lumped")
        model.check_well_posedness()

        # xyz-lumped returns the same as x-lumped
        model = pybamm.lithium_ion.SPM()
        model.options_set(thermal="xyz-lumped")
        model.check_well_posedness()

    def test_x_lumped_thermal_model_0D_current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(thermal_current_collector=True, thermal="x-lumped")
        model.check_well_posedness()

        # xyz-lumped returns the same as x-lumped
        model = pybamm.lithium_ion.SPM()
        model.options_set(thermal_current_collector=True, thermal="xyz-lumped")
        model.check_well_posedness()

        model = pybamm.lithium_ion.SPM()
        model.options_set(thermal="lumped")
        model.check_well_posedness()

    def test_xyz_lumped_thermal_1D_current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(
            current_collector="potential pair", dimensionality=1, thermal="xyz-lumped"
        )
        model.check_well_posedness()

        model = pybamm.lithium_ion.SPM()
        model.options_set(
            current_collector="potential pair", dimensionality=1, thermal="lumped"
        )
        model.check_well_posedness()

    def test_xyz_lumped_thermal_2D_current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(
            current_collector="potential pair", dimensionality=2, thermal="xyz-lumped"
        )
        model.check_well_posedness()

        model = pybamm.lithium_ion.SPM()
        model.options_set(
            current_collector="potential pair", dimensionality=2, thermal="lumped"
        )
        model.check_well_posedness()

    def test_x_lumped_thermal_1D_current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(
            current_collector="potential pair", dimensionality=1, thermal="x-lumped"
        )
        model.check_well_posedness()

    def test_x_lumped_thermal_2D_current_collector(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(
            current_collector="potential pair", dimensionality=2, thermal="x-lumped"
        )
        model.check_well_posedness()

    def test_particle_fast_diffusion(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(particle="fast diffusion")
        model.check_well_posedness()

    def test_surface_form_differential(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(surface_form="differential")
        model.check_well_posedness()

    def test_surface_form_algebraic(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(surface_form="algebraic")
        model.check_well_posedness()


class TestSPMExternalCircuits(unittest.TestCase):
    def test_well_posed_voltage(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(operating_mode="voltage")
        model.check_well_posedness()

    def test_well_posed_power(self):
        model = pybamm.lithium_ion.SPM()
        model.options_set(operating_mode="power")
        model.check_well_posedness()

    def test_well_posed_function(self):
        def external_circuit_function(variables):
            I = variables["Current [A]"]
            V = variables["Terminal voltage [V]"]
            return V + I - pybamm.FunctionParameter("Function", pybamm.t)

        model = pybamm.lithium_ion.SPM()
        model.options_set(operating_mode=external_circuit_function)
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
