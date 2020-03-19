#
# Lithium-ion base model class
#
import pybamm


class BaseModel(pybamm.BaseBatteryModel):
    """
    Overwrites default parameters from Base Model with default parameters for
    lithium-ion models

    **Extends:** :class:`pybamm.BaseBatteryModel`

    """

    def __init__(self, name="Unnamed lithium-ion model"):
        super().__init__(name)
        self.param = pybamm.standard_parameters_lithium_ion

        # Default timescale is discharge timescale
        self.timescale = self.param.tau_discharge
        self.set_standard_output_variables()

    def reset_options(self):
        "Default options for lithium-ion models"

        dimensionality = pybamm.Option("dimensionality", 0, [0, 1, 2])

        current_collector = pybamm.Option(
            "current collector", "uniform", ["uniform", "potential pair"]
        )

        particle = pybamm.Option(
            "particle", "Fickian diffusion", ["Fickian diffusion", "fast diffusion"]
        )

        thermal = pybamm.Option(
            "thermal", "isothermal", ["isothermal", "x-full", "x-lumped", "xyz-lumped"]
        )

        thermal_cc = pybamm.Option("thermal current collector", False, [True, False])

        external_submodels = pybamm.Option("external submodels", [], [])

        self.options = pybamm.ModelOptions(
            dimensionality,
            current_collector,
            particle,
            thermal,
            thermal_cc,
            external_submodels,
        )

        # some presets
        self.options.add_preset(
            "isothermal coin cell",
            {
                "dimensionality": 0,
                "current collector": "uniform",
                "particle": "Fickian diffusion",
                "thermal": "isothermal",
                "thermal current collector": False,
                "external submodel": [],
            },
        )

        self.options.add_preset(
            "thermal coin cell",
            {
                "dimensionality": 0,
                "current collector": "uniform",
                "particle": "Fickian diffusion",
                "thermal": "x-lumped",
                "thermal current collector": False,
                "external submodel": [],
            },
        )

        self.options.add_preset(
            "1+1D isothermal pouch cell",
            {
                "dimensionality": 1,
                "current collector": "potential pair",
                "particle": "Fickian diffusion",
                "thermal": "isothermal",
                "thermal current collector": False,
                "external submodel": [],
            },
        )

        self.options.add_preset(
            "1+1D thermal pouch cell",
            {
                "dimensionality": 1,
                "current collector": "potential pair",
                "particle": "Fickian diffusion",
                "thermal": "thermal",
                "thermal current collector": True,
                "external submodel": [],
            },
        )

        self.options.add_preset(
            "2+1D isothermal pouch cell",
            {
                "dimensionality": 2,
                "current collector": "potential pair",
                "particle": "Fickian diffusion",
                "thermal": "isothermal",
                "thermal current collector": False,
                "external submodel": [],
            },
        )

        self.options.add_preset(
            "2+1D thermal pouch cell",
            {
                "dimensionality": 2,
                "current collector": "potential pair",
                "particle": "Fickian diffusion",
                "thermal": "thermal",
                "thermal current collector": True,
                "external submodel": [],
            },
        )

    def set_options(
        self,
        preset=None,
        dimensionality=None,
        current_collector=None,
        particle=None,
        thermal=None,
        thermal_current_collector=None,
        external_submodels=None,
    ):
        """
        Function to set model options.

        Parameters
        ----------
        preset: str
            Name of the preset options to use. If you enter another option,
            the value in the preset will be overwritten with the value of the
            other option. Can be: 'isothermal coin cell', 'thermal coin cell',
            '1+1D isothermal pouch cell', "1+1D thermal pouch cell',
            '2+1D isothermal pouch cell' , "2+1D thermal pouch cell'.
        dimensionality : int, optional
            Sets the dimension of the current collector problem. Can be 0
            (default), 1 or 2.
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

        if preset:
            self.options.load_preset(preset)

        if dimensionality:
            self.options["dimensionality"] = dimensionality
        if current_collector:
            self.options["current collector"] = current_collector
        if particle:
            self.options["particle"] = particle
        if thermal:
            self.options["thermal"] = thermal
        if thermal_current_collector:
            self.options["thermal current collector"] = thermal_current_collector
        if external_submodels:
            self.options["external submodels"] = external_submodels

    def set_standard_output_variables(self):
        super().set_standard_output_variables()

        # Particle concentration position
        var = pybamm.standard_spatial_vars
        param = pybamm.geometric_parameters
        self.variables.update(
            {
                "r_n": var.r_n,
                "r_n [m]": var.r_n * param.R_n,
                "r_p": var.r_p,
                "r_p [m]": var.r_p * param.R_p,
            }
        )

    def set_reactions(self):

        # Should probably refactor as this is a bit clunky at the moment
        # Maybe each reaction as a Reaction class so we can just list names of classes
        icd = " interfacial current density"
        self.reactions = {
            "main": {
                "Negative": {
                    "s": 1 - self.param.t_plus,
                    "aj": "Negative electrode" + icd,
                },
                "Positive": {
                    "s": 1 - self.param.t_plus,
                    "aj": "Positive electrode" + icd,
                },
            }
        }
