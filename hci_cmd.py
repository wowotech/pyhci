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

hci_cmd_struct = Struct('hci_cmd',
	cmd_opcode,
	param_len,
	Switch('cmd_params', lambda ctx: ctx['cmd_opcode'],
		{
			'inquiry': inquiry_cmd_params_struct,
		},
		default = Array(lambda ctx: ctx['param_len'], Byte('cmd_params')),
	)
)


#
# Reset command.
#
def reset_cmd_container():
	return cmd_container('reset')
