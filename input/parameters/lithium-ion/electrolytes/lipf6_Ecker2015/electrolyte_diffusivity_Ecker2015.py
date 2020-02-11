from pybamm import exp


def electrolyte_diffusivity_Ecker2015(c_e, T, T_inf, E_D_e, R_g):
    """
    Diffusivity of LiPF6 in EC:DMC as a function of ion concentration [1, 2].

    References
    ----------
    .. [1] Ecker, Madeleine, et al. "Parameterization of a physico-chemical model of
    a lithium-ion battery i. determination of parameters." Journal of the
    Electrochemical Society 162.9 (2015): A1836-A1848.
    .. [2] Ecker, Madeleine, et al. "Parameterization of a physico-chemical model of
    a lithium-ion battery ii. model validation." Journal of The Electrochemical
    Society 162.9 (2015): A1849-A1857.
l

    Parameters
    ----------
    c_e: :class: `numpy.Array`
        Dimensional electrolyte concentration
    T: :class: `numpy.Array`
        Dimensional temperature
    T_inf: double
        Reference temperature
    E_D_e: double
        Electrolyte diffusion activation energy
    R_g: double
        The ideal gas constant

    Returns
    -------
    :`numpy.Array`
        Solid diffusivity
    """

    D_c_e = 2.4 * 10 ** (-10)
    arrhenius = exp(E_D_e / R_g * (1 / T_inf - 1 / T))

    return D_c_e * arrhenius
