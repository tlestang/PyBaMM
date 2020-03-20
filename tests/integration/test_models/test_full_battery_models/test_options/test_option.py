#
# Test option class
#
import pybamm
import unittest


def option_for_testing():
    name = "test option"
    value = "a"
    possible_values = ["a", "b", "c"]
    option = pybamm.Option(name, value, possible_values)
    return option


def list_option_for_testing():
    name = "test list option"
    value = ["list", "test"]
    possible_values = []
    option = pybamm.Option(name, value, possible_values)
    return option


class TestOption(unittest.TestCase):
    def test_initialize(self):

        name = "test option"
        value = "a"
        possible_values = ["a", "b", "c"]
        option = pybamm.Option(name, value, possible_values)

        self.assertEqual(option.name, name)
        self.assertEqual(option.value, value)
        self.assertEqual(option.possible_values, option.possible_values)

        with self.assertRaises(pybamm.OptionError):
            option = pybamm.Option(name, "d", possible_values)
            option = pybamm.Option(name, 5, possible_values)

    def test_has(self):

        option = option_for_testing()

        self.assertEqual(option.has("a"), True)
        self.assertEqual(option.has("b"), True)
        self.assertEqual(option.has("c"), True)

        self.assertEqual(option.has("d"), False)
        self.assertEqual(option.has(5), False)

        list_option = list_option_for_testing()
        self.assertEqual(list_option.has(["some", "things"]), True)
        self.assertEqual(list_option.has("just one"), False)

    def test_info(self):
        option = option_for_testing()
        option.info()

        list_option = list_option_for_testing()
        list_option.info()

    def test_get_value_strings_and_types(self):
        option = option_for_testing()
        self.assertEqual("a", option.get_values_str())
        self.assertEqual("str", option.get_value_type())

        list_option = list_option_for_testing()
        self.assertEqual("List of length 2", list_option.get_values_str())
        self.assertEqual("list", list_option.get_value_type())

    def test_get_possible_values_strings_and_types(self):
        option = option_for_testing()
        self.assertEqual("a, b, c", option.get_possible_values_str())
        self.assertEqual("str, str, str", option.get_possible_values_types())

        list_option = list_option_for_testing()
        self.assertEqual("List of strings", list_option.get_possible_values_str())
        self.assertEqual("List of strings", list_option.get_possible_values_types())

    def test_set_value(self):

        option = option_for_testing()

        option.value = "b"
        self.assertEqual(option.value, "b")

        with self.assertRaises(pybamm.OptionError):
            option.value = "d"

        with self.assertRaises(pybamm.OptionError):
            option.value = 5


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
