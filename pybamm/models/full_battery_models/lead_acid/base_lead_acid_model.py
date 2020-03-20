#
# Lead acid base model class
#

import pybamm


class BaseModel(pybamm.BaseBatteryModel):
    """
    Overwrites default parameters from Base Model with default parameters for
    lead-acid models


    **Extends:** :class:`pybamm.BaseBatteryModel`

    """

    def __init__(self, options=None, name="Unnamed lead-acid model"):
        super().__init__(options, name)

    def reset_model(self):
        super().reset_model()
        self.param = pybamm.standard_parameters_lead_acid
        # Default timescale is discharge timescale
        self.timescale = self.param.tau_discharge
        self.set_standard_output_variables()

    def reset_options(self):
        "Default options for lead acid models"

        std_opt = pybamm.standard_model_options

        current_collector = pybamm.Option(
            "current collector",
            "uniform",
            ["uniform", "potential pair", "potential pair quite conductive"],
        )

        self.options = pybamm.ModelOptions(
            std_opt.operating_mode,
            std_opt.dimensionality,
            std_opt.surface_form,
            std_opt.side_reactions,
            std_opt.convection,
            current_collector,
            std_opt.thermal,
            std_opt.external_submodels,
        )

        # rules for incompatible options
        self.options.add_rule(
            "Thermal models only available for dimensionality = 0",
            lambda x: x["thermal"] != "isothermal" and x["dimensionality"] != 0,
        )

        self.options.add_preset(
            "1D isothermal cell",
            {
                "opterating mode": "current",
                "dimensionality": 0,
                "surface form": False,
                "side reactions": [],
                "convection": False,
                "current collector": "uniform",
                "thermal": False,
                "external submodels": [],
            },
        )

        self.options.add_preset(
            "1D thermal cell",
            {
                "opterating mode": "current",
                "dimensionality": 0,
                "surface form": False,
                "side reactions": [],
                "convection": False,
                "current collector": "uniform",
                "thermal": True,
                "external submodels": [],
            },
        )

    def options_set(
        self,
        preset=None,
        operating_mode=None,
        dimensionality=None,
        surface_form=None,
        side_reactions=None,
        current_collector=None,
        thermal=None,
        external_submodels=None,
        build=True,
    ):
        """
        Function to set model options.

        Parameters
        ----------
        preset: str, optional
            Name of the preset options to use. If you enter another option,
            the value in the preset will be overwritten with the value of the
            other option. Can be: '1D isothermal cell', '1D thermal cell',
        operating_mode: str, optional
            The operating mode of the system. Can be 'current', 'power', or
            'voltage'.
        dimensionality : int, optional
            Sets the dimension of the current collector problem. Can be 0
            (default), 1 or 2.
        surface_form: bool or str
            Whether to use the surface formulation of the model. Can be:
            False (bool), 'differential', or 'algebraic'.
        side_reactions: list, optional
            List of the side reactions (str) to activate.
        current collector : str, optional
            Sets the current collector model to use. Can be "uniform" (default),
            "potential pair" or "potential pair quite conductive".
        thermal : str, optional
            Sets the thermal model to use. Can be "isothermal" (default),
            "x-full", "x-lumped", "xyz-lumped" or "lumped".
        external submodels : list
            A list of the submodels that you would like to supply an external
                variable for instead of solving in PyBaMM. The entries of the lists
                are strings that correspond to the submodel names in the keys
                of `self.submodels`.
        build: bool
            Whether to rebuild the model after setting options.
        """

        if preset:
            self.options.load_preset(preset)

        if dimensionality:
            self.options["dimensionality"] = dimensionality
        if current_collector:
            self.options["current collector"] = current_collector
        if side_reactions:
            self.options["side reactions"] = side_reactions
        if thermal:
            self.options["thermal"] = thermal
        if external_submodels:
            self.options["external submodels"] = external_submodels

        if build:
            self.build_model()

    @property
    def default_parameter_values(self):
        return pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Sulzer2019)

    @property
    def default_geometry(self):
        if self.options["dimensionality"] == 0:
            return pybamm.Geometry("1D macro")
        elif self.options["dimensionality"] == 1:
            return pybamm.Geometry("1+1D macro")
        elif self.options["dimensionality"] == 2:
            return pybamm.Geometry("2+1D macro")

    @property
    def default_var_pts(self):
        # Choose points that give uniform grid for the standard parameter values
        var = pybamm.standard_spatial_vars
        return {var.x_n: 25, var.x_s: 41, var.x_p: 34, var.y: 10, var.z: 10}

    @property
    def default_solver(self):
        """
        Return default solver based on whether model is ODE model or DAE model.
        There are bugs with KLU on the lead-acid models.
        """
        if len(self.algebraic) == 0:
            return pybamm.ScipySolver()
        elif pybamm.have_scikits_odes():
            return pybamm.ScikitsDaeSolver()
        else:  # pragma: no cover
            return pybamm.CasadiSolver(mode="safe")

    def set_reactions(self):

        # Should probably refactor as this is a bit clunky at the moment
        # Maybe each reaction as a Reaction class so we can just list names of classes
        param = self.param
        icd = " interfacial current density"
        self.reactions = {
            "main": {
                "Negative": {"s": param.s_n, "aj": "Negative electrode" + icd},
                "Positive": {"s": param.s_p, "aj": "Positive electrode" + icd},
            }
        }
        if "oxygen" in self.options["side reactions"]:
            self.reactions["oxygen"] = {
                "Negative": {
                    "s": -(param.s_plus_Ox + param.t_plus),
                    "s_ox": -param.s_ox_Ox,
                    "aj": "Negative electrode oxygen" + icd,
                },
                "Positive": {
                    "s": -(param.s_plus_Ox + param.t_plus),
                    "s_ox": -param.s_ox_Ox,
                    "aj": "Positive electrode oxygen" + icd,
                },
            }
            self.reactions["main"]["Negative"]["s_ox"] = 0
            self.reactions["main"]["Positive"]["s_ox"] = 0

    def set_soc_variables(self):
        "Set variables relating to the state of charge."
        # State of Charge defined as function of dimensionless electrolyte concentration
        soc = self.variables["X-averaged electrolyte concentration"] * 100
        self.variables.update({"State of Charge": soc, "Depth of Discharge": 100 - soc})

        # Fractional charge input
        if "Fractional Charge Input" not in self.variables:
            fci = pybamm.Variable("Fractional Charge Input", domain="current collector")
            self.variables["Fractional Charge Input"] = fci
            self.rhs[fci] = -self.variables["Total current density"] * 100
            self.initial_conditions[fci] = self.param.q_init * 100
