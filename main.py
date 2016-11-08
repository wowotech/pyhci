#
# www.wowotech.net
#

import sys

from construct import *

from hci_common import *
from hci_cmd import *
from hci_pkt import *

def test_code():
	cmd = reset_cmd_container()
	ret = build(cmd)
	print('reset')
	print(ret.encode('hex'))

	cmd = read_buffer_size_cmd_container()
	ret = build(cmd)
	print('read_buffer_size')
	print(ret.encode('hex'))

	cmd = inquiry_cmd_container(0x123456, 0x7, 0x8)
	ret = build(cmd)
	print('inquiry')
	print(ret.encode('hex'))

def parse_from_stdin():
	while 1:
		print('> '),
		sys.stdout.flush()

		try:
			line = sys.stdin.readline()
		except KeyboardInterrupt:
			break

		if not line:
			break

		try:
			ret = parse_str(line)
			print(ret)
		except MappingError:
			print('Error: not found')
		except TypeError:
			print('Error: invalid input')

		sys.stdout.flush()

def parse_from_file(filename, mode):
	print('todo')

def main(argv):
	if (len(argv) < 3):
		print('Usage:')
		print('    %s [cmd] [args...]' % argv[0])
		print('    %s parse s, parse from stdin in string format' % argv[0])
		print('    %s parse s [filename], parse from file in string format' % argv[0])
		print('    %s parse b [filename], parse from file in binary format' % argv[0])
		test_code()
		return

	if (argv[1] == 'parse'):
		if (argv[2] == 's'):
			if (len(argv) == 3):
				parse_from_stdin()
			else:
				parse_from_file(argv[3], 's')
		else:
			parse_from_file(argv[3], 'b')

if __name__ == '__main__':
	main(sys.argv)
