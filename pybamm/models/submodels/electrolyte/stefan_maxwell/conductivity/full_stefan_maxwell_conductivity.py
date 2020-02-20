#
# Class for electrolyte conductivity employing stefan-maxwell
#
import pybamm

from .base_stefan_maxwell_conductivity import BaseModel


class Full(BaseModel):
    """Full model for conservation of charge in the electrolyte employing the
    Stefan-Maxwell constitutive equations. (Full refers to unreduced by
    asymptotic methods)

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    reactions : dict
        Dictionary of reaction terms

    **Extends:** :class:`pybamm.BaseStefanMaxwellConductivity`
    """

    def __init__(self, param, reactions):
        super().__init__(param, reactions=reactions)

    def get_fundamental_variables(self):
        phi_e = pybamm.standard_variables.phi_e
        phi_e_av = pybamm.x_average(phi_e)

        variables = self._get_standard_potential_variables(phi_e, phi_e_av)
        return variables

    def get_coupled_variables(self, variables):
        param = self.param
        T = variables["Cell temperature"]
        T_av = variables["X-averaged cell temperature"]
        tor = variables["Electrolyte tortuosity"]
        c_e = variables["Electrolyte concentration"]
        i_boundary_cc_0 = variables["Leading-order current collector current density"]
        c_e_n, c_e_s, c_e_p = c_e.orphans
        c_e_av = pybamm.x_average(c_e)
        phi_e = variables["Electrolyte potential"]
        chi_av = param.chi(c_e_av)
        i_e = (param.kappa_e(c_e, T) * tor * param.gamma_e / param.C_e) * (
            param.chi(c_e) * (1 + param.Theta * T) * pybamm.grad(c_e) / c_e
            - pybamm.grad(phi_e)
        )
        # concentration overpotential
        eta_c_av = (
            chi_av
            * (1 + param.Theta * T_av)
            * (
                pybamm.x_average(c_e_p / c_e_av)
                - pybamm.x_average(c_e_n / c_e_av)
            )
        )
        tor_n_av = variables["X-averaged negative electrolyte tortuosity"]
        tor_s_av = variables["X-averaged separator tortuosity"]
        tor_p_av = variables["X-averaged positive electrolyte tortuosity"]
        # bulk conductivities
        kappa_n_av = param.kappa_e(c_e_av, T_av) * tor_n_av
        kappa_s_av = param.kappa_e(c_e_av, T_av) * tor_s_av
        kappa_p_av = param.kappa_e(c_e_av, T_av) * tor_p_av
        # average electrolyte ohmic losses
        delta_phi_e_av = -(param.C_e * i_boundary_cc_0 / param.gamma_e) * (
            param.l_n / (3 * kappa_n_av)
            + param.l_s / (kappa_s_av)
            + param.l_p / (3 * kappa_p_av)
        )
        variables.update(self._get_standard_current_variables(i_e))
        variables.update(self._get_split_overpotential(eta_c_av, delta_phi_e_av))

        return variables

    def set_algebraic(self, variables):
        phi_e = variables["Electrolyte potential"]
        i_e = variables["Electrolyte current density"]
        sum_j = sum(
            pybamm.Concatenation(
                variables[reaction["Negative"]["aj"]],
                pybamm.FullBroadcast(0, "separator", "current collector"),
                variables[reaction["Positive"]["aj"]],
            )
            for reaction in self.reactions.values()
        )

        self.algebraic = {phi_e: pybamm.div(i_e) - sum_j}

    def set_initial_conditions(self, variables):
        phi_e = variables["Electrolyte potential"]
        T_init = self.param.T_init
        self.initial_conditions = {
            phi_e: -self.param.U_n(self.param.c_n_init(0), T_init)
        }
