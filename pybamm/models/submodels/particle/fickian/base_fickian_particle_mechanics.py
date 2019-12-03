#
# Base class for particles with Fickian diffusion
#
import pybamm

from ..base_particle import BaseParticle


class BaseModel(BaseParticle):
    """Base class for molar conservation in particles which employ Fick's law.

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    domain : str
        The domain of the model either 'Negative' or 'Positive'

    * Should find a proper place to add the following mechanics parameters 
    * values are from Journal of The Electrochemical Society, 2020 167 013512 [DOI: 10.1149/2.0122001JES]
    param.mechanics=1   # flag: 1 - activate mechanical effects; 0 - ignore
    param.nu_p=0.2  # Poisson's ratio for cathode
    param.E_p=375e9 # Young's modulus for cathode [GPa]
    param.c_p_0 # Reference concentration when cathode particle is free of stress 
    param.Omega_p= -7.28e-7 # Partial molar volume for cathode, Dimentionless 
    param.theta_p= param.Omega_p**2/param.R*2/9*param.E_p*(1-param.nu_p) # intermediate variable  [K*m^3/mol]
    param.nu_n=0.3  # Poisson's ratio for anode
    param.E_n=15e9 # Young's modulus for anode [GPa]
    param.c_n_0 # Reference concentration when anode particle is free of stress, Dimentionless 
    param.Omega_n= 3.1e-6 # Partial molar volume for anode [m^3/mol]
    param.theta_n= param.Omega_n**2/param.R*2/9*param.E_n*(1-param.nu_n) # intermediate variable  [K*m^3/mol]

    **Extends:** :class:`pybamm.particle.BaseParticle`
    """

    def __init__(self, param, domain):
        super().__init__(param, domain)

    def _flux_law(self, c, T):

        if self.domain == "Negative":
            # dimentionless intermediate variable  
            theta=self.param.mechanics*self.param.theta_p*self.param.c_p_max/T
            c0=self.param.c_p_0
            D = self.param.D_n(c, T)*(1+theta*(c-c0))
        elif self.domain == "Positive":
            # dimentionless intermediate variable  
            theta=self.param.mechanics*self.param.theta_n*self.param.c_n_max/T
            c0=self.param.c_n_0
            D = self.param.D_p(c, T)*(1+theta*(c-c0))

        return -D * pybamm.grad(c)

    def _unpack(self, variables):
        raise NotImplementedError

    def set_rhs(self, variables):

        c, N, _ = self._unpack(variables)

        if self.domain == "Negative":
            self.rhs = {c: -(1 / self.param.C_n) * pybamm.div(N)}

        elif self.domain == "Positive":
            self.rhs = {c: -(1 / self.param.C_p) * pybamm.div(N)}

    def set_boundary_conditions(self, variables):

        c, _, j = self._unpack(variables)

        if self.domain == "Negative":
            rbc = -self.param.C_n * j / self.param.a_n

        elif self.domain == "Positive":
            rbc = -self.param.C_p * j / self.param.a_p / self.param.gamma_p

        self.boundary_conditions = {
            c: {"left": (pybamm.Scalar(0), "Neumann"), "right": (rbc, "Neumann")}
        }
