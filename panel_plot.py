# panel_plot.py
# some plots
import numpy as np
import matplotlib.pyplot as plt
import zylconst
import utils
import os

# ==== settings ====
datadir = 'data'

datname = ['prop.rd300.rh11.mp1em8.a0p01.irr.abpoll.p3p5.amax100.h.dat']
tag = ['1']
ndat = len(datname)

phys = ['Tvis', 'Tirr','H','Sigma'] # the physical keys to be plotted
nphys = len(phys)
ylog = [True, True]
yunit = [1, 1, zylconst.AU, 1]

# ==== read ====
dat = []
for ii in range(ndat):
    fname = os.path.join(datadir, datname[ii])
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
