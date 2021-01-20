from scipy.optimize import minimize, Bounds
import model as m
import numpy as np

if __name__ == '__main__':
    x0 = np.full(8, 0.1)

    s = 0.00001 #factor used to convert > to >=
    ineq_cons = {'type': 'ineq',
                'fun': lambda x: np.array([m.T/(m.mass_initial(x)*m.g) - 3 - s,
                                x[2]/x[1] - 4 - s,
                                np.pi*x[5]*(x[4]/2)**2 - x[0]*m.ratio_o2f - s,
                                np.pi*x[7]*(x[6]/2)**2 - x[0] - s,
                                x[2] - x[5] - 2*m.tank_thickness(x[4]),
                                x[2] - x[7] - 2*m.tank_thickness(x[6]),
                                x[1] - x[4] - x[6] - 2*m.tank_thickness(x[4])- 2*m.tank_thickness(x[6])])
                }

    bounds = Bounds(np.zeros(8), np.full(8, np.inf))

    res = minimize(m.func, x0, method='SLSQP', constraints=[ineq_cons], bounds=bounds, options={'ftol': 0.02,"eps": 1e-8, "disp": True})
    print(res)
    print('----------------------------------------')
    print("Constraints Valid:", ineq_cons['fun'](res.x) >= 0)
    print('----------------------------------------')

    delta_v = m.ideal_rocket(-res.fun)
    w_takeoff = m.mass_initial(res.x)*m.g
    m_dot = m.T/(m.Isp*m.g) #kg/s
    delta_m = m.mass_initial(res.x)-m.mass_final(res.x) #kg
    t_burn = delta_m/m_dot #s

    h_b = m.g*(-t_burn*m.Isp*np.log(-res.fun)/(-res.fun - 1) + t_burn*m.Isp - 1/2*t_burn**2)
    t_burnToMax = delta_v/m.g
    h_max = -1/2*m.g*t_burnToMax**2 + delta_v*t_burnToMax + h_b

    print('Delta-V:', delta_v, 'm/s')
    print('Take-off weight:', w_takeoff, 'N')
    print('Burn time:', t_burn, 's')
    print('Height at burnout:', h_b, 'm')
    print('Time to max height:', t_burn+t_burnToMax, 's')
    print('Max height:', h_max, 'm')
