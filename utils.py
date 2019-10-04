# utils.py
# some tools 
import numpy as np
import pdb
import os

def getDiskName(datdir='/scratch/zdl3gk/mainProjects/DAlessioDisk/data', 
        Tstar=4000, Age=1, 
        Rdisk=300, dM=1e-9, alpha=0.001, amax=1, p=3.5):
    """ get the name of the file for disk properties based on the parameters
    datdir = str
        the directory where data is stored
    Tstar = 4000 [K]
        the star effective temperature
    Age = 1, 10 [Myr]
        the age of the star
    Rdisk = 300, 100	[AU]
        the radius of the disk
    dM = 1e-9, 1e-8, 1e-7, 1e-6 [Msun/yr]
        accretion rate
    alpha = 0.001, 0.01, 0.1
        viscosity parameter
    amax = 1, 10, 1e2, 1e3, 1e4, 1e5 [micron]
        maximum grain size
    p = 3.5, 2.5 
        size distribution
    """
    # determine directory
    fdir = os.path.join(datdir, 'T%d_%dmyr'%(Tstar, Age))

    # determine the specific name
    # grain size power-law
    if p == 3.5:
        plaw = 'p3p5'
    elif p == 2.5:
        plaw = 'p2p5'
    else:
        raise ValueError('poor input for p')

    # maximum grain size
    if amax == 1:
        asize = '1p0'
    elif amax == 10:
        asize = '10p0'
    elif amax == 1e2:
        asize = '100'
    elif amax == 1e3:
        asize = '1mm'
    elif amax == 1e4:
        asize = '1cm'
    elif amax == 1e5:
        asize = '10cm'
    else:
        raise ValueError('bad input for amax')

    # Rhole which depends on accretion rate
    if dM == 1e-6:
        Rhole = 22
    elif dM == 1e-7:
        Rhole = 11
    elif dM == 1e-8:
        Rhole = 9
    elif dM == 1e-9:
        Rhole = 9
    else:
        raise ValueError('bad input for dM')

    fname = ('prop.'+'rd%d.'%Rdisk + 'rh%d.'%Rhole + 'mp1em%d.'%abs(np.log10(dM)) + 
        'a0p01.irr.abpoll.' + '%s.'%plaw + 'amax%s.'%asize + 'h.dat')

    return os.path.join(fdir, fname)

def readDAlessio(fname):
    # reads D'Allesio disk. output in cgs
    au = 14960000000000.0

    nhdr = 8 #number of header lines
    phys = ['R', 'Tphot', 'Tc', 'Tirr', 'To', 'Tvis',
               'Sigma', 'H', 'Ztauss', 'Zinf', 'tau_r']
    unit = [au,       1.,   1.,     1.,   1.,     1.,
                   1.,    au,      au,      au,    1.]
    nelem = len(phys) # 11 physical elements
    num_lines = sum(1 for line in open(fname))
    nvec = num_lines - nhdr
    dat = np.zeros([nvec, nelem], dtype=np.float64)
    outdata = {}
    with open(fname, 'r') as rfile:
        # headers
        dum = rfile.readline().split() 		# Teff, Age,  M*, R*
        outdata['Teff'] = float(dum[2]) 	# [K]
        outdata['age'] = float(dum[5]) 		# [Myr]
        outdata['mstar'] = float(dum[8]) 	# [Msun]
        
        dum = rfile.readline() 			# separator #

        dum = rfile.readline().split() 		# Rdisk, Rhole
        outdata['Rdisk'] = float(dum[2]) * au
        outdata['Rhole'] = float(dum[5]) 	# [Rsun]

        dum = rfile.readline().split() 		# Mdot, alpha, Mass
        outdata['Mdot'] = float(dum[2]) 	# [Msun/year]
        outdata['alpha'] = float(dum[5])	
        outdata['mdisk'] = float(dum[7])	# [Msun]

        dum = rfile.readline().split() 		# p, amin, amax
        outdata['p'] = float(dum[2])
        outdata['amin'] = 0.005 		# [micron] seems always constant
        outdata['amax'] = float(dum[6])		# [micron]

        dum = rfile.readline() # separator #

        dum = rfile.readline() # column headers
        dum = rfile.readline() # separator #
        for ii in range(nvec):
            dum = rfile.readline().split()
            for jj in range(nelem):
                dat[ii,jj] = float(dum[jj])

    for ii in range(nelem):
        outdata.update({phys[ii]:unit[ii]*np.squeeze(10.**dat[:,ii])})

    return outdata


