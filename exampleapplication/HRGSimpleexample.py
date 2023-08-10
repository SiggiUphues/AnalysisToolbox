import numpy as np
import latqcdtools.base.logger as logger
from latqcdtools.physics.HRG import HRG
from latqcdtools.base.readWrite import readTable, writeTable
from latqcdtools.base.initialize import initialize, finalize

# Write terminal output to log file. Includes git commit hash.
initialize('HRG.log')

T = np.arange(120, 166, 0.5)

# Read in hadron names, masses, charges, baryon number, strangeness,
# charm, and degeneracy factor. This table is provided with LatticeToolbox.
hadrons, M, Q, B, S, C, g = readTable('QM_hadron_list_ext_strange_2020.txt',
                                      usecols=(0,1,2,3,4,5,6),
                                      dtype="U11,f8,i8,i8,i8,i8,i8")
w = np.array([1 if ba==0 else -1 for ba in B])

# choose a fixed muB / T value
muB_div_T = 0.3
# Instantiate HRG object.
QMhrg = HRG(M,g,w,B,S,Q,C)

# This computation is vectorized since T is a numpy array.
logger.info('Computing chi2B.')
chi = QMhrg.gen_chi(T, B_order=2, Q_order=0, S_order=0, C_order=0,
                    muB_div_T=muB_div_T, muQ_div_T=0, muS_div_T=0, muC_div_T=0)

# Output T and chi2B as columns in this table.
writeTable("chi2B.txt", T, chi, header=['T [MeV]','QM-HRG'])

finalize()
