#
# Tests for the lead-acid LOQS model
#
import pybamm
import unittest


class TestLeadAcidLOQS(unittest.TestCase):
    def test_well_posed(self):
        model = pybamm.lead_acid.LOQS()
        model.check_well_posedness()

    def test_well_posed_with_convection(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(convection=True)
        model.check_well_posedness()

    def test_well_posed_1plus1D(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(
            surface_form="differential",
            current_collector="potential pair",
            dimensionality=1,
        )
        model.check_well_posedness()

    def test_well_posed_2plus1D(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(
            surface_form="differential",
            current_collector="potential pair",
            dimensionality=2,
        )
        model.check_well_posedness()

    def test_default_geometry(self):
        model = pybamm.lead_acid.LOQS()
        self.assertIsInstance(model.default_geometry, pybamm.Geometry)
        self.assertNotIn("negative particle", model.default_geometry)

    def test_defaults_dimensions(self):
        model = pybamm.lead_acid.LOQS()
        self.assertIsInstance(model.default_spatial_methods, dict)
        self.assertNotIn("negative particle", model.default_geometry)
        self.assertTrue(
            isinstance(
                model.default_spatial_methods["current collector"],
                pybamm.ZeroDimensionalMethod,
            )
        )
        self.assertTrue(
            issubclass(
                model.default_submesh_types["current collector"].submesh_type,
                pybamm.SubMesh0D,
            )
        )
        model = pybamm.lead_acid.LOQS()
        model.options_set(
            surface_form="differential",
            current_collector="potential pair",
            dimensionality=1,
        )
        self.assertTrue(
            isinstance(
                model.default_spatial_methods["current collector"], pybamm.FiniteVolume
            )
        )
        self.assertTrue(
            issubclass(
                model.default_submesh_types["current collector"].submesh_type,
                pybamm.Uniform1DSubMesh,
            )
        )
        model = pybamm.lead_acid.LOQS()
        model.options_set(
            surface_form="differential",
            current_collector="potential pair",
            dimensionality=2,
        )
        self.assertTrue(
            isinstance(
                model.default_spatial_methods["current collector"],
                pybamm.ScikitFiniteElement,
            )
        )
        self.assertTrue(
            issubclass(
                model.default_submesh_types["current collector"].submesh_type,
                pybamm.ScikitUniform2DSubMesh,
            )
        )


class TestLeadAcidLOQSWithSideReactions(unittest.TestCase):
    def test_well_posed_differential(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(surface_form="differential", side_reactions=["oxygen"])
        model.check_well_posedness()

    def test_well_posed_algebraic(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(surface_form="algebraic", side_reactions=["oxygen"])
        model.check_well_posedness()

    def test_varying_surface_area(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(
            surface_form="differential",
            side_reactions=["oxygen"],
            interfacial_surface_area="varying",
        )
        model.check_well_posedness()

    def test_incompatible_options(self):
        model = pybamm.lead_acid.LOQS()
        with self.assertRaises(pybamm.OptionError):
            model.options_set(side_reactions=["something"])


class TestLeadAcidLOQSSurfaceForm(unittest.TestCase):
    def test_well_posed_differential(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(surface_form="differential")
        model.check_well_posedness()

    def test_well_posed_algebraic(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(surface_form="algebraic")
        model.check_well_posedness()

    def test_well_posed_1plus1D(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(
            surface_form="differential",
            current_collector="potential pair",
            dimensionality=1,
        )
        model.check_well_posedness()

    def test_default_geometry(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(surface_form="differential")
        self.assertIn("current collector", model.default_geometry)

        model = pybamm.lead_acid.LOQS()
        model.options_set(
            current_collector="potential pair",
            dimensionality=1,
            surface_form="differential",
        )
        self.assertIn("current collector", model.default_geometry)


class TestLeadAcidLOQSExternalCircuits(unittest.TestCase):
    def test_well_posed_voltage(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(operating_mode="voltage")
        model.check_well_posedness()

    def test_well_posed_power(self):
        model = pybamm.lead_acid.LOQS()
        model.options_set(operating_mode="power")
        model.check_well_posedness()

    def test_well_posed_function(self):
        def external_circuit_function(variables):
            I = variables["Current [A]"]
            V = variables["Terminal voltage [V]"]
            return V + I - pybamm.FunctionParameter("Function", pybamm.t)

        model = pybamm.lead_acid.LOQS()
        model.options_set(operating_mode=external_circuit_function)
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
