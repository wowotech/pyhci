from construct import *

from hci_common import *

cmd_opcode = Enum(ULInt16('cmd_opcode'),
	nop				= opcode_encode(0x00, 0x0000),

	# Controller & Baseband Commands
	reset				= opcode_encode(0x03, 0x0003),

	# Vendor Specific Commands
	vst_set_power_management	= opcode_encode(0x3f, 0x0202),
	vss_test_exec			= opcode_encode(0x3f, 0x0005),
)

hci_cmd_struct = Struct("hci_cmd",
	cmd_opcode,
	param_len,
	Switch("cmd_params", lambda ctx: ctx["cmd_opcode"],
		{
		},
		default = Array(lambda ctx: ctx["param_len"], Byte("cmd_params")),
	)
)


