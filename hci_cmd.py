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
	le_set_random_address		= opcode_encode(0x08, 0x0005),
	le_set_advertising_parameters	= opcode_encode(0x08, 0x0006),
	le_set_advertising_data		= opcode_encode(0x08, 0x0008),
	le_set_scan_response_data	= opcode_encode(0x08, 0x0009),
	le_set_advertise_enable		= opcode_encode(0x08, 0x000a),
	le_set_scan_parameters		= opcode_encode(0x08, 0x000b),
	le_set_scan_enable		= opcode_encode(0x08, 0x000c),
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
inquiry_cmd_struct = Struct('inquiry_cmd',
	Array(3, Byte('lap')),
	OneOf(Byte('inquiry_length'), range(0x01, 0x30 + 1)),
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
	plen = len(inquiry_cmd_struct.build(params))
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
# LE set random address command.
#
le_set_random_address_cmd_struct = Struct('le_set_random_address_cmd',
	Array(6, Byte('random_address')),
)
#
# LE set random address command End.
#


#
# LE set advertising parameters command.
#
# eg. 01 06 20 0f 40 06 80 07 05 00 00 00 00 00 00 00 00 07 00
#
le_set_advertising_parameters_cmd_struct = Struct('le_set_advertising_parameters_cmd',
	OneOf(ULInt16('advertising_interval_min'), range(0x0020, 0x40000 + 1)),
	OneOf(ULInt16('advertising_interval_max'), range(0x0020, 0x40000 + 1)),
	le_advertising_type,
	le_own_address_type,
	le_peer_address_type,
	Array(6, Byte('peer_address')),
	OneOf(Byte('advertising_channel_map'), range(256)),
	OneOf(Byte('advertising_filter_policy'), range(0x0, 0x3 + 1)),
)
#
# LE set advertising parameters command End.
#

#
# LE set advertising data command.
#
le_set_advertising_data_cmd_struct = Struct('le_set_advertising_data_cmd',
	OneOf(ULInt8('advertising_data_len'), range(0x00, 0x1F + 1)),
	Array(31, Byte('advertising_data')),
)
#
# LE set advertising data command End.
#

#
# LE set scan response data command.
#
le_set_scan_response_data_cmd_struct = Struct('le_set_scan_response_data_cmd',
	OneOf(ULInt8('scan_response_data_len'), range(0x00, 0x1F + 1)),
	Array(31, Byte('scan_response_data')),
)
#
# LE set scan response data command End.
#

#
# LE set advertise enable command.
#
le_set_advertise_enable_cmd_struct = Struct('le_set_advertise_enable_cmd',
	Enum(Byte('advertise_enable'),
		disable = 0x00,
		enable = 0x01,
	),
)
#
# LE set advertise enable command End.
#

#
# LE set scan parameters command.
#
le_set_scan_parameters_cmd_struct = Struct('le_set_scan_parameters_cmd',
	le_scan_type,
	OneOf(ULInt16('scan_interval'), range(0x0004, 0x40000 + 1)),
	OneOf(ULInt16('scan_window'), range(0x0004, 0x40000 + 1)),
	le_own_address_type,
	OneOf(Byte('scanning_filter_policy'), range(0x0, 0x4 + 1)),
)
#
# LE set scan parameters command End.
#

#
# LE set scan enable command.
#
le_set_scan_enable_cmd_struct = Struct('le_set_scan_enable_cmd',
	Enum(Byte('scan_enable'),
		disable = 0x00,
		enable = 0x01,
	),
	Enum(Byte('filter_duplicates'),
		disable = 0x00,
		enable = 0x01,
	),
)
#
# LE set scan enable command End.
#

hci_cmd_struct = Struct('hci_cmd',
	cmd_opcode,
	param_len,
	Switch('cmd_params', lambda ctx: ctx['cmd_opcode'],
		{
			'inquiry': inquiry_cmd_struct,
			'le_set_random_address': le_set_random_address_cmd_struct,
			'le_set_advertising_parameters': le_set_advertising_parameters_cmd_struct,
			'le_set_advertising_data': le_set_advertising_data_cmd_struct,
			'le_set_scan_response_data': le_set_scan_response_data_cmd_struct,
			'le_set_advertise_enable': le_set_advertise_enable_cmd_struct,
			'le_set_scan_parameters': le_set_scan_parameters_cmd_struct,
			'le_set_scan_enable': le_set_scan_enable_cmd_struct,
		},
		default = Array(lambda ctx: ctx['param_len'], Byte('cmd_params')),
	)
)
