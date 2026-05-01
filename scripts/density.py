# Import libraries
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl

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

# Import data
DF = 'lvl8_rho1.0_P0.1_v0_noG.npz'
data = np.load(f'../derived_data/extract_files/{DF}', allow_pickle=True)

# Output folder
out_dir = '../results/figures'

# Extract data
t = data['time']
rho_1d = data['rho_1d']

# Compute RMS density
rho_list = []
for i, rho in enumerate(rho_1d):
    rho_0 = np.mean(rho)
    drho = rho - rho_0
    rms = np.sqrt(np.mean(drho**2))
    rho_list.append(rms)

# Plot RMS density versus time
fig, ax = plt.subplots()
ax.plot(t, rho_list, color='#009E73')
ax.set_yscale('log')
ax.set_xlabel(r'Time $t$ [code units]')
ax.set_ylabel(r'Density $\rho$ [code units]')
ax.minorticks_on()
ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.5)
plt.tight_layout(pad=0.5)
fig.savefig(f'{out_dir}/RMS_density.png', dpi=300)