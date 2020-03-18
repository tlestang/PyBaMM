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
        print_row("Option", "Current value", "Other values")
        print_dash()
        for option_name, option in self._dict_items.items():
            value_str = option.get_values_str()
            possible_values_str = option.get_possible_values_str()
            print_row(option_name, value_str, possible_values_str)
        print()

    def list_options(self):
        return list(self._dict_items.keys())

    def default_isothermal_coin_cell(self):
        self["dimensionality"] = 0
        self["surface form"] = False
        self["side reactions"] = []
        self["interfacial surface area"] = "constant"
        self["current collector"] = "uniform"
        self["particles"] = "Fickian diffusion"
        self["thermal"] = "isothermal"
        self["thermal current collector"] = False
        self["external submodels"] = []

    # def default_thermal_coin_cell(self):
    #     self.use_0D_current_collectors()
    #     self.use_standard_form()
    #     self.use_no_convection()
    #     self.use_no_side_reactions()
    #     self.use_constant_surface_area()
    #     self.use_uniform_current_collector()
    #     self.use_fickian_diffusion_in_particles()
    #     self.use_xyz_lumped_thermal_model()
    #     self.use_no_current_collector_thermal_effects()
    #     self.use_no_external_submodels()

    # def default_1_plus_1D_isothermal_pouch_cell(self):
    #     self.use_1D_current_collectors()
    #     self.use_standard_form()
    #     self.use_no_convection()
    #     self.use_no_side_reactions()
    #     self.use_constant_surface_area()
    #     self.use_potential_pair_current_collector()
    #     self.use_fickian_diffusion_in_particles()
    #     self.use_isothermal_model()
    #     self.use_no_current_collector_thermal_effects()
    #     self.use_no_external_submodels()

    # def default_1_plus_1D_thermal_pouch_cell(self):
    #     self.use_1D_current_collectors()
    #     self.use_standard_form()
    #     self.use_no_convection()
    #     self.use_no_side_reactions()
    #     self.use_constant_surface_area()
    #     self.use_potential_pair_current_collector()
    #     self.use_fickian_diffusion_in_particles()
    #     self.use_thermal_model()
    #     self.use_current_collector_thermal_effects()
    #     self.use_no_external_submodels()

    # def default_2_plus_1D_isothermal_pouch_cell(self):
    #     self.use_2D_current_collectors()
    #     self.use_standard_form()
    #     self.use_no_convection()
    #     self.use_no_side_reactions()
    #     self.use_constant_surface_area()
    #     self.use_potential_pair_current_collector()
    #     self.use_fickian_diffusion_in_particles()
    #     self.use_isothermal_model()
    #     self.use_no_current_collector_thermal_effects()
    #     self.use_no_external_submodels()

    # def default_2_plus_1D_thermal_pouch_cell(self):
    #     self.use_2D_current_collectors()
    #     self.use_standard_form()
    #     self.use_no_convection()
    #     self.use_no_side_reactions()
    #     self.use_constant_surface_area()
    #     self.use_potential_pair_current_collector()
    #     self.use_fickian_diffusion_in_particles()
    #     self.use_thermal_model()
    #     self.use_current_collector_thermal_effects()
    #     self.use_no_external_submodels()

    # # options information helpers
    # def info(self):
    #     self._print_row("Option", "Current value", "Other values")
    #     self._print_dash()
    #     self.current_collector_dimensionality
    #     self.surface_form
    #     self.convection
    #     self.side_reactions
    #     self.interfacial_surface_area
    #     self.current_collector_model_type
    #     self.particle
    #     self.thermal
    #     self.current_collector_thermal_effects
    #     self.external_submodels

    # def _print_row(self, option, value, other_values):
    #     print("{:<40s}{:<20s}{:<50s}".format(option, value, other_values))

    # def _print_dash(self):
    #     print("=" * 95)

    # # dimensionality helpers
    # @property
    # def current_collector_dimensionality(self):
    #     self._print_row(
    #         "Current collector dimensionality",
    #         str(self._model_options_dict["dimensionality"]),
    #         "[0, 1, 2]",

    # @current_collector_dimensionality.setter
    # def current_collector_dimensionality(self, dim):
    #     if dim not in [0, 1, 2]:
    #         raise pybamm.ModelError(
    #             "Current collector dimensionality must be either 0, 1, or, 2."
    #         )
    #     self._model_options_dict["dimensionality"] = dim

    # def use_0D_current_collectors(self):
    #     self._model_options_dict["dimensionality"] = 0

    # def use_1D_current_collectors(self):
    #     self._model_options_dict["dimensionality"] = 1

    # def use_2D_current_collectors(self):
    #     self._model_options_dict["dimensionality"] = 2

    # # surface form helpers
    # @property
    # def surface_form(self):
    #     self._print_row(
    #         "Surface form",
    #         str(self._model_options_dict["surface form"]),
    #         "[False, 'differential', 'algebraic']",
    #     )

    # @surface_form.setter
    # def surface_form(self, form):

    #     if form not in [False, "differential", "algebraic"]:
    #         raise pybamm.ModelError(
    #             "Model form must be either False, 'differential', or 'algebraic'"
    #         )

    #     self._model_options_dict["surface form"] = form

    # def use_standard_form(self):
    #     self._model_options_dict["surface form"] = False

    # def use_surface_form_with_capacitance(self):
    #     self._model_options_dict["surface form"] = "differential"

    # def use_surface_form_without_capacitance(self):
    #     self._model_options_dict["surface form"] = "algebraic"

    # # convection helpers
    # @property
    # def convection(self):
    #     print(
    #         "Convection:", self._model_options_dict["convection"],
    #     )
    #     self._print_row("Convection", str(self._model_options_dict), "")

    # @convection.setter
    # def convection(self, conv):

    #     if conv not in [False, True]:
    #         raise pybamm.ModelError("Convection must be either True or False")

    #     self._model_options_dict["convection"] = conv

    # def use_no_convection(self):
    #     self._model_options_dict["convection"] = False

    # def use_convection(self):
    #     self._model_options_dict["convection"] = True

    # # side reaction helpers
    # @property
    # def side_reactions(self):
    #     print(
    #         "Side reactions:", self._model_options_dict["side reactions"],
    #     )

    # @side_reactions.setter
    # def side_reactions(self, reactions):
    #     self._model_options_dict["side reactions"] = reactions

    # def use_no_side_reactions(self):
    #     self._model_options_dict["side reactions"] = []

    # # interfacial surface area helpers
    # @property
    # def interfacial_surface_area(self):
    #     print(
    #         "Interfacial surface area:",
    #         self._model_options_dict["interfacial surface area"],
    #     )

    # @interfacial_surface_area.setter
    # def interfacial_surface_area(self, setting):

    #     if setting == "varying":
    #         NotImplementedError("Varying interfacial surface area not yet implemented.")

    #     else:
    #         raise pybamm.ModelError(
    #             "Interfacial surface area must be either 'constant' or 'varying'."
    #         )

    #     self._model_options_dict["interfacial surface area"] = setting

    # def use_constant_surface_area(self):
    #     self._model_options_dict["interfacial surface area"] = "constant"

    # # current collector helpers
    # @property
    # def current_collector_model_type(self):
    #     print(
    #         "Current collector model type:",
    #         self._model_options_dict["current collector"],
    #     )

    # @current_collector_model_type.setter
    # def current_collector_model_type(self, model_type):

    #     if model_type not in [
    #         "uniform",
    #         "potential pair",
    #         "potential pair quite conductive",
    #     ]:
    #         raise pybamm.ModelError(
    #             "Current collector model type must be either:"
    #             + "'uniform', 'potential pair', or"
    #             + "'potential pair quite conductive'"
    #         )

    #     self._model_options_dict["current collector"] = model_type

    # def use_uniform_current_collector(self):
    #     self._model_options_dict["current collector"] = "uniform"

    # def use_potential_pair_current_collector(self):
    #     self._model_options_dict["current collector"] = "potential pair"

    # # particle helpers
    # @property
    # def particle(self):
    #     print(
    #         "Particle:", self._model_options_dict["particle"],
    #     )

    # @particle.setter
    # def particle(self, model_type):

    #     if model_type not in [
    #         "Fickian diffusion",
    #         "fast diffusion",
    #     ]:
    #         raise pybamm.ModelError(
    #             "Particle model must be either:"
    #             + " 'Fickian diffusion', or 'fast diffusion'"
    #         )

    #     self._model_options_dict["particle"] = model_type

    # def use_fickian_diffusion_in_particles(self):
    #     self._model_options_dict["particle"] = "Fickian diffusion"

    # def use_fast_diffusion_in_particles(self):
    #     self._model_options_dict["particle"] = "fast diffusion"

    # # thermal helpers
    # @property
    # def thermal(self):
    #     print(
    #         "Thermal model:", self._model_options_dict["thermal"],
    #     )

    # @thermal.setter
    # def thermal(self, model_type):

    #     if model_type not in [
    #         "isothermal",
    #         "x-full",
    #         "x-lumped",
    #         "xyz-lumped",
    #         "lumped",
    #     ]:
    #         raise pybamm.ModelError(
    #             "Thermal model must be either:"
    #             + "'isothermal'"
    #             + "'x-full'"
    #             + "'x-lumped'"
    #             + "'xyz-lumped'",
    #             +" or 'lumped'",
    #         )

    #     self._model_options_dict["thermal"] = model_type

    # def use_isothermal_model(self):
    #     self._model_options_dict["thermal"] = "isothermal"

    # def use_x_full_thermal_model(self):
    #     self._model_options_dict["thermal"] = "x-full"

    # def use_x_lumped_thermal_model(self):
    #     self._model_options_dict["thermal"] = "x-lumped"

    # def use_xyz_lumped_thermal_model(self):
    #     self._model_options_dict["thermal"] = "xyz-lumped"

    # def use_lumped_thermal_model(self):
    #     self._model_options_dict["thermal"] = "lumped"

    # # current collector thermal effects helpers
    # @property
    # def current_collector_thermal_effects(self):
    #     print(
    #         "Current collector thermal effects: ",
    #         self._model_options_dict["thermal current collector"],
    #     )

    # @current_collector_thermal_effects.setter
    # def current_collector_thermal_effects(self, value):

    #     if value not in [
    #         True,
    #         False,
    #     ]:
    #         raise pybamm.ModelError(
    #             "Current collector thermal model must be either: True, or False"
    #         )

    #     self._model_options_dict["thermal current collector"] = value

    # def use_no_current_collector_thermal_effects(self):
    #     self._model_options_dict["thermal current collector"] = False

    # def use_current_collector_thermal_effects(self):
    #     self._model_options_dict["thermal current collector"] = True

    # # external_submodel helpers
    # @property
    # def external_submodels(self):
    #     print(
    #         "External submodels:", self._model_options_dict["external submodels"],
    #     )

    # @external_submodels.setter
    # def external_submodels(self, submodels):
    #     self._model_options_dict["external submodels"] = submodels

    # def use_no_external_submodels(self):
    #     self._model_options_dict["external submodels"] = []

