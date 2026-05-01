# Import libraries
import yt
import numpy as np 

# Enable parallelism
yt.enable_parallelism()
comm = yt.communication_system.communicators[-1]
rank = comm.rank

# RAMSES outputs -> yt dataseries
folder = '...'
base_dir = '...'
ts = yt.DatasetSeries(base_dir + folder + '/output_*/info_*.txt')

# Output file
out_file = '../derived_data/extract_files/....npz'

# Variable lists
t_list = []
rho_max_list = []
x_1d_list = []
rho_1d_list = []
vx_1d_list = []
P_1d_list = []

# Iterate through RAMSES outputs
for ds in ts.piter():
    ad = ds.all_data()
    line = ds.ray((0.0,0.5,0.5),(1.0,0.5,0.5))
    slc = ds.slice('z',0.5)

    x_1d = line['ramses','x'].to('code_length').v
    rho_1d = line['ramses','Density'].to('code_density').v
    vx_1d = line['ramses','x-velocity'].to('code_velocity').v
    P_1d = line['ramses','Pressure'].to('code_pressure').v

    t = ds.current_time.v
    rho_max = np.max(rho_1d)

    idx = np.argsort(x_1d)
    x_1d = x_1d[idx]
    rho_1d = rho_1d[idx]
    vx_1d = vx_1d[idx]
    P_1d = P_1d[idx]

    t_list.append(t)
    rho_max_list.append(rho_max)

    x_1d_list.append(x_1d)
    rho_1d_list.append(rho_1d)
    P_1d_list.append(P_1d)
    vx_1d_list.append(vx_1d)

t_all = comm.comm.gather(t_list, root=0)
rho_max_all = comm.comm.gather(rho_max_list, root=0)

x_1d_all = comm.comm.gather(x_1d_list, root=0)
rho_1d_all = comm.comm.gather(rho_1d_list, root=0)
P_1d_all = comm.comm.gather(P_1d_list, root=0)
vx_1d_all = comm.comm.gather(vx_1d_list, root=0)

# Group data
if rank == 0:
    time = np.concatenate(t_all)
    rho_max = np.concatenate(rho_max_all)

    x_1d = np.concatenate(x_1d_all, dtype=object)
    rho_1d = np.concatenate(rho_1d_all, dtype=object)
    P_1d = np.concatenate(P_1d_all, dtype=object)
    vx_1d = np.concatenate(vx_1d_all, dtype=object)

    idx = np.argsort(time)
    time = time[idx]
    rho_max = rho_max[idx]

    x_1d = x_1d[idx]
    rho_1d = rho_1d[idx]
    P_1d = P_1d[idx]
    vx_1d = vx_1d[idx]

    # Add data to output file
    np.savez(
        out_file,
        time=time,
        rho_max=rho_max,
        x_1d=x_1d,
        rho_1d=rho_1d,
        P_1d=P_1d,
        vx_1d=vx_1d
    )
