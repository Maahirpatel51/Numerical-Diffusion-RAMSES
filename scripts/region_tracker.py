# Import libraries
import yt
import numpy as np
import matplotlib.pyplot as plt
from yt.units import kpc, Myr
from pathlib import Path

# Load data
base_dir = '...'
ts = yt.DatasetSeries(f'{base_dir}/output_*/info_*.txt')
ts = ts[15:65]

# Output folder
out_dir = '../results/animations/region_tracker_3'

# Initial conditions
R0 = 4 * kpc
R_local = 3.5 * kpc
theta0 = 0
omega = 35 / Myr
vx = 200 * (kpc / Myr)
t0 = ts[0].current_time

# Intital galaxy center from max density
center = ts[0].find_max('Density')[1].to('kpc')

# Iterate through RAMSES outputs
for i in range(0, len(ts), 1):
    
    # Select output
    ds = ts[i]

    # Update time
    dt = ds.quan(ds.current_time - t0, 'Myr')
    t0 = ds.current_time

    # Update theta
    theta0 += omega * dt

    # Update center
    center[0] += vx * dt

    # Compute offset 
    x_offset = R0 * np.cos(theta0)
    y_offset = R0 * np.sin(theta0)
    r_offset = np.sqrt(x_offset**2 + y_offset**2)

    # Galaxy center
    center_yt = ds.arr(center, 'kpc')

    # Region center
    center_local = ds.arr([center[0] + x_offset, center[1] + y_offset, center[2]], 'kpc')

    # Print variables
    if False:
        print('dt:', dt)
        print('theta0 (rad):', theta0)
        print('center:', center)
        print('x_offset:', x_offset)
        print('y_offset:', y_offset)
        print('r_offset:', r_offset)
        print('local center:', center_local)
        print('local radius:', R_local)

    # Define rectangular region
    LE = ds.arr(center_local - R_local)
    RE = ds.arr(center_local + R_local)
    sp = ds.region(center_local, LE, RE)

    # Plot markers
    if False:
        p = yt.ProjectionPlot(ds, 'z', 'Density', center=center_yt)
        p.set_width((30, 'kpc'))
        p.annotate_marker(center_local, coord_system='data', color='black', s=200)
        p.annotate_marker(center_yt, coord_system='data', color='blue', s=200)
        p.annotate_sphere(center_local, radius=(R_local, 'kpc'), circle_args={'color': 'green'})
        p.set_cmap('Density', 'rainbow')
        p.set_unit('Density', 'Msun/pc**2')
        p.set_zlim('Density', 0.1, 80)  
        p.hide_axes()
        p.save(f'{out_dir}/marker_{i:04d}.png', mpl_kwargs={'dpi': 300})
    
    # Plot galaxy region
    if True:
        p = yt.ProjectionPlot(ds, 'z', 'Density', data_source=sp, center=center_local)
        p.set_width(2 * R_local)
        p.set_cmap('Density', 'magma')
        p.set_unit('Density', 'Msun/pc**2')
        p.set_zlim('Density', 10, 200)  
        p.hide_axes()
        p.save(f'{out_dir}/region_{i:04d}.png', mpl_kwargs={'dpi': 300})

