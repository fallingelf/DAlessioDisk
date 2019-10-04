# panel_plot.py
# plot series of accretion rate
import numpy as np
import matplotlib.pyplot as plt
import zylconst
import utils
import os

# ==== settings ====
datdir = 'data'

# properties to iterate
prop = [1e-9, 1e-8, 1e-7, 1e-6]	# accretion rate
tag = ['1e-9', '1e-8', '1e-7', 1e-6]
ndat = len(prop)

phys = ['Tvis', 'Tirr','H','Sigma'] # the physical keys to be plotted
nphys = len(phys)
ylog = [True, True]
yunit = [1, 1, zylconst.AU, 1]

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
for ii in range(nphys):
    ax = fig.add_subplot(nrow, ncol, ii+1)
    for idat in range(ndat):
        datii = dat[idat]
        ax.plot(datii['R']/zylconst.AU, datii[phys[ii]]/yunit[idat], 
            label=tag[idat])
        ax.set_xlabel('R [AU]')
        ax.set_xscale('log')
        if ylog[idat]:
            ax.set_yscale('log')
    ax.set_title(phys[ii])

fig.tight_layout()
plt.show()
