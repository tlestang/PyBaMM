#
# Model options class
#

import pybamm


def print_row(option, value, other_values):
    print("{:<30s}{:<20s}{:<50s}".format(option, value, other_values))


def print_dash():
    print("=" * 100)


class Option:
    """
    A generic option class to make model options cleaner.
    """

    def __init__(self, value, possible_values):
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
            value_type = "List"
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

    def dict_entry(self):
        return {self.name: self.current_value}

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.has(value):
            self._value = value
        else:
            possible_values_str = self.get_possible_values_str()
            raise pybamm.ModelError(
                str(value)
                + " is an invalid option argument please enter: "
                + possible_values_str
            )


class ModelOptions:
    """
    Model options class

    Attributes
    ----------
    dimensionality : int, optional
        Sets the dimension of the current collector problem. Can be 0
        (default), 1 or 2.
    surface form : bool or str, optional
        Whether to use the surface formulation of the problem. Can be False
        (default), "differential" or "algebraic". Must be 'False' for
        lithium-ion models.
    convection : bool or str, optional
        Whether to include the effects of convection in the model. Can be
        False (default) or True. Must be 'False' for lithium-ion models.
    side reactions : list, optional
        Contains a list of any side reactions to include. Default is []. If this
        list is not empty (i.e. side reactions are included in the model), then
        "surface form" cannot be 'False'.
    interfacial surface area : str, optional
        Sets the model for the interfacial surface area. Can be "constant"
        (default) or "varying". Not currently implemented in any of the models.
    current collector : str, optional
        Sets the current collector model to use. Can be "uniform" (default),
        "potential pair" or "potential pair quite conductive".
    particle : str, optional
        Sets the submodel to use to describe behaviour within the particle.
        Can be "Fickian diffusion" (default) or "fast diffusion".
    thermal : str, optional
        Sets the thermal model to use. Can be "isothermal" (default),
        "x-full", "x-lumped", "xyz-lumped" or "lumped".
    thermal current collector : bool, optional
        Whether to include thermal effects in the current collector in
        one-dimensional models (default is False). Note that this option
        only takes effect if "dimensionality" is 0. If "dimensionality"
        is 1 or 2 current collector effects are always included. Must be 'False'
        for lead-acid models.
    external submodels : list
        A list of the submodels that you would like to supply an external
        variable for instead of solving in PyBaMM. The entries of the lists
        are strings that correspond to the submodel names in the keys
        of `self.submodels`.
    """

    def __init__(
        self,
        dimensionality=0,
        surface_form=False,
        convection=False,
        side_reactions=None,
        interfacial_surface_area="constant",
        current_collector="uniform",
        particle="Fickian diffusion",
        thermal="isothermal",
        thermal_current_collector=False,
        external_submodels=None,
    ):

        self._model_options_dict = {}

        if not side_reactions:
            side_reactions = []

        if not external_submodels:
            external_submodels = []

        self._dict_items = {
            "dimensionality": Option(dimensionality, [0, 1, 2]),
            "surface form": Option(surface_form, [False, "differential", "algebriac"]),
            "convection": Option(convection, [False, True]),
            "side reactions": Option(side_reactions, []),
            "interfacial surface area": Option(interfacial_surface_area, ["constant"]),
            "current collector": Option(
                current_collector,
                ["uniform", "potential pair", "potential pair quite conductive"],
            ),
            "particle": Option(particle, ["Fickian diffusion", "fast diffusion"]),
            "thermal": Option(
                thermal, ["isothermal", "x-full", "x-lumped", "xyz-lumped", "lumped"]
            ),
            "thermal current collector": Option(
                thermal_current_collector, [False, True]
            ),
            "external submodels": Option(external_submodels, []),
        }

    def __getitem__(self, key):
        return self._dict_items[key]

    def __setitem__(self, key, value):
        "Update the value in the option."
        self._dict_items[key].value = value

    def __delitem__(self, key):
        del self._dict_items[key]

    def keys(self):
        "Get the keys of the dictionary"
        return self._dict_items.keys()

    def values(self):
        "Get the values of the dictionary"
        return self._dict_items.values()

    def items(self):
        "Get the items of the dictionary"
        return self._dict_items.items()

    def search(self, key, print_values=True):
        """
        Search dictionary for keys containing 'key'.
        See :meth:`pybamm.FuzzyDict.search()`.
        """
        return self._dict_items.search(key, print_values)

    def _ipython_key_completions_(self):
        return list(self._dict_items.keys())

    def info(self):
        print()
        print_row("Option", "Current value", "Possible values")
        print_dash()
        for option_name, option in self._dict_items.items():
            value_str = option.get_values_str()
            possible_values_str = option.get_possible_values_str()
            print_row(option_name, value_str, possible_values_str)
        print()

    def list_options(self):
        return list(self._dict_items.keys())

    # presets
    def isothermal_coin_cell(self):
        self["dimensionality"] = 0
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "uniform"
        self["particle"] = "Fickian diffusion"
        self["thermal"] = "isothermal"
        self["thermal current collector"] = False
        self["external submodels"] = []

    def thermal_coin_cell(self):
        self["dimensionality"] = 0
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "uniform"
        self["particle"] = "Fickian diffusion"
        self["thermal"] = "xyz-lumped"
        self["thermal current collector"] = False
        self["external submodels"] = []

    def isothermal_pouch_cell_1_plus_1D(self):
        self["dimensionality"] = 1
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "potential pair"
        self["particle"] = "Fickian diffusion"
        self["thermal"] = "isothermal"
        self["thermal current collector"] = False
        self["external submodels"] = []

    def thermal_pouch_cell_1_plus_1D(self):
        self["dimensionality"] = 1
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "potential pair"
        self["particle"] = "Fickian diffusion"
        self["thermal"] = "x-lumped"
        self["thermal current collector"] = True
        self["external submodels"] = []

    def isothermal_pouch_cell_2_plus_1D(self):
        self["dimensionality"] = 2
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "potential pair"
        self["particle"] = "Fickian diffusion"
        self["thermal"] = "isothermal"
        self["thermal current collector"] = False
        self["external submodels"] = []

    def thermal_pouch_cell_2_plus_1D(self):
        self["dimensionality"] = 2
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "potential pair"
        self["particle"] = "Fickian diffusion"
        self["thermal"] = "x-lumped"
        self["thermal current collector"] = True
        self["external submodels"] = []

