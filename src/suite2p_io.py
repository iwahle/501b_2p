from suite2p.run_s2p import s2p
from suite2p import default_ops
from suite2p.io.binary import BinaryFile as BF

ops = default_ops()

# Import annotations from deepcell: X.ome.tiff is the raw data, Y.ome.tiff is the mask


pipeline(f_reg, run_registration=True, ops=ops, stat=None):