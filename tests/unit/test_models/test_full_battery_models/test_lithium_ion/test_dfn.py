#
# Tests for the lithium-ion DFN model
#
import pybamm
import unittest


class TestDFN(unittest.TestCase):
    def test_well_posed(self):
        model = pybamm.lithium_ion.DFN()
        model.check_well_posedness()

    def test_default_geometry(self):
        model = pybamm.lithium_ion.DFN()
        self.assertIsInstance(model.default_geometry, pybamm.Geometry)
        self.assertTrue("secondary" in model.default_geometry["negative particle"])

        model = pybamm.lithium_ion.DFN()
        model.options_set("1+1D isothermal pouch cell")
        self.assertIn("current collector", model.default_geometry)

        model = pybamm.lithium_ion.DFN()
        model.options_set("2+1D isothermal pouch cell")
        self.assertIn("current collector", model.default_geometry)

    def test_well_posed_x_plus1D(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set("1+1D isothermal pouch cell")
        model.check_well_posedness()

        model = pybamm.lithium_ion.DFN()
        model.options_set("2+1D isothermal pouch cell")
        model.check_well_posedness()

    def test_x_full_thermal_model_no_current_collector(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(thermal="x-full")
        model.check_well_posedness()

        # Not implemented with current collectors
        model = pybamm.lithium_ion.DFN()

        with self.assertRaises(pybamm.OptionWarning):
            model.options_set(thermal="x-full", thermal_current_collector=True)

        with self.assertRaises(pybamm.OptionError):
            model.options.check_rules()

    def test_x_full_Nplus1D_not_implemented(self):
        # 1plus1D
        model = pybamm.lithium_ion.DFN()
        with self.assertRaises(pybamm.OptionWarning):
            model.options_set("1+1D thermal pouch cell", thermal="x-full")

        # 2plus1D
        with self.assertRaises(pybamm.OptionWarning):
            model.options_set("2+1D thermal pouch cell", thermal="x-full")

    def test_x_lumped_thermal_model_no_Current_collector(self):
        options = {"thermal": "x-lumped"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

        # xyz-lumped returns the same as x-lumped
        model = pybamm.lithium_ion.DFN()
        model.options_set(thermal="xyz-lumped")
        model.check_well_posedness()

    def test_x_lumped_thermal_model_0D_current_collector(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(thermal="x-lumped", thermal_current_collector=True)
        model.check_well_posedness()

        # xyz-lumped returns the same as x-lumped
        model = pybamm.lithium_ion.DFN()
        model.options_set(thermal="xyz-lumped", thermal_current_collector=True)
        model.check_well_posedness()

        model = pybamm.lithium_ion.DFN()
        model.options_set(thermal="lumped")
        model.check_well_posedness()

    def test_xyz_lumped_thermal_1D_current_collector(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(
            current_collector="potential pair", dimensionality=1, thermal="xyz-lumped"
        )
        model.check_well_posedness()

        model = pybamm.lithium_ion.DFN()
        model.options_set(
            current_collector="potential pair", dimensionality=1, thermal="lumped"
        )
        model.check_well_posedness()

    def test_xyz_lumped_thermal_2D_current_collector(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(
            current_collector="potential pair", dimensionality=2, thermal="xyz-lumped"
        )
        model.check_well_posedness()

        model = pybamm.lithium_ion.DFN()
        model.options_set(
            current_collector="potential pair", dimensionality=2, thermal="lumped"
        )
        model.check_well_posedness()

    def test_x_lumped_thermal_1D_current_collector(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(
            current_collector="potential pair", dimensionality=1, thermal="x-lumped"
        )
        model.check_well_posedness()

    def test_x_lumped_thermal_2D_current_collector(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(
            current_collector="potential pair", dimensionality=2, thermal="x-lumped"
        )
        model.check_well_posedness()

    def test_particle_fast_diffusion(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(particle="fast diffusion")
        model.check_well_posedness()

    def test_surface_form_differential(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(surface_form="differential")
        model.check_well_posedness()

    def test_surface_form_algebraic(self):
        model = pybamm.lithium_ion.DFN()
        model.options_set(surface_form="algebriac")
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
