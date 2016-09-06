# pyhci
Description:
--------------

A small tools for Bluetooth HCI test, which can:<br>
Parse HCI command/event from cmdline, files etc. into human readable format;<br>
Packet HCI command/event to binary data, then can be transmit from UART etc.<br>
Other, TODO.<br>

Usage
--------------

1. Prepare<br>
Install python-pip:<br>
```Bash
sudo apt-get install python-pip
```
Install python construct:<br>
```Bash
pip install construct
```
2. Parse HCI command/event from stdin<br>
```Bash
$ python main.py parse s
> 01 00 00 00
Container:
    pkt_type = command
    cmd_opcode = nop
    param_len = 0
    cmd_params = ListContainer:
> 04 0E 04 01 13 FE 00
Error: not found
>
```
3. others, todo<br>

Contact us
--------------

www.wowotech.net

Thanks for
--------------

"https://github.com/hughobrien/py-ble-hci"
