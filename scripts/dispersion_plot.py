# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import glob
import re
from scipy.signal import find_peaks
import matplotlib as mpl
from pathlib import Path

# Plot formatting
mpl.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.5,
})
colors = ['#E69F00', '#56B4E9', '#009E73']
labels = ['$\Delta x = 2^{-6}$', '$\Delta x = 2^{-7}$', '$\Delta x = 2^{-8}$']
markers = ['o', 's', '^', 'D']
linestyles = ['-', '-.', ':']

# Function to assist with file sorting
def get_velocity(file):
    return float(re.search(r'_v([0-9.]+)_', file).group(1))

# Function to compute period from peaks
def compute_period(time, rho_max):
    peaks, _ = find_peaks(rho_max)
    peak_times = time[peaks]
    periods = np.diff(peak_times)

    return np.mean(periods)

# Input folder
base_dir = '../derived_data/extract_files'

# Import data
DF1 = glob.glob(f'{base_dir}/lvl6_rho1.0_P0.1_v*_noG.npz')
DF2 = glob.glob(f'{base_dir}/lvl7_rho1.0_P0.1_v*_noG.npz')
DF3 = glob.glob(f'{base_dir}/lvl8_rho1.0_P0.1_v*_noG.npz')

# Sort files by velocity
DF1 = sorted(DF1, key=get_velocity)
DF2 = sorted(DF2, key=get_velocity)
DF3 = sorted(DF3, key=get_velocity)

# Combine files
DF_list = [DF1, DF2, DF3]

# Output folder
out_dir = '../results/figures'

# Exact angular frequency
k = 2*np.pi/0.5
c_s = np.sqrt((5/3)*0.4/1)
omega_theory = np.sqrt((c_s * k)**2)

# Velocity array
V = np.array([0,1,2,4,8,16,32,64,128])

# Begin plot generation
fig, ax = plt.subplots(figsize=(6,4))

# Iterate through resolutions
for i, DF in enumerate(DF_list):

    # Define angular velocity array
    omega = np.array([])

    # Iterate through files for each resolution
    for f in DF:
        
        # Extract time and density data
        data = np.load(f, allow_pickle=True)
        time = data["time"]
        rho_max = data["rho_max"]

        # Sort data
        idx = np.argsort(time)
        time = time[idx]
        rho_max = rho_max[idx]

        # Measured angular frequency array
        T = compute_period(time, rho_max)
        omega = np.append(omega, 2*np.pi/T)

    # Curvefit data
    m, b = np.polyfit(V, omega, 1)
    V_fit = np.linspace(V[0], V[-1], 2000)

    # Plot angular velocity versus velocity data
    y_fit = m * V_fit + b
    ax.plot(V, omega, marker=markers[i], linestyle='none', color=colors[i], markersize=7, label=labels[i])
    ax.plot(V_fit, np.abs(y_fit), color=colors[i], linestyle=linestyles[i], alpha=0.9)

ax.axhline(omega_theory, linestyle='--', label='Expected $\omega$', color='black', linewidth=1.0)
ax.set_xlabel(r'Velocity $v_0$ [code units]')
ax.set_ylabel(r'Angular frequency $\omega$ [code units]')
ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.5)
ax.legend(frameon=False, loc='best')
ax.minorticks_on()
plt.tight_layout(pad=0.5)
plt.savefig(f'{out_dir}/dispersion.png', dpi=300)  
