import asyncio
import os
import socks
import stem.process
import tempfile

class ChatServer(asyncio.Protocol):

	def connection_made(self, transport):
		peername = transport.get_extra_info('peername')
		print('connection from {}'.format(peername))
		self.transport = transport

	def data_received(self, data):
		pass

class ChatHiddenService():

	def __init__(self):
		self.hidden_service_dir = tempfile.TemporaryDirectory()
		self.tor_process = stem.process.launch_tor_with_config(
			config = {
				'HiddenServiceDir': self.hidden_service_dir.name,
				'HiddenServicePort': '9999 127.0.0.1:9999'
			},
			take_ownership = True
		)
		with self.hidden_service_dir as h:
			with open(os.path.join(h, 'hostname'), 'r') as f:
				self.onion_address = f.read()
		print('Tor hidden service address: {}'.format(self.onion_address))

	def get_socket():
		s = socks.socksocket()
		s.setproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
		return s

hs = ChatHiddenService()
s = hs.get_socket()

loop = asyncio.get_event_loop()
coro = loop.create_server(ChatServer, '127.0.0.1', 9999)
server = loop.run_until_complete(coro)
print('Server running on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()