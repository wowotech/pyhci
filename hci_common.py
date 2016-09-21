#
# www.wowotech.net
#

from construct import *

param_len = OneOf(Byte("param_len"), range(256))

#
# LE
#
le_scan_type = Enum(Byte('scan_type'),
	without_scan_req = 0x00,
	with_scan_req = 0x01,
)

le_advertising_type = Enum(Byte('advertising_type'),
	connectable_undirected_advertising = 0x00,
	connectable_directed_advertising_high_duty = 0x01,
	scannable_undirected_advertising = 0x02,
	non_connectable_undirected_advertising = 0x03,
	connectable_directed_advertising_low_duty = 0x04,
	reserved_for_future_use = 0x05,
)

le_own_address_type = Enum(Byte('own_address_type'),
	public = 0x00,
	random = 0x01,
	private_or_public = 0x02,
	private_or_random = 0x03,
)

le_peer_address_type = Enum(Byte('peer_address_type'),
	public = 0x00,
	random = 0x01,
	private_or_public = 0x02,
	private_or_random = 0x03,
)

def opcode_encode(ogf, ocf):
	r = (ogf << 10) + ocf
	return r
