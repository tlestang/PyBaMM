#
# Tests for the lead-acid composite model
#
import pybamm
import unittest


class TestLeadAcidCompositeCapacitance(unittest.TestCase):
    def test_well_posed(self):
        model = pybamm.lead_acid.CompositeCapacitance()
        model.check_well_posedness()

    def test_well_posed_no_capacitance(self):
        model = pybamm.lead_acid.CompositeCapacitance(use_capacitance=False)
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()