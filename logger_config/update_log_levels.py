"""
Usage:

First, `cd` to the folder
% cd logger_config

Second, run the script to update the log level
% python update_log_level.py debug.conf
"""
import socket
import struct
import sys

with open(sys.argv[1], 'rb') as f:
    data_to_send = f.read()

HOST = 'localhost'
PORT = 9001  # Must be the same as the port in `lib/logger.py`
UPDATED_SERVERS = 0

# Loop through all the ports on the server until we get one that does not have a logging server
# `29` comes from the limit in the while loop in the aforementioned file, i.e. 9001..9030
for port_num in range(PORT, PORT + 29):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, port_num))
        print(f'Connecting to logging server on port {port_num}...')
    except ConnectionRefusedError:
        break
    print('Sending new config...')
    s.send(struct.pack('>L', len(data_to_send)))
    s.send(data_to_send)
    UPDATED_SERVERS += 1
    s.close()
if UPDATED_SERVERS > 0:
    print('Logging configuration updated!')
else:
    print('Unable to connect to any logging servers!')
