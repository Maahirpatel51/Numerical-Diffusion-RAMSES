# Import library
import os

# Input folder
base_dir = 'galaxy_frames/GSD_%04d.png'

# Output folder
out_dir = 'galaxy_sim.mp4'

# Execute terminal command
os.system(f'ffmpeg -framerate 30 -i ../results/animations/{base_dir} -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -c:v libx264 -pix_fmt yuv420p ../results/animations/{out_dir}')