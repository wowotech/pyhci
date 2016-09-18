#
# HCI command struct definitions.
#
# Author: www.wowotech.net
#

from construct import *

from hci_common import *

cmd_opcode = Enum(ULInt16('cmd_opcode'),
	nop				= opcode_encode(0x00, 0x0000),

	# Link Control commands
	inquiry				= opcode_encode(0x01, 0x0001),

	# Controller & Baseband Commands
	reset				= opcode_encode(0x03, 0x0003),

	# Vendor Specific Commands
	vst_set_power_management	= opcode_encode(0x3f, 0x0202),
	vss_test_exec			= opcode_encode(0x3f, 0x0005),

	# LE Controller Commands
	le_set_scan_parameters		= opcode_encode(0x08, 0x000b),
)

# common command builder.
def cmd_container(_opcode, _params = [], _params_len = 0):
	return Container(
			pkt_type = 'command',
			cmd_opcode = _opcode,
			param_len = _params_len,
			cmd_params = _params,
		)

#
# Inquiry command.
#
inquiry_cmd_params_struct = Struct('inquiry_cmd',
	Array(3, Byte('lap')),
	OneOf(Byte('inquiry_length'), range(0x01, 0x31)),
	OneOf(Byte('num_responses'), range(256)),
)

def inquiry_cmd_params_container(_lap, _inquiry_length, _num_responses):
	b0 = _lap & 0xff
	b1 = (_lap >> 8) & 0xff
	b2 = (_lap >> 16) & 0xff

	return Container(
			lap = [b0, b1, b2],
			inquiry_length = _inquiry_length,
			num_responses = _num_responses,
		)

def inquiry_cmd_container(_lap, _inquiry_length, _num_responses):
	params = inquiry_cmd_params_container(_lap, _inquiry_length, _num_responses)
	plen = len(inquiry_cmd_params_struct.build(params))
	return cmd_container('inquiry', params, plen)
#
# Inquiry command End.
#

#
# Reset command.
#
def reset_cmd_container():
	return cmd_container('reset')
#
# Reset command End.
#


#
# LE set scan parameters command.
#
le_scan_type = Enum(Byte('scan_type'),
	without_scan_req = 0x00,
	with_scan_req = 0x01,
)

own_address_type = Enum(Byte('own_address_type'),
	public = 0x00,
	random = 0x01,
	private_or_public = 0x02,
	private_or_random = 0x03,
)

le_set_scan_parameters_cmd_params_struct = Struct('le_set_scan_parameters_cmd',
	le_scan_type,
	OneOf(ULInt16('scan_interval'), range(0x0004, 0x40001)),
	OneOf(ULInt16('scan_window'), range(0x0004, 0x40001)),
	own_address_type,
	OneOf(Byte('scanning_filter_policy'), range(0x0, 0x5)),
)
#
# LE set scan parameters command End.
#


hci_cmd_struct = Struct('hci_cmd',
	cmd_opcode,
	param_len,
	Switch('cmd_params', lambda ctx: ctx['cmd_opcode'],
		{
			'inquiry': inquiry_cmd_params_struct,
			'le_set_scan_parameters': le_set_scan_parameters_cmd_params_struct,
		},
		default = Array(lambda ctx: ctx['param_len'], Byte('cmd_params')),
	)
)
