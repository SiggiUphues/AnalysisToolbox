# 
# denseObs.py                                                               
# 
# D. Clarke
# 
# Methods to turn output from C. Schmidt's dense code into observables.
# 

import numpy as np
import latqcdtools.base.logger as logger
from latqcdtools.base.readWrite import writeTable
from latqcdtools.base.check import checkType, checkDomain


_allowed_observables = ["confID",
                        "Nl", "NB", "NQ", "NS", "NI",
                        "dN/dmul", "dN/dmus", "dN/dmuB", "dN/dmuQ", "dN/dmuS", "dN/dmuI",
                        "Nl^2", "NB^2", "NQ^2", "NS^2",
                        "chi2l", "chi2s", "chi11ll", "chi11ls", "chi2B", "chi2Q"]


class observablesOfInterest(list):

    """ A class to specify the dense observables you want to look at. It contains some consistency checks, like making
    sure that you don't add an observable that is not yet computable. It also has some attributes that help streamline
    using methods like np.genfromtxt. """


    def __init__(self,iterable=None):
        if iterable is None:
            iterable = _allowed_observables
        super().__init__(iterable)
        checkType(iterable,list)
        for item in iterable:
            checkDomain(item,_allowed_observables)
        if not iterable[0] == "confID":
            logger.TBError('observablesOfInterest[0] must be confID.')
        self.dtypes=('U12',)
        for item in range(1,len(iterable)):
            self.dtypes += (float,float,)


    def __repr__(self) -> str:
        return "observablesOfInterest"


    def getCol(self,part,obs):
        """ op_to_obs will give back complex numbers, which are then output to a table. Given an observable obs with
        real or imaginary part part, getCol returns the column index. """
        checkDomain(obs,_allowed_observables)
        if obs=="confID":
            return 0
        if part == "Re":
            return 2*self.index(obs)-1
        elif part == "Im":
            return 2*self.index(obs)
        else:
            logger.TBError('part must be Re or Im. Got', part)


def mean_square(vec):
    """ Unbiased calculation of < vec**2 >. """
    N = len(vec)
    return ( np.sum(vec)**2 - np.sum(vec**2) )/( N*(N-1))


