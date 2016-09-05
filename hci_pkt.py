from construct import *

from hci_common import *
from hci_cmd import *
from hci_evt import *

pkt_type = Enum(Byte('pkt_type'),
	command = 1,
	async_data = 2,
	sync_data = 3,
	event = 4,
)

hci_pkt_struct = Struct("hci_pkt",
	pkt_type,
	Switch("pkt_type", lambda ctx: ctx["pkt_type"],
		{
			"command": Embed(hci_cmd_struct),
			"event": Embed(hci_evt_struct),
		}
	)
)


def cmd_container(opcode, cmd_params=[]):
	return Container(
			pkt_type = 'command',
			cmd_opcode = opcode,
			param_len = len(cmd_params),
			cmd_params = cmd_params,
		)

def build(input):
	return hci_pkt_struct.build(input)

def parse(input):
	return hci_pkt_struct.parse(input)

def parse_str(input):
	s = ''.join(input.split())
	return hci_pkt_struct.parse(s.decode('hex'))
