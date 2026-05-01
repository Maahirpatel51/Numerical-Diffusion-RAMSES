# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import glob
import pandas as pd 

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
colors = ['#000000', '#E69F00', '#56B4E9', '#009E73']
labels_resolution = ['$\Delta x = 2^{-5}$', '$\Delta x = 2^{-6}$', '$\Delta x = 2^{-7}$', '$\Delta x = 2^{-8}$']
labels_scale = [r'$k = 2\pi$', r'$k = 4\pi$', r'$k = 6\pi$', r'$k = 8\pi$']
markers = ['o', 's', '^', 'D']
linestyles = ['-', '--', '-.', ':']

# Output folder
out_dir = '../results/figures'

# Import resolution data
file1 = glob.glob('../derived_data/resolution_data/*.csv')

# Import scale data
file2 = glob.glob('../derived_data/scale_data/*.csv')

# Combine data files
DF1 = pd.concat((pd.read_csv(f) for f in file1), ignore_index=True)
DF2 = pd.concat((pd.read_csv(f) for f in file2), ignore_index=True)

# Convert to numpy arrays
M1 = DF1.iloc[:-1, 1:-1].to_numpy()
M2 = DF2.iloc[0:, 1:].to_numpy()

# Sort arrays
idx1 = np.argsort(M1[:, -1])
idx2 = np.argsort(M2[:, -1])
M1 = M1[idx1]
M2 = M2[idx2]

# Define velocity arrays
V1 = np.array([0,1,2,4,8,16,32,64])
V2 = np.array([0,1,2,4,8,16])

# Curvefit data
m1, b1 = np.polyfit(V1, M1.T, 1)
m2, b2 = np.polyfit(V2, M2.T, 1)
V_fit1 = np.linspace(V1[0], V1[-1], 2000)
V_fit2 = np.linspace(V2[0], V2[-1], 2000)

# Plot resolution-dependence
fig1, ax1 = plt.subplots(figsize=(6, 4))
for i in range(np.shape(M1)[0]):
    y_fit = m1[i] * V_fit1 + b1[i]
    ax1.plot(V1, np.abs(M1[i]), marker=markers[i], linestyle='none', color=colors[i], markersize=7, label=labels_resolution[i])
    ax1.plot(V_fit1, np.abs(y_fit), color=colors[i], linestyle=linestyles[i], alpha=0.9)

ax1.set_xlabel('Velocity $v_0$ [code units]')
ax1.set_ylabel('RMS density decay rate [code units]')
ax1.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.5)
ax1.legend(frameon=False, loc='best')
ax1.minorticks_on()
plt.tight_layout(pad=0.5)
plt.savefig(f'{out_dir}/diffusion_resolution.png')

# Plot scale-dependence
fig2, ax2 = plt.subplots(figsize=(6, 4))
for i in range(np.shape(M2)[0]):
    y_fit = m2[i] * V_fit2 + b2[i]
    ax2.plot(V2, np.abs(M2[i]), marker=markers[i], linestyle='none', color=colors[i], markersize=7, label=labels_scale[i])
    ax2.plot(V_fit2, np.abs(y_fit), color=colors[i], linestyle=linestyles[i], alpha=0.9)

ax2.set_xlabel('Velocity $v_0$ [code units]')
ax2.set_ylabel('RMS density decay rate [code units]')
ax2.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.5)
ax2.legend(frameon=False, loc='best')
ax2.minorticks_on()
plt.tight_layout(pad=0.5)
plt.savefig(f'{out_dir}/diffusion_scale.png')

