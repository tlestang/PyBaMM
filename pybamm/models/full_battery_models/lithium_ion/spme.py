#
# Single Particle Model with Electrolyte (SPMe)
#
import pybamm
from .base_lithium_ion_model import BaseModel


class SPMe(BaseModel):
    """Single Particle Model with Electrolyte (SPMe) of a lithium-ion battery, from
    [1]_.

    Parameters
    ----------
    name : str, optional
        The name of the model.

    References
    ----------
    .. [1] SG Marquis, V Sulzer, R Timms, CP Please and SJ Chapman. “An asymptotic
           derivation of a single particle model with electrolyte”. Journal of The
           Electrochemical Society, 166(15):A3693–A3706, 2019

    **Extends:** :class:`pybamm.lithium_ion.BaseModel`
    """

    def __init__(self, name="Single Particle Model with electrolyte"):
        super().__init__(name)
        pybamm.citations.register("marquis2019asymptotic")

    def reset_model(self):
        super().reset_model()

        self.set_external_circuit_submodel()
        self.set_reactions()
        self.set_porosity_submodel()
        self.set_tortuosity_submodels()
        self.set_convection_submodel()
        self.set_interfacial_submodel()
        self.set_particle_submodel()
        self.set_negative_electrode_submodel()
        self.set_electrolyte_submodel()
        self.set_positive_electrode_submodel()
        self.set_thermal_submodel()
        self.set_current_collector_submodel()

    def set_porosity_submodel(self):

        self.submodels["porosity"] = pybamm.porosity.Constant(self.param)

    def set_tortuosity_submodels(self):
        self.submodels["electrolyte tortuosity"] = pybamm.tortuosity.Bruggeman(
            self.param, "Electrolyte", True
        )
        self.submodels["electrode tortuosity"] = pybamm.tortuosity.Bruggeman(
            self.param, "Electrode", True
        )

    def set_convection_submodel(self):

        self.submodels["convection"] = pybamm.convection.NoConvection(self.param)

    def set_interfacial_submodel(self):

        self.submodels["negative interface"] = pybamm.interface.InverseButlerVolmer(
            self.param, "Negative", "lithium-ion main"
        )
        self.submodels["positive interface"] = pybamm.interface.InverseButlerVolmer(
            self.param, "Positive", "lithium-ion main"
        )

    def set_particle_submodel(self):

        if self.options["particle"] == "Fickian diffusion":
            self.submodels["negative particle"] = pybamm.particle.FickianSingleParticle(
                self.param, "Negative"
            )
            self.submodels["positive particle"] = pybamm.particle.FickianSingleParticle(
                self.param, "Positive"
            )
        elif self.options["particle"] == "fast diffusion":
            self.submodels["negative particle"] = pybamm.particle.FastSingleParticle(
                self.param, "Negative"
            )
            self.submodels["positive particle"] = pybamm.particle.FastSingleParticle(
                self.param, "Positive"
            )

    def set_negative_electrode_submodel(self):

        self.submodels["negative electrode"] = pybamm.electrode.ohm.Composite(
            self.param, "Negative"
        )

    def set_positive_electrode_submodel(self):

        self.submodels["positive electrode"] = pybamm.electrode.ohm.Composite(
            self.param, "Positive"
        )

    def set_electrolyte_submodel(self):

        electrolyte = pybamm.electrolyte.stefan_maxwell

        self.submodels["electrolyte conductivity"] = electrolyte.conductivity.Composite(
            self.param
        )
        self.submodels["electrolyte diffusion"] = electrolyte.diffusion.Full(
            self.param, self.reactions
        )

    @property
    def default_geometry(self):
        dimensionality = self.options["dimensionality"]
        if dimensionality == 0:
            return pybamm.Geometry("1D macro", "1D micro")
        elif dimensionality == 1:
            return pybamm.Geometry("1+1D macro", "(1+0)+1D micro")
        elif dimensionality == 2:
            return pybamm.Geometry("2+1D macro", "(2+0)+1D micro")
