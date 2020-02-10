import autograd.numpy as np


def electrolyte_conductivity_Capiglia1999(c_e, T, T_inf, E_k_e, R_g):
    """
    Conductivity of LiPF6 in EC:DMC as a function of ion concentration [1, 2].

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
    c_e: :class: `numpy.Array`
        Dimensional electrolyte concentration
    T: :class: `numpy.Array`
        Dimensional temperature
    T_inf: double
        Reference temperature
    E_k_e: double
        Electrolyte conductivity activation energy
    R_g: double
        The ideal gas constant

    Returns
    -------
    :`numpy.Array`
        Solid diffusivity
    """

    x = c_e / 1000

    # in mS / cm
    sigma_e = 2.667 * x ** 3 - 12.983 * x ** 2 + 17.919 * x + 1.726

    # convert to S / m
    sigma_e = sigma_e / 10

    # In Ecker paper there is factor of 1/T out the front but this doesn't
    # make much sense so just going to leave it out for now
    arrhenius = np.exp(E_k_e / R_g * (1 / T_inf - 1 / T))

    return sigma_e * arrhenius
