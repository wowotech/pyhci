#
# www.wowotech.net
#

from construct import *

from hci_common import *
from hci_cmd import *

evt_code = Enum(ULInt8('evt_code'),
	cmd_complete			= 0x0e,
	number_of_completed_packets	= 0x13,
)

evt_status = Enum(Byte('evt_status'),
	success				= 0x00,
	disallowed			= 0x0c,
	role_change_not_allowed		= 0x21,
)

evt_status_struct = Struct("evt_status",
	evt_status,
)

buffer_size_result_struct = Struct("buffer_size",
	evt_status,
	OneOf(ULInt16('HC_ACL_Data_Packet_Length'), range(65536)),
	OneOf(Byte('HC_Synchronous_Data_Packet_Length'), range(256)),
	OneOf(ULInt16('HC_Total_Num_ACL_Data_Packets'), range(65536)),
	OneOf(ULInt16('HC_Total_Num_Synchronous_Data_Packets'), range(65536)),
)

#
# command complete event.
#
cmd_complete_struct = Struct("cmd_complete",
	Byte("flow_control"),
	cmd_opcode,
	Switch("cmd_response", lambda ctx: ctx["cmd_opcode"],
		{
			'read_buffer_size': buffer_size_result_struct,
		},
		default = evt_status_struct,
	)
)
#
# command complete event End.
#

#
# Number Of Completed Packets Event.
#
number_of_handles = OneOf(Byte("number_of_handles"), range(256))

nocp_by_handle_struct = Struct("number_of_completed_packets_by_handle",
	OneOf(ULInt16('Connection_Handle'), range(0x0000, 0x0EFF + 1)),
	OneOf(ULInt16('HC_Num_Of_Completed_Packets'), range(0xFFFF)),
)

number_of_completed_packets_struct = Struct("number_of_completed_packets",
	number_of_handles,
	Array(lambda ctx: ctx["number_of_handles"], nocp_by_handle_struct),
)
#
# Number Of Completed Packets Event End.
#

hci_evt_struct = Struct("hci_evt",
	evt_code,
	param_len,
	Switch("evt_params", lambda ctx: ctx["evt_code"],
		{
			"cmd_complete":	cmd_complete_struct,
			"number_of_completed_packets":	number_of_completed_packets_struct,
		},
		default = Array(lambda ctx: ctx["param_len"], Byte("evt_params")),
	)
)


