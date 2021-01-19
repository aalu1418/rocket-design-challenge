import numpy as np
import constants as const

# OBJECTIVE FUNCTION
#parameters
# 0: V_fuel (fuel/kerosene volume)
# 1: d_B (body diameter)
# 2: l_B (body length)
# 3: l_c (fairing/cone length)
# 4: d_ox (oxygen tank diameter)
# 5: l_ox (oxygen tank length)
# 6: d_fuel (kerosene tank diameter)
# 7: l_fuel (kerosene tank length)
def func(x):
    m_f = mass_final(x)
    m_0 = mass_initial(x)

    return const.Isp*const.g*np.log(m_0/m_f)

# Final Mass of Rocket (after fuel expended)
def mass_final(x):
    m_oxTank = tank_mass(x[4], x[5])
    m_fuelTank = tank_mass(x[6], x[7])

    m_f = const.m_engine + const.m_payload + \
            m_fuelTank + m_oxTank + \
            np.pi*const.t_b*x[1]*x[2] + np.pi*const.t_b*x[1]/2*const.rho_cone
    return m_f

# Takeoff Mass of Rocket
def mass_initial(x):
    m_f = mass_final(x)
    V_ox = 2.5*x[0]
    m_0 = m_f + const.rho_ox*V_ox + const.rho_fuel*x[0]
    return m_0

# Tank mass
def tank_mass(d, l):
    t = tank_thickness(d)
    return (2*np.pi*(d/2)**2 + np.pi*d/2*l)*t*const.rho_tank

# Tank wall thickness
def tank_thickness(d):
    return (d/2)*const.P_tank/(2*const.sigma_tank*np.sqrt(3))

if __name__ == '__main__':
    x = np.random.rand(8)
    deltaV = func(x)
    print(deltaV)