def op_to_obs(opTable,lp,obs=None,filename='denseObservables.d'):

    """ Take the operators from loadDens and combine them into physically meaningful observables. Some terminology:
        l--light
        s--strange
        B--baryon number
        Q--electric charge
        I--isospin
        S--strangeness

    Parameters
    ----------
    opTable : dict
        A table indexed by confID. Its values are a list of operators that have been measured.
    lp : latticeParams
        Parameters for the ensemle the configuration belongs to.
    obs : observablesOfInterest, optional
        A list of the observables you want to compute.
    filename : str, optional
        Name for output table.
    """

    # Initialize
    if obs is None:
        obs = observablesOfInterest()
    vol4     = lp.vol4
    mu       = lp.mu
    outTable = {}
    for observable in _allowed_observables:
        outTable[observable] = []

    # Construct the output table
    for cID in opTable:

        if len(cID) != len(cID.strip()):
            logger.TBError('confIDs must not have whitespace! This throws off the column indexing.')

        nlVec=np.array(opTable[cID][0]) 
        nsVec=np.array(opTable[cID][1])
        numVec_l=len(nlVec)
        numVec_s=len(nsVec)

        if not numVec_l==numVec_s:
            logger.warn("Unexpected numVec for nf, cID = "+cID+"... skipping")
            continue

        nl2Vec=np.array(opTable[cID][2])  # tr ( M^-1 d M )^2
        ns2Vec=np.array(opTable[cID][3])
        numVec_l2=len(nl2Vec)
        numVec_s2=len(ns2Vec)

        if not numVec_l2==numVec_s2:
            logger.warn("Unexpected numVec for nf**2, cID = "+cID+"... skipping")
            continue

        MddMlVec=np.array(opTable[cID][4])
        MddMsVec=np.array(opTable[cID][5])
        numVec_Ml=len(MddMlVec)
        numVec_Ms=len(MddMsVec)

        if not numVec_Ml==numVec_Ms:
            logger.warn("Unexpected numVec for tr M^-1 dd M, cID = "+cID+"... skipping")
            continue

        trMinvlVec=np.array(opTable[cID][6])
        trMinvsVec=np.array(opTable[cID][7])
        numVec_trMinvl=len(trMinvlVec)
        numVec_trMinvs=len(trMinvsVec)

        if not numVec_trMinvl==numVec_trMinvs:
            logger.warn("Unexpected numVec for tr M^-1, cID = "+cID+"... skipping")
            continue

        if numVec_l==0 or numVec_l2==0 or numVec_Ml==0 or numVec_trMinvl==0:
            logger.warn("Found zero random vectors for an observable, cID = "+cID+"... skipping")
            continue

        # I follow the QCD Thermodynamics section of my researchNotes. In the dense code, each trace comes
        # with a 1/vol4. So whenever we have stuff like obs**2, since each factor obs has a trace, we need
        # to multiply by vol4 to a correct normalization.
        chi2l   = + vol4*( mean_square(nlVec) )/16 - vol4*np.mean(nlVec)**2/16 - (1/4)*np.mean(nl2Vec) + (1/4)*np.mean(MddMlVec)
        chi2s   = + vol4*( mean_square(nsVec) )/16 - vol4*np.mean(nsVec)**2/16 - (1/4)*np.mean(ns2Vec) + (1/4)*np.mean(MddMsVec)
        chi11ll = + vol4*( mean_square(nlVec) )/16 - vol4*np.mean(nlVec)**2/16
        chi11ls = + vol4*( np.mean(nlVec*nsVec) - np.mean(nlVec)*np.mean(nsVec) )/16

        # TODO: There seems to be a possibility for reuse of this number above 
        nl2  = mean_square(nlVec)*vol4/16
        ns2  = mean_square(nsVec)*vol4/16
        nlns = np.mean(nlVec)*np.mean(nsVec)*vol4/16

        chi2Q = (1/9)*( 5*chi2l + chi2s - 4*chi11ll - 2*chi11ls )
        chi2B = (1/9)*( 2*chi2l + chi2s + 2*chi11ll + 4*chi11ls )

        dnl  = -( np.mean(nl2Vec) - np.mean(MddMlVec) )/4
        dns  = -( np.mean(ns2Vec) - np.mean(MddMsVec) )/4

        dnS  =           dns
        dnQ  = ( 5*dnl + dns )/9
        dnI  =     dnl + dns
        dn   = ( 2*dnl + dns )/9

        # TODO: possiblity for reuse above
        nl   =  np.mean( nlVec )/4
        ns   =  np.mean( nsVec )/4
        n    =  (2*nl + ns)/3
        nS   = -        ns
        nQ   =  (  nl - ns)/3
        nI   = complex(0)

        nS2  =            ns2
        nQ2  =  (   nl2 + ns2 - 2*nlns )/9
        n2   =  ( 4*nl2 + ns2 + 4*nlns )/9
        nl2  =      nl2

        outTable["confID"].append(cID)
        outTable["Nl"].append(nl)
        outTable["NB"].append(n)
        outTable["NQ"].append(nQ)
        outTable["NS"].append(nS)
        outTable["NI"].append(nI)
        outTable["dN/dmul"].append(dnl)
        outTable["dN/dmus"].append(dns)
        outTable["dN/dmuB"].append(dn )
        outTable["dN/dmuQ"].append(dnQ)
        outTable["dN/dmuS"].append(dnS)
        outTable["dN/dmuI"].append(dnI)
        outTable["Nl^2"].append(nl2)
        outTable["NB^2"].append(n2)
        outTable["NQ^2"].append(nQ2)
        outTable["NS^2"].append(nS2)
        outTable["chi2l"].append(chi2l)
        outTable["chi2s"].append(chi2s)
        outTable["chi11ll"].append(chi11ll)
        outTable["chi11ls"].append(chi11ls)
        outTable["chi2B"].append(chi2B)
        outTable["chi2Q"].append(chi2Q)


    # Prepare the table for file output
    outData   = ()
    outHeader = []
    for observable in obs:
        outData += (outTable[observable],)
        if isinstance(outTable[observable][0],complex):
            outHeader.append('Re '+observable)
            outHeader.append('Im '+observable)
        else:
            outHeader.append(observable)

    writeTable(filename,*outData,header=outHeader)