#
# Option class
#
import pybamm


class Option:
    """
    A generic option class to make model options cleaner.

    Parameters
    -----------
    name : str
        The name of the option
    value:
        The current value of the option
    possible values: list
        List of possible option values
    """

    def __init__(self, name, value, possible_values):
        self.name = name
        self.possible_values = possible_values
        self.value = value

    def has(self, value):
        if self.possible_values == []:
            return isinstance(value, list)
        else:
            return value in self.possible_values

    def info(self):
        value_str = self.get_values_str()
        possible_values_str = self.get_possible_values_str()

        value_type = self.get_value_type()
        possible_values_types = self.get_possible_values_types()

        print(self.name)
        print("Current value = " + value_str + " (" + value_type + ")")
        print(
            "Possible values = ["
            + possible_values_str
            + "]"
            + " ("
            + possible_values_types
            + ")"
        )

    def get_values_str(self):
        if self.possible_values == []:
            value_str = "List of length " + str(len(self.value))
        else:
            value_str = str(self.value)
        return value_str

    def get_value_type(self):
        if self.possible_values == []:
            value_type = "list"
        else:
            value_type = self.value.__class__.__name__
        return value_type

    def get_possible_values_str(self):
        if self.possible_values == []:
            possible_values_str = "List of strings"
        else:
            possible_values_str = ", ".join(map(str, self.possible_values))
        return possible_values_str

    def get_possible_values_types(self):
        if self.possible_values == []:
            possible_values_types = "List of strings"
        else:

            types = [val.__class__.__name__ for val in self.possible_values]
            possible_values_types = ", ".join(types)
        return possible_values_types

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.has(value):
            self._value = value
        else:
            possible_values_str = self.get_possible_values_str()
            raise pybamm.OptionError(
                str(value)
                + " is an invalid option argument please enter: "
                + possible_values_str
            )

