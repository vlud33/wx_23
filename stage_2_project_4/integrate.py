import glob
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.constants import c, m_p, e
from scipy.optimize import minimize

# Global variable
x_data = None


def dataframe(path):
    """Fetch and convert raw data into a numpy array."""
    files = glob.glob('*.csv')
    # print(files)
    selected_file = files[0]
    global x_data
    x_time = np.linspace(-0.5, 10.5, 2200)
    x_data = x_time[2:] 
    input_data = pd.read_csv(selected_file)
    data = input_data.drop(columns=input_data.columns[0]).to_numpy()

    return data


def integrate_blm_data(blm_data):
    """Integrate data by bin."""
    integrated_data = []
    for blm in blm_data:
        blm_intg = scipy.integrate.cumulative_trapezoid(
            blm, x=np.linspace(-0.5, 10.5, 2200))
        blm_intg = np.diff(blm_intg)
        integrated_data.append(blm_intg)

    return integrated_data


def synchrotron_momentum(max_E, time):
    """Calculate synchrotron momentum."""
    mpeV = m_p * c**2 / e
    R0 = 26
    n_dip = 10
    dip_l = 4.4

    dip_angle = 2 * np.pi / n_dip
    rho = dip_l / dip_angle
    omega = 2 * np.pi * 50

    Ek = np.array([70, max_E]) * 1e6
    E = Ek + mpeV
    p = np.sqrt(E**2 - mpeV**2)

    B = p / c / rho

    Bdip = lambda t: (B[1] + B[0] - (B[1] - B[0]) * np.cos(omega * t)) / 2
    pdip = lambda t: Bdip(t) * rho * c

    return pdip(time*1E-3)


def synchrotron_kinetic_energy(max_E, time):
    """Convert time to energy."""
    mpeV = m_p * c**2 / e
    return (np.sqrt(synchrotron_momentum(max_E, time)**2 + mpeV**2) - mpeV) / 1E6


def divided_diff(x, y):
    """Calculate the divided differences table."""
    n = len(y)
    coef = np.zeros([n, n])
    coef[:, 0] = y

    for j in range(1, n):
        for i in range(n-j):
            coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j]-x[i])

    return coef


def newton_poly(coef, x_data, x):
    """Evaluate the newton polynomial at x."""
    n = len(x_data) - 1
    p = coef[n]
    for k in range(1, n+1):
        p = coef[n-k] + (x - x_data[n-k]) * p
    return p


def calibration_curve_beta(array):
    """Obtain array of calibration coefficient data on each value."""
    x = np.array([70, 172, 374, 617, 780])
    y = np.array([2.22E-13, 2.59E-13, 4.31E-12, 1.60E-11, 3.50E-11])

    a_s = divided_diff(x[1:], y[1:])[0, :]

    y_new = np.empty_like(array)

    for i, x_value in enumerate(array):
        if x_value < 70:
            y_new[i] = y[0]
        elif x_value < 172:
            y_new[i] = y[0] + (y[1] - y[0]) * (x_value - x[0]) / (x[1] - x[0])
        else:
            y_new[i] = newton_poly(a_s, x[1:], x_value)

    return y_new


def div_coef(y, coef):
    """Divide n*m BLM integration array by coefficient array."""
    result = []
    for row in y:
        stor = np.divide(row, coef)
        result.append(stor)
    return result


# Main execution
data = dataframe('C:/Users/ehh69283/Desktop/1g_colab/BLM_R5IM_Data/cycle/*.csv')
data = data[1:-1, :]
synchrotron_kinetic_energy_array = synchrotron_kinetic_energy(800, x_data)
# print(synchrotron_kinetic_energy_array)

coef = calibration_curve_beta(synchrotron_kinetic_energy_array)

plt.figure(1)
plt.plot(synchrotron_kinetic_energy_array, coef)
plt.title("Graph of coefficient against energy")
plt.xlabel("Energy/MeV")
plt.ylabel("Coefficient/V")

integration_volt = integrate_blm_data(data)
# print(f"The integral of the function is {integration_volt}")

for i, row in enumerate(integration_volt):
    plt.figure(2)
    plt.plot(x_data[:len(row)], row, label=f'Integration {i+1}')

plt.title("Integrated BLM in Volts by BLM")
plt.xlabel("Time/ms")
plt.ylabel("Beam loss/Volt")

integration_proton = div_coef(integration_volt, coef)
sum_integration_proton = np.sum(integration_proton, axis=0)
# print(f"The result is {integration_proton}")
# print(f"The sum of result is {sum_integration_proton}")

for row in integration_proton:
    plt.figure(3)
    plt.plot(x_data, row)
plt.title("Integrated BLM in proton by BLM")
plt.xlabel("Time/ms")
plt.ylabel("Beam loss/unit proton*s")

plt.figure(4)
plt.plot(x_data, sum_integration_proton)
plt.title('Integrated BLM in proton sum up')
plt.xlabel("Time/ms")
plt.ylabel("Beam loss/unit proton*s")

plt.show()
