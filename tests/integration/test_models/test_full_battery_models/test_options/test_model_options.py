#
# Test option class
#
import pybamm
import unittest


def model_options_for_testing():
    option_1 = pybamm.Option("option 1", "a", ["a", "b", "c"])
    option_2 = pybamm.Option("option 2", [1, 2], [])
    options = pybamm.ModelOptions(option_1, option_2)
    return options


class TestOption(unittest.TestCase):
    def test_initialize(self):

        option_1 = pybamm.Option("option 1", "a", ["a", "b", "c"])
        option_2 = pybamm.Option("option 2", [1, 2], [])

        options = pybamm.ModelOptions()
        self.assertEqual(len(options.values()), 0)

        options = pybamm.ModelOptions(option_1)
        self.assertEqual(options["option 1"], "a")
        self.assertEqual(len(options.values()), 1)

        options = pybamm.ModelOptions(option_1, option_2)
        self.assertEqual(options["option 1"], "a")
        self.assertEqual(options["option 2"], [1, 2])
        self.assertEqual(len(options.values()), 2)

    def test_set_value(self):
        options = model_options_for_testing()

        options["option 1"] = "b"
        self.assertEqual(options["option 1"], "b")

        with self.assertRaises(pybamm.OptionError):
            options["option 1"] = "d"

        options["option 2"] = ["another", "list"]
        self.assertEqual(options["option 2"], ["another", "list"])

        with self.assertRaises(pybamm.OptionError):
            options["option 2"] = "d"

    def test_search(self):
        options = model_options_for_testing()
        options.search("opti")

    def test_info(self):
        options = model_options_for_testing()
        options.info()

    def test_presets(self):
        options = model_options_for_testing()

        options.add_preset("preset 1", {"option 1": "b", "option 2": []})
        options.load_preset("preset 1")

        self.assertEqual(options["option 1"], "b")
        self.assertEqual(options["option 2"], [])

        with self.assertRaises(pybamm.OptionError):
            options.add_preset("preset 2", {"option 1": "b"})

        with self.assertRaises(pybamm.OptionError):
            options.add_preset("preset 2", {"option 1": "d", "option 2": []})
            options.load_preset()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
