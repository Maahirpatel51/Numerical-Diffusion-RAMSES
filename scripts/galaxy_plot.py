# Import libraries
import yt
from yt.units import kpc
import matplotlib.pyplot as plt
import numpy as np

# Input data
base_dir = '/home/maahir/links/scratch/vgal_sims/10417306'
ts = yt.DatasetSeries(f'{base_dir}/output_*/info_*.txt')

# Output folder
out_dir = '../results/animations/galaxy_frames'

# Iterate through RAMSES outputs
for i in range(len(ts)):

    # Select output
    ds = ts[i]

    # Region center
    center = yt.YTArray([0.5, 0.5, 0.5], 'code_length', registry=ts[0].unit_registry)

    # Set center in simulation units
    center[0] += ts[0].quan(12.5, 'kpc')
    center[1] += ts[0].quan(0, 'kpc')

    # Create projection plot 
    p = yt.ProjectionPlot(ds, 'z', 'Density', center=center, fontsize=20)
    p.set_cmap('Density', 'rainbow')
    p.set_unit('Density', 'Msun/pc**2')
    p.set_zlim('Density', 0.3, 80)
    p.set_width((60*kpc, 40*kpc))
    p.set_xlabel('')
    p.set_ylabel('')
    p.hide_axes()
    p.annotate_scale(coeff=5, unit='kpc', text_args={'size': 20}, size_bar_args={'color': 'black'}, pos=[0.2, 0.05])

    # Save snapshot to output folder
    p.save(f'{out_dir}/GSD_{i:04d}.png', mpl_kwargs={'dpi': 300})

    # Free memory
    del ds, p