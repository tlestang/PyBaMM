from pybamm import exp
from pybamm import FunctionParameter


def graphite_diffusivity_Ecker2015(sto, T, T_inf, E_D_s, R_g):
    """
    Graphite diffusivity as a function of stochiometry [1, 2].

    References
    ----------
     .. [1] Ecker, Madeleine, et al. "Parameterization of a physico-chemical model of
    a lithium-ion battery i. determination of parameters." Journal of the
    Electrochemical Society 162.9 (2015): A1836-A1848.
    .. [2] Ecker, Madeleine, et al. "Parameterization of a physico-chemical model of
    a lithium-ion battery ii. model validation." Journal of The Electrochemical
    Society 162.9 (2015): A1849-A1857.

    Parameters
    ----------
    sto: :class: `numpy.Array`
        Electrode stochiometry
    T: :class: `numpy.Array`
        Dimensional temperature
    T_inf: double
        Reference temperature
    E_D_s: double
        Solid diffusion activation energy
    R_g: double
        The ideal gas constant

    Returns
    -------
    : double
        Solid diffusivity
   """

    D_ref = FunctionParameter("Measured negative electrode diffusivity [m2.s-1]", sto)
    arrhenius = exp(E_D_s / R_g * (1 / T_inf - 1 / T))

    return D_ref * arrhenius
