from construct import *

param_len = OneOf(Byte("param_len"), range(256))

def opcode_encode(ogf, ocf):
	r = (ogf << 10) + ocf
	return r
