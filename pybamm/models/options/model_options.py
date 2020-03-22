#
# Model options class
#

import pybamm
import copy


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
        self._dict_items = pybamm.FuzzyDict()
        for opt in options:
            self._dict_items[opt.name] = copy.deepcopy(opt)

        self.presets = {}

    def __getitem__(self, key):
        return self._dict_items[key].value

    def __setitem__(self, key, value):
        "Update the value in the option."
        self._dict_items[key].value = value
        self.check_rules(warn=True)

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

    def info(self, presets=True, rules=True):
        """
        Parameters
        ----------
        presets: bool (optional)
            Whether to print presets (default is True)
        rules: bool (optional)
            Whether to print rules (default is True)
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
            if len(self.presets) > 0:
                print("Presets")
                print_dash()
                for preset in self.presets.keys():
                    print(preset)
                print()

        if rules:
            if len(self.rules) > 0:
                print("Rules")
                print_dash()
                for rule in self.rules.keys():
                    print(rule)
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

        for option_name, option, in self._dict_items.items():
            if not option.has(values_dict[option_name]):
                raise pybamm.OptionError(
                    "Preset value: '"
                    + str(values_dict[option_name])
                    + "' for "
                    + option_name
                    + " is incompatible with the options"
                )

        self.check_rules()

        self.presets.update({name: values_dict})

    def load_preset(self, name):
        preset_dict = self.presets[name]
        for key, val in preset_dict.items():
            self[key] = val

    def add_rule(self, name, rule):
        """
        Method to add rules (constraints that cannot be violated)
        to prevent inconsistent options. A rule returns True when
        the options are inconsistent.

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

        if not isinstance(name, str):
            raise pybamm.OptionError("The name of the rule must be a str.")

        if not callable(rule):
            raise pybamm.OptionError("The rule must be a callable function.")

        self.check_rules(warn=True)

        self.rules[name] = rule

    def check_rules(self, warn=False):
        """
        Method to check whether the current set of rules are satisfied by
        the current set of options.
        """

        pybamm.logger.info("Checking model options are consistent.")

        for name, rule in self.rules.items():
            if rule(self):
                message = (
                    "The current options are incompatible according to: '" + name + "'"
                )
                if warn:
                    raise pybamm.OptionWarning(message)
                else:
                    raise pybamm.OptionError(message)
