# 
# testReadWriteConf.py                                                               
# 
# D. Clarke
# 
# To test correct read/write of configurations.
# 

from latqcdtools.interfaces.confReader import NERSCReader
import latqcdtools.base.logger as logger

reader = NERSCReader(Ns=8, Nt=4)

gauge = reader.readConf('nersc.l8t4b3360')

# Get the link at site (0,0,1,1) pointing in the 0 direction.
print(gauge.getLink(0,0,1,1,0))

logger.TBPass('All tests passed!')