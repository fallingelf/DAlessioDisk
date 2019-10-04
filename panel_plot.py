# panel_plot.py
# plot series of accretion rate
import numpy as np
import matplotlib.pyplot as plt
import zylconst
import utils
import os
import pdb

# ==== settings ====
datdir = 'data'

# properties to iterate
prop = [1e-9, 1e-8, 1e-7, 1e-6]	# accretion rate
tag = ['1e-9', '1e-8', '1e-7', 1e-6]
ndat = len(prop)

phys = ['Tc', 'Tvis', 'Tirr', 'H', 'Sigma'] # the physical keys to be plotted
nphys = len(phys)
ylog = [True, True, True, True, True]
yunit = [1, 1, 1, zylconst.AU, 1]

# ==== read ====
dat = []
for ii in range(ndat):
    dM = prop[ii]
    fname = utils.getDiskName(datdir=datdir, Tstar=4000, Age=1, 
        dM=dM, alpha=0.01, amax=10, p=3.5)

    dum = utils.readDAlessio(fname)
    dat.append(dum)

# ==== plotting ====
nrow = np.floor(np.sqrt(nphys))
ncol = np.ceil(nphys / nrow)
nrow, ncol = int(nrow), int(ncol)

fig = plt.figure(0, figsize=(4*ncol, 3*nrow))
for ii, iphys in enumerate(phys):
    ax = fig.add_subplot(nrow, ncol, ii+1)

    for jj, datii in enumerate(dat):
        ax.plot(datii['R']/zylconst.AU, datii[iphys]/yunit[ii], 
            label=tag[jj])

    ax.set_xlabel('R [AU]')
    ax.set_xscale('log')
    if ylog[ii]:
        ax.set_yscale('log')
    ax.set_title(iphys)
    ax.legend(loc='best')

fig.tight_layout()
plt.show()
