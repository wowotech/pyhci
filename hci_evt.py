#
# www.wowotech.net
#

from construct import *

from hci_common import *
from hci_cmd import *

evt_code = Enum(ULInt8('evt_code'),
	cmd_complete			= 0x0e,
)

evt_status = Enum(Byte('evt_status'),
	success				= 0x00,
	disallowed			= 0x0c,
	role_change_not_allowed		= 0x21,
)

evt_status_struct = Struct("evt_status",
	evt_status,
)

cmd_complete_struct = Struct("cmd_complete",
	Byte("flow_control"),
	cmd_opcode,
	Switch("cmd_response", lambda ctx: ctx["cmd_opcode"],
		{
		},
		default = evt_status_struct,
	)
)

hci_evt_struct = Struct("hci_evt",
	evt_code,
	param_len,
	Switch("evt_params", lambda ctx: ctx["evt_code"],
		{
			"cmd_complete":	cmd_complete_struct,
		},
		default = Array(lambda ctx: ctx["param_len"], Byte("evt_params")),
	)
)


