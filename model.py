import numpy as np

# CONSTANTS
m_payload = 10 #kg (payload mass)
T = 10000 #N (thrust)
ratio_o2f = 2.5 #(O2 to Fuel ratio - volume)
Isp = 250 #s (specific impulse)
m_engine = 15 #kg (engine mass)
P_tank = 2.5*10**6 #Pa (tank pressure)
rho_ox = 1141 #kg/m^3 (density liquid O2)
rho_fuel = 810 #kg/m^3 (density kerosene)
g = 9.81 #m/s^2 (gravity constant)
t_b = 2*10**-3 #m (body thickness)
rho_cone = 1410 #kg/m^3 (cone shell density)
rho_tank = 1410 #kg/m^3 (tank density)
sigma_tank = 919*10**6 #N/m^2 (tank yield strength)

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
    # return -ideal_rocket(m_0/m_f)
    return -(m_0/m_f)

def ideal_rocket(m_ratio):
    return Isp*g*np.log(m_ratio)

# Final Mass of Rocket (after fuel expended)
def mass_final(x):
    m_oxTank = tank_mass(x[4], x[5])
    m_fuelTank = tank_mass(x[6], x[7])

    m_f = m_engine + m_payload + \
            m_fuelTank + m_oxTank + \
            np.pi*t_b*x[1]*x[2] + np.pi*t_b*x[1]*x[3]/2*rho_cone
    return m_f

# Takeoff Mass of Rocket
def mass_initial(x):
    m_f = mass_final(x)
    V_ox = 2.5*x[0]
    m_0 = m_f + rho_ox*V_ox + rho_fuel*x[0]
    return m_0

# Tank mass
def tank_mass(d, l):
    t = tank_thickness(d)
    return (2*np.pi*(d/2)**2 + np.pi*d*l)*t*rho_tank

# Tank wall thickness
def tank_thickness(d):
    return (d/2)*P_tank/(2*sigma_tank*np.sqrt(3))

if __name__ == '__main__':
    # x = np.random.rand(8)
    x = np.full(8, 0.2)

    deltaV = func(x)
    print(deltaV)
