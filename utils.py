# utils.py
# some tools 
import numpy as np
import pdb

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


