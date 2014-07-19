import argparse
import asyncio
import socks
import stem.process

class ChatClient:
	
	def connection_made(self, transport):
		transport.write('a message')

	def data_received(self, data):
		pass

class ChatTorTunnel():

	def __init__(self, onion_address):
		self.onion_address = onion_address
		self.tor_process = stem.process.launch_tor(take_ownership=True)
		print('Tor started')

	def get_socket(self):
		s = socks.socksocket()
		s.setproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
		s.connect((self.onion_address, 9999))
		return s

parser = argparse.ArgumentParser()
parser.add_argument('onion_address', type=str, help='the onion address of the chat server')
args = parser.parse_args()

tt = ChatTorTunnel(args.onion_address)
s = tt.get_socket()

loop = asyncio.get_event_loop()
coro = loop.create_connection(ChatClient, '127.0.0.1', sock=s)
loop.run_until_complete(coro)
loop.run_forever()
