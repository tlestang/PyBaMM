#
# Model options class
#

import pybamm


def print_row(option, value, other_values):
    print("{:<30s}{:<20s}{:<50s}".format(option, value, other_values))


def print_dash():
    print("=" * 100)


class ModelOptions:
    """
    Model options class containing helper functions to make
    defining and interactive with model options easier.

    Parameters
    ----------
    options: :class:`pybamm.Option`
        The option/options that you wish to use.

    """

    def __init__(self, *options):

        self._model_options_dict = {}
        self.rules = {}

        # put into dictionary for easy acesss
        self._dict_items = {}
        for opt in options:
            self._dict_items[opt.name] = opt

        self.presets = {}

    def __getitem__(self, key):
        return self._dict_items[key].value

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

    def info(self, presets=True):
        """
        Parameters
        ----------
        presets: bool (optional)
            Whether to print presets (default is True)
        """

        print()
        print_row("Option", "Current value", "Possible values")
        print_dash()
        for option_name, option in self._dict_items.items():
            value_str = option.get_values_str()
            possible_values_str = option.get_possible_values_str()
            print_row(option_name, value_str, possible_values_str)
        print()

        if presets:
            print("Presets")
            print("=" * 30)
            for preset in self.presets.keys():
                print(preset)
            print()

    def list_options(self):
        return list(self._dict_items.keys())

    def add_preset(self, name, values_dict):
        preset_keys = set(values_dict.keys())
        option_keys = set(self._dict_items.keys())

        if preset_keys != option_keys:
            raise pybamm.OptionError(
                "Preset keys ({}) must match all of the option keys ({}).".format(
                    preset_keys, option_keys
                )
            )

        self.presets.update({name: values_dict})

    def load_preset(self, name):
        preset_dict = self.presets[name]
        for key, val in preset_dict.items():
            self[key] = val

    def add_rule(self, name, rule):
        """
        Method to add rules to prevent inconsistent options.

        Parameters
        ----------
        name: str
            The name of the rule. Will be reported in case of
            rule failure.
        rule: method
            A function that takes a dictionary of model options
            as an input and returns True or False. When the rule
            is violated, return True.
        """
        self.rules[name] = rule


"""
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
